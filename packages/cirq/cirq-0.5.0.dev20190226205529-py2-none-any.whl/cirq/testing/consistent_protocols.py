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
from typing import Any, Dict, Optional, Sequence, Type, Union

import sympy

from cirq import ops, protocols
from cirq.testing.circuit_compare import (
        assert_has_consistent_apply_unitary)
from cirq.testing.consistent_decomposition import (
        assert_decompose_is_consistent_with_unitary)
from cirq.testing.consistent_phase_by import (
        assert_phase_by_is_consistent_with_unitary)
from cirq.testing.consistent_qasm import (
        assert_qasm_is_consistent_with_unitary)
from cirq.testing.consistent_pauli_expansion import (
        assert_pauli_expansion_is_consistent_with_unitary)
from cirq.testing.equivalent_repr_eval import assert_equivalent_repr


def assert_implements_consistent_protocols(
        val, **_3to2kwargs
        ):
    if 'local_vals' in _3to2kwargs: local_vals = _3to2kwargs['local_vals']; del _3to2kwargs['local_vals']
    else: local_vals =  None
    if 'global_vals' in _3to2kwargs: global_vals = _3to2kwargs['global_vals']; del _3to2kwargs['global_vals']
    else: global_vals =  None
    if 'setup_code' in _3to2kwargs: setup_code = _3to2kwargs['setup_code']; del _3to2kwargs['setup_code']
    else: setup_code =  u'import cirq\nimport numpy as np\nimport sympy'
    if 'ignoring_global_phase' in _3to2kwargs: ignoring_global_phase = _3to2kwargs['ignoring_global_phase']; del _3to2kwargs['ignoring_global_phase']
    else: ignoring_global_phase = False
    if 'qubit_count' in _3to2kwargs: qubit_count = _3to2kwargs['qubit_count']; del _3to2kwargs['qubit_count']
    else: qubit_count =  None
    if 'exponents' in _3to2kwargs: exponents = _3to2kwargs['exponents']; del _3to2kwargs['exponents']
    else: exponents =  (
            0, 1, -1, 0.5, 0.25, -0.5, 0.1, sympy.Symbol(u's'))
    u"""Checks that a value is internally consistent and has a good __repr__."""
    global_vals = global_vals or {}
    local_vals = local_vals or {}

    _assert_meets_standards_helper(val,
                                   qubit_count,
                                   ignoring_global_phase,
                                   setup_code,
                                   global_vals,
                                   local_vals)

    for exponent in exponents:
        p = protocols.pow(val, exponent, None)
        if p is not None:
            _assert_meets_standards_helper(val**exponent,
                                           qubit_count,
                                           ignoring_global_phase,
                                           setup_code,
                                           global_vals,
                                           local_vals)


def assert_eigengate_implements_consistent_protocols(
        eigen_gate_type, **_3to2kwargs):
    if 'local_vals' in _3to2kwargs: local_vals = _3to2kwargs['local_vals']; del _3to2kwargs['local_vals']
    else: local_vals =  None
    if 'global_vals' in _3to2kwargs: global_vals = _3to2kwargs['global_vals']; del _3to2kwargs['global_vals']
    else: global_vals =  None
    if 'setup_code' in _3to2kwargs: setup_code = _3to2kwargs['setup_code']; del _3to2kwargs['setup_code']
    else: setup_code =  u'import cirq\nimport numpy as np\nimport sympy'
    if 'ignoring_global_phase' in _3to2kwargs: ignoring_global_phase = _3to2kwargs['ignoring_global_phase']; del _3to2kwargs['ignoring_global_phase']
    else: ignoring_global_phase = False
    if 'qubit_count' in _3to2kwargs: qubit_count = _3to2kwargs['qubit_count']; del _3to2kwargs['qubit_count']
    else: qubit_count =  None
    if 'global_shifts' in _3to2kwargs: global_shifts = _3to2kwargs['global_shifts']; del _3to2kwargs['global_shifts']
    else: global_shifts =  (0, -0.5, 0.1)
    if 'exponents' in _3to2kwargs: exponents = _3to2kwargs['exponents']; del _3to2kwargs['exponents']
    else: exponents =  (
            0, 1, -1, 0.25, -0.5, 0.1, sympy.Symbol(u's'))
    u"""Checks that an EigenGate subclass is internally consistent and has a
    good __repr__."""
    for exponent in exponents:
        for shift in global_shifts:
            _assert_meets_standards_helper(
                    eigen_gate_type(exponent=exponent, global_shift=shift),
                    qubit_count,
                    ignoring_global_phase,
                    setup_code,
                    global_vals,
                    local_vals)


def assert_eigen_shifts_is_consistent_with_eigen_components(
        val):
    assert val._eigen_shifts() == [e[0] for e in val._eigen_components()]


def _assert_meets_standards_helper(
        val,
        qubit_count,
        ignoring_global_phase,
        setup_code,
        global_vals,
        local_vals):
    assert_has_consistent_apply_unitary(val, qubit_count=qubit_count)
    assert_qasm_is_consistent_with_unitary(val)
    assert_decompose_is_consistent_with_unitary(val,
        ignoring_global_phase=ignoring_global_phase)
    assert_phase_by_is_consistent_with_unitary(val)
    assert_pauli_expansion_is_consistent_with_unitary(val)
    assert_equivalent_repr(val,
                           setup_code=setup_code,
                           global_vals=global_vals,
                           local_vals=local_vals)
    if isinstance(val, ops.EigenGate):
        assert_eigen_shifts_is_consistent_with_eigen_components(val)
