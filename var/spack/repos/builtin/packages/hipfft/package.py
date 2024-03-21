# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Hipfft(CMakePackage, CudaPackage, ROCmPackage):
    """hipFFT is an FFT marshalling library. Currently, hipFFT supports
    either rocFFT or cuFFT as backends.hipFFT exports an interface that
    does not require the client to change, regardless of the chosen backend.
    It sits between the application and the backend FFT library, marshalling
    inputs into the backend and results back to the application."""

    homepage = "https://github.com/ROCm/hipFFT"
    git = "https://github.com/ROCm/hipFFT.git"
    url = "https://github.com/ROCm/hipfft/archive/rocm-6.0.2.tar.gz"
    tags = ["rocm"]

    maintainers("renjithravindrankannath", "srekolam")

    license("MIT")

    version("master", branch="master")
    version("6.0.2", sha256="c0a4bac5fa9a757a19a4995fa9571328b6ee0a71e93c66a880069794d65d284a")
    version("6.0.0", sha256="44f328b7862c066459089dfe62833cb7d626c6ceb71c57d8c7d6bba45dad491e")
    version("5.7.1", sha256="33452576649df479f084076c47d0b30f6f1da34864094bce767dd9bf609f04aa")
    version("5.7.0", sha256="daa5dc44580145e85ff8ffa7eb40a3d1ef41f3217549c01281715ff696a31588")
    version("5.6.1", sha256="d2ae36b8eacd39b865e8a7972b8eb86bcea2de4ac90711bba7e29b39b01eaa74")
    version("5.6.0", sha256="c7f425b693caf9371b42226d86392335d993a117d23219b6ba1fd13523cb8261")
    version("5.5.1", sha256="3addd15a459752ad657e84c2a7b6b6289600d1d0a5f90d6e0946ba11e8148fc0")
    version("5.5.0", sha256="47ec6f7da7346c312b80daaa8f763e86c7bdc33ac8617cfa3344068e5b20dd9e")
    version("5.4.3", sha256="ae37f40b6019a11f10646ef193716836f366d269eab3c5cc2ed09af85355b945")
    version("5.4.0", sha256="d0a8e790182928b3d19774b8db1eece9b881a422f6a7055c051b12739fded624")
    version("5.3.3", sha256="fd1662cd5b1e1bce9db53b320c0fe614179cd196251efc2ef3365d38922b5cdc")
    version("5.3.0", sha256="ebbe2009b86b688809b6b4d5c3929fc589db455218d54a37790f21339147c5df")
    with default_args(deprecated=True):
        version("5.2.3", sha256="10be731fe91ede5e9f254f6eb3bc00b4dbeab449477f3cac03de358a7d0a6fa1")
        version("5.2.1", sha256="6c8fbace2864ca992b2fca9dc8d0bb4488aef62045acdfcf249d53dd005ebd35")
        version("5.2.0", sha256="ec37edcd61837281c403802ccc1cb01ec3fa3ba135b5ab16617961b66d4cc3e2")
        version("5.1.3", sha256="c26fa64499293b25d0686bed04feb61378c878a4bb4a6d559e6cb7be1f6bf2ec")
        version("5.1.0", sha256="1bac7761c055355216cd262cdc0450aabb383addcb739b56ba849b2e6e013fa5")

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

    depends_on("cmake@3.5:", type="build")

    depends_on("hip +cuda", when="+cuda")

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
        depends_on(f"rocfft@{ver}", when=f"+rocm @{ver}")

    for tgt in ROCmPackage.amdgpu_targets:
        depends_on(f"rocfft amdgpu_target={tgt}", when=f"+rocm amdgpu_target={tgt}")
    # https://github.com/ROCm/rocFFT/pull/85)
    patch("001-remove-submodule-and-sync-shared-files-from-rocFFT.patch", when="@6.0.0")

    def cmake_args(self):
        args = [self.define("BUILD_CLIENTS_SAMPLES", "OFF")]

        if self.spec.satisfies("+rocm"):
            args.append(self.define("BUILD_WITH_LIB", "ROCM"))
        elif self.spec.satisfies("+cuda"):
            args.append(self.define("BUILD_WITH_LIB", "CUDA"))

        # FindHIP.cmake is still used for both +rocm and +cuda
        if self.spec["hip"].satisfies("@:5.1"):
            args.append(self.define("CMAKE_MODULE_PATH", self.spec["hip"].prefix.cmake))
        else:
            args.append(self.define("CMAKE_MODULE_PATH", self.spec["hip"].prefix.lib.cmake.hip))

        if self.spec.satisfies("@5.2.0:"):
            args.append(self.define("BUILD_FILE_REORG_BACKWARD_COMPATIBILITY", True))

        if self.spec.satisfies("@5.3.0:"):
            args.append(self.define("CMAKE_INSTALL_LIBDIR", "lib"))
        return args
