# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import tempfile

from spack.package import *


class PyKeras(PythonPackage):
    """Multi-backend Keras.

    Keras 3 is a new multi-backend implementation of the Keras API,
    with support for TensorFlow, JAX, and PyTorch.
    """

    homepage = "https://keras.io"
    git = "https://github.com/keras-team/keras.git"
    pypi = "keras/keras-3.0.0.tar.gz"

    maintainers("adamjstewart")
    license("Apache-2.0")

    version("3.1.0", sha256="cac46e053f0493da313e7c9b16379a532b1a38f9f19c7a5fe4578759f4c6aa4d")
    version("3.0.5", sha256="df3d3795e12c3f6035e811c43c13f1eb41e37241796a0fea120ede4ebe1c4496")
    version("3.0.4", sha256="ff2204792582e3889c51c77722cc6e8258dbb1ece7db192f5a9bcd1887cf3385")
    version("3.0.3", sha256="1e455a82be63b7fb4f699e26bd1e04b7dbcbf66fa3a799117afca9ab067b5d61")
    version("3.0.2", sha256="526b6c053cdd880a33467c5bfd5c460a5bdc0c58869c2683171c2dec2ad3c2d0")
    version("3.0.1", sha256="d993721510fa654582132192193f69b1b3165418a6e00a73c3edce615b3cc672")
    version("3.0.0", sha256="82a9fa4b32a049b38151d11188ed15d74f21f853f163e78da0950dce1f244ccc")
    version("2.15.0", sha256="b281ce09226576e0593b8dab0d9e5d42c334e053ce6f4f154dc6cd745ab93d2f")
    version("2.14.0", sha256="a845d446b6ae626f61dde5ab2fa952530b6c17b4f9ed03e9362bd20172d00cca")
    version("2.13.1", sha256="b3591493cce75a69adef7b192cec6be222e76e2386d132cd4e34aa190b0ecbd5")
    version("2.12.0", sha256="6336cebb6b2b0a91f7efd3ff3a9db3a94f2abccf07a40323138afb80826aec62")
    version("2.11.0", sha256="e7a7c4199ac76ea750d145c1d84ae1b932e68b9bca34e83596bd66b2fc2ad79e")
    version("2.10.0", sha256="b1d8d9358700f4a585455854a142d88cc987419c1638ef935b440842d593ad04")
    version("2.9.0", sha256="90226eaa0337573304f3e5ab44d4d9e3a65fe002776c5cbd0f65b738152c1084")
    version("2.8.0", sha256="5e777b0101d8385d3a90fc9056f1b2f6313f2c830d2e8181828b300c9229ec0c")
    version("2.7.0", sha256="7502746467ab15184e2e267f13fbb2c3f33ba24f8e02a097d229ba376dabaa04")
    version("2.6.0", sha256="15586a3f3e1ed9182e6e0d4c0dbd052dfb7250e779ceb7e24f8839db5c63fcae")
    version("2.4.3", sha256="fedd729b52572fb108a98e3d97e1bac10a81d3917d2103cc20ab2a5f03beb973")
    version("2.4.2", sha256="e26bc51b7b8fb7add452cdf6fba77d6509e6c78b9d9ef5fd32fe132c6d9182d2")
    version("2.4.1", sha256="e282cc9c5c996043b21d045765c0c5bf541c1879232a97a574c51af0ce132cb1")
    version("2.4.0", sha256="e31c6d2910767ab72f630309286fb7bf5476810dd64fde3e254054478442e9b0")
    version("2.3.1", sha256="321d43772006a25a1d58eea17401ef2a34d388b588c9f7646c34796151ebc8cc")
    version("2.3.0", sha256="a0d6ecf1d71cd0b85ea1da27ea7314a9d4723f5b468b7cedd87dcad0a491b354")
    version("2.2.5", sha256="0fb448b95643a708d25d2394183a2f3a84eefb55fb64917152a46826990113ea")
    version("2.2.4", sha256="90b610a3dbbf6d257b20a079eba3fdf2eed2158f64066a7c6f7227023fd60bc9")
    version("2.2.3", sha256="694aee60a6f8e0d3d6d3e4967e063b4623e3ca90032f023fd6d16bb5f81d18de")
    version("2.2.2", sha256="468d98da104ec5c3dbb10c2ef6bb345ab154f6ca2d722d4c250ef4d6105de17a")
    version("2.2.1", sha256="0d3cb14260a3fa2f4a5c4c9efa72226ffac3b4c50135ba6edaf2b3d1d23b11ee")
    version("2.2.0", sha256="5b8499d157af217f1a5ee33589e774127ebc3e266c833c22cb5afbb0ed1734bf")

    variant(
        "backend",
        default="tensorflow",
        description="backend library",
        values=["tensorflow", "jax", "torch"],
        multi=False,
        when="@3:",
    )

    # setup.py
    depends_on("python@3.9:", type=("build", "run"), when="@3:")
    depends_on("python@3.8:", type=("build", "run"), when="@2.12:")
    depends_on("py-setuptools", type="build")
    depends_on("py-absl-py", type=("build", "run"), when="@2.6:")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-rich", type=("build", "run"), when="@3:")
    depends_on("py-namex", type=("build", "run"), when="@3:")
    depends_on("py-h5py", type=("build", "run"))
    depends_on("py-dm-tree", type=("build", "run"), when="@3:")
    depends_on("py-ml-dtypes", type=("build", "run"), when="@3.0.5:")

    # requirements-common.txt
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"), when="@3:")
    depends_on("py-protobuf", type=("build", "run"), when="@3:")

    # requirements-tensorflow-cuda.txt
    depends_on("py-tensorflow@2.16.1", type=("build", "run"), when="@3.0: backend=tensorflow")

    # requirements-jax-cuda.txt
    depends_on("py-jax@0.4.23", type=("build", "run"), when="@3.0.5: backend=jax")
    depends_on("py-jax", type=("build", "run"), when="@3: backend=jax")

    # requirements-torch-cuda.txt
    depends_on("py-torch@2.2.1", type=("build", "run"), when="@3.1.0: backend=torch")
    depends_on("py-torch@2.1.2", type=("build", "run"), when="@3.0.3:3.0.5 backend=torch")
    depends_on("py-torch@2.1.1", type=("build", "run"), when="@3.0.1:3.0.2 backend=torch")
    depends_on("py-torch@2.1.0", type=("build", "run"), when="@3.0.0 backend=torch")
    depends_on("py-torchvision@0.17.1", type=("build", "run"), when="@3.1.0: backend=torch")
    depends_on("py-torchvision@0.16.2", type=("build", "run"), when="@3.0.3:3.0.5 backend=torch")
    depends_on("py-torchvision@0.16.1", type=("build", "run"), when="@3.0.1:3.0.2 backend=torch")
    depends_on("py-torchvision@0.16.0", type=("build", "run"), when="@3.0.0 backend=torch")

    # Historical dependencies
    depends_on("bazel", type="build", when="@2.5:2")
    depends_on("protobuf", type="build", when="@2.5:2")
    depends_on("pil", type=("build", "run"), when="@:2")
    depends_on("py-portpicker", type=("build", "run"), when="@2.10:2")
    depends_on("py-pydot", type=("build", "run"), when="@:2")
    depends_on("py-pyyaml", type=("build", "run"), when="@:2")
    depends_on("py-six", type=("build", "run"), when="@:2")
    for minor_ver in range(6, 16):
        depends_on(
            "py-tensorflow@2.{}".format(minor_ver),
            type=("build", "run"),
            when="@2.{}".format(minor_ver),
        )
        depends_on(
            "py-tensorboard@2.{}".format(minor_ver),
            type=("build", "run"),
            when="@2.{}".format(minor_ver),
        )

    def url_for_version(self, version):
        if version >= Version("3"):
            url = "https://files.pythonhosted.org/packages/source/k/keras/keras-{}.tar.gz"
        elif version >= Version("2.6"):
            url = "https://github.com/keras-team/keras/archive/refs/tags/v{}.tar.gz"
        else:
            url = "https://files.pythonhosted.org/packages/source/k/keras/Keras-{}.tar.gz"
        return url.format(version)

    def setup_run_environment(self, env):
        if self.spec.satisfies("@3:"):
            env.set("KERAS_BACKEND", self.spec.variants["backend"].value)

    @when("@2.5:2")
    def patch(self):
        infile = join_path(self.package_dir, "protobuf_build.patch")
        with open(infile, "r") as source_file:
            text = source_file.read()
        with open("keras/keras.bzl", mode="a") as f:
            f.write(text)

        filter_file(
            'load("@com_google_protobuf//:protobuf.bzl", "py_proto_library")',
            'load("@org_keras//keras:keras.bzl", "py_proto_library")',
            "keras/protobuf/BUILD",
            string=True,
        )

    @when("@2.5:2")
    def install(self, spec, prefix):
        self.tmp_path = tempfile.mkdtemp(prefix="spack")
        env["HOME"] = self.tmp_path

        args = [
            # Don't allow user or system .bazelrc to override build settings
            "--nohome_rc",
            "--nosystem_rc",
            # Bazel does not work properly on NFS, switch to /tmp
            "--output_user_root=" + self.tmp_path,
            "build",
            # Spack logs don't handle colored output well
            "--color=no",
            "--jobs={0}".format(make_jobs),
            # Enable verbose output for failures
            "--verbose_failures",
            "--spawn_strategy=local",
            # bazel uses system PYTHONPATH instead of spack paths
            "--action_env",
            "PYTHONPATH={0}".format(env["PYTHONPATH"]),
            "//keras/tools/pip_package:build_pip_package",
        ]

        bazel(*args)

        build_pip_package = Executable("bazel-bin/keras/tools/pip_package/build_pip_package")
        buildpath = join_path(self.stage.source_path, "spack-build")
        build_pip_package("--src", buildpath)

        with working_dir(buildpath):
            args = std_pip_args + ["--prefix=" + prefix, "."]
            pip(*args)
        remove_linked_tree(self.tmp_path)
