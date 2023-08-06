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
from __future__ import division
from __future__ import absolute_import
from typing import Union, Tuple, cast

import numpy as np
import pytest
import sympy

import cirq
from cirq import protocols
from cirq.type_workarounds import NotImplementedType


class GateUsingWorkspaceForApplyUnitary(cirq.SingleQubitGate):
    def _apply_unitary_(self, args
                        ):
        args.available_buffer[...] = args.target_tensor
        args.target_tensor[...] = 0
        return args.available_buffer

    def _unitary_(self):
        return np.eye(2)


    def __eq__(self, other):
        return isinstance(other, type(self))

    def __repr__(self):
        return (u'cirq.ops.controlled_operation_test.'
                u'GateUsingWorkspaceForApplyUnitary()')


class GateAllocatingNewSpaceForResult(cirq.SingleQubitGate):
    def _apply_unitary_(self, args
                        ):
        assert len(args.axes) == 1
        a = args.axes[0]
        seed = cast(Tuple[Union[int, slice, u'ellipsis'], ...],
                    (slice(None),))
        zero = seed*a + (0, Ellipsis)
        one = seed*a + (1, Ellipsis)
        result = np.zeros(args.target_tensor.shape, args.target_tensor.dtype)
        result[zero] = args.target_tensor[zero]*2 + args.target_tensor[one]*3
        result[one] = args.target_tensor[zero]*5 + args.target_tensor[one]*7
        return result

    def _unitary_(self):
        return np.array([[2, 3], [5, 7]])

    def __eq__(self, other):
        return isinstance(other, type(self))

    def __repr__(self):
        return (u'cirq.ops.controlled_operation_test.'
                u'GateAllocatingNewSpaceForResult()')


def test_controlled_operation_init():
    cb = cirq.NamedQubit(u'ctr')
    q = cirq.NamedQubit(u'q')
    g = cirq.SingleQubitGate()
    v = cirq.GateOperation(g, (q,))
    c = cirq.ControlledOperation(cb, v)
    assert c.sub_operation == v
    assert c.control == cb
    assert c.qubits == (cb, q)
    assert c == c.with_qubits(cb, q)


def test_controlled_operation_eq():
    c1 = cirq.NamedQubit(u'c1')
    q1 = cirq.NamedQubit(u'q1')
    c2 = cirq.NamedQubit(u'c2')

    eq = cirq.testing.EqualsTester()

    eq.make_equality_group(lambda: cirq.ControlledOperation(c1, cirq.X(q1)))
    eq.make_equality_group(lambda: cirq.ControlledOperation(c2, cirq.X(q1)))
    eq.make_equality_group(lambda: cirq.ControlledOperation(c1, cirq.Z(q1)))
    eq.make_equality_group(lambda: cirq.ControlledOperation(c2, cirq.Z(q1)))


def test_str():
    c1 = cirq.NamedQubit(u'c1')
    c2 = cirq.NamedQubit(u'c2')
    q2 = cirq.NamedQubit(u'q2')

    assert (unicode(cirq.ControlledOperation(c1, cirq.CZ(c2, q2))) ==
            u"C(c1)CZ(c2, q2)")


def test_repr():
    qubits = cirq.LineQubit.range(3)

    ccz = cirq.ControlledOperation(qubits[0], cirq.CZ(*qubits[1:]))
    assert (repr(ccz) ==
            u"cirq.ControlledOperation(control=cirq.LineQubit(0), "
            u"sub_operation=cirq.CZ.on(cirq.LineQubit(1), cirq.LineQubit(2)))")
    cirq.testing.assert_equivalent_repr(ccz)


# A contrived multiqubit Hadamard gate that asserts the consistency of
# the passed in Args and puts an H on all qubits
# displays them as 'H(qubit)' on the wire
class MultiH(cirq.MultiQubitGate):

    def _circuit_diagram_info_(self,
                               args
                               ):
        assert args.known_qubit_count is not None
        assert args.known_qubits is not None

        return protocols.CircuitDiagramInfo(
            wire_symbols=tuple(u'H({})'.format(q) for q in args.known_qubits),
            connected=True
        )


