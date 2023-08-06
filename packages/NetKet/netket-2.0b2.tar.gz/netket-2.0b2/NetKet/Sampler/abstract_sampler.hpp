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

#ifndef NETKET_ABSTRACTSAMPLER_HPP
#define NETKET_ABSTRACTSAMPLER_HPP

#include <memory>
#include <vector>
#include "Hilbert/abstract_hilbert.hpp"

namespace netket {

template <class WfType>
class AbstractSampler {
 public:
  virtual void Reset(bool initrandom = false) = 0;

  virtual void Sweep() = 0;

  virtual Eigen::VectorXd Visible() = 0;

  virtual void SetVisible(const Eigen::VectorXd& v) = 0;

  virtual WfType& GetMachine() noexcept = 0;

  virtual Eigen::VectorXd Acceptance() const = 0;

  virtual const AbstractHilbert& GetHilbert() const noexcept = 0;

  virtual ~AbstractSampler() {}

  void Seed(DistributedRandomEngine::ResultType base_seed) {
    engine_.Seed(base_seed);
    this->Reset(true);
  }

 protected:
  default_random_engine& GetRandomEngine() { return engine_.Get(); }

 private:
  DistributedRandomEngine engine_;
};

}  // namespace netket
#endif
