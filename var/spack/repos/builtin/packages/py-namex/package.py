# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNamex(PythonPackage):
    """A simple utility to separate the implementation of your Python package
    and its public API surface."""

    pypi = "namex/namex-0.0.7.tar.gz"

    license("Apache-2.0")

    version("0.0.7", sha256="84ba65bc4d22bd909e3d26bf2ffb4b9529b608cb3f9a4336f776b04204ced69b")

    depends_on("py-setuptools", type="build")
