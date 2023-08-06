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
import collections
from typing import TYPE_CHECKING, Callable, Union, Any, Tuple, Iterable, \
    TypeVar, List, Optional, overload

from typing_extensions import Protocol


from cirq.type_workarounds import NotImplementedType

if TYPE_CHECKING:
    # pylint: disable=unused-import
    import cirq


TValue = TypeVar(u'TValue')

TDefault = TypeVar(u'TDefault')

TError = TypeVar(u'TError', bound=Exception)

RaiseTypeErrorIfNotProvided = ([],)  # type: Any


def _value_error_describing_bad_operation(op):
    return ValueError(
        u"Operation doesn't satisfy the given `keep` "
        u"but can't be decomposed: {!r}".format(op))


class SupportsDecompose(Protocol):
    u"""An object that can be decomposed into simpler operations.

    All decomposition methods should ultimately terminate on basic 1-qubit and
    2-qubit gates included by default in Cirq. Cirq does not make any guarantees
    about what the final gate set is. Currently, decompositions within Cirq
    happen to converge towards the X, Y, Z, CZ, PhasedX, specified-matrix gates,
    and others. This set will vary from release to release. Because of this
    variability, it is important for consumers of decomposition to look for
    generic properties of gates, such as "two qubit gate with a unitary matrix",
    instead of specific gate types such as CZ gates (though a consumer is
    of course free to handle CZ gates in a special way, and consumers can
    give an `intercepting_decomposer` to `cirq.decompose` that attempts to
    target a specific gate set).

    For example, `cirq.TOFFOLI` has a `_decompose_` method that returns a pair
    of Hadamard gates surrounding a `cirq.CCZ`. Although `cirq.CCZ` is not a
    1-qubit or 2-qubit operation, it specifies its own `_decompose_` method
    that only returns 1-qubit or 2-qubit operations. This means that iteratively
    decomposing `cirq.TOFFOLI` terminates in 1-qubit and 2-qubit operations, and
    so almost all decomposition-aware code will be able to handle `cirq.TOFFOLI`
    instances.

    Callers are responsible for iteratively decomposing until they are given
    operations that they understand. The `cirq.decompose` method is a simple way
    to do this, because it has logic to recursively decompose until a given
    `keep` predicate is satisfied.

    Code implementing `_decompose_` MUST NOT create cycles, such as a gate A
    decomposes into a gate B which decomposes back into gate A. This will result
    in infinite loops when calling `cirq.decompose`.

    It is permitted (though not recommended) for the chain of decompositions
    resulting from an operation to hit a dead end before reaching 1-qubit or
    2-qubit operations. When this happens, `cirq.decompose` will raise
    a `TypeError` by default, but can be configured to ignore the issue or
    raise a caller-provided error.
    """

    def _decompose_(self):
        pass


class SupportsDecomposeWithQubits(Protocol):
    u"""An object that can be decomposed into operations on given qubits.

    Returning `NotImplemented` or `None` means "not decomposable". Otherwise an
    operation, list of operations, or generally anything meeting the `OP_TREE`
    contract can be returned.

    For example, a SWAP gate can be turned into three CNOTs. But in order to
    describe those CNOTs one must be able to talk about "the target qubit" and
    "the control qubit". This can only be done once the qubits-to-be-swapped are
    known.

    The main user of this protocol is `GateOperation`, which decomposes itself
    by delegating to its gate. The qubits argument is needed because gates are
    specified independently of target qubits and so must be told the relevant
    qubits. A `GateOperation` implements `SupportsDecompose` as long as its gate
    implements `SupportsDecomposeWithQubits`.
    """

    def _decompose_(self, qubits
                    ):
        pass


def _default_decomposer(op
                        ):
    return decompose_once(op, default=NotImplemented)


# pylint: disable=function-redefined
@overload
def decompose(
    val, **_3to2kwargs
):
    if 'keep' in _3to2kwargs: keep = _3to2kwargs['keep']; del _3to2kwargs['keep']
    else: keep =  None
    if 'fallback_decomposer' in _3to2kwargs: fallback_decomposer = _3to2kwargs['fallback_decomposer']; del _3to2kwargs['fallback_decomposer']
    else: fallback_decomposer =  None
    if 'intercepting_decomposer' in _3to2kwargs: intercepting_decomposer = _3to2kwargs['intercepting_decomposer']; del _3to2kwargs['intercepting_decomposer']
    else: intercepting_decomposer =  None
    pass


