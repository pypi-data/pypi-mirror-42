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
from typing import cast, Optional, Tuple

from cirq import ops, protocols


def escape_text_for_latex(text):
    escaped = (text
               .replace(u'\\', u'\\textbackslash{}')
               .replace(u'^', u'\\textasciicircum{}')
               .replace(u'~', u'\\textasciitilde{}')
               .replace(u'_', u'\\_')
               .replace(u'{', u'\\{')
               .replace(u'}', u'\\}')
               .replace(u'$', u'\\$')
               .replace(u'%', u'\\%')
               .replace(u'&', u'\\&')
               .replace(u'#', u'\\#'))
    return u'\\text{' + escaped + u'}'


def get_multigate_parameters(
        args
        ):
    if (args.qubit_map is None) or (args.known_qubits is None):
        return None

    indices = [args.qubit_map[q] for q in args.known_qubits]
    min_index = min(indices)
    n_qubits = len(args.known_qubits)
    if sorted(indices) != range(min_index, min_index + n_qubits):
        return None
    return min_index, n_qubits


def hardcoded_qcircuit_diagram_info(
        op):
    if not isinstance(op, ops.GateOperation):
        return None
    symbols = (
        (ur'\targ',) if op.gate == ops.X else
        (ur'\control', ur'\control') if op.gate == ops.CZ else
        (ur'\control', ur'\targ') if op.gate == ops.CNOT else
        (ur'\meter',) if ops.MeasurementGate.is_measurement(op.gate) else
        ())
    return (protocols.CircuitDiagramInfo(cast(Tuple[unicode, ...], symbols))
            if symbols else None)


def convert_text_diagram_info_to_qcircuit_diagram_info(
        info):
    labels = [escape_text_for_latex(e) for e in info.wire_symbols]
    if info.exponent != 1:
        labels[0] += u'^{' + unicode(info.exponent) + u'}'
    symbols = tuple(u'\\gate{' + l + u'}' for l in labels)
    return protocols.CircuitDiagramInfo(symbols)


def multigate_qcircuit_diagram_info(
        op,
        args,
        ):
    if not (isinstance(op, ops.GateOperation) and
            isinstance(op.gate, ops.InterchangeableQubitsGate)):
        return None

    multigate_parameters = get_multigate_parameters(args)
    if multigate_parameters is None:
        return None

    info = protocols.circuit_diagram_info(op, args, default=None)

    min_index, n_qubits = multigate_parameters
    name = escape_text_for_latex(
            unicode(op.gate).rsplit(u'**', 1)[0]
            if isinstance(op, ops.GateOperation) else
            unicode(op))
    if (info is not None) and (info.exponent != 1):
        name += u'^{' + unicode(info.exponent) + u'}'
    box = u'\multigate{' + unicode(n_qubits - 1) + u'}{' + name + u'}'
    ghost = u'\ghost{' + name + u'}'
    assert args.qubit_map is not None
    assert args.known_qubits is not None
    symbols = tuple(box if (args.qubit_map[q] == min_index) else
                    ghost for q in args.known_qubits)
    return protocols.CircuitDiagramInfo(symbols,
                                        exponent=info.exponent,
                                        connected=False)


def fallback_qcircuit_diagram_info(
        op,
        args
        ):
    args = args.with_args(use_unicode_characters=False)
    info = protocols.circuit_diagram_info(op, args, default=None)
    if info is None:
        name = unicode(op.gate if isinstance(op, ops.GateOperation) else op)
        n_qubits = len(op.qubits)
        symbols = tuple(u'#{}'.format(i + 1) if i else name
                for i in xrange( n_qubits))
        info = protocols.CircuitDiagramInfo(symbols)
    return convert_text_diagram_info_to_qcircuit_diagram_info(info)


def get_qcircuit_diagram_info(op,
                              args
                              ):
    info = hardcoded_qcircuit_diagram_info(op)
    if info is None:
        info = multigate_qcircuit_diagram_info(op, args)
    if info is None:
        info = fallback_qcircuit_diagram_info(op, args)
    return info
