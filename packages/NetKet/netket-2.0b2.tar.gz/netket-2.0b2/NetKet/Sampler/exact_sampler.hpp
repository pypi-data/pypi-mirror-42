// Copyright 2018 The Simons Foundation, Inc. - All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//    http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#ifndef NETKET_EXACT_SAMPLER_HPP
#define NETKET_EXACT_SAMPLER_HPP

#include <mpi.h>
#include <Eigen/Dense>
#include <iostream>
#include <limits>
#include "Utils/parallel_utils.hpp"
#include "Utils/random_utils.hpp"
#include "abstract_sampler.hpp"

namespace netket {

// Exact sampling using heat bath, mostly for testing purposes on small systems
template <class WfType>
class ExactSampler: public AbstractSampler<WfType> {
  WfType& psi_;

  const AbstractHilbert& hilbert_;

  // number of visible units
  const int nv_;

  // states of visible units
  Eigen::VectorXd v_;

  Eigen::VectorXd accept_;
  Eigen::VectorXd moves_;

  int mynode_;
  int totalnodes_;

  const HilbertIndex hilbert_index_;

  const int dim_;

  std::discrete_distribution<int> dist_;

  std::vector<std::complex<double>> logpsivals_;
  std::vector<double> psivals_;

 public:
  explicit ExactSampler(WfType& psi)
      : psi_(psi),
        hilbert_(psi.GetHilbert()),
        nv_(hilbert_.Size()),
        hilbert_index_(hilbert_),
        dim_(hilbert_index_.NStates()) {
    Init();
  }

  void Init() {
    v_.resize(nv_);

    MPI_Comm_size(MPI_COMM_WORLD, &totalnodes_);
    MPI_Comm_rank(MPI_COMM_WORLD, &mynode_);

    if (!hilbert_.IsDiscrete()) {
      throw InvalidInputError(
          "Exact sampler works only for discrete "
          "Hilbert spaces");
    }

    accept_.resize(1);
    moves_.resize(1);

    Reset(true);

    InfoMessage() << "Exact sampler is ready " << std::endl;
  }

  void Reset(bool initrandom) override {
    if (initrandom) {
      hilbert_.RandomVals(v_, this->GetRandomEngine());
    }

    double logmax = -std::numeric_limits<double>::infinity();

    logpsivals_.resize(dim_);
    psivals_.resize(dim_);

    for (int i = 0; i < dim_; ++i) {
      auto v = hilbert_index_.NumberToState(i);
      logpsivals_[i] = psi_.LogVal(v);
      logmax = std::max(logmax, std::real(logpsivals_[i]));
    }

    for (int i = 0; i < dim_; ++i) {
      psivals_[i] = std::norm(std::exp(logpsivals_[i] - logmax));
    }

    dist_ = std::discrete_distribution<int>(psivals_.begin(), psivals_.end());

    accept_ = Eigen::VectorXd::Zero(1);
    moves_ = Eigen::VectorXd::Zero(1);
  }

  void Sweep() override {
    int newstate = dist_(this->GetRandomEngine());
    v_ = hilbert_index_.NumberToState(newstate);

    accept_(0) += 1;
    moves_(0) += 1;
  }

  Eigen::VectorXd Visible() override { return v_; }

  void SetVisible(const Eigen::VectorXd& v) override { v_ = v; }

  WfType& GetMachine() noexcept override { return psi_; }

  const AbstractHilbert& GetHilbert() const noexcept override {
    return hilbert_;
  }

  Eigen::VectorXd Acceptance() const override {
    Eigen::VectorXd acc = accept_;
    for (int i = 0; i < 1; i++) {
      acc(i) /= moves_(i);
    }
    return acc;
  }
};

}  // namespace netket

#endif
