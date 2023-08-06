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

#include <Eigen/Dense>
#include <iostream>
#include <map>
#include <vector>
#include "Utils/all_utils.hpp"
#include "Utils/lookup.hpp"
#include "abstract_machine.hpp"
#include "rbm_spin.hpp"

#ifndef NETKET_RBM_MULTIVAL_HPP
#define NETKET_RBM_MULTIVAL_HPP

namespace netket {

// Restricted Boltzman Machine wave function
// for generic (finite) local hilbert space
template <typename T>
class RbmMultival : public AbstractMachine<T> {
  using VectorType = typename AbstractMachine<T>::VectorType;
  using MatrixType = typename AbstractMachine<T>::MatrixType;
  using VectorRefType = typename AbstractMachine<T>::VectorRefType;
  using VectorConstRefType = typename AbstractMachine<T>::VectorConstRefType;
  using VisibleConstType = typename AbstractMachine<T>::VisibleConstType;

  const AbstractHilbert &hilbert_;

  // number of visible units
  int nv_;

  // number of hidden units
  int nh_;

  // number of parameters
  int npar_;

  // local size of hilbert space
  int ls_;

  // weights
  MatrixType W_;

  // visible units bias
  VectorType a_;

  // hidden units bias
  VectorType b_;

  VectorType thetas_;
  VectorType lnthetas_;
  VectorType thetasnew_;
  VectorType lnthetasnew_;

  bool usea_;
  bool useb_;

  Eigen::VectorXd localconfs_;
  Eigen::MatrixXd mask_;

  Eigen::VectorXd vtilde_;

  std::map<double, int> confindex_;

 public:
  using StateType = typename AbstractMachine<T>::StateType;
  using LookupType = typename AbstractMachine<T>::LookupType;

  explicit RbmMultival(const AbstractHilbert &hilbert, int nhidden = 0,
                       int alpha = 0, bool usea = true, bool useb = true)
      : hilbert_(hilbert),
        nv_(hilbert.Size()),
        ls_(hilbert.LocalSize()),
        usea_(usea),
        useb_(useb) {
    nh_ = std::max(nhidden, alpha * nv_);
    Init();
  }

  void Init() {
    W_.resize(nv_ * ls_, nh_);
    a_.resize(nv_ * ls_);
    b_.resize(nh_);

    thetas_.resize(nh_);
    lnthetas_.resize(nh_);
    thetasnew_.resize(nh_);
    lnthetasnew_.resize(nh_);

    npar_ = nv_ * nh_ * ls_;

    if (usea_) {
      npar_ += nv_ * ls_;
    } else {
      a_.setZero();
    }

    if (useb_) {
      npar_ += nh_;
    } else {
      b_.setZero();
    }

    auto localstates = hilbert_.LocalStates();

    localconfs_.resize(nv_ * ls_);
    for (int i = 0; i < nv_ * ls_; i += ls_) {
      for (int j = 0; j < ls_; j++) {
        localconfs_(i + j) = localstates[j];
      }
    }

    mask_.resize(nv_ * ls_, nv_);
    mask_.setZero();

    for (int i = 0; i < nv_ * ls_; i++) {
      mask_(i, i / ls_) = 1;
    }

    for (int i = 0; i < ls_; i++) {
      confindex_[localstates[i]] = i;
    }

    vtilde_.resize(nv_ * ls_);

    InfoMessage() << "RBM Multival Initizialized with nvisible = " << nv_
                  << " and nhidden = " << nh_ << std::endl;
    InfoMessage() << "Using visible bias = " << usea_ << std::endl;
    InfoMessage() << "Using hidden bias  = " << useb_ << std::endl;
    InfoMessage() << "Local size is      = " << ls_ << std::endl;
  }

  int Nvisible() const override { return nv_; }

  int Nhidden() const { return nh_; }

  int Npar() const override { return npar_; }

  void InitRandomPars(int seed, double sigma) override {
    VectorType par(npar_);

    netket::RandomGaussian(par, seed, sigma);

    SetParameters(par);
  }

