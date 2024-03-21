# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Rccl(CMakePackage):
    """RCCL (pronounced "Rickle") is a stand-alone library
    of standard collective communication routines for GPUs,
    implementing all-reduce, all-gather, reduce, broadcast,
    and reduce-scatter."""

    homepage = "https://github.com/ROCm/rccl"
    git = "https://github.com/ROCm/rccl.git"
    url = "https://github.com/ROCm/rccl/archive/rocm-6.0.2.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath")
    libraries = ["librccl"]
    version("6.0.2", sha256="5c8495acba3d620b751e729d1157e7b4eea8f5e5692c50ce47c5204d3dfd443c")
    version("6.0.0", sha256="0496d5a5f2e48c92cd390ab318df31a53cf7ec590988c2574c9f3d99c38b0fa7")
    version("5.7.1", sha256="fb4c1f0084196d1226ce8a726d0f012d3890b54508a06ca87bbda619be8b90b1")
    version("5.7.0", sha256="4c2825a3e4323ef3c2f8855ef445c1a81cf1992fb37e3e8a07a50db354aa3954")
    version("5.6.1", sha256="27ec6b86a1a329684d808f728c1fce134517ac8e6e7047689f95dbf8386c077e")
    version("5.6.0", sha256="cce13c8a9e233e7ddf91a67b1626b7aaeaf818fefe61af8de6b6b6ff47cb358c")
    version("5.5.1", sha256="f6b9dc6dafeb49d95c085825876b09317d8252771c746ccf5aa19a9204a404b2")
    version("5.5.0", sha256="be2964b408741d046bcd606d339a233d1d1deac7b841647ec53d6d62d71452ba")
    version("5.4.3", sha256="a2524f602bd7b3b6afeb8ba9aff660216ee807fa836e46442d068b5ed5f51a4d")
    version("5.4.0", sha256="213f4f3d75389be588673e43f563e5c0d6908798228b0b6a71f27138fd4ed0c7")
    version("5.3.3", sha256="8995a2d010ad0748fc85ac06e8da7e8d110ba996db04d42b77526c9c059c05bb")
    version("5.3.0", sha256="51da5099fa58c2be882319cebe9ceabe2062feebcc0c5849e8c109030882c10a")
    with default_args(deprecated=True):
        version("5.2.3", sha256="ecba09f4c95b4b2dae81b88231a972ac956d29909b5e712e21cf2a74bd251ff4")
        version("5.2.1", sha256="cfd17dc003f19900e44928d81111570d3720d4905321f2a18c909909c4bee822")
        version("5.2.0", sha256="6ee3a04da0d16eb53f768a088633a7d8ecc4416a2d0c07f7ba8426ab7892b060")
        version("5.1.3", sha256="56491257f27b48bf85f4b91434a2a6e49a448337c889db181b02c8a4a260a4bc")
        version("5.1.0", sha256="02b0180857e615326f9cab775573436b9162899ad8e526830f54392b8a51b1f5")

    amdgpu_targets = ROCmPackage.amdgpu_targets

    variant(
        "amdgpu_target",
        description="AMD GPU architecture",
        values=auto_or_any_combination_of(*amdgpu_targets),
        sticky=True,
    )

    patch("0002-Fix-numactl-rocm-smi-path-issue.patch", when="@:5.2.1")
    patch("0003-Fix-numactl-rocm-smi-path-issue.patch", when="@5.2.3:5.6")
    patch("0004-Set-rocm-core-path-for-version-file.patch", when="@6.0:")

    depends_on("cmake@3.5:", type="build")
    depends_on("chrpath", when="@5.3.0:5", type="build")
    depends_on("numactl@2:")

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
        depends_on(f"hip@{ver}", when=f"@{ver}")
        depends_on(f"comgr@{ver}", when=f"@{ver}")
        depends_on(f"hsa-rocr-dev@{ver}", when=f"@{ver}")

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
        depends_on(f"rocm-smi-lib@{ver}", when=f"@{ver}")

    for ver in ["5.5.0", "5.5.1", "5.6.0", "5.6.1", "5.7.0", "5.7.1", "6.0.0", "6.0.2"]:
        depends_on(f"rocm-core@{ver}", when=f"@{ver}")

    depends_on("googletest@1.11.0:", when="@5.3:")

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

    def setup_build_environment(self, env):
        env.set("CXX", self.spec["hip"].hipcc)
        env.set("ROCMCORE_PATH", self.spec["rocm-core"].prefix)

    def cmake_args(self):
        args = [
            self.define("NUMACTL_DIR", self.spec["numactl"].prefix),
            self.define("ROCM_SMI_DIR", self.spec["rocm-smi-lib"].prefix),
        ]
        if "auto" not in self.spec.variants["amdgpu_target"]:
            args.append(self.define_from_variant("AMDGPU_TARGETS", "amdgpu_target"))

        if self.spec.satisfies("^cmake@3.21.0:3.21.2"):
            args.append(self.define("__skip_rocmclang", "ON"))

        if self.spec.satisfies("@5.3.0:"):
            args.append(self.define("BUILD_TESTS", "ON"))
        return args

    def test(self):
        if self.spec.satisfies("@:5.3.0"):
            print("Skipping: stand-alone tests")
            return
        test_dir = join_path(self.spec["rccl"].prefix, "bin")
        with working_dir(test_dir, create=True):
            self.run_test("UnitTests")
