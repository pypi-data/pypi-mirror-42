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

#ifndef NETKET_PYMACHINE_HPP
#define NETKET_PYMACHINE_HPP

#include <mpi.h>
#include <pybind11/complex.h>
#include <pybind11/eigen.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>
#include <complex>
#include <vector>
#include "Layers/py_layer.hpp"
#include "abstract_machine.hpp"
#include "py_ffnn.hpp"
#include "py_jastrow.hpp"
#include "py_jastrow_symm.hpp"
#include "py_mps_periodic.hpp"
#include "py_rbm_multival.hpp"
#include "py_rbm_spin.hpp"
#include "py_rbm_spin_symm.hpp"

namespace py = pybind11;

namespace netket {

void AddMachineModule(py::module &m) {
  auto subm = m.def_submodule("machine");

  py::class_<MachineType>(subm, "Machine")
      .def_property_readonly(
          "n_par", &MachineType::Npar,
          R"EOF(int: The number of parameters in the machine.)EOF")
      .def_property("parameters", &MachineType::GetParameters,
                    &MachineType::SetParameters,
                    R"EOF(list: List containing the parameters within the layer.
            Read and write)EOF")
      .def("init_random_parameters", &MachineType::InitRandomPars,
           py::arg("seed") = 1234, py::arg("sigma") = 0.1,
           R"EOF(
             Member function to initialise machine parameters.

             Args:
                 seed: The random number generator seed.
                 sigma: Standard deviation of normal distribution from which
                     parameters are drawn.
           )EOF")
      .def("log_val",
           (StateType(MachineType::*)(MachineType::VisibleConstType)) &
               MachineType::LogVal,
           py::arg("v"),
           R"EOF(
                 Member function to obtain log value of machine given an input
                 vector.

                 Args:
                     v: Input vector to machine.
           )EOF")
      .def("log_val_diff",
           (MachineType::VectorType(MachineType::*)(
               MachineType::VisibleConstType,
               const std::vector<std::vector<int>> &,
               const std::vector<std::vector<double>> &)) &
               MachineType::LogValDiff,
           py::arg("v"), py::arg("tochange"), py::arg("newconf"),
           R"EOF(
                 Member function to obtain difference in log value of machine
                 given an input and a change to the input.

                 Args:
                     v: Input vector to machine.
                     tochange: list containing the indices of the input to be
                         changed
                     newconf: list containing the new (changed) values at the
                         indices specified in tochange
           )EOF")
      .def("der_log",
           (MachineType::VectorType(MachineType::*)(
               MachineType::VisibleConstType)) &
               MachineType::DerLog,
           py::arg("v"),
           R"EOF(
                 Member function to obtain the derivatives of log value of
                 machine given an input wrt the machine's parameters.

                 Args:
                     v: Input vector to machine.
           )EOF")
      .def_property_readonly(
          "n_visible", &MachineType::Nvisible,
          R"EOF(int: The number of inputs into the machine aka visible units in
            the case of Restricted Boltzmann Machines.)EOF")
      .def_property_readonly(
          "hilbert", &MachineType::GetHilbert,
          R"EOF(netket.hilbert.Hilbert: The hilbert space object of the system.)EOF")
      .def("save",
           [](const MachineType &a, std::string filename) {
             json j;
             a.to_json(j);
             std::ofstream filewf(filename);
             filewf << j << std::endl;
             filewf.close();
           },
           py::arg("filename"),
           R"EOF(
                 Member function to save the machine parameters.

                 Args:
                     filename: name of file to save parameters to.
           )EOF")
      .def("load",
           [](MachineType &a, std::string filename) {
             std::ifstream filewf(filename);
             if (filewf.is_open()) {
               json j;
               filewf >> j;
               filewf.close();
               a.from_json(j);
             }
           },
           py::arg("filename"),
           R"EOF(
                 Member function to load machine parameters from a json file.

                 Args:
                     filename: name of file to load parameters from.
           )EOF");

  AddRbmSpin(subm);
  AddRbmSpinSymm(subm);
  AddRbmMultival(subm);
  AddJastrow(subm);
  AddJastrowSymm(subm);
  AddMpsPeriodic(subm);
  AddFFNN(subm);
  AddLayerModule(m);
}

}  // namespace netket

#endif
