"""
Tests for the BSE main API
"""

import random
import pytest

import basis_set_exchange as bse

pytestmark = pytest.mark.xfail


@pytest.mark.parametrize('basis_name', ['cc-pv0z', 'madeup_name'])
def test_get_basis_fail_name(basis_name):
    """Test get_basis with bad names """
    bse.get_basis(basis_name)


@pytest.mark.parametrize('elements', [100, '100', [1, 100], [1, '100']])
def test_get_basis_fail_elements(elements):
    """Test get_basis with bad elements """

    bse.get_basis('cc-pvdz', elements=elements)


@pytest.mark.parametrize('fmt', ['nwchemm', 'nofmt', 1])
def test_get_basis_fail_fmt(fmt):
    """Test get_basis with bad formats """

    bse.get_basis('cc-pvdz', fmt=fmt)


@pytest.mark.parametrize('version', ['v1', -1, '-1', 100])
def test_get_basis_fail_version(version):
    """Test get_basis with bad versions """

    bse.get_basis('cc-pvdz', version=version)


@pytest.mark.parametrize('fmt', ['nwchemm', 'nofmt', 1])
def test_get_basis_fail_data_dir(tmp_path):
    """Test get_basis with bad data dir """

    tmp_path = str(tmp_path)  # Needed for python 3.5
    bse.get_basis('cc-pvdz', data_dir=tmp_path)


def test_get_basis_fail_data_dir(tmp_path):
    """Test get_basis with bad data dir """

    tmp_path = str(tmp_path)  # Needed for python 3.5
    bse.get_basis('cc-pvdz', data_dir=tmp_path)


def test_get_all_basis_names_fail(tmp_path):
    """Test get_all_basis_names with bad data dir """

    tmp_path = str(tmp_path)  # Needed for python 3.5
    bse.get_all_basis_names(tmp_path)


@pytest.mark.parametrize('basis_name', ['cc-pv0z', 'madeup_name'])
def test_lookup_role_fail_name(basis_name):
    """Test get_basis with bad versions """

    bse.lookup_basis_by_role(basis_name, 'rifit')


@pytest.mark.parametrize('role', ['admmfit', 'madeup_name'])
def test_lookup_role_fail_role(role):
    """Test get_basis with bad versions """

    bse.lookup_basis_by_role('def2-tzvp', role)


# yapf: disable
@pytest.mark.parametrize('substr,family,role', [['def2', 'ahlrichsx', 'jkfit'],
                                                ['qqqqq', None, 'notarole'],
                                                ['6-31', 'poplexx,', 'admmfit']])
# yapf: enable
def test_filter_fail(substr, family, role):
    """Test filtering basis set (returning zero results)"""
    md = bse.filter_basis_sets(substr, family, role)
