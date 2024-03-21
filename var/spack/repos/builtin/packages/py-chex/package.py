# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyChex(PythonPackage):
    """Chex is a library of utilities for helping to write reliable JAX code."""

    homepage = "https://github.com/deepmind/chex"
    pypi = "chex/chex-0.1.0.tar.gz"

    license("Apache-2.0")

    version("0.1.85", sha256="a27cfe87119d6e1fe24ccc1438a59195e6dc1d6e0e10099fcf618c3f64771faf")
    version("0.1.5", sha256="686858320f8f220c82a6c7eeb54dcdcaa4f3d7f66690dacd13a24baa1ee8299e")
    version("0.1.0", sha256="9e032058f5fed2fc1d5e9bf8e12ece5910cf6a478c12d402b6d30984695f2161")

    depends_on("python@3.9:", type=("build", "run"), when="@0.1.85:")
    depends_on("py-setuptools", type="build")
    depends_on("py-absl-py@0.9.0:", type=("build", "run"))
    depends_on("py-typing-extensions@4.2:", type=("build", "run"), when="@0.1.85:")
    depends_on("py-jax@0.4.16:", type=("build", "run"), when="@0.1.85:")
    depends_on("py-jax@0.1.55:", type=("build", "run"))
    depends_on("py-jaxlib@0.1.37:", type=("build", "run"))
    depends_on("py-numpy@1.24.1:", type=("build", "run"), when="@0.1.85:")
    depends_on("py-numpy@1.18.0:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"), when="@0.1.85: ^python@3.12:")
    depends_on("py-toolz@0.9.0:", type=("build", "run"))

    # Historical dependencies
    depends_on("py-dm-tree@0.1.5:", type=("build", "run"), when="@:0.1.5")

    # AttributeError: module 'jax.interpreters.pxla' has no attribute 'ShardedDeviceArray'
    conflicts("^py-jax@0.4.14:", when="@:0.1.5")