  void InitLookup(VisibleConstType v, LookupType &lt) override {
    if (lt.VectorSize() == 0) {
      lt.AddVector(b_.size());
    }
    if (lt.V(0).size() != b_.size()) {
      lt.V(0).resize(b_.size());
    }
    ComputeTheta(v, lt.V(0));
  }

  void UpdateLookup(VisibleConstType v, const std::vector<int> &tochange,
                    const std::vector<double> &newconf,
                    LookupType &lt) override {
    if (tochange.size() != 0) {
      for (std::size_t s = 0; s < tochange.size(); s++) {
        const int sf = tochange[s];
        const int oldtilde = confindex_[v[sf]];
        const int newtilde = confindex_[newconf[s]];

        lt.V(0) -= W_.row(ls_ * sf + oldtilde);
        lt.V(0) += W_.row(ls_ * sf + newtilde);
      }
    }
  }

  VectorType DerLog(VisibleConstType v) override {
    VectorType der(npar_);
    der.setZero();

    int k = 0;

    ComputeTheta(v, thetas_);

    if (usea_) {
      for (; k < nv_ * ls_; k++) {
        der(k) = vtilde_(k);
      }
    }

    RbmSpin<T>::tanh(thetas_, lnthetas_);

    if (useb_) {
      for (int p = 0; p < nh_; p++) {
        der(k) = lnthetas_(p);
        k++;
      }
    }

    for (int i = 0; i < nv_ * ls_; i++) {
      for (int j = 0; j < nh_; j++) {
        der(k) = lnthetas_(j) * vtilde_(i);
        k++;
      }
    }
    return der;
  }

  VectorType GetParameters() override {
    VectorType pars(npar_);

    int k = 0;

    if (usea_) {
      for (; k < nv_ * ls_; k++) {
        pars(k) = a_(k);
      }
    }

    if (useb_) {
      for (int p = 0; p < nh_; p++) {
        pars(k) = b_(p);
        k++;
      }
    }

    for (int i = 0; i < nv_ * ls_; i++) {
      for (int j = 0; j < nh_; j++) {
        pars(k) = W_(i, j);
        k++;
      }
    }

    return pars;
  }

  void SetParameters(VectorConstRefType pars) override {
    int k = 0;

    if (usea_) {
      for (; k < nv_ * ls_; k++) {
        a_(k) = pars(k);
      }
    }

    if (useb_) {
      for (int p = 0; p < nh_; p++) {
        b_(p) = pars(k);
        k++;
      }
    }

    for (int i = 0; i < nv_ * ls_; i++) {
      for (int j = 0; j < nh_; j++) {
        W_(i, j) = pars(k);
        k++;
      }
    }
  }

  // Value of the logarithm of the wave-function
  T LogVal(VisibleConstType v) override {
    ComputeTheta(v, thetas_);
    RbmSpin<T>::lncosh(thetas_, lnthetas_);

    return (vtilde_.dot(a_) + lnthetas_.sum());
  }

  // Value of the logarithm of the wave-function
  // using pre-computed look-up tables for efficiency
  T LogVal(VisibleConstType v, const LookupType &lt) override {
    RbmSpin<T>::lncosh(lt.V(0), lnthetas_);

    ComputeVtilde(v, vtilde_);
    return (vtilde_.dot(a_) + lnthetas_.sum());
  }

  // Difference between logarithms of values, when one or more visible variables
  // are being changed
  VectorType LogValDiff(
      VisibleConstType v, const std::vector<std::vector<int>> &tochange,
      const std::vector<std::vector<double>> &newconf) override {
    const std::size_t nconn = tochange.size();
    VectorType logvaldiffs = VectorType::Zero(nconn);

    ComputeTheta(v, thetas_);
    RbmSpin<T>::lncosh(thetas_, lnthetas_);

    T logtsum = lnthetas_.sum();

    for (std::size_t k = 0; k < nconn; k++) {
      if (tochange[k].size() != 0) {
        thetasnew_ = thetas_;

        for (std::size_t s = 0; s < tochange[k].size(); s++) {
          const int sf = tochange[k][s];
          const int oldtilde = confindex_[v[sf]];
          const int newtilde = confindex_[newconf[k][s]];

          logvaldiffs(k) -= a_(ls_ * sf + oldtilde);
          logvaldiffs(k) += a_(ls_ * sf + newtilde);

          thetasnew_ -= W_.row(ls_ * sf + oldtilde);
          thetasnew_ += W_.row(ls_ * sf + newtilde);
        }

        RbmSpin<T>::lncosh(thetasnew_, lnthetasnew_);
        logvaldiffs(k) += lnthetasnew_.sum() - logtsum;
      }
    }
    return logvaldiffs;
  }

