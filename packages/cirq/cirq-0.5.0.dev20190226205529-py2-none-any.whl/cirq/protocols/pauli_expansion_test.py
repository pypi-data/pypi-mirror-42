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
from __future__ import with_statement
from __future__ import absolute_import
from typing import Dict

import numpy as np
import pytest

import cirq


class NoMethod(object):
    pass


class ReturnsNotImplemented(object):
    def _pauli_expansion_(self):
        return NotImplemented


class ReturnsExpansion(object):
    def __init__(self, expansion):
        self._expansion = expansion

    def _pauli_expansion_(self):
        return self._expansion


class HasUnitary(object):
    def __init__(self, unitary):
        self._unitary = unitary

    def _unitary_(self):
        return self._unitary


@pytest.mark.parametrize(u'val', (
    NoMethod(),
    ReturnsNotImplemented(),
    123,
    np.eye(2),
    object(),
    cirq,
))
def test_raises_no_pauli_expansion(val):
    assert cirq.pauli_expansion(val, default=None) is None
    with pytest.raises(TypeError):
        cirq.pauli_expansion(val)


@pytest.mark.parametrize(u'val, expected_expansion', (
    (ReturnsExpansion({u'X': 1, u'Y': 2, u'Z': 3}), {u'X': 1, u'Y': 2, u'Z': 3}),
    (HasUnitary(np.eye(2)), {u'I': 1}),
    (HasUnitary(np.array([[1, -1j], [1j, -1]])), {u'Y': 1, u'Z': 1}),
    (HasUnitary(np.array([[0., 1.], [0., 0.]])), {u'X': 0.5, u'Y': 0.5j}),
    (HasUnitary(np.eye(16)), {u'IIII': 1.0}),
    (cirq.H, {u'X': np.sqrt(0.5), u'Z': np.sqrt(0.5)}),
    (cirq.Ry(np.pi / 2),
        {u'I': np.cos(np.pi / 4), u'Y': -1j * np.sin(np.pi / 4)}),
))
def test_pauli_expansion(val, expected_expansion):
    actual_expansion = cirq.pauli_expansion(val)
    assert set(actual_expansion.keys()) == set(expected_expansion.keys())
    for name in actual_expansion.keys():
        assert np.abs(actual_expansion[name] - expected_expansion[name]) < 1e-12