@overload
def decompose(
    val, **_3to2kwargs
):
    on_stuck_raise = _3to2kwargs['on_stuck_raise']; del _3to2kwargs['on_stuck_raise']
    if 'keep' in _3to2kwargs: keep = _3to2kwargs['keep']; del _3to2kwargs['keep']
    else: keep =  None
    if 'fallback_decomposer' in _3to2kwargs: fallback_decomposer = _3to2kwargs['fallback_decomposer']; del _3to2kwargs['fallback_decomposer']
    else: fallback_decomposer =  None
    if 'intercepting_decomposer' in _3to2kwargs: intercepting_decomposer = _3to2kwargs['intercepting_decomposer']; del _3to2kwargs['intercepting_decomposer']
    else: intercepting_decomposer =  None
    pass


def decompose(
    val, **_3to2kwargs
):
    if 'on_stuck_raise' in _3to2kwargs: on_stuck_raise = _3to2kwargs['on_stuck_raise']; del _3to2kwargs['on_stuck_raise']
    else: on_stuck_raise =  _value_error_describing_bad_operation
    if 'keep' in _3to2kwargs: keep = _3to2kwargs['keep']; del _3to2kwargs['keep']
    else: keep =  None
    if 'fallback_decomposer' in _3to2kwargs: fallback_decomposer = _3to2kwargs['fallback_decomposer']; del _3to2kwargs['fallback_decomposer']
    else: fallback_decomposer =  None
    if 'intercepting_decomposer' in _3to2kwargs: intercepting_decomposer = _3to2kwargs['intercepting_decomposer']; del _3to2kwargs['intercepting_decomposer']
    else: intercepting_decomposer =  None
    u"""Recursively decomposes a value into `cirq.Operation`s meeting a criteria.

    Args:
        val: The value to decompose into operations.
        intercepting_decomposer: An optional method that is called before the
            default decomposer (the value's `_decompose_` method). If
            `intercepting_decomposer` is specified and returns a result that
            isn't `NotImplemented` or `None`, that result is used. Otherwise the
            decomposition falls back to the default decomposer.

            Note that `val` will be passed into `intercepting_decomposer`, even
            if `val` isn't a `cirq.Operation`.
        fallback_decomposer: An optional decomposition that used after the
            `intercepting_decomposer` and the default decomposer (the value's
            `_decompose_` method) both fail.
        keep: A predicate that determines if the initial operation or
            intermediate decomposed operations should be kept or else need to be
            decomposed further. If `keep` isn't specified, it defaults to "value
            can't be decomposed anymore".
        on_stuck_raise: If there is an operation that can't be decomposed and
            also can't be kept, `on_stuck_raise` is used to determine what error
            to raise. `on_stuck_raise` can either directly be an `Exception`, or
            a method that takes the problematic operation and returns an
            `Exception`. If `on_stuck_raise` is set to `None` or a method that
            returns `None`, undecomposable operations are simply silently kept.
            `on_stuck_raise` defaults to a `ValueError` describing the unwanted
            undecomposable operation.

    Returns:
        A list of operations that the given value was decomposed into. If
        `on_stuck_raise` isn't set to None, all operations in the list will
        satisfy the predicate specified by `keep`.

    Raises:
        TypeError:
            `val` isn't a `cirq.Operation` and can't be decomposed even once.
            (So it's not possible to return a list of operations.)

        ValueError:
            Default type of error raised if there's an undecomposable operation
            that doesn't satisfy the given `keep` predicate.

        TError:
            Custom type of error raised if there's an undecomposable operation
            that doesn't satisfy the given `keep` predicate.
    """
    from cirq import ops  # HACK: Avoids circular dependencies.

    if (on_stuck_raise is not _value_error_describing_bad_operation and
            keep is None):
        raise ValueError(
            u"Must specify 'keep' if specifying 'on_stuck_raise', because it's "
            u"not possible to get stuck if you don't have a criteria on what's "
            u"acceptable to keep.")

    decomposers = [d
                   for d in [intercepting_decomposer,
                             _default_decomposer,
                             fallback_decomposer]
                   if d]

    def decomposer(op):
        for d in decomposers:
            r = d(op)
            if r is not NotImplemented and r is not None:
                return r
        return NotImplemented

    output = []
    queue = [val]  # type: List[Any]
    while queue:
        item = queue.pop(0)

        if isinstance(item, ops.Operation) and keep is not None and keep(item):
            output.append(item)
            continue

        decomposed = decomposer(item)
        if decomposed is not NotImplemented and decomposed is not None:
            queue[:0] = ops.flatten_op_tree(decomposed)
            continue

        if isinstance(item, collections.Iterable):
            queue[:0] = ops.flatten_op_tree(item)
            continue

        if keep is not None and on_stuck_raise is not None:
            if isinstance(on_stuck_raise, Exception):
                raise on_stuck_raise
            elif callable(on_stuck_raise):
                error = on_stuck_raise(item)
                if error is not None:
                    raise error

        output.append(item)

    return output


