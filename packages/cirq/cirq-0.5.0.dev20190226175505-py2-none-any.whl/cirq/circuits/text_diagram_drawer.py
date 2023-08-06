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
from typing import Callable, List, NamedTuple, Tuple, TYPE_CHECKING, cast, Union

import numpy as np

from cirq.circuits._block_diagram_drawer import BlockDiagramDrawer
from cirq.circuits._box_drawing_character_data import (
    BoxDrawCharacterSet,
    NORMAL_BOX_CHARS,
    BOLD_BOX_CHARS,
    ASCII_BOX_CHARS,
)


if TYPE_CHECKING:
    # pylint: disable=unused-import
    from typing import Tuple, Dict, Optional


_HorizontalLine = NamedTuple(u'HorizontalLine', [
    (u'y', Union[int, float]),
    (u'x1', Union[int, float]),
    (u'x2', Union[int, float]),
    (u'emphasize', bool),
])
_VerticalLine = NamedTuple(u'VerticalLine', [
    (u'x', Union[int, float]),
    (u'y1', Union[int, float]),
    (u'y2', Union[int, float]),
    (u'emphasize', bool),
])
_DiagramText = NamedTuple(u'DiagramText', [
    (u'text', unicode),
    (u'transposed_text', unicode),
])


def pick_charset(use_unicode, emphasize):
    if not use_unicode:
        return ASCII_BOX_CHARS
    if emphasize:
        return BOLD_BOX_CHARS
    return NORMAL_BOX_CHARS