def test_circuit_diagram():
    qubits = cirq.LineQubit.range(3)
    c = cirq.Circuit()
    c.append(cirq.ControlledOperation(qubits[0], MultiH(2)(*qubits[1:])))

    cirq.testing.assert_has_diagram(c, u"""
0: ───@──────
      │
1: ───H(1)───
      │
2: ───H(2)───
""")


class MockGate(cirq.TwoQubitGate):

    def _circuit_diagram_info_(self,
                               args
                               ):
        self.captured_diagram_args = args
        return cirq.CircuitDiagramInfo(wire_symbols=tuple([u'MOCK']), exponent=1,
                                       connected=True)


def test_uninformed_circuit_diagram_info():
    qbits = cirq.LineQubit.range(3)
    mock_gate = MockGate()
    c_op = cirq.ControlledOperation(qbits[0],
                                    mock_gate(*qbits[1:]))

    args = protocols.CircuitDiagramInfoArgs.UNINFORMED_DEFAULT

    assert (cirq.circuit_diagram_info(c_op, args) ==
            cirq.CircuitDiagramInfo(wire_symbols=(u'@', u'MOCK'), exponent=1,
                                    connected=True))
    assert mock_gate.captured_diagram_args == args


def test_non_diagrammable_subop():
    qbits = cirq.LineQubit.range(2)

    class UndiagrammableGate(cirq.SingleQubitGate):
        pass

    undiagrammable_op = UndiagrammableGate()(qbits[1])

    c_op = cirq.ControlledOperation(qbits[0], undiagrammable_op)
    assert cirq.circuit_diagram_info(c_op,
                                     default=None) is None


@pytest.mark.parametrize(u'gate', [
    cirq.X(cirq.NamedQubit(u'q1')),
    cirq.X(cirq.NamedQubit(u'q1')) ** 0.5,
    cirq.Rx(np.pi)(cirq.NamedQubit(u'q1')),
    cirq.Rx(np.pi / 2)(cirq.NamedQubit(u'q1')),
    cirq.Z(cirq.NamedQubit(u'q1')),
    cirq.H(cirq.NamedQubit(u'q1')),
    cirq.CNOT(cirq.NamedQubit(u'q1'), cirq.NamedQubit(u'q2')),
    cirq.SWAP(cirq.NamedQubit(u'q1'), cirq.NamedQubit(u'q2')),
    cirq.CCZ(cirq.NamedQubit(u'q1'), cirq.NamedQubit(u'q2'),
             cirq.NamedQubit(u'q3')),
    cirq.ControlledGate(cirq.ControlledGate(cirq.CCZ))(
        *cirq.LineQubit.range(5)),
    GateUsingWorkspaceForApplyUnitary()(cirq.NamedQubit(u'q1')),
    GateAllocatingNewSpaceForResult()(cirq.NamedQubit(u'q1')),
])
def test_controlled_operation_is_consistent(gate):
    cb = cirq.NamedQubit(u'ctr')
    cgate = cirq.ControlledOperation(cb, gate)
    cirq.testing.assert_implements_consistent_protocols(cgate)


def test_parameterizable():
    a = sympy.Symbol(u'a')
    qubits = cirq.LineQubit.range(3)

    cz = cirq.ControlledOperation(qubits[0], cirq.Z(qubits[1]))
    cza = cirq.ControlledOperation(qubits[0],
                                   cirq.ZPowGate(exponent=a)(qubits[1]))
    assert cirq.is_parameterized(cza)
    assert not cirq.is_parameterized(cz)
    assert cirq.resolve_parameters(cza, cirq.ParamResolver({u'a': 1})) == cz


def test_bounded_effect():
    qubits = cirq.LineQubit.range(2)
    cy = cirq.ControlledOperation(qubits[0], cirq.Y(qubits[1]))
    assert cirq.trace_distance_bound(cy ** 0.001) < 0.01
