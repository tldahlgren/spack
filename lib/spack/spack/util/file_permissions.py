# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path
import llnl.util.filesystem as fs
import spack.package_prefs as pp


def set_permissions_by_spec(path, spec):
    if os.path.isdir(path):
        perms = pp.get_package_dir_permissions(spec)
    else:
        perms = pp.get_package_permissions(spec)
    group = pp.get_package_group(spec)

    fs.chmod_x(path, perms)
    if group:
        fs.chgrp(path, group)
