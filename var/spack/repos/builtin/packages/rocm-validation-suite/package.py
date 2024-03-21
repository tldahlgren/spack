# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class RocmValidationSuite(CMakePackage):
    """The ROCm Validation Suite (RVS) is a system administrators
    and cluster manager's tool for detecting and troubleshooting
    common problems affecting AMD GPU(s) running in a high-performance
    computing environment, enabled using the ROCm software stack on a
    compatible platform."""

    homepage = "https://github.com/ROCm/ROCmValidationSuite"
    url = "https://github.com/ROCm/ROCmValidationSuite/archive/rocm-6.0.2.tar.gz"
    tags = ["rocm"]

    license("MIT")

    maintainers("srekolam", "renjithravindrankannath")
    version("6.0.2", sha256="8286d00ce290eeace3697138da9d7a9669f54152e5febcd9e5c5156ae79f0c0c")
    version("6.0.0", sha256="a84e36b5e50e70ba033fb6bc6fa99da2e32bf7eaef2098df3164365a77a8f14c")
    version("5.7.1", sha256="202f2b6e014bbbeec40af5d3ec630c042f09a61087a77bd70715d81044ea4d65")
    version("5.7.0", sha256="f049b7786a220e9b6dfe099f17727dd0d9e41be9e680fe8309eae400cc5536ea")
    version("5.6.1", sha256="d5e4100e2d07311dfa101563c15d026a8130442cdee8af9ef861832cd7866c0d")
    version("5.6.0", sha256="54cc5167055870570c97ee7114f48d24d5415f984e0c9d7b58b83467e0cf18fb")
    version("5.5.1", sha256="0fbfaa9f68642b590ef04f9778013925bbf3f17bdcd35d4c85a8ffd091169a6e")
    version("5.5.0", sha256="296add772171db67ab8838d2db1ea56df21e895c0348c038768e40146e4fe86a")
    version("5.4.3", sha256="1f0888e559104a4b8c2f5322f7463e425f2baaf12aeb1a8982a5974516e7b667")
    version("5.4.0", sha256="ca2abfa739c2853f71453e65787e318ab879be8a6a362c4cb4d27baa90f3cd5f")
    version("5.3.3", sha256="9acbc8de9b2e18659f51bd49f6e92ab6c93742e2ed0046322025f017fc12497f")
    version("5.3.0", sha256="d6afb8a5f4eaf860fd510bcfe65e735cbf96d4b8817c758ea7aee84d4c994382")
    with default_args(deprecated=True):
        version("5.2.3", sha256="5dfbd41c694bf2eb4368edad8653dc60ec2927d174fc7aaa5fa416156c5f921f")
        version("5.2.1", sha256="a0ea3ab9cbb8ac17bfa4537713a4d7075f869949bfdead4565a46f75864bd4a9")
        version("5.2.0", sha256="2dfef5d66f544230957ac9aaf647b2f1dccf3cc7592cc322cae9fbdcf3321365")
        version("5.1.3", sha256="0140a4128c31749c078d9e1dc863cbbd690efc65843c34a4b80f0056e5b8c7b6")
        version("5.1.0", sha256="d9b9771b885bd94e5d0352290d3fe0fa12f94ce3f384c3844002cd7614880010")

    patch("005-cleanup-path-reference-donot-download-googletest-yaml.patch", when="@:5.2")
    patch("006-library-path.patch", when="@:5.2")
    patch(
        "007-cleanup-path-reference-donot-download-googletest-yaml-library-path_5.3.patch",
        when="@5.3.0:5.5",
    )
    patch(
        "007-cleanup-path-reference-donot-download-googletest-yaml-library-path_5.6.patch",
        when="@5.6",
    )
    patch("008-correcting-library-and-include-path-WITHOUT-RVS-BUILD-TESTS.patch", when="@5.7")
    patch("009-replacing-rocm-path-with-package-path.patch", when="@6.0")
    depends_on("cmake@3.5:", type="build")
    depends_on("zlib-api", type="link")
    depends_on("yaml-cpp~shared")
    depends_on("googletest")
    depends_on("doxygen", type="build")

    def setup_build_environment(self, build_env):
        spec = self.spec
        build_env.set("HIPCC_PATH", spec["hip"].prefix)

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
        depends_on(f"hip@{ver}", when=f"@{ver}")
        depends_on(f"rocminfo@{ver}", when=f"@{ver}")
        depends_on(f"rocblas@{ver}", when=f"@{ver}")
        depends_on(f"rocm-smi-lib@{ver}", when=f"@{ver}")

    def patch(self):
        if self.spec.satisfies("@:5.1"):
            filter_file(
                r"@ROCM_PATH@/rvs", self.spec.prefix.rvs, "rvs/conf/deviceid.sh.in", string=True
            )
        elif self.spec.satisfies("@5.2:5.4"):
            filter_file(
                r"@ROCM_PATH@/bin", self.spec.prefix.bin, "rvs/conf/deviceid.sh.in", string=True
            )
        elif self.spec.satisfies("@5.5:"):
            filter_file(
                r"@ROCM_PATH@/rvs", self.spec.prefix.rvs, "rvs/conf/deviceid.sh.in", string=True
            )

    def cmake_args(self):
        args = [
            self.define("RVS_BUILD_TESTS", False),
            self.define("HIP_PATH", self.spec["hip"].prefix),
            self.define("HSA_PATH", self.spec["hsa-rocr-dev"].prefix),
            self.define("ROCM_SMI_DIR", self.spec["rocm-smi-lib"].prefix),
            self.define("ROCBLAS_DIR", self.spec["rocblas"].prefix),
            self.define("YAML_INC_DIR", self.spec["yaml-cpp"].prefix.include),
            self.define("YAML_LIB_DIR", self.spec["yaml-cpp"].prefix.lib64),
            self.define("UT_INC", self.spec["googletest"].prefix.include),
        ]
        libloc = self.spec["googletest"].prefix.lib64
        if not os.path.isdir(libloc):
            libloc = self.spec["googletest"].prefix.lib
        args.append(self.define("UT_LIB", libloc))
        libloc = self.spec["hsakmt-roct"].prefix.lib64
        if not os.path.isdir(libloc):
            libloc = self.spec["hsakmt-roct"].prefix.lib
        args.append(self.define("HSAKMT_LIB_DIR", libloc))
        return args
