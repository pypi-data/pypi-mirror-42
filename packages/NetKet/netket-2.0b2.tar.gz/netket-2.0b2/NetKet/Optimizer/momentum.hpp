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

#ifndef NETKET_MOMENTUM_HPP
#define NETKET_MOMENTUM_HPP

#include <Eigen/Core>
#include <Eigen/Dense>
#include <cassert>
#include <cmath>
#include <complex>
#include <iostream>
#include "abstract_optimizer.hpp"

namespace netket {

class Momentum : public AbstractOptimizer {
  int npar_;

  double eta_;
  double beta_;

  Eigen::VectorXd mt_;

  const Complex I_;

 public:
  explicit Momentum(double eta = 0.001, double beta = 0.9)
      : eta_(eta), beta_(beta), I_(0, 1) {
    npar_ = -1;
    PrintParameters();
  }

  // TODO remove
  // Json constructor
  explicit Momentum(const json &pars) : I_(0, 1) {
    npar_ = -1;

    from_json(pars);
    PrintParameters();
  }

  void PrintParameters() {
    InfoMessage() << "Momentum optimizer initialized with these parameters :"
                  << std::endl;
    InfoMessage() << "Learning Rate = " << eta_ << std::endl;
    InfoMessage() << "Beta = " << beta_ << std::endl;
  }

  void Init(const Eigen::VectorXd &pars) override {
    npar_ = pars.size();
    mt_.setZero(npar_);
  }

  void Init(const Eigen::VectorXcd &pars) override {
    npar_ = 2 * pars.size();
    mt_.setZero(npar_);
  }

  void Update(const Eigen::VectorXd &grad, Eigen::VectorXd &pars) override {
    assert(npar_ > 0);

    mt_ = beta_ * mt_ + (1. - beta_) * grad;

    for (int i = 0; i < npar_; i++) {
      pars(i) -= eta_ * mt_(i);
    }
  }

  void Update(const Eigen::VectorXcd &grad, Eigen::VectorXd &pars) override {
    Update(Eigen::VectorXd(grad.real()), pars);
  }

  void Update(const Eigen::VectorXcd &grad, Eigen::VectorXcd &pars) override {
    assert(npar_ == 2 * pars.size());

    for (int i = 0; i < pars.size(); i++) {
      mt_(2 * i) = beta_ * mt_(2 * i) + (1. - beta_) * grad(i).real();
      mt_(2 * i + 1) = beta_ * mt_(2 * i + 1) + (1. - beta_) * grad(i).imag();
    }

    for (int i = 0; i < pars.size(); i++) {
      pars(i) -= eta_ * mt_(2 * i);
      pars(i) -= eta_ * I_ * mt_(2 * i + 1);
    }
  }

  void Reset() override { mt_ = Eigen::VectorXd::Zero(npar_); }

  // TODO remove
  void from_json(const json &pars) {
    // DEPRECATED (to remove for v2.0.0)
    std::string section = "Optimizer";
    if (!FieldExists(pars, section)) {
      section = "Learning";
    }
    eta_ = FieldOrDefaultVal(pars[section], "LearningRate", 0.001);
    beta_ = FieldOrDefaultVal(pars[section], "Beta", 0.9);
  }
};

}  // namespace netket

#endif
