# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class BigdftAtlab(AutotoolsPackage):
    """BigDFT-atlab: library for ATomic related operations."""

    homepage = "https://bigdft.org/"
    url = "https://gitlab.com/l_sim/bigdft-suite/-/archive/1.9.2/bigdft-suite-1.9.2.tar.gz"
    git = "https://gitlab.com/l_sim/bigdft-suite.git"

    version("develop", branch="devel")
    version("1.9.4", sha256="fa22115e6353e553d2277bf054eb73a4710e92dfeb1ed9c5bf245337187f393d")
    version("1.9.3", sha256="f5f3da95d7552219f94366b4d2a524b2beac988fb2921673a65a128f9a8f0489")
    version("1.9.2", sha256="dc9e49b68f122a9886fa0ef09970f62e7ba21bb9ab1b86be9b7d7e22ed8fbe0f")
    version("1.9.1", sha256="3c334da26d2a201b572579fc1a7f8caad1cbf971e848a3e10d83bc4dc8c82e41")
    version("1.9.0", sha256="4500e505f5a29d213f678a91d00a10fef9dc00860ea4b3edf9280f33ed0d1ac8")

    variant("mpi", default=True, description="Enable MPI support")
    variant("openmp", default=True, description="Enable OpenMP support")
    variant("openbabel", default=False, description="Enable detection of openbabel compilation")
    variant(
        "shared", default=True, description="Build shared libraries"
    )  # Not default in bigdft, but is typically the default expectation

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")

    depends_on("mpi", when="+mpi")
    depends_on("openbabel", when="+openbabel")

    for vers in ["1.9.0", "1.9.1", "1.9.2", "1.9.3", "1.9.4", "develop"]:
        depends_on(f"bigdft-futile@{vers}", when=f"@{vers}")

    configure_directory = "atlab"

    def configure_args(self):
        spec = self.spec
        prefix = self.prefix

        fcflags = []
        cflags = []
        cxxflags = []

        if "+openmp" in spec:
            fcflags.append(self.compiler.openmp_flag)

        if spec.satisfies("+shared"):
            fcflags.append("-fPIC")
            cflags.append("-fPIC")
            cxxflags.append("-fPIC")
        if self.spec.satisfies("%gcc@10:"):
            fcflags.append("-fallow-argument-mismatch")

        args = [
            f"FCFLAGS={' '.join(fcflags)}",
            f"CFLAGS={' '.join(cflags)}",
            f"CXXFLAGS={' '.join(cxxflags)}",
            f"--with-futile-libs={spec['bigdft-futile'].libs.ld_flags}",
            f"--with-futile-incs={spec['bigdft-futile'].headers.include_flags}/futile",
            f"--with-moduledir={prefix.include}",
            f"--prefix={prefix}",
            "--without-etsf-io",
        ]
        if spec.satisfies("+shared"):
            args.append("--enable-dynamic-libraries")

        if "+mpi" in spec:
            args.append(f"CC={spec['mpi'].mpicc}")
            args.append(f"CXX={spec['mpi'].mpicxx}")
            args.append(f"FC={spec['mpi'].mpifc}")
            args.append(f"F90={spec['mpi'].mpifc}")
            args.append(f"F77={spec['mpi'].mpif77}")
        else:
            args.append("--disable-mpi")

        if "+openmp" in spec:
            args.append("--with-openmp")
        else:
            args.append("--without-openmp")

        if "+openbabel" in spec:
            args.append("--enable-openbabel")
            args.append(f"--with-openbabel-libs={spec['openbabel'].prefix.lib}")
            args.append(f"--with-openbabel-incs={spec['openbabel'].prefix.include}")

        return args

    @property
    def libs(self):
        shared = "+shared" in self.spec
        return find_libraries("libatlab-*", root=self.prefix, shared=shared, recursive=True)
