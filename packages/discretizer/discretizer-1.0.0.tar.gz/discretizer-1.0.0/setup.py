# This file is part of Discretizer.
#
# Copyright (c) 2017 Jan Plhak
# https://github.com/loschmidt/discretizer
#
# Discretizer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Discretizer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Discretizer.  If not, see <https://www.gnu.org/licenses/>.

import sys
import setuptools
from setuptools.command.build_ext import build_ext
from distutils.core import Extension

import discretizer


###############################################################################
#
# Code adapted from pybind11 python_example project.
#
# This code is necessary to build the package correctly on older or special
# distributions (e.g. Ubuntu 14.04).
#
# Credits: pybind11 project
# URL: https://github.com/pybind/python_example
#
class get_pybind_include(object):
    """Helper class to determine the pybind11 include path
    The purpose of this class is to postpone importing pybind11
    until it is actually installed, so that the ``get_include()``
    method can be invoked. """

    def __init__(self, user=False):
        self.user = user

    def __str__(self):
        import pybind11
        return pybind11.get_include(self.user)

# As of Python 3.6, CCompiler has a `has_flag` method.
# cf http://bugs.python.org/issue26689
def has_flag(compiler, flagname):
    """Return a boolean indicating whether a flag name is supported on
    the specified compiler.
    """
    import tempfile
    with tempfile.NamedTemporaryFile('w', suffix='.cpp') as f:
        f.write('int main (int argc, char **argv) { return 0; }')
        try:
            compiler.compile([f.name], extra_postargs=[flagname])
        except setuptools.distutils.errors.CompileError:
            return False
    return True


def cpp_flag(compiler):
    """Return the -std=c++[11/14] compiler flag.
    The c++14 is prefered over c++11 (when it is available).
    """
    if has_flag(compiler, '-std=c++14'):
        return '-std=c++14'
    elif has_flag(compiler, '-std=c++11'):
        return '-std=c++11'
    else:
        raise RuntimeError('Unsupported compiler -- at least C++11 support '
                           'is needed!')


class BuildExt(build_ext):
    """A custom build extension for adding compiler-specific options."""
    c_opts = {
        'msvc': ['/EHsc'],
        'unix': [],
    }

    if sys.platform == 'darwin':
        c_opts['unix'] += ['-stdlib=libc++', '-mmacosx-version-min=10.7']

    def build_extensions(self):
        ct = self.compiler.compiler_type
        opts = self.c_opts.get(ct, [])
        if ct == 'unix':
            opts.append('-DVERSION_INFO="%s"' % self.distribution.get_version())
            opts.append(cpp_flag(self.compiler))
            if has_flag(self.compiler, '-fvisibility=hidden'):
                opts.append('-fvisibility=hidden')
        elif ct == 'msvc':
            opts.append('/DVERSION_INFO=\\"%s\\"' % self.distribution.get_version())
        for ext in self.extensions:
            ext.extra_compile_args = opts
        build_ext.build_extensions(self)
#
#
###############################################################################


ext_minball = Extension('discretizer.minball',
                    sources=['ext/minball/minball.cpp'],
                    depends=['ext/minball/minball.hpp'],
                    libraries=['CGAL'],
                    include_dirs=[
                        'ext/minball',
                        get_pybind_include(),
                        get_pybind_include(user=True)
                    ],
                    language='c++')

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="discretizer",
    version=discretizer.__version__,
    author="Jan Plhak",
    author_email="408420@mail.muni.cz",
    description="Tool used to transform tunnel in protein to a sequence of disks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/loschmidt/discretizer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    install_requires=[
        'pybind11',
        'docopt==0.*',
        'numpy',
        'scipy',
    ],
    cmdclass={'build_ext': BuildExt},
    scripts=['scripts/discretizer'],
    ext_modules = [ext_minball],
)
