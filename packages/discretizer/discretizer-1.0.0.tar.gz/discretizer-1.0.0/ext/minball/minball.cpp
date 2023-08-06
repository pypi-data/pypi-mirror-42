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

#include <CGAL/Cartesian_d.h>
#include <CGAL/Random.h>
#include <CGAL/Min_sphere_of_spheres_d.h>
#include <array>
#include <vector>
#include "minball.hpp"

PYBIND11_PLUGIN(minball) {
    pybind11::module m("discretizer.minball");
    minball::py_bind(m);
    return m.ptr();
}

namespace minball {

template <uint16_t Dim>
struct Sphere {
    const std::array<double, Dim> center;
    const double radius;

    Sphere(const std::array<double, Dim> center_vec, const double radius)
     : center(center_vec), radius(radius)
    { }
};

template <uint16_t Dim>
void py_bind(py::module& m) {
    typedef double                            FT;
    typedef CGAL::Cartesian_d<FT>             K;
    typedef CGAL::Min_sphere_of_spheres_d_traits_d<K,FT,Dim> Traits;
    typedef CGAL::Min_sphere_of_spheres_d<Traits> Min_sphere;
    typedef K::Point_d                        Point;

    const std::string str_dim = std::to_string(Dim) + "D";
    const auto class_name = "Sphere" + str_dim;
    const auto fun_name = "get_min_sphere" + str_dim;

    py::class_<Sphere<Dim>>(m, class_name.c_str())
    .def(py::init<const std::array<double, Dim>, const double>())
    .def_property_readonly("center", [](const Sphere<Dim>& self) {
        return self.center;
    })
    .def_property_readonly("radius", [](const Sphere<Dim>& self) {
        return self.radius;
    });

    m.def(fun_name.c_str(), [&](const std::vector<Sphere<Dim>>& spheres) {
        std::vector<typename Traits::Sphere> mSpheres;
        for (const auto& s : spheres) {
            Point center(Dim, s.center.begin(), s.center.end());
            mSpheres.emplace_back(center, s.radius);
        }

        Min_sphere ms(mSpheres.begin(), mSpheres.end());
        CGAL_assertion(ms.is_valid());

        std::array<double, Dim> center;

        auto begin = ms.center_cartesian_begin();
        auto end = ms.center_cartesian_end();
        size_t i = 0;

        for (auto it = begin; it != end; ++it, ++i) {
            center[i] = *it;
        }
        return Sphere<Dim>(center, ms.radius());
    });
    py_bind<Dim + 1>(m);
}

template <>
void py_bind<DIM_TO + 1>(py::module&) {
}

}
