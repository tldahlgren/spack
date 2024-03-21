# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class RocmDebugAgent(CMakePackage):
    """Radeon Open Compute (ROCm) debug agent"""

    homepage = "https://github.com/ROCm/rocr_debug_agent"
    git = "https://github.com/ROCm/rocr_debug_agent.git"
    url = "https://github.com/ROCm/rocr_debug_agent/archive/rocm-6.0.0.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath")
    libraries = ["librocm-debug-agent"]
    version("6.0.2", sha256="da8da1241a6cbb9d0b2a3b81829faf632225a7a27ca881c9715b9f05bca54c89")
    version("6.0.0", sha256="705be2c2bd0f5c7d1e286eb9b94045b2bd017ff323f07bca9aa7c81f2d168524")
    version("5.7.1", sha256="3b8d2835935da98f41e7cfc5b808c596ac06dd705b9a07bb70283e002f8dea6a")
    version("5.7.0", sha256="d9344ed02e82a01140f2162e901e6a519e5fee6b498e2f49417730ee2660c5c1")
    version("5.6.1", sha256="d3b1d5d757489ed3cc66d351cec56b7b850aaa7ecf6a55b0350b89c3dee3153a")
    version("5.6.0", sha256="0bed788f07906afeb9092d0bec184a7963233ac9d8ccd20b4afeb624a1d20698")
    version("5.5.1", sha256="1bb66734f11bb57df6efa507f0217651446653bf28b3ca36acfcf94511a7c2bc")
    version("5.5.0", sha256="4f2431a395a77a06dc417ed1e9188731b031a0c680e62c6eee19d60965317f5a")
    version("5.4.3", sha256="b2c9ac198ea3cbf35e7e80f57c5d81c461de78b821d07b637ea4037a65cdf49f")
    version("5.4.0", sha256="94bef73ea0a6d385dab2292ee591ca1dc268a5585cf9f1b5092a1530949f575e")
    version("5.3.3", sha256="7170312d08e91334ee03586aa1f23d67f33d9ec0df25a5556cbfa3f210b15b06")
    version("5.3.0", sha256="8dfb6aa442ce136207c0c089321c8099042395977b4a488e4ca219661df0cd78")
    with default_args(deprecated=True):
        version("5.2.3", sha256="5d31372e2980738271ae26b92dcc402c387cdf5f23710ce6feeb2bd303ff7ea0")
        version("5.2.1", sha256="a60c224c546a25dafcff1e50ce3a1605e152efdb36624a672ddb5812cd34773e")
        version("5.2.0", sha256="f8e8d5ad691033d0c0f1850d69f35c98ba9722ab4adc66c4251f22257f56f0a2")
        version("5.1.3", sha256="ef26130829f3348d503669467ab1ea39fb67d943d88d64e7ac04b9617ec6067d")
        version("5.1.0", sha256="e0ceeef575d8645385bc6e4c9c3accaa192a93c42d83545cf5626c848f59806b")

    depends_on("cmake@3:", type="build")
    depends_on("elfutils@:0.168", type="link")

    for ver in [
        "5.1.0",
        "5.1.3",
        "5.2.0",
        "5.2.1",
        "5.2.3",
        "5.3.0",
        "5.3.3",
        "5.4.0",
        "5.4.3",
        "5.5.0",
        "5.5.1",
        "5.6.0",
        "5.6.1",
        "5.7.0",
        "5.7.1",
        "6.0.0",
        "6.0.2",
    ]:
        depends_on(f"hsa-rocr-dev@{ver}", when=f"@{ver}")
        depends_on(f"hsakmt-roct@{ver}", when=f"@{ver}")

    for ver in [
        "5.1.0",
        "5.1.3",
        "5.2.0",
        "5.2.1",
        "5.2.3",
        "5.3.0",
        "5.3.3",
        "5.4.0",
        "5.4.3",
        "5.5.0",
        "5.5.1",
        "5.6.0",
        "5.6.1",
        "5.7.0",
        "5.7.1",
        "6.0.0",
        "6.0.2",
    ]:
        depends_on(f"rocm-dbgapi@{ver}", when=f"@{ver}")
        depends_on(f"hip@{ver}", when=f"@{ver}")

    for ver in ["5.5.0", "5.5.1", "5.6.0", "5.6.1", "5.7.0", "5.7.1", "6.0.0", "6.0.2"]:
        depends_on(f"rocm-core@{ver}", when=f"@{ver}")

    # https://github.com/ROCm/rocr_debug_agent/pull/4
    patch("0001-Drop-overly-strict-Werror-flag.patch")
    patch("0002-add-hip-architecture.patch")

    @classmethod
    def determine_version(cls, lib):
        match = re.search(r"lib\S*\.so\.\d+\.\d+\.(\d)(\d\d)(\d\d)", lib)
        if match:
            return "{0}.{1}.{2}".format(
                int(match.group(1)), int(match.group(2)), int(match.group(3))
            )
        return None

    def cmake_args(self):
        spec = self.spec
        args = []

        if spec.satisfies("@:5.1"):
            args.append(self.define("CMAKE_MODULE_PATH", spec["hip"].prefix.cmake))
        elif spec.satisfies("@5.2.0:"):
            args.append(self.define("CMAKE_MODULE_PATH", spec["hip"].prefix.lib.cmake.hip))
        return args
