# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Comgr(CMakePackage):
    """This provides various Lightning Compiler related services. It currently
    contains one library, the Code Object Manager (Comgr)"""

    homepage = "https://github.com/ROCm/ROCm-CompilerSupport"
    git = "https://github.com/ROCm/ROCm-CompilerSupport.git"
    url = "https://github.com/ROCm/ROCm-CompilerSupport/archive/rocm-6.0.0.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath", "haampie")
    libraries = ["libamd_comgr"]

    license("NCSA")

    version("master", branch="amd-stg-open")
    version("6.0.2", sha256="737b110d9402509db200ee413fb139a78369cf517453395b96bda52d0aa362b9")
    version("6.0.0", sha256="04353d27a512642a5e5339532a39d0aabe44e0964985de37b150a2550385800a")
    version("5.7.1", sha256="3b9433b4a0527167c3e9dfc37a3c54e0550744b8d4a8e1be298c8d4bcedfee7c")
    version("5.7.0", sha256="e234bcb93d602377cfaaacb59aeac5796edcd842a618162867b7e670c3a2c42c")
    version("5.6.1", sha256="0a85d84619f98be26ca7a32c71f94ed3c4e9866133789eabb451be64ce739300")
    version("5.6.0", sha256="9396a7238b547ee68146c669b10b9d5de8f1d76527c649133c75d8076a185a72")
    version("5.5.1", sha256="0fbb15fe5a95c2e141ccd360bc413e1feda283334781540a6e5095ab27fd8019")
    version("5.5.0", sha256="97dfff03226ce0902b9d5d1c8c7bebb7a15978a81b6e9c750bf2d2473890bd42")
    version("5.4.3", sha256="8af18035550977fe0aa9cca8dfacbe65fe292e971de5a0e160710bafda05a81f")
    version("5.4.0", sha256="f4b83b27ff6195679d695c3f41fa25456e9c50bae6d978f46d3541b472aef757")
    version("5.3.3", sha256="6a4ef69e672a077b5909977248445f0eedf5e124af9812993a4d444be030c78b")
    version("5.3.0", sha256="072f849d79476d87d31d62b962e368762368d540a9da02ee2675963dc4942b2c")
    with default_args(deprecated=True):
        version("5.2.3", sha256="36d67dbe791d08ad0a02f0f3aedd46059848a0a232c5f999670103b0410c89dc")
        version("5.2.1", sha256="ebeaea8e653fc2b9d67d3271be44690ac7876ee679baa01d47863e75362b8c85")
        version("5.2.0", sha256="5f63fa93739ee9230756ef93c53019474b6cdddea3b588492d785dae1b08c087")
        version("5.1.3", sha256="3078c10e9a852fe8357712a263ad775b15944e083f93a879935c877511066ac9")
        version("5.1.0", sha256="1cdcfe5acb768ef50fb0026d4ee7ba01e615251ad3c27bb2593cdcf8c070a894")

    # Disable the hip compile tests.  Spack should not be using
    # /opt/rocm, and this breaks the build when /opt/rocm exists.
    patch("hip-tests.patch", when="@:4.2.0")

    depends_on("cmake@3.13.4:", type="build")

    depends_on("zlib-api", type="link")
    depends_on("z3", type="link")
    depends_on("ncurses", type="link")

    depends_on("rocm-cmake@3.5.0:", type="build")

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
        # llvm libs are linked statically, so this *could* be a build dep
        depends_on(f"llvm-amdgpu@{ver}", when=f"@{ver}")

        # aomp may not build rocm-device-libs as part of llvm-amdgpu, so make
        # that a conditional dependency
        depends_on(f"rocm-device-libs@{ver}", when=f"@{ver} ^llvm-amdgpu ~rocm-device-libs")

    for ver in ["5.5.0", "5.5.1", "5.6.0", "5.6.1", "5.7.0", "5.7.1", "6.0.0"]:
        depends_on(f"rocm-core@{ver}", when=f"@{ver}")

    root_cmakelists_dir = join_path("lib", "comgr")

    def cmake_args(self):
        args = [self.define("BUILD_TESTING", self.run_tests)]
        if self.spec.satisfies("@5.4.3:"):
            args.append("-DCMAKE_INSTALL_LIBDIR=lib")
        return args

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
