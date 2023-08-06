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

u"""Exposes structured data about unicode/ascii box drawing characters."""

from __future__ import absolute_import
from typing import List, NamedTuple, Optional


_BoxDrawCharacterSet = NamedTuple(
    u'_BoxDrawCharacterSet',
    [
        (u'top', unicode),
        (u'bottom', unicode),
        (u'left', unicode),
        (u'right', unicode),

        (u'top_bottom', unicode),
        (u'top_left', unicode),
        (u'top_right', unicode),
        (u'bottom_left', unicode),
        (u'bottom_right', unicode),
        (u'left_right', unicode),

        (u'top_bottom_left', unicode),
        (u'top_bottom_right', unicode),
        (u'top_left_right', unicode),
        (u'bottom_left_right', unicode),

        (u'top_bottom_left_right', unicode),
    ]
)


class BoxDrawCharacterSet(_BoxDrawCharacterSet):
    def char(self,
             top = False,
             bottom = False,
             left = False,
             right = False):
        parts = []
        if top:
            parts.append(u'top')
        if bottom:
            parts.append(u'bottom')
        if left:
            parts.append(u'left')
        if right:
            parts.append(u'right')
        if not parts:
            return None
        return getattr(self, u'_'.join(parts))


_MixedBoxDrawCharacterSet = NamedTuple(
    u'_MixedBoxDrawCharacterSet',
    [
        (u'first_char_set', BoxDrawCharacterSet),
        (u'second_char_set', BoxDrawCharacterSet),

        (u'top_then_bottom', unicode),
        (u'top_then_left', unicode),
        (u'top_then_right', unicode),
        (u'top_then_bottom_left', unicode),
        (u'top_then_bottom_right', unicode),
        (u'top_then_left_right', unicode),
        (u'top_then_bottom_left_right', unicode),

        (u'bottom_then_top', unicode),
        (u'bottom_then_left', unicode),
        (u'bottom_then_right', unicode),
        (u'bottom_then_top_left', unicode),
        (u'bottom_then_top_right', unicode),
        (u'bottom_then_left_right', unicode),
        (u'bottom_then_top_left_right', unicode),

        (u'left_then_top', unicode),
        (u'left_then_bottom', unicode),
        (u'left_then_right', unicode),
        (u'left_then_top_bottom', unicode),
        (u'left_then_bottom_right', unicode),
        (u'left_then_top_right', unicode),
        (u'left_then_top_bottom_right', unicode),

        (u'right_then_top', unicode),
        (u'right_then_bottom', unicode),
        (u'right_then_left', unicode),
        (u'right_then_top_bottom', unicode),
        (u'right_then_top_left', unicode),
        (u'right_then_bottom_left', unicode),
        (u'right_then_top_bottom_left', unicode),

        (u'top_bottom_then_left', unicode),
        (u'top_bottom_then_right', unicode),
        (u'top_bottom_then_left_right', unicode),

        (u'top_left_then_bottom', unicode),
        (u'top_left_then_right', unicode),
        (u'top_left_then_bottom_right', unicode),

        (u'top_right_then_bottom', unicode),
        (u'top_right_then_left', unicode),
        (u'top_right_then_bottom_left', unicode),

        (u'bottom_left_then_top', unicode),
        (u'bottom_left_then_right', unicode),
        (u'bottom_left_then_top_right', unicode),

        (u'bottom_right_then_top', unicode),
        (u'bottom_right_then_left', unicode),
        (u'bottom_right_then_top_left', unicode),

        (u'left_right_then_top', unicode),
        (u'left_right_then_bottom', unicode),
        (u'left_right_then_top_bottom', unicode),

        (u'top_bottom_left_then_right', unicode),
        (u'top_bottom_right_then_left', unicode),
        (u'top_left_right_then_bottom', unicode),
        (u'bottom_left_right_then_top', unicode),
    ]
)


