
# This file is part of PyEMMA.
#
# Copyright (c) 2015, 2014 Computational Molecular Biology Group, Freie Universitaet Berlin (GER)
#
# PyEMMA is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''
Created on 28.10.2013

@author: marscher
'''
from numpy.testing import assert_allclose as assert_allclose_np

__all__ = ['assert_allclose',
           ]


def assert_allclose(actual, desired, rtol=1.e-5, atol=1.e-8,
                    err_msg='', verbose=True):
    r"""wrapper for numpy.testing.allclose with default tolerances of
    numpy.allclose. Needed since testing method has different values."""
    return assert_allclose_np(actual, desired, rtol=rtol, atol=atol,
                              err_msg=err_msg, verbose=verbose)


def _hash_numpy_array(x):
    import numpy as np
    x = np.ascontiguousarray(x)
    import hashlib
    old = x.flags.writeable
    try:
        x.flags.writeable = False
        v = hashlib.sha1(x)
    finally:
        x.flags.writeable = old
    hash_value = hash((x.shape, x.strides, v.digest()))

    return hash_value