@overload
def decompose_once(val, **kwargs):
    pass


@overload
def decompose_once(val,
                   default,
                   **kwargs
                   ):
    pass


def decompose_once(val,
                   default=RaiseTypeErrorIfNotProvided,
                   **kwargs):
    u"""Decomposes a value into operations, if possible.

    This method decomposes the value exactly once, instead of decomposing it
    and then continuing to decomposing the decomposed operations recursively
    until some criteria is met (which is what `cirq.decompose` does).

    Args:
        val: The value to call `_decompose_` on, if possible.
        default: A default result to use if the value doesn't have a
            `_decompose_` method or that method returns `NotImplemented` or
            `None`. If not specified, undecomposable values cause a `TypeError`.
        kwargs: Arguments to forward into the `_decompose_` method of `val`.
            For example, this is used to tell gates what qubits they are being
            applied to.

    Returns:
        The result of `val._decompose_(**kwargs)`, if `val` has a `_decompose_`
        method and it didn't return `NotImplemented` or `None`. Otherwise
        `default` is returned, if it was specified. Otherwise an error is
        raised.

    TypeError:
        `val` didn't have a `_decompose_` method (or that method returned
        `NotImplemented` or `None`) and `default` wasn't set.
    """
    method = getattr(val, u'_decompose_', None)
    decomposed = NotImplemented if method is None else method(**kwargs)

    if decomposed is not NotImplemented and decomposed is not None:
        from cirq import ops  # HACK: Avoids circular dependencies.
        return list(ops.flatten_op_tree(decomposed))

    if default is not RaiseTypeErrorIfNotProvided:
        return default
    if method is None:
        raise TypeError(u"object of type '{}' "
                        u"has no _decompose_ method.".format(type(val)))
    raise TypeError(u"object of type '{}' does have a _decompose_ method, "
                    u"but it returned NotImplemented or None.".format(type(val)))


@overload
def decompose_once_with_qubits(val,
                               qubits
                               ):
    pass


@overload
def decompose_once_with_qubits(val,
                               qubits,
                               # NOTE: should be TDefault instead of Any, but
                               # mypy has false positive errors when setting
                               # default to None.
                               default,
                               ):
    pass


def decompose_once_with_qubits(val,
                               qubits,
                               default=RaiseTypeErrorIfNotProvided):
    u"""Decomposes a value into operations on the given qubits.

    This method is used when decomposing gates, which don't know which qubits
    they are being applied to unless told. It decomposes the gate exactly once,
    instead of decomposing it and then continuing to decomposing the decomposed
    operations recursively until some criteria is met.

    Args:
        val: The value to call `._decompose_(qubits=qubits)` on, if possible.
        qubits: The value to pass into the named `qubits` parameter of
            `val._decompose_`.
        default: A default result to use if the value doesn't have a
            `_decompose_` method or that method returns `NotImplemented` or
            `None`. If not specified, undecomposable values cause a `TypeError`.

    Returns:
        The result of `val._decompose_(qubits=qubits)`, if `val` has a
        `_decompose_` method and it didn't return `NotImplemented` or `None`.
        Otherwise `default` is returned, if it was specified. Otherwise an error
        is raised.

    TypeError:
        `val` didn't have a `_decompose_` method (or that method returned
        `NotImplemented` or `None`) and `default` wasn't set.
    """
    return decompose_once(val, default, qubits=tuple(qubits))
# pylint: enable=function-redefined
