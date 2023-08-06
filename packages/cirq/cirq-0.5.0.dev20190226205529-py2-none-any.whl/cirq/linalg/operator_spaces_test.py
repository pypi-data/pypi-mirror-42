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

from __future__ import division
from __future__ import absolute_import
import itertools

import numpy as np
import pytest
import scipy.linalg

import cirq

I = np.eye(2)
X = np.array([[0, 1], [1, 0]])
Y = np.array([[0, -1j], [1j, 0]])
Z = np.array([[1, 0], [0, -1]])
H = np.array([[1, 1], [1, -1]]) * np.sqrt(0.5)
SQRT_X = np.array([[np.sqrt(1j), np.sqrt(-1j)],
                   [np.sqrt(-1j), np.sqrt(1j)]]) * np.sqrt(0.5)
SQRT_Y = np.array([[np.sqrt(1j), -np.sqrt(1j)],
                   [np.sqrt(1j), np.sqrt(1j)]]) * np.sqrt(0.5)
SQRT_Z = np.diag([1, 1j])
E00 = np.diag([1, 0])
E01 = np.array([[0, 1], [0, 0]])
E10 = np.array([[0, 0], [1, 0]])
E11 = np.diag([0, 1])
PAULI_BASIS = cirq.PAULI_BASIS
STANDARD_BASIS = {u'a': E00, u'b': E01, u'c': E10, u'd': E11}


def _one_hot_matrix(size, i, j):
    result = np.zeros((size, size))
    result[i, j] = 1
    return result


@pytest.mark.parametrize(u'basis1, basis2, expected_kron_basis', (
    (PAULI_BASIS, PAULI_BASIS, {
        u'II': np.eye(4),
        u'IX': scipy.linalg.block_diag(X, X),
        u'IY': scipy.linalg.block_diag(Y, Y),
        u'IZ': np.diag([1, -1, 1, -1]),
        u'XI': np.array([[0, 0, 1, 0],
                        [0, 0, 0, 1],
                        [1, 0, 0, 0],
                        [0, 1, 0, 0]]),
        u'XX': np.rot90(np.eye(4)),
        u'XY': np.rot90(np.diag([1j, -1j, 1j, -1j])),
        u'XZ': np.array([[0, 0, 1, 0],
                        [0, 0, 0, -1],
                        [1, 0, 0, 0],
                        [0, -1, 0, 0]]),
        u'YI': np.array([[0, 0, -1j, 0],
                        [0, 0, 0, -1j],
                        [1j, 0, 0, 0],
                        [0, 1j, 0, 0]]),
        u'YX': np.rot90(np.diag([1j, 1j, -1j, -1j])),
        u'YY': np.rot90(np.diag([-1, 1, 1, -1])),
        u'YZ': np.array([[0, 0, -1j, 0],
                        [0, 0, 0, 1j],
                        [1j, 0, 0, 0],
                        [0, -1j, 0, 0]]),
        u'ZI': np.diag([1, 1, -1, -1]),
        u'ZX': scipy.linalg.block_diag(X, -X),
        u'ZY': scipy.linalg.block_diag(Y, -Y),
        u'ZZ': np.diag([1, -1, -1, 1]),
    }),
    (STANDARD_BASIS, STANDARD_BASIS, {
        u'abcd'[2 * row_outer + col_outer] + u'abcd'[2 * row_inner + col_inner]:
        _one_hot_matrix(4, 2 * row_outer + row_inner, 2 * col_outer + col_inner)
        for row_outer in xrange(2)
        for row_inner in xrange(2)
        for col_outer in xrange(2)
        for col_inner in xrange(2)
    }),
))
def test_kron_bases(basis1, basis2, expected_kron_basis):
    kron_basis = cirq.kron_bases(basis1, basis2)
    assert len(kron_basis) == 16
    assert set(kron_basis.keys()) == set(expected_kron_basis.keys())
    for name in kron_basis.keys():
        assert np.all(kron_basis[name] == expected_kron_basis[name])


@pytest.mark.parametrize(u'basis1,basis2', (
    (PAULI_BASIS, cirq.kron_bases(PAULI_BASIS)),
    (STANDARD_BASIS, cirq.kron_bases(STANDARD_BASIS, repeat=1)),
    (cirq.kron_bases(PAULI_BASIS, PAULI_BASIS),
     cirq.kron_bases(PAULI_BASIS, repeat=2)),
    (cirq.kron_bases(
        cirq.kron_bases(PAULI_BASIS, repeat=2),
        cirq.kron_bases(PAULI_BASIS, repeat=3),
        PAULI_BASIS),
     cirq.kron_bases(PAULI_BASIS, repeat=6)),
    (cirq.kron_bases(
        cirq.kron_bases(PAULI_BASIS, STANDARD_BASIS),
        cirq.kron_bases(PAULI_BASIS, STANDARD_BASIS)),
     cirq.kron_bases(PAULI_BASIS, STANDARD_BASIS, repeat=2)),
))
def test_kron_bases_consistency(basis1, basis2):
    assert set(basis1.keys()) == set(basis2.keys())
    for name in basis1.keys():
        assert np.all(basis1[name] == basis2[name])


