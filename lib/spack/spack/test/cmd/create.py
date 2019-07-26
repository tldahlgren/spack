# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import os
import pytest

import spack.cmd.create
import spack.util.editor
from spack.url import UndetectableNameError
from spack.main import SpackCommand


create = SpackCommand('create')


@pytest.fixture(scope='module')
def parser():
    """Returns the parser for the module"""
    prs = argparse.ArgumentParser()
    spack.cmd.create.setup_parser(prs)
    return prs


@pytest.mark.parametrize('args,name_index,expected', [
    (['test-package'], 0, [r'TestPackage(Package)', r'def install(self']),
    (['-n', 'test-named-package', 'file://example.tar.gz'], 1,
     [r'TestNamedPackage(Package)', r'def install(self']),
    (['-t', 'bundle', 'test-bundle'], 2, [r'TestBundle(BundlePackage)']),
    (['-n', 'test-named-bundle'], 1, [r'TestNamedBundle(BundlePackage)'])
])
def test_create_template(parser, mock_test_repo, args, name_index, expected):
    """Test template creation."""
    repo, repodir = mock_test_repo

    constr_args = parser.parse_args(['--skip-editor'] + args)
    spack.cmd.create.create(parser, constr_args)

    filename = repo.filename_for_package_name(args[name_index])
    assert os.path.exists(filename)

    with open(filename, 'r') as package_file:
        content = ' '.join(package_file.readlines())
        for entry in expected:
            assert entry in content


@pytest.mark.parametrize('url,expected', [
    (None, 'bundle'),
    ('downloads.sourceforge.net/octave/', 'octave'),
])
def test_build_system_guesser_urls(parser, url, expected):
    """Test basic build systems based solely on urls."""
    guesser = spack.cmd.create.BuildSystemGuesser()

    # Ensure get the expected build system
    opts = {'stage': None, 'url': url}
    guesser(**opts)
    assert guesser.build_system == expected

    # Also ensure get the correct template
    args = parser.parse_args([url])
    bs = spack.cmd.create.get_build_system(args, guesser)
    assert bs == expected


@pytest.mark.parametrize('url,expected', [
    ('testname', 'testname'),
    ('file://example.com/archive.tar.gz', 'archive'),
])
def test_get_name_urls(parser, url, expected):
    """Test get_name with different URLs."""
    args = parser.parse_args([url])
    name = spack.cmd.create.get_name(args)
    assert name == expected


def test_get_name_error(parser, monkeypatch):
    """Test get_name UndetectableNameError exception path."""
    def _parse_name_offset(path, v):
        raise UndetectableNameError(path)

    monkeypatch.setattr(spack.url, 'parse_name_offset', _parse_name_offset)

    url = 'downloads.sourceforge.net/noapp/'
    args = parser.parse_args([url])

    with pytest.raises(SystemExit, matches="Couldn't guess a name"):
        spack.cmd.create.get_name(args)
