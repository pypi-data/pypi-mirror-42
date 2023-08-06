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

from __future__ import with_statement
from __future__ import absolute_import
import itertools
import random

import pytest

import cirq
import cirq.contrib.acquaintance as cca


def test_bad_qubit_pairs():
    a, b, c, d, e = cirq.LineQubit.range(5)
    bad_qubit_pairs = [(a, b), (c, d), (e,)]
    with pytest.raises(ValueError):
        cca.strategies.quartic_paired.qubit_pairs_to_qubit_order(
                bad_qubit_pairs)


def random_index_pairs(n_pairs):
    indices = range(2 * n_pairs)
    random.shuffle(indices)
    return tuple(indices[2 * i: 2 * (i + 1)] for i in xrange(n_pairs))


@pytest.mark.parametrize(u'index_pairs',
    [random_index_pairs(n_pairs)
     for n_pairs in xrange(2, 7)
     for _ in xrange(2)])
def test_quartic_paired_acquaintances(index_pairs):
    n_pairs = len(index_pairs)
    qubit_pairs = tuple(tuple(cirq.LineQubit(x) for x in index_pair)
                        for index_pair in index_pairs)
    strategy, qubits = cca.quartic_paired_acquaintance_strategy(qubit_pairs)
    initial_mapping = dict((q, q.x) for q in qubits)
    opps = cca.get_logical_acquaintance_opportunities(
            strategy, initial_mapping)
    assert set(len(opp) for opp in opps) == set([2, 4])
    quadratic_opps = set(opp for opp in opps if len(opp) == 2)
    expected_quadratic_opps = set(
            frozenset(index_pair) for index_pair in
                itertools.combinations(xrange(2 * n_pairs), 2))
    assert quadratic_opps == expected_quadratic_opps
    quartic_opps = set(opp for opp in opps if len(opp) == 4)
    expected_quartic_opps = set(
            frozenset(I + J) for I, J in
                itertools.combinations(index_pairs, 2))
    assert quartic_opps == expected_quartic_opps