class MixedBoxDrawCharacterSet(_MixedBoxDrawCharacterSet):
    def char(self, **_3to2kwargs):

        if 'right' in _3to2kwargs: right = _3to2kwargs['right']; del _3to2kwargs['right']
        else: right =  0
        if 'left' in _3to2kwargs: left = _3to2kwargs['left']; del _3to2kwargs['left']
        else: left =  0
        if 'bottom' in _3to2kwargs: bottom = _3to2kwargs['bottom']; del _3to2kwargs['bottom']
        else: bottom =  0
        if 'top' in _3to2kwargs: top = _3to2kwargs['top']; del _3to2kwargs['top']
        else: top =  0
        def parts_with(val):
            parts = []
            if top == val:
                parts.append(u'top')
            if bottom == val:
                parts.append(u'bottom')
            if left == val:
                parts.append(u'left')
            if right == val:
                parts.append(u'right')
            return parts

        first_key = u'_'.join(parts_with(-1))
        second_key = u'_'.join(parts_with(+1))

        if not first_key and not second_key:
            return None
        if not first_key:
            return getattr(self.second_char_set, second_key)
        if not second_key:
            return getattr(self.first_char_set, first_key)
        return getattr(self, u'{}_then_{}'.format(first_key, second_key))


NORMAL_BOX_CHARS = BoxDrawCharacterSet(
    top=u'╵',
    bottom=u'╷',
    left=u'╴',
    right=u'╶',

    top_bottom=u'│',
    top_left=u'┘',
    top_right=u'└',
    bottom_left=u'┐',
    bottom_right=u'┌',
    left_right=u'─',

    top_bottom_left=u'┤',
    top_bottom_right=u'├',
    top_left_right=u'┴',
    bottom_left_right=u'┬',

    top_bottom_left_right=u'┼',
)


BOLD_BOX_CHARS = BoxDrawCharacterSet(
    top=u'╹',
    bottom=u'╻',
    left=u'╸',
    right=u'╺',

    top_bottom=u'┃',
    top_left=u'┛',
    top_right=u'┗',
    bottom_left=u'┓',
    bottom_right=u'┏',
    left_right=u'━',

    top_bottom_left=u'┫',
    top_bottom_right=u'┣',
    top_left_right=u'┻',
    bottom_left_right=u'┳',

    top_bottom_left_right=u'╋',
)


DOUBLED_BOX_CHARS = BoxDrawCharacterSet(
    # No special end caps for these ones :(.
    top=u'║',
    bottom=u'║',
    left=u'═',
    right=u'═',

    top_bottom=u'║',
    top_left=u'╝',
    top_right=u'╚',
    bottom_left=u'╗',
    bottom_right=u'╔',
    left_right=u'═',

    top_bottom_left=u'╣',
    top_bottom_right=u'╠',
    top_left_right=u'╩',
    bottom_left_right=u'╦',

    top_bottom_left_right=u'╬',
)


ASCII_BOX_CHARS = BoxDrawCharacterSet(
    # We can round the half-caps up to full or down to nothing.
    top=u' ',
    bottom=u' ',
    left=u' ',
    right=u' ',

    top_bottom=u'|',
    top_left=u'/',
    top_right=u'\\',
    bottom_left=u'\\',
    bottom_right=u'/',
    left_right=u'-',

    top_bottom_left=u'+',
    top_bottom_right=u'+',
    top_left_right=u'+',
    bottom_left_right=u'+',

    top_bottom_left_right=u'+',
)


