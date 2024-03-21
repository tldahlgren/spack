# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class RoctracerDev(CMakePackage, ROCmPackage):
    """ROC-tracer library: Runtimes Generic Callback/Activity APIs.
    The goal of the implementation is to provide a generic independent from
    specific runtime profiler to trace API and asyncronous activity."""

    homepage = "https://github.com/ROCm/roctracer"
    git = "https://github.com/ROCm/roctracer.git"
    url = "https://github.com/ROCm/roctracer/archive/rocm-6.0.2.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath")
    libraries = ["libroctracer64"]

    license("MIT")
    version("6.0.2", sha256="1e0105b32fdd9c010aab304bb2ca1a5a38ba323cea610afe1135657edda8f26e")
    version("6.0.0", sha256="941166a0363c5689bfec118d54e986c43fb1ec8cbf18d95721d9a824bd52c0f8")
    version("5.7.1", sha256="ec0453adac7e62b142eb0df1e1e2506863aac4c3f2ce9d117c3184c08c0c6b48")
    version("5.7.0", sha256="40bb757920488466e29df90bb80a975cc340bf7f8771fb1d754dfbb6b688d78e")
    version("5.6.1", sha256="007c498be25b067ad9a7631a2b0892f9129150ee9714e471a921225875d45e69")
    version("5.6.0", sha256="cbcfe4fa2e8b627006b320a93992fb3078696d8ef2ef049b4b880b6b7d57e13e")
    version("5.5.1", sha256="3afc31ebfdb14b0365185ca6b9326a83b1503a94a51d910f5ce7ced192d8c133")
    version("5.5.0", sha256="fe9ad95628fa96639db6fc33f78d334c814c7161b4a754598f5a4a7852625777")
    version("5.4.3", sha256="6b5111be5efd4d7fd6935ca99b06fab19b43d97a58d26fc1fe6e783c4de9a926")
    version("5.4.0", sha256="04c1e955267a3e8440833a177bb976f57697aba0b90c325d07fc0c6bd4065aea")
    version("5.3.3", sha256="f2cb1e6bb69ea1a628c04f984741f781ae1d8498dc58e15795bb03015f924d13")
    version("5.3.0", sha256="36f1da60863a113bb9fe2957949c661f00a702e249bb0523cda1fb755c053808")
    with default_args(deprecated=True):
        version("5.2.3", sha256="93f4bb7529db732060bc12055aa10dc346a459a1086cddd5d86c7b509301be4f")
        version("5.2.1", sha256="e200b5342bdf840960ced6919d4bf42c8f30f8013513f25a2190ee8767667e59")
        version("5.2.0", sha256="9747356ce61c57d22c2e0a6c90b66a055e435d235ba3459dc3e3f62aabae6a03")
        version("5.1.3", sha256="45f19875c15eb609b993788b47fd9c773b4216074749d7744f3a671be17ef33c")
        version("5.1.0", sha256="58b535f5d6772258190e4adcc23f37c916f775057a91b960e1f2ee1f40ed5aac")

    depends_on("cmake@3:", type="build")
    depends_on("python@3:", type="build")
    depends_on("py-cppheaderparser", type="build")

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
        depends_on(f"hsakmt-roct@{ver}", when=f"@{ver}")
        depends_on(f"hsa-rocr-dev@{ver}", when=f"@{ver}")
        depends_on(f"rocminfo@{ver}", when=f"@{ver}")
        depends_on(f"hip@{ver}", when=f"@{ver}")
    for ver in ["5.1.0", "5.1.3", "5.2.0", "5.2.1", "5.2.3", "5.3.0", "5.3.3", "5.4.0", "5.4.3"]:
        depends_on(f"rocprofiler-dev@{ver}", when=f"@{ver}")

    for ver in ["5.5.0", "5.5.1", "5.6.0", "5.6.1", "5.7.0", "5.7.1", "6.0.0", "6.0.2"]:
        depends_on(f"rocm-core@{ver}", when=f"@{ver}")

    patch("0001-include-rocprofiler-dev-path.patch", when="@5.3:5.4")

    @classmethod
    def determine_version(cls, lib):
        match = re.search(r"rocm-(\d+)\.(\d+)\.(\d)/lib/lib\S*\.so\.\d+\.\d+\.\d+", lib)
        if match:
            return "{0}.{1}.{2}".format(
                int(match.group(1)), int(match.group(2)), int(match.group(3))
            )
        return None

    def patch(self):
        filter_file(
            r"${CMAKE_PREFIX_PATH}/hsa",
            "${HSA_RUNTIME_INC_PATH}",
            "src/CMakeLists.txt",
            string=True,
        )
        with working_dir("script"):
            filter_file(
                "^#!/usr/bin/python[23]",
                f"#!{self.spec['python'].command.path}",
                "check_trace.py",
                "gen_ostream_ops.py",
                "hsaap.py",
            )

    def cmake_args(self):
        args = [
            self.define("HIP_VDI", "1"),
            self.define("CMAKE_MODULE_PATH", f"{self.stage.source_path}/cmake_modules"),
            self.define("HSA_RUNTIME_HSA_INC_PATH", self.spec["hsa-rocr-dev"].prefix.include),
            self.define("CMAKE_POSITION_INDEPENDENT_CODE", True),
        ]
        if self.spec.satisfies("@:5.4.0"):
            args.append(self.define("ROCPROFILER_PATH", self.spec["rocprofiler-dev"].prefix))
        if self.spec.satisfies("@6.0:"):
            args.append("-DCMAKE_INSTALL_LIBDIR=lib")

        return args
