# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ripgrep(CargoPackage):
    """ripgrep is a line-oriented search tool that recursively searches
    your current directory for a regex pattern.  ripgrep is similar to
    other popular search tools like The Silver Searcher, ack and grep.
    """

    homepage = "https://github.com/BurntSushi/ripgrep"
    url = "https://github.com/BurntSushi/ripgrep/archive/11.0.2.tar.gz"

    maintainers("alecbcs")

    license("MIT OR Unlicense")

    version("14.1.0", sha256="33c6169596a6bbfdc81415910008f26e0809422fda2d849562637996553b2ab6")
    version("14.0.3", sha256="f5794364ddfda1e0411ab6cad6dd63abe3a6b421d658d9fee017540ea4c31a0e")
    version("13.0.0", sha256="0fb17aaf285b3eee8ddab17b833af1e190d73de317ff9648751ab0660d763ed2")
    version("11.0.2", sha256="0983861279936ada8bc7a6d5d663d590ad34eb44a44c75c2d6ccd0ab33490055")
