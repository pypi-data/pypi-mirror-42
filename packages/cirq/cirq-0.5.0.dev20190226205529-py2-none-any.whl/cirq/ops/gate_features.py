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

u"""Marker classes for indicating which additional features gates support.

For example: some gates are reversible, some have known matrices, etc.
"""

from __future__ import absolute_import
from typing import Iterable

import abc

from cirq.ops import op_tree, raw_types


class InterchangeableQubitsGate(object):
    __metaclass__ = abc.ABCMeta
    u"""Indicates operations should be equal under some qubit permutations."""

    def qubit_index_to_equivalence_group_key(self, index):
        u"""Returns a key that differs between non-interchangeable qubits."""
        return 0


class SingleQubitGate(raw_types.Gate):
    __metaclass__ = abc.ABCMeta
    u"""A gate that must be applied to exactly one qubit."""
    def num_qubits(self):
        return 1

    def validate_args(self, qubits):
        if len(qubits) != 1:
            raise ValueError(
                u'Single-qubit gate applied to {} qubits, instead of 1: {}({})'.
                format(len(qubits), self, qubits))

    def on_each(self, *targets):
        u"""Returns a list of operations apply this gate to each of the targets.

        Args:
            *targets: The qubits to apply this gate to.

        Returns:
            Operations applying this gate to the target qubits.

        Raises:
            ValueError if targets are not instances of QubitId.
        """
        if any([not isinstance(target, raw_types.QubitId)
                for target in targets]):
            raise ValueError(
                    u'on_each() was called with type different than QubitId.')
        return [self.on(target) for target in targets]


class TwoQubitGate(raw_types.Gate):
    __metaclass__ = abc.ABCMeta
    u"""A gate that must be applied to exactly two qubits."""
    def num_qubits(self):
        return 2

    def validate_args(self, qubits):
        if len(qubits) != 2:
            raise ValueError(
                u'Two-qubit gate not applied to two qubits: {}({})'.
                format(self, qubits))


class ThreeQubitGate(raw_types.Gate):
    __metaclass__ = abc.ABCMeta
    u"""A gate that must be applied to exactly three qubits."""
    def num_qubits(self):
        return 3

    def validate_args(self, qubits):
        if len(qubits) != 3:
            raise ValueError(
                u'Three-qubit gate not applied to three qubits: {}({})'.
                format(self, qubits))


class MultiQubitGate(raw_types.Gate):
    __metaclass__ = abc.ABCMeta
    u"""A gate that must be applied to multiple qubits.

    This class can be used to get rid of a bit of boiler plate. Typically one
    would implement a multiqubit gate like

        class MyGate:

            def __init__(self, num_qubits, **args):
                self._num_qubits
                # other arg work

            def num_qubits(self):
                return self._num_qubits

            def validate_args(self, qubits):
                if self.num_qubits != len(qubits):
                    raise ValueError('Acting on wrong number of qubits')

    This class allows you to instead use

        class MyGate(MultiQubitGate):

            def __init__(self, num_qubits, **args):
                super().__init__(num_qubits)
                # other arg work

    Validation of number of qubits is handled in this class. If more validation
    is necessary, remember to call the super method:

            def validate_args(self, qubits):
                super().validate_args(qubits)
                # your validation here
    """

    def __init__(self, num_qubits):
        self._num_qubits = num_qubits

    def num_qubits(self):
        return self._num_qubits

    def validate_args(self, qubits):
        if len(qubits) != self.num_qubits():
            raise ValueError(
                u'{}-qubit gate was applied to {} qubits'.
                    format(self.num_qubits(), len(qubits)))
