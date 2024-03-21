# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Hipsparse(CMakePackage, CudaPackage, ROCmPackage):
    """hipSPARSE is a SPARSE marshalling library, with
    multiple supported backends"""

    homepage = "https://github.com/ROCm/hipSPARSE"
    git = "https://github.com/ROCm/hipSPARSE.git"
    url = "https://github.com/ROCm/hipSPARSE/archive/rocm-6.0.2.tar.gz"
    tags = ["rocm"]

    maintainers("cgmb", "srekolam", "renjithravindrankannath", "haampie")
    libraries = ["libhipsparse"]

    license("MIT")
    version("6.0.2", sha256="40c1d2493f87c686d9afd84a00321ad10ca0d0d80d6dcfeee8e51858dd1bd8c1")
    version("6.0.0", sha256="718a5f03b6a579c0542a60d00f5688bec53a181b429b7ee8ce3c8b6c4a78d754")
    version("5.7.1", sha256="16c3818260611226c3576d8d55ad8f51e0890d2473503edf2c9313250ae65ca7")
    version("5.7.0", sha256="729b749b5340034639873a99e6091963374f6f0456c8f36d076c96f03fe43888")
    version("5.6.1", sha256="d636d0c5d1e38cc0c09b1e95380199ec82bd465b94bd6661f0c8d9374d9b565d")
    version("5.6.0", sha256="3a6931b744ebaa4469a4c50d059a008403e4dc2a4f04dd69c3c6d20916b4a491")
    version("5.5.1", sha256="3d291e4fe2c611d555e54de66149b204fe7ac59f5dd00a9ad93bc6dca0528880")
    version("5.5.0", sha256="8122c8f17d899385de83efb7ac0d8a4fabfcd2aa21bbed63e63ea7adf0d22df6")
    version("5.4.3", sha256="b373eccd03679a13fab4e740fc780da25cbd598abca3a1e5e3613ae14954f9db")
    version("5.4.0", sha256="47420d38483c8124813b744971e428a0352c83d9b62a5a50f74ffa8f9b785b20")
    version("5.3.3", sha256="d96d0e47594ab12e8c380da2300704c105736a0771940d7d2fae666f2869e457")
    version("5.3.0", sha256="691b32b916952ed9af008aa29f60cc190322b73cfc098bb2eda3ff68c89c7b35")
    with default_args(deprecated=True):
        version("5.2.3", sha256="f70d3deff13188adc4105ef3ead53510e4b54075b9ffcfe3d3355d90d4b6eadd")
        version("5.2.1", sha256="7b8e4ff264285ae5aabb3c5c2b38bf28f90b2af44efb0398fcf13ffc24bc000a")
        version("5.2.0", sha256="4fdab6ec953c6d2d000687c5979077deafd37208cd722554b5a6ede1e5ba170c")
        version("5.1.3", sha256="6e6a0752654f0d391533df8cedf4b630a78ad34c99087741520c582963ce1602")
        version("5.1.0", sha256="f41329534f2ff477a0db6b7f77a72bb062f117800970c122d676db8b207ce80b")

    # default to an 'auto' variant until amdgpu_targets can be given a better default than 'none'
    amdgpu_targets = ROCmPackage.amdgpu_targets
    variant(
        "amdgpu_target",
        description="AMD GPU architecture",
        values=spack.variant.DisjointSetsOfValues(("auto",), ("none",), amdgpu_targets)
        .with_default("auto")
        .with_error(
            "the values 'auto' and 'none' are mutually exclusive with any of the other values"
        )
        .with_non_feature_values("auto", "none"),
        sticky=True,
    )
    variant("rocm", default=True, description="Enable ROCm support")
    conflicts("+cuda +rocm", msg="CUDA and ROCm support are mutually exclusive")
    conflicts("~cuda ~rocm", msg="CUDA or ROCm support is required")

    depends_on("hip +cuda", when="+cuda")

    depends_on("cmake@3.5:", type="build")
    depends_on("git", type="build")

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
        depends_on(f"rocm-cmake@{ver}:", type="build", when=f"@{ver}")
        depends_on(f"rocsparse@{ver}", when=f"+rocm @{ver}")

    for tgt in ROCmPackage.amdgpu_targets:
        depends_on(f"rocsparse amdgpu_target={tgt}", when=f"+rocm amdgpu_target={tgt}")

    patch("0a90ddc4c33ed409a938513b9dbdca8bfad65e06.patch", when="@:5.4")

    @classmethod
    def determine_version(cls, lib):
        match = re.search(r"lib\S*\.so\.\d+\.\d+\.(\d)(\d\d)(\d\d)", lib)
        if match:
            ver = "{0}.{1}.{2}".format(
                int(match.group(1)), int(match.group(2)), int(match.group(3))
            )
        else:
            ver = None
        return ver

    def cmake_args(self):
        args = [
            self.define("CMAKE_CXX_STANDARD", "14"),
            self.define("BUILD_CLIENTS_SAMPLES", "OFF"),
            self.define("BUILD_CLIENTS_TESTS", "OFF"),
        ]

        args.append(self.define_from_variant("BUILD_CUDA", "cuda"))

        # FindHIP.cmake is still used for +cuda
        if self.spec.satisfies("+cuda"):
            if self.spec["hip"].satisfies("@:5.1"):
                args.append(self.define("CMAKE_MODULE_PATH", self.spec["hip"].prefix.cmake))
            else:
                args.append(
                    self.define("CMAKE_MODULE_PATH", self.spec["hip"].prefix.lib.cmake.hip)
                )

        if self.spec.satisfies("@5.2.0:"):
            args.append(self.define("BUILD_FILE_REORG_BACKWARD_COMPATIBILITY", True))

        if self.spec.satisfies("@5.3.0:"):
            args.append("-DCMAKE_INSTALL_LIBDIR=lib")

        return args
