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
import numpy as np

import cirq


# Python 2 gives a different repr due to unicode strings being prefixed with u.
@cirq.testing.only_test_in_python3
def test_wave_function_trial_result_repr():
    final_simulator_state = cirq.WaveFunctionSimulatorState(
        qubit_map={cirq.NamedQubit(u'a'): 0}, state_vector=np.array([0, 1]))
    trial_result = cirq.WaveFunctionTrialResult(
        params=cirq.ParamResolver({u's': 1}),
        measurements={u'm': np.array([[1]])},
        final_simulator_state=final_simulator_state)
    assert repr(trial_result) == (
               u"cirq.WaveFunctionTrialResult("
               u"params=cirq.ParamResolver({'s': 1}), "
               u"measurements={'m': array([[1]])}, "
               u"final_simulator_state=cirq.WaveFunctionSimulatorState("
                   u"state_vector=array([0, 1]), "
                   u"qubit_map={cirq.NamedQubit('a'): 0}))")


def test_wave_function_trial_result_equality():
    eq = cirq.testing.EqualsTester()
    eq.add_equality_group(
        cirq.WaveFunctionTrialResult(
            params=cirq.ParamResolver({}),
            measurements={},
            final_simulator_state=cirq.WaveFunctionSimulatorState(np.array([]),
                                                                  {})),
        cirq.WaveFunctionTrialResult(
            params=cirq.ParamResolver({}),
            measurements={},
            final_simulator_state=cirq.WaveFunctionSimulatorState(np.array([]),
                                                                  {})))
    eq.add_equality_group(
        cirq.WaveFunctionTrialResult(
            params=cirq.ParamResolver({u's': 1}),
            measurements={},
            final_simulator_state=cirq.WaveFunctionSimulatorState(np.array([]),
                                                                  {})))
    eq.add_equality_group(
        cirq.WaveFunctionTrialResult(
            params=cirq.ParamResolver({u's': 1}),
            measurements={u'm': np.array([[1]])},
            final_simulator_state=cirq.WaveFunctionSimulatorState(np.array([]),
                                                                  {})))
    eq.add_equality_group(
        cirq.WaveFunctionTrialResult(
            params=cirq.ParamResolver({u's': 1}),
            measurements={u'm': np.array([[1]])},
            final_simulator_state=cirq.WaveFunctionSimulatorState(np.array([1]),
                                                                  {})))


def test_wave_function_trial_result_state_mixin():
    qubits = cirq.LineQubit.range(2)
    qubit_map = dict((qubits[i], i) for i in xrange(2))
    result = cirq.WaveFunctionTrialResult(
        params=cirq.ParamResolver({u'a': 2}),
        measurements={u'm': np.array([1, 2])},
        final_simulator_state=cirq.WaveFunctionSimulatorState(
            qubit_map=qubit_map, state_vector=np.array([0, 1, 0, 0])))
    rho = np.array([[0, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]])
    np.testing.assert_array_almost_equal(rho,
                                         result.density_matrix_of(qubits))
    bloch = np.array([0,0,-1])
    np.testing.assert_array_almost_equal(bloch,
                                         result.bloch_vector_of(qubits[1]))
    assert result.dirac_notation() == u'|01⟩'