class TextDiagramDrawer(object):
    u"""A utility class for creating simple text diagrams.
    """

    def __init__(self):
        self.entries = dict()  # type: Dict[Tuple[int, int], _DiagramText]
        self.vertical_lines = []  # type: List[_VerticalLine]
        self.horizontal_lines = []  # type: List[_HorizontalLine]
        self.horizontal_padding = {}  # type: Dict[int, Union[int, float]]
        self.vertical_padding = {}  # type: Dict[int, Union[int, float]]

    def write(self,
              x,
              y,
              text,
              transposed_text = None):
        u"""Adds text to the given location.

        Args:
            x: The column in which to write the text.
            y: The row in which to write the text.
            text: The text to write at location (x, y).
            transposed_text: Optional text to write instead, if the text
                diagram is transposed.
        """
        entry = self.entries.get((x, y), _DiagramText(u'', u''))
        self.entries[(x, y)] = _DiagramText(
            entry.text + text,
            entry.transposed_text + (transposed_text if transposed_text
                                     else text))

    def content_present(self, x, y):
        u"""Determines if a line or printed text is at the given location."""

        # Text?
        if (x, y) in self.entries:
            return True

        # Vertical line?
        if any(v.x == x and v.y1 < y < v.y2 for v in self.vertical_lines):
            return True

        # Horizontal line?
        if any(line_y == y and x1 < x < x2
               for line_y, x1, x2, _ in self.horizontal_lines):
            return True

        return False

    def grid_line(self, x1, y1, x2, y2,
                  emphasize = False):
        u"""Adds a vertical or horizontal line from (x1, y1) to (x2, y2).

        Horizontal line is selected on equality in the second coordinate and
        vertical line is selected on equality in the first coordinate.

        Raises:
            ValueError: If line is neither horizontal nor vertical.
        """
        if x1 == x2:
            self.vertical_line(x1, y1, y2, emphasize)
        elif y1 == y2:
            self.horizontal_line(y1, x1, x2, emphasize)
        else:
            raise ValueError(u"Line is neither horizontal nor vertical")

    def vertical_line(self,
                      x,
                      y1,
                      y2,
                      emphasize = False
                      ):
        u"""Adds a line from (x, y1) to (x, y2)."""
        y1, y2 = sorted([y1, y2])
        self.vertical_lines.append(_VerticalLine(x, y1, y2, emphasize))

    def horizontal_line(self,
                        y,
                        x1,
                        x2,
                        emphasize = False
                        ):
        u"""Adds a line from (x1, y) to (x2, y)."""
        x1, x2 = sorted([x1, x2])
        self.horizontal_lines.append(_HorizontalLine(y, x1, x2, emphasize))

    def transpose(self):
        u"""Returns the same diagram, but mirrored across its diagonal."""
        out = TextDiagramDrawer()
        out.entries = dict(((y, x), _DiagramText(v.transposed_text, v.text))
                       for (x, y), v in self.entries.items())
        out.vertical_lines = [_VerticalLine(*e)
                              for e in self.horizontal_lines]
        out.horizontal_lines = [_HorizontalLine(*e)
                                for e in self.vertical_lines]
        out.vertical_padding = self.horizontal_padding.copy()
        out.horizontal_padding = self.vertical_padding.copy()
        return out

    def width(self):
        u"""Determines how many entry columns are in the diagram."""
        max_x = -1.0
        for x, _ in self.entries.keys():
            max_x = max(max_x, x)
        for v in self.vertical_lines:
            max_x = max(max_x, v.x)
        for h in self.horizontal_lines:
            max_x = max(max_x, h.x1, h.x2)
        return 1 + int(max_x)

    def height(self):
        u"""Determines how many entry rows are in the diagram."""
        max_y = -1.0
        for _, y in self.entries.keys():
            max_y = max(max_y, y)
        for h in self.horizontal_lines:
            max_y = max(max_y, h.y)
        for v in self.vertical_lines:
            max_y = max(max_y, v.y1, v.y2)
        return 1 + int(max_y)

    def force_horizontal_padding_after(
            self, index, padding):
        u"""Change the padding after the given column."""
        self.horizontal_padding[index] = padding

    def force_vertical_padding_after(
            self, index, padding):
        u"""Change the padding after the given row."""
        self.vertical_padding[index] = padding

    def _transform_coordinates(
            self,
            func
    ):
        u"""Helper method to transformer either row or column coordinates."""

        def func_x(x):
            return func(x, 0)[0]

        def func_y(y):
            return func(0, y)[1]

        self.entries = dict((
            cast(Tuple[int, int], func(int(x), int(y))), v)
            for (x, y), v in self.entries.items())
        self.vertical_lines = [
            _VerticalLine(func_x(x), func_y(y1), func_y(y2), emph)
            for x, y1, y2, emph in self.vertical_lines]
        self.horizontal_lines = [
            _HorizontalLine(func_y(y), func_x(x1), func_x(x2), emph)
            for y, x1, x2, emph in self.horizontal_lines]
        self.horizontal_padding = dict((
            int(func_x(int(x))), padding)
            for x, padding in self.horizontal_padding.items())
        self.vertical_padding = dict((
            int(func_y(int(y))), padding)
            for y, padding in self.vertical_padding.items())

    def insert_empty_columns(self, x, amount = 1):
        u"""Insert a number of columns after the given column."""
        def transform_columns(
                column,
                row
        ):
            return column + (amount if column >= x else 0), row
        self._transform_coordinates(transform_columns)

    def insert_empty_rows(self, y, amount = 1):
        u"""Insert a number of rows after the given row."""
        def transform_rows(
                column,
                row
        ):
            return column, row + (amount if row >= y else 0)
        self._transform_coordinates(transform_rows)

    def render(self,
               horizontal_spacing = 1,
               vertical_spacing = 1,
               crossing_char = None,
               use_unicode_characters = True):
        u"""Outputs text containing the diagram."""

        block_diagram = BlockDiagramDrawer()

        w = self.width()
        h = self.height()

        # Communicate padding into block diagram.
        for x in xrange(0, w - 1):
            block_diagram.set_col_min_width(
                x*2 + 1,
                # Horizontal separation looks narrow, so partials round up.
                int(np.ceil(self.horizontal_padding.get(x, horizontal_spacing)))
            )
            block_diagram.set_col_min_width(x*2, 1)
        for y in xrange(0, h - 1):
            block_diagram.set_row_min_height(
                y*2 + 1,
                # Vertical separation looks wide, so partials round down.
                int(np.floor(self.vertical_padding.get(y, vertical_spacing)))
            )
            block_diagram.set_row_min_height(y*2, 1)

        # Draw vertical lines.
        for x_b, y1_b, y2_b, emphasize in self.vertical_lines:
            x = int(x_b * 2)
            y1, y2 = int(min(y1_b, y2_b) * 2), int(max(y1_b, y2_b) * 2)
            charset = pick_charset(use_unicode_characters, emphasize)

            # Caps.
            block_diagram.mutable_block(x, y1).draw_curve(
                charset, bottom=True)
            block_diagram.mutable_block(x, y2).draw_curve(
                charset, top=True)

            # Span.
            for y in xrange(y1 + 1, y2):
                block_diagram.mutable_block(x, y).draw_curve(
                    charset, top=True, bottom=True)

        # Draw horizontal lines.
        for y_b, x1_b, x2_b, emphasize in self.horizontal_lines:
            y = int(y_b * 2)
            x1, x2 = int(min(x1_b, x2_b) * 2), int(max(x1_b, x2_b) * 2)
            charset = pick_charset(use_unicode_characters, emphasize)

            # Caps.
            block_diagram.mutable_block(x1, y).draw_curve(
                charset, right=True)
            block_diagram.mutable_block(x2, y).draw_curve(
                charset, left=True)

            # Span.
            for x in xrange(x1 + 1, x2):
                block_diagram.mutable_block(x, y).draw_curve(
                    charset, left=True, right=True, crossing_char=crossing_char)

        # Place entries.
        for (x, y), v in self.entries.items():
            x *= 2
            y *= 2
            block_diagram.mutable_block(x, y).content = v.text

        return block_diagram.render()
