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

#ifndef NETKET_SGD_HPP
#define NETKET_SGD_HPP

#include <Eigen/Core>
#include <Eigen/Dense>
#include <cassert>
#include <cmath>
#include <iostream>
#include "abstract_optimizer.hpp"

namespace netket {

class Sgd : public AbstractOptimizer {
  // decay constant
  double eta_;

  int npar_;

  double l2reg_;

  double decay_factor_;

 public:
  explicit Sgd(double learning_rate, double l2reg = 0,
               double decay_factor = 1.0)
      : eta_(learning_rate), l2reg_(l2reg) {
    npar_ = -1;
    SetDecayFactor(decay_factor);
    PrintParameters();
  }

  // TODO remove
  // Json constructor
  explicit Sgd(const json &pars) {
    npar_ = -1;

    from_json(pars);
    PrintParameters();
  }

  void PrintParameters() {
    InfoMessage() << "Sgd optimizer initialized with these parameters :"
                  << std::endl;
    InfoMessage() << "Learning Rate = " << eta_ << std::endl;
    InfoMessage() << "L2 Regularization = " << l2reg_ << std::endl;
    InfoMessage() << "Decay Factor = " << decay_factor_ << std::endl;
  }

  void Init(const Eigen::VectorXd &pars) override { npar_ = pars.size(); }

  void Init(const Eigen::VectorXcd &pars) override { npar_ = 2 * pars.size(); }

  void Update(const Eigen::VectorXd &grad, Eigen::VectorXd &pars) override {
    assert(npar_ > 0);

    eta_ *= decay_factor_;

    for (int i = 0; i < npar_; i++) {
      pars(i) = pars(i) - (grad(i) + l2reg_ * pars(i)) * eta_;
    }
  }

  void Update(const Eigen::VectorXcd &grad, Eigen::VectorXd &pars) override {
    Update(Eigen::VectorXd(grad.real()), pars);
  }

  void Update(const Eigen::VectorXcd &grad, Eigen::VectorXcd &pars) override {
    eta_ *= decay_factor_;

    for (int i = 0; i < pars.size(); i++) {
      pars(i) = pars(i) - (grad(i) + l2reg_ * pars(i)) * eta_;
    }
  }

  void SetDecayFactor(double decay_factor) {
    assert(decay_factor <= 1.00001);
    decay_factor_ = decay_factor;
  }

  void Reset() override {}

  void from_json(const json &pars) {
    // DEPRECATED (to remove for v2.0.0)
    std::string section = "Optimizer";
    if (!FieldExists(pars, section)) {
      section = "Learning";
    }

    eta_ = FieldVal(pars[section], "LearningRate");
    l2reg_ = FieldOrDefaultVal(pars[section], "L2Reg", 0.0);
    SetDecayFactor(FieldOrDefaultVal(pars[section], "DecayFactor", 1.0));
  }
};

}  // namespace netket

#endif