NORMAL_THEN_BOLD_MIXED_BOX_CHARS = MixedBoxDrawCharacterSet(
    first_char_set=NORMAL_BOX_CHARS,
    second_char_set=BOLD_BOX_CHARS,

    top_then_bottom=u'╽',
    top_then_left=u'┙',
    top_then_right=u'┕',
    top_then_bottom_left=u'┪',
    top_then_bottom_right=u'┢',
    top_then_left_right=u'┷',
    top_then_bottom_left_right=u'╈',

    bottom_then_top=u'╿',
    bottom_then_left=u'┑',
    bottom_then_right=u'┍',
    bottom_then_top_left=u'┩',
    bottom_then_top_right=u'┡',
    bottom_then_left_right=u'┯',
    bottom_then_top_left_right=u'╇',

    left_then_top=u'┚',
    left_then_bottom=u'┒',
    left_then_right=u'╼',
    left_then_top_bottom=u'┨',
    left_then_bottom_right=u'┲',
    left_then_top_right=u'┺',
    left_then_top_bottom_right=u'╊',

    right_then_top=u'┖',
    right_then_bottom=u'┎',
    right_then_left=u'╾',
    right_then_top_bottom=u'┠',
    right_then_top_left=u'┹',
    right_then_bottom_left=u'┱',
    right_then_top_bottom_left=u'╉',

    top_bottom_then_left=u'┥',
    top_bottom_then_right=u'┝',
    top_bottom_then_left_right=u'┿',

    top_left_then_bottom=u'┧',
    top_left_then_right=u'┶',
    top_left_then_bottom_right=u'╆',

    top_right_then_bottom=u'┟',
    top_right_then_left=u'┵',
    top_right_then_bottom_left=u'╅',

    bottom_left_then_top=u'┦',
    bottom_left_then_right=u'┮',
    bottom_left_then_top_right=u'╄',

    bottom_right_then_top=u'┞',
    bottom_right_then_left=u'┭',
    bottom_right_then_top_left=u'╃',

    left_right_then_top=u'┸',
    left_right_then_bottom=u'┰',
    left_right_then_top_bottom=u'╂',

    top_bottom_left_then_right=u'┾',
    top_bottom_right_then_left=u'┽',
    top_left_right_then_bottom=u'╁',
    bottom_left_right_then_top=u'╀',

    # You're right, it *was* tedious.
    # If the box drawing character set was laid out so that certain bits
    # corresponded to certain legs in a reasonable way, this wouldn't have been
    # needed...
)


def box_draw_character(first,
                       second, **_3to2kwargs):
    if 'right' in _3to2kwargs: right = _3to2kwargs['right']; del _3to2kwargs['right']
    else: right =  0
    if 'left' in _3to2kwargs: left = _3to2kwargs['left']; del _3to2kwargs['left']
    else: left =  0
    if 'bottom' in _3to2kwargs: bottom = _3to2kwargs['bottom']; del _3to2kwargs['bottom']
    else: bottom =  0
    if 'top' in _3to2kwargs: top = _3to2kwargs['top']; del _3to2kwargs['top']
    else: top =  0
    u"""Finds a box drawing character based on its connectivity.

    For example:

        box_draw_character(
            NORMAL_BOX_CHARS,
            BOLD_BOX_CHARS,
            top=-1,
            right=+1)

    evaluates to '┕', which has a normal upward leg and bold rightward leg.

    Args:
        first: The character set to use for legs set to -1. If set to None,
            defaults to the same thing as the second character set.
        second: The character set to use for legs set to +1.
        top: Whether the upward leg should be present.
        bottom: Whether the bottom leg should be present.
        left: Whether the left leg should be present.
        right: Whether the right leg should be present.

    Returns:
        A box drawing character approximating the desired properties, or None
        if all legs are set to 0.
    """
    if first is None:
        first = second
    sign = +1
    combo = None

    # Known combinations.
    if first is NORMAL_BOX_CHARS and second is BOLD_BOX_CHARS:
        combo = NORMAL_THEN_BOLD_MIXED_BOX_CHARS
    if first is BOLD_BOX_CHARS and second is NORMAL_BOX_CHARS:
        combo = NORMAL_THEN_BOLD_MIXED_BOX_CHARS
        sign = -1

    if combo is None:
        choice = second if +1 in [top, bottom, left, right] else first
        return choice.char(top=bool(top),
                           bottom=bool(bottom),
                           left=bool(left),
                           right=bool(right))

    return combo.char(top=top * sign,
                      bottom=bottom * sign,
                      left=left * sign,
                      right=right * sign)
