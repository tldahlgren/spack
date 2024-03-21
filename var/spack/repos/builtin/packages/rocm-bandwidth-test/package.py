# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RocmBandwidthTest(CMakePackage):
    """Test to measure PciE bandwidth on ROCm platforms"""

    homepage = "https://github.com/ROCm/rocm_bandwidth_test"
    git = "https://github.com/ROCm/rocm_bandwidth_test.git"
    url = "https://github.com/ROCm/rocm_bandwidth_test/archive/rocm-6.0.0.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath")

    version("master", branch="master")
    version("6.0.2", sha256="af95fe84729701184aeb14917cee0d8d77ab1858ddcced01eb7380401e2134ae")
    version("6.0.0", sha256="9023401bd6a896059545b8e6263c6730afd89d7d45c0f5866261c300415532a6")
    version("5.7.1", sha256="7426ef1e317b8293e4d6389673cfa8c63efb3f7d061e2f50a6f0b1b706e2a2a7")
    version("5.7.0", sha256="fa95c28488ab4bb6d920b9f3c316554ca340f44c87ec2efb4cf8fa488e63ddd9")
    version("5.6.1", sha256="849af715d08dfd89e7aa5e4453b624151db1cafaa567ab5fa36a77948b90bf0d")
    version("5.6.0", sha256="ae2f7263a21a3a650068f43e3112b2b765eea80a5af2297572f850c77f83c85e")
    version("5.5.1", sha256="768b3da49fe7d4bb4e6536a8ee15be9f5e865d961e813ed4a407f32402685e1f")
    version("5.5.0", sha256="1070ce14d45f34c2c6b2fb003184f3ae735ccfd640e9df1c228988b2a5a82949")
    version("5.4.3", sha256="a2f5a75bf47db1e39a4626a9f5cd2d120bcafe56b1baf2455d794f7a4734993e")
    version("5.4.0", sha256="47a1ef92e565d5ce7a167cc1ebe3d4198cc04d598b259426245b8c11eb795677")
    version("5.3.3", sha256="2bc079297e639d45d57c8017f6f47bc44d4ed34613ec76c80574bb703d79b498")
    version("5.3.0", sha256="a97365c04d79663db7c85027c63a12d56356abc0a351697f49c2d82bf9ef8999")
    with default_args(deprecated=True):
        version("5.2.3", sha256="b76fe33898d67ec1f5f1ec58adaea88e88ed28b1f5470aa4c08c347d8f558af2")
        version("5.2.1", sha256="ebdf868bef8ab6c7f32775ba6eab85cf3e078af1fc1b1a11fdbaad777f37a190")
        version("5.2.0", sha256="046f2a6984c62899f57a557490136fbe7ab28e2fd334750abac71b03609226ef")
        version("5.1.3", sha256="6a6e7fb998c886951db75dcf34dca523d9caaff8d0ccf2b7431504a1808b1ff3")
        version("5.1.0", sha256="18fe51f0ba61760fc89ffc81f737fd4fa20fb4b00df3f35145be77c3e0a6162b")

    depends_on("cmake@3:", type="build")

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
        depends_on(f"hsa-rocr-dev@{ver}", when=f"@{ver}")
        depends_on(f"hsakmt-roct@{ver}", when=f"@{ver}")

    for ver in ["5.5.0", "5.5.1", "5.6.0", "5.6.1", "5.7.0", "5.7.1", "6.0.0", "6.0.2"]:
        depends_on(f"rocm-core@{ver}", when=f"@{ver}")

    build_targets = ["package"]