@pytest.mark.parametrize(u'basis,repeat', itertools.product(
    (PAULI_BASIS, STANDARD_BASIS),
    xrange(1, 5)
))
def test_kron_bases_repeat_sanity_checks(basis, repeat):
    product_basis = cirq.kron_bases(basis, repeat=repeat)
    assert len(product_basis) == 4**repeat
    for name1, matrix1 in product_basis.items():
        for name2, matrix2 in product_basis.items():
            p = cirq.hilbert_schmidt_inner_product(matrix1, matrix2)
            if name1 != name2:
                assert p == 0
            else:
                assert abs(p) >= 1


@pytest.mark.parametrize(u'm1,m2,expect_real', (
    (X, X, True),
    (X, Y, True),
    (X, H, True),
    (X, SQRT_X, False),
    (I, SQRT_Z, False),
))
def test_hilbert_schmidt_inner_product_is_conjugate_symmetric(
        m1, m2, expect_real):
    v1 = cirq.hilbert_schmidt_inner_product(m1, m2)
    v2 = cirq.hilbert_schmidt_inner_product(m2, m1)
    assert v1 == v2.conjugate()

    assert np.isreal(v1) == expect_real
    if not expect_real:
        assert v1 != v2


@pytest.mark.parametrize(u'a,m1,b,m2', (
    (1, X, 1, Z),
    (2, X, 3, Y),
    (2j, X, 3, I),
    (2, X, 3, X),
))
def test_hilbert_schmidt_inner_product_is_linear(a, m1, b, m2):
    v1 = cirq.hilbert_schmidt_inner_product(H, (a * m1 + b * m2))
    v2 = (a * cirq.hilbert_schmidt_inner_product(H, m1) +
          b * cirq.hilbert_schmidt_inner_product(H, m2))
    assert v1 == v2


@pytest.mark.parametrize(u'm', (I, X, Y, Z, H, SQRT_X, SQRT_Y, SQRT_Z))
def test_hilbert_schmidt_inner_product_is_positive_definite(m):
    v = cirq.hilbert_schmidt_inner_product(m, m)
    assert np.isreal(v)
    assert v.real > 0


@pytest.mark.parametrize(u'm1,m2,expected_value', (
    (X, I, 0),
    (X, X, 2),
    (X, Y, 0),
    (X, Z, 0),
    (H, X, np.sqrt(2)),
    (H, Y, 0),
    (H, Z, np.sqrt(2)),
    (Z, E00, 1),
    (Z, E01, 0),
    (Z, E10, 0),
    (Z, E11, -1),
    (SQRT_X, E00, np.sqrt(-.5j)),
    (SQRT_X, E01, np.sqrt(.5j)),
    (SQRT_X, E10, np.sqrt(.5j)),
    (SQRT_X, E11, np.sqrt(-.5j)),
))
def test_hilbert_schmidt_inner_product_values(m1, m2, expected_value):
    v = cirq.hilbert_schmidt_inner_product(m1, m2)
    assert np.isclose(v, expected_value)


@pytest.mark.parametrize(u'm,basis', itertools.product(
    (I, X, Y, Z, H, SQRT_X, SQRT_Y, SQRT_Z),
    (PAULI_BASIS, STANDARD_BASIS),
))
def test_expand_matrix_in_orthogonal_basis(m, basis):
    expansion = cirq.expand_matrix_in_orthogonal_basis(m, basis)

    reconstructed = np.zeros(m.shape, dtype=complex)
    for name, coefficient in expansion.items():
        reconstructed += coefficient * basis[name]
    assert np.allclose(m, reconstructed)


@pytest.mark.parametrize(u'expansion', (
    {u'I': 1}, {u'X': 1}, {u'Y': 1}, {u'Z': 1}, {u'X': 1, u'Z': 1},
    {u'I': 0.5, u'X': 0.4, u'Y': 0.3, u'Z': 0.2},
    {u'I': 1, u'X': 2, u'Y': 3, u'Z': 4},
))
def test_matrix_from_basis_coefficients(expansion):
    m = cirq.matrix_from_basis_coefficients(expansion, PAULI_BASIS)

    for name, coefficient in expansion.items():
        element = PAULI_BASIS[name]
        expected_coefficient = (
                cirq.hilbert_schmidt_inner_product(m, element) /
                cirq.hilbert_schmidt_inner_product(element, element)
        )
        assert np.isclose(coefficient, expected_coefficient)


@pytest.mark.parametrize(
    u'm1,basis', (
    itertools.product(
        (I, X, Y, Z, H, SQRT_X, SQRT_Y, SQRT_Z, E00, E01, E10, E11),
        (PAULI_BASIS, STANDARD_BASIS),
    )
))
def test_expand_is_inverse_of_reconstruct(m1, basis):
    c1 = cirq.expand_matrix_in_orthogonal_basis(m1, basis)
    m2 = cirq.matrix_from_basis_coefficients(c1, basis)
    c2 = cirq.expand_matrix_in_orthogonal_basis(m2, basis)
    assert np.allclose(m1, m2)
    assert c1 == c2
