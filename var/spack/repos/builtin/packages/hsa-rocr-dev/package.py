# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

from spack.package import *


class HsaRocrDev(CMakePackage):
    """This repository includes the user mode API nterfaces and libraries
    necessary for host applications to launch computer kernels to available
    HSA ROCm kernel agents.AMD Heterogeneous System Architecture HSA -
    Linux HSA Runtime for Boltzmann (ROCm) platforms."""

    homepage = "https://github.com/ROCm/ROCR-Runtime"
    git = "https://github.com/ROCm/ROCR-Runtime.git"
    url = "https://github.com/ROCm/ROCR-Runtime/archive/rocm-6.0.2.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath", "haampie")
    libraries = ["libhsa-runtime64"]

    version("master", branch="master")
    version("6.0.2", sha256="e7ff4d7ac35a2dd8aad1cb40b96511a77a9c23fe4d1607902328e53728e05c28")
    version("6.0.0", sha256="99e8fa1af52d0bf382f28468e1a345af1ff3452c35914a6a7b5eeaf69fc568db")
    version("5.7.1", sha256="655e9bfef4b0b6ad3f9b89c934dc0a8377273bb0bccbda6c399ac5d5d2c1c04c")
    version("5.7.0", sha256="2c56ec5c78a36f2b847afd4632cb25dbf6ecc58661eb2ae038c2552342e6ce23")
    version("5.6.1", sha256="4de9a57c2092edf9398d671c8a2c60626eb7daf358caf710da70d9c105490221")
    version("5.6.0", sha256="30875d440df9d8481ffb24d87755eae20a0efc1114849a72619ea954f1e9206c")
    version("5.5.1", sha256="53d84ad5ba5086ed4ad67ad892c52c0e4eba8ddfa85c2dd341bf825f4d5fe4ee")
    version("5.5.0", sha256="8dbc776b56f93ddaa2ca38bf3b88299b8091de7c1b3f2e481064896cf6808e6c")
    version("5.4.3", sha256="a600eed848d47a7578c60da7e64eb92f29bbce2ec67932b251eafd4c2974cb67")
    version("5.4.0", sha256="476cd18500cc227d01f6b44c00c7adc8574eb8234b6b4daefc219650183fa090")
    version("5.3.3", sha256="aca88d90f169f35bd65ce3366b8670c7cdbe3abc0a2056eab805d0192cfd7130")
    version("5.3.0", sha256="b51dbedbe73390e0be748b92158839c82d7fa0e514fede60aa7696dc498facf0")
    with default_args(deprecated=True):
        version("5.2.3", sha256="978de85d3455207bb82bef2254a4624e9116b1258a8c164d7a7e21a644eff12f")
        version("5.2.1", sha256="448a7409bdc6618332a42b9503122996f26b91768140b710ba99bff8a8c03dd9")
        version("5.2.0", sha256="529e49693dd9f6459586dd0a26f14dd77dbdf8c0b45fb54830b294eba7babd27")
        version("5.1.3", sha256="479340ec34cdffbbdb1002c85a47d1fccd23e8394631a1f001ef6130be08287d")
        version("5.1.0", sha256="a5f7245059c3d28dbc037e1e6fa3f09084e29147096dd61f7ce5560291ab330f")

    variant("shared", default=True, description="Build shared or static library")
    variant("image", default=True, description="build with or without image support")
    variant("asan", default=False, description="Build with address-sanitizer enabled or disabled")

    depends_on("cmake@3:", type="build")
    depends_on("pkgconfig", type="build", when="@5.3.0:")

    # Note, technically only necessary when='@3.7: +image', but added to all
    # to work around https://github.com/spack/spack/issues/23951
    depends_on("xxd", when="+image", type="build")
    depends_on("elf", type="link")
    depends_on("numactl")
    depends_on("pkgconfig", type="build", when="@5.3.0:")

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
        depends_on(f"hsakmt-roct@{ver}", when=f"@{ver}")
        depends_on(f"llvm-amdgpu@{ver}", when=f"@{ver}")
        # allow standalone rocm-device-libs (useful for aomp)
        depends_on(f"rocm-device-libs@{ver}", when=f"@{ver} ^llvm-amdgpu ~rocm-device-libs")

    for ver in ["5.5.0", "5.5.1", "5.6.0", "5.6.1", "5.7.0", "5.7.1", "6.0.0", "6.0.2"]:
        depends_on(f"rocm-core@{ver}", when=f"@{ver}")

    patch("0002-Remove-explicit-RPATH-again.patch", when="@3.7.0:5.6")

    root_cmakelists_dir = "src"

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
        spec = self.spec

        # hsa-rocr-dev wants the directory containing the header files, but
        # libelf adds an extra path (include/libelf) compared to elfutils
        libelf_include = os.path.dirname(
            find_headers("libelf", spec["elf"].prefix.include, recursive=True)[0]
        )

        args = [
            self.define("LIBELF_INCLUDE_DIRS", libelf_include),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("IMAGE_SUPPORT", "image"),
        ]

        # device libs is bundled with llvm-amdgpu (default) or standalone
        if self.spec.satisfies("^rocm-device-libs"):
            bitcode_dir = spec["rocm-device-libs"].prefix.amdgcn.bitcode
        else:
            bitcode_dir = spec["llvm-amdgpu"].prefix.amdgcn.bitcode

        args.append(self.define("BITCODE_DIR", bitcode_dir))

        if self.spec.satisfies("@5.6:"):
            args.append("-DCMAKE_INSTALL_LIBDIR=lib")
        if self.spec.satisfies("@6.0:"):
            args.append(self.define("ROCM_PATCH_VERSION", "60000"))

        return args
