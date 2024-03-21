# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os

from spack.package import *


class HsakmtRoct(CMakePackage):
    """This is a thunk python recipe to build and install Thunk Interface.
    Thunk Interface is a user-mode API interfaces used to interact
    with the ROCk driver."""

    homepage = "https://github.com/ROCm/ROCT-Thunk-Interface"
    git = "https://github.com/ROCm/ROCT-Thunk-Interface.git"
    url = "https://github.com/ROCm/ROCT-Thunk-Interface/archive/rocm-6.0.2.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath")

    version("master", branch="master")
    version("6.0.2", sha256="5354bda9382f80edad834463f2c684289841770a4f7b13f0f40bd8271cc4c71d")
    version("6.0.0", sha256="9f4e80bd0a714ce45326941b906a62298c62025eff186dc6c48282ce84c787c7")
    version("5.7.1", sha256="38bc3732886a52ca9cd477ec6fcde3ab17a0ba5dc8e2f7ac34c4de597bd00e8b")
    version("5.7.0", sha256="52293e40c4ba0c653d796e2f6109f5fb4c79f5fb82310ecbfd9a5432acf9da43")
    version("5.6.1", sha256="d60b355bfd21a08e0e36270fd56f98d052c3c6edca47da887fa32bf32759c29b")
    version("5.6.0", sha256="cd009c5c09f664f046c428ba9843582ab468f7b88d560747eb949d8d7f8c5567")
    version("5.5.1", sha256="4ffde3fc1f91f24cdbf09263fd8e012a3995ad10854f4c1d866beab7b9f36bf4")
    version("5.5.0", sha256="2b11fd8937c2b06cd4ddea2c3699fbf3d1651892c4c5957d38553b993dd9af18")
    version("5.4.3", sha256="3799abbe7177fbff3b304e2a363e2b39e8864f8650ae569b2b88b9291f9a710c")
    version("5.4.0", sha256="690a78a6e67ae2b3f518dbc4a1e267237d6a342e1063b31eef297f4a04d780f8")
    version("5.3.3", sha256="b5350de915997ed48072b37a21c2c44438028255f6cc147c25a196ad383c52e7")
    version("5.3.0", sha256="c150be3958fd46e57bfc9db187819ec34b1db8f0cf9b69f8c3f8915001800ab8")
    with default_args(deprecated=True):
        version("5.2.3", sha256="8d313b8fd945a8d7248c00a2de9a2ee896fe77e464430a91b63400a986ec0bf0")
        version("5.2.1", sha256="13c4a6748c4ae70f87869f10fda101d67c9dbaecf040687f7f5d9bb8b6d0506c")
        version("5.2.0", sha256="3797cb0eafbec3fd3d4a2b53f789eb8cdbab30729f13dbcca0a10bc1bafd2187")
        version("5.1.3", sha256="3c66b1aa7451571ce8bee10e601d34b93c9416b9be476610ee5685dbad81034a")
        version("5.1.0", sha256="032717e80b1aefed59f11399e575564ee86ee7c125e889f7c79c2afdfab1eb93")

    variant("shared", default=True, description="Build shared or static library")
    variant("asan", default=False, description="Build with address-sanitizer enabled or disabled")

    depends_on("pkgconfig", type="build", when="@4.5.0:")
    depends_on("cmake@3:", type="build")
    depends_on("numactl")
    depends_on("libdrm", when="@4.5.0:")

    for ver in ["5.3.0", "5.4.0", "5.4.3"]:
        depends_on(f"llvm-amdgpu@{ver}", type="test", when=f"@{ver}")

    for ver in ["5.5.0", "5.5.1", "5.6.0", "5.6.1", "5.7.0", "5.7.1", "6.0.0", "6.0.2"]:
        depends_on(f"rocm-core@{ver}", when=f"@{ver}")
        depends_on(f"llvm-amdgpu@{ver}", type="test", when=f"@{ver}")

    # See https://github.com/ROCm/ROCT-Thunk-Interface/issues/72
    # and https://github.com/spack/spack/issues/28398
    patch("0001-Remove-compiler-support-libraries-and-libudev-as-req.patch", when="@4.5.0:5.2")
    patch("0002-Remove-compiler-support-libraries-and-libudev-as-req-5.3.patch", when="@5.3.0:5.4")

    def cmake_args(self):
        args = []
        if self.spec.satisfies("@:5.4.3"):
            args.append(self.define_from_variant("BUILD_SHARED_LIBS", "shared"))
        else:
            args.append(self.define("BUILD_SHARED_LIBS", False))
        if self.spec.satisfies("@5.4.3:"):
            args.append(self.define("CMAKE_INSTALL_LIBDIR", "lib"))
        if self.spec.satisfies("@5.7.0:"):
            args.append(self.define_from_variant("ADDRESS_SANITIZER", "asan"))

        return args

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check_install(self):
        if self.spec.satisfies("@:5.3.0"):
            print("Skipping: stand-alone tests")
            return
        test_dir = "tests/kfdtest"
        with working_dir(test_dir, create=True):
            cmake_bin = join_path(self.spec["cmake"].prefix.bin, "cmake")
            prefixes = ";".join(
                [
                    self.spec["libdrm"].prefix,
                    self.spec["hsakmt-roct"].prefix,
                    self.spec["numactl"].prefix,
                    self.spec["pkgconfig"].prefix,
                    self.spec["llvm-amdgpu"].prefix,
                    self.spec["zlib-api"].prefix,
                    self.spec["ncurses"].prefix,
                ]
            )
            hsakmt_path = ";".join([self.spec["hsakmt-roct"].prefix])
            cc_options = [
                "-DCMAKE_PREFIX_PATH=" + prefixes,
                "-DLIBHSAKMT_PATH=" + hsakmt_path,
                ".",
            ]
            self.run_test(cmake_bin, cc_options)
            make()
            os.environ["LD_LIBRARY_PATH"] = hsakmt_path
            os.environ["BIN_DIR"] = os.getcwd()
            self.run_test("scripts/run_kfdtest.sh")
            make("clean")
