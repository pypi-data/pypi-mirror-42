// This file is part of Discretizer.

// Copyright (c) 2017 Jan Plhak
// https://github.com/loschmidt/discretizer

// Discretizer is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// Discretizer is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with Discretizer.  If not, see <https://www.gnu.org/licenses/>.

#pragma once
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>);

namespace minball {
    namespace py = pybind11;

    constexpr uint16_t DIM_FROM = 1;
    constexpr uint16_t DIM_TO = 4;
    template <uint16_t Dim = DIM_FROM>
    void py_bind(py::module& m);
}