  // Difference between logarithms of values, when one or more visible variables
  // are being changed Version using pre-computed look-up tables for efficiency
  // on a small number of local changes
  T LogValDiff(VisibleConstType v, const std::vector<int> &tochange,
               const std::vector<double> &newconf,
               const LookupType &lt) override {
    T logvaldiff = 0.;

    if (tochange.size() != 0) {
      RbmSpin<T>::lncosh(lt.V(0), lnthetas_);

      thetasnew_ = lt.V(0);

      for (std::size_t s = 0; s < tochange.size(); s++) {
        const int sf = tochange[s];
        const int oldtilde = confindex_[v[sf]];
        const int newtilde = confindex_[newconf[s]];

        logvaldiff -= a_(ls_ * sf + oldtilde);
        logvaldiff += a_(ls_ * sf + newtilde);

        thetasnew_ -= W_.row(ls_ * sf + oldtilde);
        thetasnew_ += W_.row(ls_ * sf + newtilde);
      }

      RbmSpin<T>::lncosh(thetasnew_, lnthetasnew_);
      logvaldiff += (lnthetasnew_.sum() - lnthetas_.sum());
    }
    return logvaldiff;
  }

  // Computhes the values of the theta pseudo-angles
  inline void ComputeTheta(VisibleConstType v, VectorType &theta) {
    ComputeVtilde(v, vtilde_);
    theta = (W_.transpose() * vtilde_ + b_);
  }

  inline void ComputeVtilde(VisibleConstType v, Eigen::VectorXd &vtilde) {
    auto t = (localconfs_.array() == (mask_ * v).array());
    vtilde = t.template cast<double>();
  }

  const AbstractHilbert &GetHilbert() const noexcept override {
    return hilbert_;
  }

  void to_json(json &j) const override {
    j["Name"] = "RbmMultival";
    j["Nvisible"] = nv_;
    j["Nhidden"] = nh_;
    j["LocalSize"] = ls_;
    j["UseVisibleBias"] = usea_;
    j["UseHiddenBias"] = useb_;
    j["a"] = a_;
    j["b"] = b_;
    j["W"] = W_;
  }

  void from_json(const json &pars) override {
    if (pars.at("Name") != "RbmMultival") {
      throw InvalidInputError(
          "Error while constructing RbmMultival from Json input");
    }

    if (FieldExists(pars, "Nvisible")) {
      nv_ = pars["Nvisible"];
    }

    if (nv_ != hilbert_.Size()) {
      throw InvalidInputError(
          "Loaded wave-function has incompatible Hilbert space");
    }

    if (FieldExists(pars, "LocalSize")) {
      ls_ = pars["LocalSize"];
    }
    if (ls_ != hilbert_.LocalSize()) {
      throw InvalidInputError(
          "Loaded wave-function has incompatible Hilbert space");
    }

    if (FieldExists(pars, "Nhidden")) {
      nh_ = FieldVal(pars, "Nhidden");
    } else {
      nh_ = nv_ * double(FieldVal(pars, "Alpha"));
    }

    usea_ = FieldOrDefaultVal(pars, "UseVisibleBias", true);
    useb_ = FieldOrDefaultVal(pars, "UseHiddenBias", true);

    Init();

    // Loading parameters, if defined in the input
    if (FieldExists(pars, "a")) {
      a_ = pars["a"];
    } else {
      a_.setZero();
    }

    if (FieldExists(pars, "b")) {
      b_ = pars["b"];
    } else {
      b_.setZero();
    }
    if (FieldExists(pars, "W")) {
      W_ = pars["W"];
    }
  }
};

}  // namespace netket

#endif
