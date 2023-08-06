# coding=utf-8
# Copyright 2019 The Cirq Developers
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
from typing import Union, Any, Optional

import numpy as np

from cirq import protocols, linalg, value
from cirq.ops import raw_types
from cirq.type_workarounds import NotImplementedType


class ControlledOperation(raw_types.Operation):
    def __init__(self,
                 control,
                 sub_operation):
        self.control = control
        self.sub_operation = sub_operation

    @property
    def qubits(self):
        return (self.control,) + self.sub_operation.qubits

    def with_qubits(self, *new_qubits):
        return ControlledOperation(
            new_qubits[0],
            self.sub_operation.with_qubits(*new_qubits[1:]))

    def _decompose_(self):
        result = protocols.decompose_once(self.sub_operation, NotImplemented)
        if result is NotImplemented:
            return NotImplemented

        return [ControlledOperation(self.control, op) for op in result]

    def _value_equality_values_(self):
        return tuple([self.control, self.sub_operation])

    def _apply_unitary_(self, args):
        control = args.axes[0]
        rest = args.axes[1:]
        active = linalg.slice_for_qubits_equal_to([control], 1)
        sub_axes = [r - int(r > control) for r in rest]
        target_view = args.target_tensor[active]
        buffer_view = args.available_buffer[active]
        result = protocols.apply_unitary(
            self.sub_operation,
            protocols.ApplyUnitaryArgs(
                target_view,
                buffer_view,
                sub_axes),
            default=NotImplemented)

        if result is NotImplemented:
            return NotImplemented

        if result is target_view:
            return args.target_tensor

        if result is buffer_view:
            inactive = linalg.slice_for_qubits_equal_to([control], 0)
            args.available_buffer[inactive] = args.target_tensor[inactive]
            return args.available_buffer

        # HACK: assume they didn't somehow escape the slice view and edit the
        # rest of target_tensor.
        args.target_tensor[active] = result
        return args.target_tensor

    def _has_unitary_(self):
        return protocols.has_unitary(self.sub_operation)

    def _unitary_(self):
        sub_matrix = protocols.unitary(self.sub_operation, None)
        if sub_matrix is None:
            return NotImplemented
        return linalg.block_diag(np.eye(sub_matrix.shape[0]), sub_matrix)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u'C({}){}'.format(self.control, unicode(self.sub_operation))

    def __repr__(self):
        return u'cirq.ControlledOperation(control={!r},' \
               u' sub_operation={!r})'.format(self.control, self.sub_operation)

    def _is_parameterized_(self):
        return protocols.is_parameterized(self.sub_operation)

    def _resolve_parameters_(self, resolver):
        new_sub_op = protocols.resolve_parameters(self.sub_operation, resolver)
        return ControlledOperation(self.control, new_sub_op)

    def _trace_distance_bound_(self):
        return protocols.trace_distance_bound(self.sub_operation)

    def __pow__(self, exponent):
        new_sub_op = protocols.pow(self.sub_operation,
                                   exponent,
                                   NotImplemented)
        if new_sub_op is NotImplemented:
            return NotImplemented
        return ControlledOperation(self.control, new_sub_op)

    def _circuit_diagram_info_(self,
                               args
                               ):

        sub_args = protocols.CircuitDiagramInfoArgs(
            known_qubit_count=(args.known_qubit_count - 1
                               if args.known_qubit_count is not None else None),
            known_qubits=(args.known_qubits[1:]
                          if args.known_qubits is not None else None),
            use_unicode_characters=args.use_unicode_characters,
            precision=args.precision,
            qubit_map=args.qubit_map
        )
        sub_info = protocols.circuit_diagram_info(self.sub_operation,
                                                  sub_args,
                                                  None)
        if sub_info is None:
            return NotImplemented

        return protocols.CircuitDiagramInfo(
            wire_symbols=(u'@',) + sub_info.wire_symbols,
            exponent=sub_info.exponent)

ControlledOperation = value.value_equality(ControlledOperation)
