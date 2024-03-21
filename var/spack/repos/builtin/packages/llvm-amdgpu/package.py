# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
import re

from spack.package import *


class LlvmAmdgpu(CMakePackage):
    """Toolkit for the construction of highly optimized compilers,
    optimizers, and run-time environments."""

    homepage = "https://github.com/ROCm/llvm-project"
    git = "https://github.com/ROCm/llvm-project.git"
    url = "https://github.com/ROCm/llvm-project/archive/rocm-6.0.2.tar.gz"
    tags = ["rocm"]
    executables = [r"amdclang", r"amdclang\+\+", r"amdflang", r"clang.*", r"flang.*", "llvm-.*"]
    generator("ninja")

    maintainers("srekolam", "renjithravindrankannath", "haampie")

    license("Apache-2.0")

    version("master", branch="amd-stg-open")
    version("6.0.2", sha256="7d35acc84de1adee65406f92a369a30364703f84279241c444cd93a48c7eeb76")
    version("6.0.0", sha256="c673708d413d60ca8606ee75c77e9871b6953c59029c987b92f2f6e85f683626")
    version("5.7.1", sha256="6b54c422e45ad19c9bf5ab090ec21753e7f7d854ca78132c30eb146657b168eb")
    version("5.7.0", sha256="4abdf00b297a77c5886cedb37e63acda2ba11cb9f4c0a64e133b05800aadfcf0")
    version("5.6.1", sha256="045e43c0c4a3f4f2f1db9fb603a4f1ea3d56e128147e19ba17909eb57d7f08e5")
    version("5.6.0", sha256="e922bd492b54d99e56ed88c81e2009ed6472059a180b10cc56ce1f9bd2d7b6ed")
    version("5.5.1", sha256="7d7181f20f89cb0715191aa32914186c67a34258c13457055570d47e15296553")
    version("5.5.0", sha256="5dc6c99f612b69ff73145bee17524e3712990100e16445b71634106acf7927cf")
    version("5.4.3", sha256="a844d3cc01613f6284a75d44db67c495ac1e9b600eacbb1eb13d2649f5d5404d")
    version("5.4.0", sha256="ff54f45a17723892cd775c1eaff9e5860527fcfd33d98759223c70e3362335bf")
    version("5.3.3", sha256="5296d5e474811c7d1e456cb6d5011db248b79b8d0512155e8a6c2aa5b5f12d38")
    version("5.3.0", sha256="4e3fcddb5b8ea8dcaa4417e0e31a9c2bbdc9e7d4ac3401635a636df32905c93e")
    with default_args(deprecated=True):
        version("5.2.3", sha256="1b852711aec3137b568fb65f93606d37fdcd62e06f5da3766f2ffcd4e0c646df")
        version("5.2.1", sha256="3644e927d943d61e22672422591c47a62ff83e3d87ced68439822156d8f79abf")
        version("5.2.0", sha256="0f892174111b78a02d1a00f8f46d9f80b9abb95513a7af38ecf2a5a0882fe87f")
        version("5.1.3", sha256="d236a2064363c0278f7ba1bb2ff1545ee4c52278c50640e8bb2b9cfef8a2f128")
        version("5.1.0", sha256="db5d45c4a7842a908527c1b7b8d4a40c688225a41d23cfa382eab23edfffdd10")

    variant(
        "rocm-device-libs",
        default=True,
        description=(
            "Build ROCm device libs as external LLVM project instead of a "
            "standalone spack package."
        ),
    )
    variant(
        "llvm_dylib",
        default=False,
        description="Build LLVM shared library, containing all "
        "components in a single shared library",
    )
    variant(
        "link_llvm_dylib",
        default=False,
        description="Link LLVM tools against the LLVM shared library",
    )

    provides("libllvm@14", when="@5:5.2")
    provides("libllvm@15", when="@5.3:5.4")
    provides("libllvm@16", when="@5.5:5.6")
    provides("libllvm@17", when="@5.7:")

    depends_on("cmake@3.13.4:", type="build")
    depends_on("python", type="build")
    depends_on("z3", type="link")
    depends_on("zlib-api", type="link")
    depends_on("ncurses+termlib", type="link")
    depends_on("pkgconfig", type="build")

    # OpenMP clang toolchain looks for bitcode files in llvm/bin/../lib
    # as per 5.2.0 llvm code. It used to be llvm/bin/../lib/libdevice.
    # Below patch is to look in the old path.
    patch("adjust-openmp-bitcode-directory-for-llvm-link.patch", when="@5.2.0:5.6")
    patch("0001-update-HIP_PATH-deduction-for-5.7.0.patch", when="@5.7.0:6.0")

    # Below patch is to set the flag -mcode-object-version=none until
    # the below fix is available in device-libs release code.
    # https://github.com/ROCm/ROCm-Device-Libs/commit/f0356159dbdc93ea9e545f9b61a7842f9c881fdf
    patch("patch-llvm-5.5.0.patch", when="@5.5:5.7 +rocm-device-libs")

    # i1 muls can sometimes happen after SCEV.
    # They resulted in ISel failures because we were missing the patterns for them.
    # This fix is targeting 6.1 rocm release.
    # Need patch until https://github.com/llvm/llvm-project/pull/67291 is merged.
    patch("001-Add-i1-mul-patterns.patch", when="@5.6")
    patch("001-Add-i1-mul-patterns-5.7.patch", when="@5.7")

    # fixes the libamdhip64.so not found in some ROCm math lib tests
    patch(
        "https://github.com/ROCm/llvm-project/commit/444d1d12bbc0269fed5451fb1a9110a049679ca5.patch?full_index=1",
        sha256="b4774ca19b030890d7b276d12c446400ccf8bc3aa724c7f2e9a73531a7400d69",
        when="@6.0",
    )

    conflicts("^cmake@3.19.0")

    root_cmakelists_dir = "llvm"
    install_targets = ["clang-tidy", "install"]

    # Add device libs sources so they can be an external LLVM project
    for d_version, d_shasum in [
        ("6.0.2", "c6d88b9b46e39d5d21bd5a0c1eba887ec473a370b1ed0cebd1d2e910eedc5837"),
        ("6.0.0", "198df4550d4560537ba60ac7af9bde31d59779c8ec5d6309627f77a43ab6ef6f"),
        ("5.7.1", "703de8403c0bd0d80f37c970a698f10f148daf144d34f982e4484d04f7c7bbef"),
        ("5.7.0", "0f8780b9098573f1c456bdc84358de924dcf00604330770a383983e1775bf61e"),
        ("5.6.1", "f0dfab272ff936225bfa1e9dabeb3c5d12ce08b812bf53ffbddd2ddfac49761c"),
        ("5.6.0", "efb5dcdca9b3a9fbe408d494fb4a23e0b78417eb5fa8eebd4a5d226088f28921"),
        ("5.5.1", "3b5f6dd85f0e3371f6078da7b59bf77d5b210e30f1cc66ef1e2de6bbcb775833"),
        ("5.5.0", "5ab95aeb9c8bed0514f96f7847e21e165ed901ed826cdc9382c14d199cbadbd3"),
        ("5.4.3", "f4f7281f2cea6d268fcc3662b37410957d4f0bc23e0df9f60b12eb0fcdf9e26e"),
        ("5.4.0", "d68813ded47179c39914c8d1b76af3dad8c714b10229d1e2246af67609473951"),
        ("5.3.3", "963c9a0561111788b55a8c3b492e2a5737047914752376226c97a28122a4d768"),
        ("5.3.0", "f7e1665a1650d3d0481bec68252e8a5e68adc2c867c63c570f6190a1d2fe735c"),
        ("5.2.3", "16b7fc7db4759bd6fb54852e9855fa16ead76c97871d7e1e9392e846381d611a"),
        ("5.2.1", "e5855387ce73ed483ed0d03dbfef31f297c6ca66cf816f6816fd5ee373fc8225"),
        ("5.2.0", "901674bc941115c72f82c5def61d42f2bebee687aefd30a460905996f838e16c"),
        ("5.1.3", "c41958560ec29c8bf91332b9f668793463904a2081c330c0d828bf2f91d4f04e"),
        ("5.1.0", "47dbcb41fb4739219cadc9f2b5f21358ed2f9895ce786d2f7a1b2c4fd044d30f"),
    ]:
        resource(
            name="rocm-device-libs",
            placement="rocm-device-libs",
            url=f"https://github.com/ROCm/ROCm-Device-Libs/archive/rocm-{d_version}.tar.gz",
            sha256=d_shasum,
            when=f"@{d_version} +rocm-device-libs",
        )

    resource(
        name="rocm-device-libs",
        placement="rocm-device-libs",
        git="https://github.com/ROCm/ROCm-Device-Libs.git",
        branch="amd-stg-open",
        when="@master +rocm-device-libs",
    )
    for d_version, d_shasum in [
        ("6.0.2", "e7ff4d7ac35a2dd8aad1cb40b96511a77a9c23fe4d1607902328e53728e05c28"),
        ("6.0.0", "99e8fa1af52d0bf382f28468e1a345af1ff3452c35914a6a7b5eeaf69fc568db"),
        ("5.7.1", "655e9bfef4b0b6ad3f9b89c934dc0a8377273bb0bccbda6c399ac5d5d2c1c04c"),
        ("5.7.0", "2c56ec5c78a36f2b847afd4632cb25dbf6ecc58661eb2ae038c2552342e6ce23"),
        ("5.6.1", "4de9a57c2092edf9398d671c8a2c60626eb7daf358caf710da70d9c105490221"),
        ("5.6.0", "30875d440df9d8481ffb24d87755eae20a0efc1114849a72619ea954f1e9206c"),
    ]:
        resource(
            name="hsa-runtime",
            placement="hsa-runtime",
            url=f"https://github.com/ROCm/ROCR-Runtime/archive/rocm-{d_version}.tar.gz",
            sha256=d_shasum,
            when=f"@{d_version}",
        )
    resource(
        name="hsa-runtime",
        placement="hsa-runtime",
        git="https://github.com/ROCm/ROCR-Runtime.git",
        branch="master",
        when="@master",
    )

    for d_version, d_shasum in [
        ("6.0.2", "737b110d9402509db200ee413fb139a78369cf517453395b96bda52d0aa362b9"),
        ("6.0.0", "04353d27a512642a5e5339532a39d0aabe44e0964985de37b150a2550385800a"),
        ("5.7.1", "3b9433b4a0527167c3e9dfc37a3c54e0550744b8d4a8e1be298c8d4bcedfee7c"),
        ("5.7.0", "e234bcb93d602377cfaaacb59aeac5796edcd842a618162867b7e670c3a2c42c"),
        ("5.6.1", "0a85d84619f98be26ca7a32c71f94ed3c4e9866133789eabb451be64ce739300"),
        ("5.6.0", "9396a7238b547ee68146c669b10b9d5de8f1d76527c649133c75d8076a185a72"),
    ]:
        resource(
            name="comgr",
            placement="comgr",
            url=f"https://github.com/ROCm/ROCm-CompilerSupport/archive/rocm-{d_version}.tar.gz",
            sha256=d_shasum,
            when=f"@{d_version}",
        )
    resource(
        name="comgr",
        placement="comgr",
        git="https://github.com/ROCm/ROCm-CompilerSupport.git",
        branch="amd-stg-open",
        when="@master",
    )

    def cmake_args(self):
        llvm_projects = ["clang", "lld", "clang-tools-extra", "compiler-rt"]
        llvm_runtimes = ["libcxx", "libcxxabi"]
        args = [
            self.define("LLVM_ENABLE_Z3_SOLVER", "OFF"),
            self.define("LLLVM_ENABLE_ZLIB", "ON"),
            self.define("CLANG_DEFAULT_LINKER", "lld"),
            self.define("LIBCXX_ENABLE_SHARED", "OFF"),
            self.define("LIBCXX_ENABLE_STATIC", "ON"),
            self.define("LIBCXX_INSTALL_LIBRARY", "OFF"),
            self.define("LIBCXX_INSTALL_HEADERS", "OFF"),
            self.define("LIBCXXABI_ENABLE_SHARED", "OFF"),
            self.define("LIBCXXABI_ENABLE_STATIC", "ON"),
            self.define("LIBCXXABI_INSTALL_STATIC_LIBRARY", "OFF"),
            self.define("LLVM_ENABLE_RTTI", "ON"),
            self.define("LLVM_TARGETS_TO_BUILD", "AMDGPU;X86"),
            self.define("LLVM_AMDGPU_ALLOW_NPI_TARGETS", "ON"),
            self.define("LLVM_ENABLE_RUNTIMES", llvm_runtimes),
            self.define("LLVM_ENABLE_PROJECTS", llvm_projects),
            self.define("PACKAGE_VENDOR", "AMD"),
            self.define("CLANG_ENABLE_AMDCLANG", "ON"),
        ]

        # Enable rocm-device-libs as a external project
        if "+rocm-device-libs" in self.spec:
            dir = os.path.join(self.stage.source_path, "rocm-device-libs")
            args.extend(
                [
                    self.define("LLVM_EXTERNAL_PROJECTS", "device-libs"),
                    self.define("LLVM_EXTERNAL_DEVICE_LIBS_SOURCE_DIR", dir),
                ]
            )

        if "+llvm_dylib" in self.spec:
            args.append(self.define("LLVM_BUILD_LLVM_DYLIB", True))

        if "+link_llvm_dylib" in self.spec:
            args.append(self.define("LLVM_LINK_LLVM_DYLIB", True))
            args.append(self.define("CLANG_LINK_CLANG_DYLIB", True))

        # Get the GCC prefix for LLVM.
        if self.compiler.name == "gcc":
            args.append(self.define("GCC_INSTALL_PREFIX", self.compiler.prefix))
        if self.spec.satisfies("@5.4.3:"):
            args.append("-DCMAKE_INSTALL_LIBDIR=lib")
        if self.spec.satisfies("@5.5.0:"):
            args.append("-DCLANG_DEFAULT_RTLIB=compiler-rt")
            args.append("-DCLANG_DEFAULT_UNWINDLIB=libgcc")
        if self.spec.satisfies("@5.5.0:"):
            args.append("-DCLANG_DEFAULT_RTLIB=compiler-rt")
            args.append("-DCLANG_DEFAULT_UNWINDLIB=libgcc")
        if self.spec.satisfies("@5.6.0:"):
            hsainc_path = os.path.join(self.stage.source_path, "hsa-runtime/src/inc")
            comgrinc_path = os.path.join(self.stage.source_path, "comgr/lib/comgr/include")
            args.append("-DSANITIZER_HSA_INCLUDE_PATH={0}".format(hsainc_path))
            args.append("-DSANITIZER_COMGR_INCLUDE_PATH={0}".format(comgrinc_path))
            args.append("-DSANITIZER_AMDGPU:Bool=ON")
        return args

    @classmethod
    def determine_version(cls, path):
        match = re.search(r"amdclang", path)
        detected_version = None
        if match:
            version_query = Executable(path)("--version", output=str)
            match = re.search(r"roc-(\d)\.(\d).(\d)", version_query)
            if match:
                detected_version = "{0}.{1}.{2}".format(
                    int(match.group(1)), int(match.group(2)), int(match.group(3))
                )
        return detected_version

    # Make sure that the compiler paths are in the LD_LIBRARY_PATH
    def setup_run_environment(self, env):
        llvm_amdgpu_home = self.spec["llvm-amdgpu"].prefix
        env.prepend_path("LD_LIBRARY_PATH", llvm_amdgpu_home + "/llvm/lib")

    # Make sure that the compiler paths are in the LD_LIBRARY_PATH
    def setup_dependent_run_environment(self, env, dependent_spec):
        llvm_amdgpu_home = self.spec["llvm-amdgpu"].prefix
        env.prepend_path("LD_LIBRARY_PATH", llvm_amdgpu_home + "/llvm/lib")
