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
from cirq import circuits, ops
from cirq.contrib.qcircuit.qcircuit_diagram_info import (
    get_qcircuit_diagram_info)


def qcircuit_qubit_namer(qubit):
    # TODO: If qubit name ends with digits, turn them into subscripts.
    return u'\\lstick{\\text{' + unicode(qubit) + u'}}&'


def _render(diagram):
    w = diagram.width()
    h = diagram.height()

    qwx = set([(x, y + 1)
           for x, y1, y2, _ in diagram.vertical_lines
           for y in xrange(int(y1), int(y2))])

    qw = set([(x, y)
          for y, x1, x2, _ in diagram.horizontal_lines
          for x in xrange(int(x1), int(x2))])

    diagram2 = circuits.TextDiagramDrawer()
    for y in xrange(h):
        for x in xrange(max(0, w - 1)):
            key = (x, y)
            diagram_text = diagram.entries.get(key)
            v = u'&' + (diagram_text.text if diagram_text else  u'') + u' '
            diagram2.write(2*x + 1, y, v)
            post1 = u'\\qw' if key in qw else u''
            post2 = u'\\qwx' if key in qwx else u''
            diagram2.write(2*x + 2, y, post1 + post2)
        diagram2.write(2*w - 1, y, u'&\\qw\\\\')
    grid = diagram2.render(horizontal_spacing=0, vertical_spacing=0)

    output = u'\Qcircuit @R=1em @C=0.75em {\n \\\\\n' + grid + u'\n \\\\\n}'

    return output


def circuit_to_latex_using_qcircuit(
        circuit,
        qubit_order = ops.QubitOrder.DEFAULT):
    u"""Returns a QCircuit-based latex diagram of the given circuit.

    Args:
        circuit: The circuit to represent in latex.
        qubit_order: Determines the order of qubit wires in the diagram.

    Returns:
        Latex code for the diagram.
    """
    diagram = circuit.to_text_diagram_drawer(
        qubit_namer=qcircuit_qubit_namer,
        qubit_order=qubit_order,
        get_circuit_diagram_info=get_qcircuit_diagram_info)
    return _render(diagram)
