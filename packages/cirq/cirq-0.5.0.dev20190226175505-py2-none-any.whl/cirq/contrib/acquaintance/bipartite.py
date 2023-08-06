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

from __future__ import absolute_import
import enum
import itertools
from typing import Dict, Sequence, Tuple, Union

from cirq import ops, protocols


from cirq.contrib.acquaintance.gates import acquaint
from cirq.contrib.acquaintance.permutation import (
        PermutationGate, SwapPermutationGate)


class BipartiteGraphType(enum.Enum):
    MATCHING = 1
    COMPLETE = 2

    def __repr__(self):
        return (u'cirq.contrib.acquaintance.bipartite.BipartiteGraphType.' +
                self.name)


BipartiteGraphType = enum.unique(BipartiteGraphType)

class BipartiteSwapNetworkGate(PermutationGate):
    u"""A swap network that acquaints qubits in one half with qubits in the
    other.


    Acts on 2k qubits, acquainting some of the first k qubits with some of the
    latter k. May have the effect permuting the qubits within each half.

    Possible subgraphs include:
        MATCHING: acquaints qubit 1 with qubit (2k - 1), qubit 2 with qubit
            (2k- 2), and so on through qubit k with qubit k + 1.
        COMPLETE: acquaints each of qubits 1 through k with each of qubits k +
            1 through 2k.

    Args:
        part_size: The number of qubits in each half.
        subgraph: The bipartite subgraph of pairs of qubits to acquaint.
        swap_gate: The gate used to swap logical indices.

    Attributes:
        part_size: See above.
        subgraph: See above.
        swap_gate: See above.
    """

    def __init__(self,
                 subgraph,
                 part_size,
                 swap_gate=ops.SWAP
                 ):
        super(BipartiteSwapNetworkGate, self).__init__(2 * part_size, swap_gate)
        self.part_size = part_size
        self.subgraph = (subgraph if isinstance(subgraph, BipartiteGraphType)
                         else BipartiteGraphType[subgraph])
        self.swap_gate = swap_gate


    def decompose_complete(self,
                           qubits
                           ):
        swap_gate = SwapPermutationGate(self.swap_gate)
        if self.part_size == 1:
            yield acquaint(*qubits)
            return
        for k in xrange(-self.part_size + 1, self.part_size - 1):
            for x in xrange(abs(k), 2 * self.part_size - abs(k), 2):
                yield acquaint(*qubits[x: x + 2])
                yield swap_gate(*qubits[x: x + 2])
        yield acquaint(qubits[self.part_size - 1], qubits[self.part_size])
        for k in reversed(xrange(-self.part_size + 1, self.part_size - 1)):
            for x in xrange(abs(k), 2 * self.part_size - abs(k), 2):
                yield acquaint(*qubits[x: x + 2])
                yield swap_gate(*qubits[x: x + 2])


    def decompose_matching(self,
                           qubits
                           ):
        swap_gate = SwapPermutationGate(self.swap_gate)
        for k in xrange(-self.part_size + 1, self.part_size):
            for x in xrange(abs(k), 2 * self.part_size - abs(k), 2):
                if (x + 1) % self.part_size:
                    yield swap_gate(*qubits[x: x + 2])
                else:
                    yield acquaint(*qubits[x: x + 2])


    def _decompose_(self, qubits):
        if len(qubits) != 2 * self.part_size:
            raise ValueError(u'len(qubits) != 2 * self.part_size')
        if self.subgraph == BipartiteGraphType.COMPLETE:
            return self.decompose_complete(qubits)
        elif self.subgraph == BipartiteGraphType.MATCHING:
            return self.decompose_matching(qubits)
        raise NotImplementedError(u'No decomposition implemented for ' +
                                  unicode(self.subgraph))

    def permutation(self):
        if self.num_qubits() != 2 * self.part_size:
            raise ValueError(u'qubit_count != 2 * self.part_size')
        if self.subgraph == BipartiteGraphType.MATCHING:
            return dict(enumerate(
                itertools.chain(*(
                    xrange(self.part_size + offset - 1, offset - 1, -1)
                    for offset in (0, self.part_size)))))
        elif self.subgraph == BipartiteGraphType.COMPLETE:
            return dict(enumerate(xrange(2 * self.part_size)))
        raise NotImplementedError(unicode(self.subgraph) + u'not implemented')

    def _circuit_diagram_info_(self, args
                               ):
        qubit_count = 2 * self.part_size
        if args.known_qubit_count not in (None, qubit_count):
            raise ValueError(u'args.known_qubit_count not in '
                             u'(None, 2 * self.part_size)')
        partial_permutation = self.permutation()
        permutation = dict((i, partial_permutation.get(i, i))
                       for i in xrange(qubit_count))

        if self.subgraph == BipartiteGraphType.MATCHING:
            name = u'Matching'
        elif self.subgraph == BipartiteGraphType.COMPLETE:
            name = u'K_{{{0}, {0}}}'.format(self.part_size)
        # NB: self.subgraph not in BipartiteGraphType caught by self.permutation
        arrow = u'↦' if args.use_unicode_characters else u'->'

        wire_symbols = tuple(
                name + u':' +
                unicode((i // self.part_size, i % self.part_size)) + arrow +
                unicode((j // self.part_size, j % self.part_size))
                for i, j in permutation.items())
        return wire_symbols


    def __repr__(self):
        return (u'cirq.contrib.acquaintance.bipartite.BipartiteSwapNetworkGate'
                u'({}, {})'.format(repr(self.subgraph), self.part_size))

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
                self.subgraph == other.subgraph and
                self.part_size == other.part_size)
