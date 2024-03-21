# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RocmDeviceLibs(CMakePackage):
    """set of AMD specific device-side language runtime libraries"""

    homepage = "https://github.com/ROCm/ROCm-Device-Libs"
    git = "https://github.com/ROCm/ROCm-Device-Libs.git"
    url = "https://github.com/ROCm/ROCm-Device-Libs/archive/rocm-6.0.2.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath", "haampie")

    version("master", branch="amd-stg-open")
    version("6.0.2", sha256="c6d88b9b46e39d5d21bd5a0c1eba887ec473a370b1ed0cebd1d2e910eedc5837")
    version("6.0.0", sha256="198df4550d4560537ba60ac7af9bde31d59779c8ec5d6309627f77a43ab6ef6f")
    version("5.7.1", sha256="703de8403c0bd0d80f37c970a698f10f148daf144d34f982e4484d04f7c7bbef")
    version("5.7.0", sha256="0f8780b9098573f1c456bdc84358de924dcf00604330770a383983e1775bf61e")
    version("5.6.1", sha256="f0dfab272ff936225bfa1e9dabeb3c5d12ce08b812bf53ffbddd2ddfac49761c")
    version("5.6.0", sha256="efb5dcdca9b3a9fbe408d494fb4a23e0b78417eb5fa8eebd4a5d226088f28921")
    version("5.5.1", sha256="3b5f6dd85f0e3371f6078da7b59bf77d5b210e30f1cc66ef1e2de6bbcb775833")
    version("5.5.0", sha256="5ab95aeb9c8bed0514f96f7847e21e165ed901ed826cdc9382c14d199cbadbd3")
    version("5.4.3", sha256="f4f7281f2cea6d268fcc3662b37410957d4f0bc23e0df9f60b12eb0fcdf9e26e")
    version("5.4.0", sha256="d68813ded47179c39914c8d1b76af3dad8c714b10229d1e2246af67609473951")
    version("5.3.3", sha256="963c9a0561111788b55a8c3b492e2a5737047914752376226c97a28122a4d768")
    version("5.3.0", sha256="f7e1665a1650d3d0481bec68252e8a5e68adc2c867c63c570f6190a1d2fe735c")
    with default_args(deprecated=True):
        version("5.2.3", sha256="16b7fc7db4759bd6fb54852e9855fa16ead76c97871d7e1e9392e846381d611a")
        version("5.2.1", sha256="e5855387ce73ed483ed0d03dbfef31f297c6ca66cf816f6816fd5ee373fc8225")
        version("5.2.0", sha256="901674bc941115c72f82c5def61d42f2bebee687aefd30a460905996f838e16c")
        version("5.1.3", sha256="c41958560ec29c8bf91332b9f668793463904a2081c330c0d828bf2f91d4f04e")
        version("5.1.0", sha256="47dbcb41fb4739219cadc9f2b5f21358ed2f9895ce786d2f7a1b2c4fd044d30f")

    depends_on("cmake@3.13.4:", type="build")

    depends_on("zlib-api", type="link")
    depends_on("texinfo", type="link")

    depends_on("rocm-cmake@3.5.0:", type="build")

    # Make sure llvm is not built with rocm-device-libs (that is, it's already
    # built with rocm-device-libs as an external project).
    depends_on("llvm-amdgpu ~rocm-device-libs")

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
        "master",
    ]:
        depends_on(f"llvm-amdgpu@{ver}", when=f"@{ver}")

    for ver in ["5.5.0", "5.5.1", "5.6.0", "5.6.1", "5.7.0", "5.7.1", "6.0.0", "6.0.2"]:
        depends_on(f"rocm-core@{ver}", when=f"@{ver}")

    def cmake_args(self):
        spec = self.spec
        return [
            self.define("LLVM_DIR", spec["llvm-amdgpu"].prefix),
            self.define("CMAKE_C_COMPILER", spec["llvm-amdgpu"].prefix.bin.clang),
        ]
