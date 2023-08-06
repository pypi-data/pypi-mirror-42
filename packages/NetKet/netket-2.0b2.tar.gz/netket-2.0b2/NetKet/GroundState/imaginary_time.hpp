#ifndef NETKET_IMAGINARY_TIME_PROPAGATION_HPP
#define NETKET_IMAGINARY_TIME_PROPAGATION_HPP

#include <Eigen/Dense>

#include "Dynamics/TimeStepper/abstract_time_stepper.hpp"
#include "Operator/MatrixWrapper/matrix_wrapper.hpp"
#include "Operator/operator.hpp"
#include "Output/json_output_writer.hpp"
#include "Stats/stats.hpp"

namespace netket {

class ImagTimePropagation {
 public:
  class Iterator;

  using StateVector = Eigen::VectorXcd;
  using Stepper = ode::AbstractTimeStepper<StateVector>;
  using Matrix = AbstractMatrixWrapper<>;

  using ObsEntry = std::pair<std::string, std::unique_ptr<Matrix>>;

  ImagTimePropagation(Matrix& matrix, Stepper& stepper, double t0,
                      StateVector initial_state)
      : matrix_(matrix),
        stepper_(stepper),
        t_(t0),
        state_(std::move(initial_state)) {
    ode_system_ = [this](const StateVector& x, StateVector& dxdt,
                         double /*t*/) { dxdt.noalias() = -matrix_.Apply(x); };
  }

  void AddObservable(const AbstractOperator& observable,
                     const std::string& name,
                     const std::string& matrix_type = "Sparse") {
    auto wrapper = CreateMatrixWrapper(observable, matrix_type);
    observables_.emplace_back(name, std::move(wrapper));
  }

  void Advance(double dt) {
    // Propagate the state
    stepper_.Propagate(ode_system_, state_, t_, dt);
    // renormalize the state to prevent unbounded growth of the norm
    state_.normalize();
    ComputeObservables(state_);
    t_ += dt;
  }

  /*void Run(StateVector& initial_state, ) {
    assert(initial_state.size() == Dimension());
    state_ = initial_state;
    for (const auto& step : Iterate(range.t0, )) {
    }
  }*/

  Iterator Iterate(double dt,
                   nonstd::optional<Index> n_iter = nonstd::nullopt) {
    return Iterator(*this, dt, std::move(n_iter));
  }

  void ComputeObservables(const StateVector& state) {
    const auto mean_variance = matrix_.MeanVariance(state);
    obsmanager_.Reset("Energy");
    obsmanager_.Push("Energy", mean_variance[0].real());
    obsmanager_.Reset("EnergyVariance");
    obsmanager_.Push("EnergyVariance", mean_variance[1].real());

    for (const auto& entry : observables_) {
      const auto& name = entry.first;
      const auto& obs = entry.second;
      obsmanager_.Reset(name);

      const auto value = obs->Mean(state).real();
      obsmanager_.Push(name, value);
    }
  }

  const ObsManager& GetObsManager() const { return obsmanager_; }

  double GetTime() const { return t_; }
  void SetTime(double t) { t_ = t; }

  class Iterator {
   public:
    // typedefs required for iterators
    using iterator_category = std::input_iterator_tag;
    using difference_type = Index;
    using value_type = Index;
    using pointer_type = Index*;
    using reference_type = Index&;

   private:
    ImagTimePropagation& driver_;
    nonstd::optional<Index> n_iter_;
    double dt_;

    Index cur_iter_;

   public:
    Iterator(ImagTimePropagation& driver, double dt,
             nonstd::optional<Index> n_iter)
        : driver_(driver), n_iter_(std::move(n_iter)), dt_(dt), cur_iter_(0) {}

    Index operator*() const { return cur_iter_; };
    Iterator& operator++() {
      driver_.Advance(dt_);
      cur_iter_ += 1;
      return *this;
    }

    // TODO(C++17): Replace with comparison to special Sentinel type, since
    // C++17 allows end() to return a different type from begin().
    bool operator!=(const Iterator&) {
      return !n_iter_.has_value() || cur_iter_ < n_iter_.value();
    }
    // pybind11::make_iterator requires operator==
    bool operator==(const Iterator& other) { return !(*this != other); }

    Iterator begin() const { return *this; }
    Iterator end() const { return *this; }
  };

 private:
  Matrix& matrix_;
  Stepper& stepper_;
  ode::OdeSystemFunction<StateVector> ode_system_;

  double t_;
  StateVector state_;

  std::vector<ObsEntry> observables_;
  ObsManager obsmanager_;
};

}  // namespace netket

#endif  // NETKET_IMAGINARY_TIME_PROPAGATION_HPP
