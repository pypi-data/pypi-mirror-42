# coding=utf-8
# Copyright 2018 The Cirq Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

u"""Utilities for manipulating linear operators as elements of vector space."""

from __future__ import division
from __future__ import absolute_import
from typing import Dict

import numpy as np

PAULI_BASIS = {
    u'I': np.eye(2),
    u'X': np.array([[0., 1.], [1., 0.]]),
    u'Y': np.array([[0., -1j], [1j, 0.]]),
    u'Z': np.diag([1., -1]),
}


def kron_bases(*bases, **_3to2kwargs):
    if 'repeat' in _3to2kwargs: repeat = _3to2kwargs['repeat']; del _3to2kwargs['repeat']
    else: repeat =  1
    u"""Creates tensor product of bases."""
    product_basis = {u'': 1}
    for basis in bases * repeat:
        product_basis = {
            name1 + name2: np.kron(matrix1, matrix2)
            for name1, matrix1 in product_basis.items()
            for name2, matrix2 in basis.items()
        }
    return product_basis


def hilbert_schmidt_inner_product(m1, m2):
    u"""Computes Hilbert-Schmidt inner product of two matrices.

    Linear in second argument.
    """
    return np.einsum(u'ij,ij', m1.conj(), m2)


def expand_matrix_in_orthogonal_basis(
        m,
        basis,
):
    u"""Computes coefficients of expansion of m in basis.

    We require that basis be orthogonal w.r.t. the Hilbert-Schmidt inner
    product. We do not require that basis be orthonormal. Note that Pauli
    basis (I, X, Y, Z) is orthogonal, but not orthonormal.
    """
    return dict((
        name, (hilbert_schmidt_inner_product(b, m) /
               hilbert_schmidt_inner_product(b, b)))
        for name, b in basis.items())


def matrix_from_basis_coefficients(expansion,
                                   basis):
    u"""Computes linear combination of basis vectors with given coefficients."""
    some_element = iter(basis.values()).next()
    result = np.zeros_like(some_element, dtype=np.complex128)
    for name, coefficient in expansion.items():
        result += coefficient * basis[name]
    return result
