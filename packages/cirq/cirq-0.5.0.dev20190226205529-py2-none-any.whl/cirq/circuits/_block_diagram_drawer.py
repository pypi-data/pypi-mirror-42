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
from typing import Dict, List, Tuple, Optional

import collections

from cirq.circuits._box_drawing_character_data import (
    box_draw_character,
    BoxDrawCharacterSet
)


class Block(object):
    u"""The mutable building block that block diagrams are made of."""
    def __init__(self):
        self.left = u''
        self.right = u''
        self.top = u''
        self.bottom = u''
        self.center = u''
        self.content = u''
        self.horizontal_alignment = 0
        self._prev_curve_grid_chars = None

    def min_width(self):
        u"""Minimum width necessary to render the block's contents."""
        return max(
            max(len(e) for e in self.content.split(u'\n')),
            # Only horizontal lines can cross 0 width blocks.
            int(any([self.top, self.bottom]))
        )

    def min_height(self):
        u"""Minimum height necessary to render the block's contents."""
        return max(
            len(self.content.split(u'\n')) if self.content else 0,
            # Only vertical lines can cross 0 height blocks.
            int(any([self.left, self.right]))
        )

    def draw_curve(self,
                   grid_characters, **_3to2kwargs):
        if 'crossing_char' in _3to2kwargs: crossing_char = _3to2kwargs['crossing_char']; del _3to2kwargs['crossing_char']
        else: crossing_char =  None
        if 'bottom' in _3to2kwargs: bottom = _3to2kwargs['bottom']; del _3to2kwargs['bottom']
        else: bottom =  False
        if 'right' in _3to2kwargs: right = _3to2kwargs['right']; del _3to2kwargs['right']
        else: right =  False
        if 'left' in _3to2kwargs: left = _3to2kwargs['left']; del _3to2kwargs['left']
        else: left =  False
        if 'top' in _3to2kwargs: top = _3to2kwargs['top']; del _3to2kwargs['top']
        else: top =  False
        u"""Draws lines in the box using the given character set.

        Supports merging the new lines with the lines from a previous call to
        draw_curve, including when they have different character sets (assuming
        there exist characters merging the two).

        Args:
            grid_characters: The character set to draw the curve with.
            top: Draw topward leg?
            left: Draw leftward leg?
            right: Draw rightward leg?
            bottom: Draw downward leg?
            crossing_char: Overrides the all-legs-present character. Useful for
                ascii diagrams, where the + doesn't always look the clearest.
        """
        if not any([top, left, right, bottom]):
            return

        # Remember which legs are new, old, or missing.
        sign_top = +1 if top else -1 if self.top else 0
        sign_bottom = +1 if bottom else -1 if self.bottom else 0
        sign_left = +1 if left else -1 if self.left else 0
        sign_right = +1 if right else -1 if self.right else 0

        # Add new segments.
        if top:
            self.top = grid_characters.top_bottom
        if bottom:
            self.bottom = grid_characters.top_bottom
        if left:
            self.left = grid_characters.left_right
        if right:
            self.right = grid_characters.left_right

        # Fill center.
        if not all([crossing_char,
                    self.top, self.bottom, self.left, self.right]):
            crossing_char = box_draw_character(
                self._prev_curve_grid_chars,
                grid_characters,
                top=sign_top,
                bottom=sign_bottom,
                left=sign_left,
                right=sign_right)
        self.center = crossing_char or u''

        self._prev_curve_grid_chars = grid_characters

    def render(self, width, height):
        u"""Returns a list of text lines representing the block's contents.

        Args:
            width: The width of the output text. Must be at least as large as
                the block's minimum width.
            height: The height of the output text. Must be at least as large as
                the block's minimum height.

        Returns:
            Text pre-split into lines.
        """
        if width == 0 or height == 0:
            return [u''] * height

        out_chars = [[u' '] * width for _ in xrange(height)]

        mid_x = int((width - 1) * self.horizontal_alignment)
        mid_y = (height - 1) // 2

        # Horizontal line legs.
        if self.left:
            out_chars[mid_y][:mid_x + 1] = self.left * (mid_x + 1)
        if self.right:
            out_chars[mid_y][mid_x:] = self.right * (width - mid_x)

        # Vertical line legs.
        if self.top:
            for y in xrange(mid_y + 1):
                out_chars[y][mid_x] = self.top
        if self.bottom:
            for y in xrange(mid_y, height):
                out_chars[y][mid_x] = self.bottom

        # Central content.
        mid = self.content or self.center
        if self.content or self.center:
            content_lines = mid.split(u'\n')
            y = mid_y - (len(content_lines) - 1) // 2
            for dy, content_line in enumerate(content_lines):
                s = int((len(content_line) - 1) * self.horizontal_alignment)
                x = mid_x - s
                for dx, c in enumerate(content_line):
                    out_chars[y + dy][x + dx] = c

        return [u''.join(line) for line in out_chars]


class BlockDiagramDrawer(object):
    u"""Aligns text and curve data placed onto an abstract 2d grid of blocks."""

    def __init__(self):
        self._blocks = collections.defaultdict(
            Block)  # type: Dict[Tuple[int, int], Block]
        self._min_widths = collections.defaultdict(
            lambda: 0)  # type: Dict[int, int]
        self._min_heights = collections.defaultdict(
            lambda: 0)  # type: Dict[int, int]

        # Populate the origin.
        _ = self._blocks[(0, 0)]
        _ = self._min_widths[0]
        _ = self._min_heights[0]

    def mutable_block(self, x, y):
        u"""Returns the block at (x, y) so it can be edited."""
        if x < 0 or y < 0:
            raise IndexError(u'x < 0 or y < 0')
        return self._blocks[(x, y)]

    def set_col_min_width(self, x, min_width):
        u"""Sets a minimum width for blocks in the column with coordinate x."""
        if x < 0:
            raise IndexError(u'x < 0')
        self._min_widths[x] = min_width

    def set_row_min_height(self, y, min_height):
        u"""Sets a minimum height for blocks in the row with coordinate y."""
        if y < 0:
            raise IndexError(u'y < 0')
        self._min_heights[y] = min_height

    def render(self, **_3to2kwargs):
        if 'min_block_height' in _3to2kwargs: min_block_height = _3to2kwargs['min_block_height']; del _3to2kwargs['min_block_height']
        else: min_block_height =  0
        if 'min_block_width' in _3to2kwargs: min_block_width = _3to2kwargs['min_block_width']; del _3to2kwargs['min_block_width']
        else: min_block_width =  0
        if 'block_span_y' in _3to2kwargs: block_span_y = _3to2kwargs['block_span_y']; del _3to2kwargs['block_span_y']
        else: block_span_y =  None
        if 'block_span_x' in _3to2kwargs: block_span_x = _3to2kwargs['block_span_x']; del _3to2kwargs['block_span_x']
        else: block_span_x =  None
        u"""Outputs text containing the diagram.

        Args:
            block_span_x: The width of the diagram in blocks. Set to None to
                default to using the smallest width that would include all
                accessed blocks and columns with a specified minimum width.
            block_span_y: The height of the diagram in blocks. Set to None to
                default to using the smallest height that would include all
                accessed blocks and rows with a specified minimum height.
            min_block_width: A global minimum width for all blocks.
            min_block_height: A global minimum height for all blocks.

        Returns:
            The diagram as a string.
        """

        # Determine desired size of diagram in blocks.
        if block_span_x is None:
            block_span_x = 1 + max(
                max(x for x, _ in self._blocks.keys()),
                max(self._min_widths.keys()),
            )
        if block_span_y is None:
            block_span_y = 1 + max(
                max(y for _, y in self._blocks.keys()),
                max(self._min_heights.keys()),
            )

        # Method for accessing blocks without creating new entries.
        empty = Block()
        def block(x, y):
            return self._blocks.get((x, y), empty)

        # Determine the width of every column and the height of every row.
        widths = dict((
            x, max(
                max(block(x, y).min_width() for y in xrange(block_span_y)),
                self._min_widths.get(x, 0),
                min_block_width,
            ))
            for x in xrange(block_span_x))
        heights = dict((
            y, max(
                max(block(x, y).min_height() for x in xrange(block_span_x)),
                self._min_heights.get(y, 0),
                min_block_height,
            ))
            for y in xrange(block_span_y))

        # Get the individually rendered blocks.
        block_renders = {
            (x, y): block(x, y).render(widths[x], heights[y])
            for x in xrange(block_span_x)
            for y in xrange(block_span_y)
        }

        # Paste together all of the rows of rendered block content.
        out_lines = []  # type: List[str]
        for y in xrange(block_span_y):
            for by in xrange(heights[y]):
                out_line_chunks = []  # type: List[str]
                for x in xrange(block_span_x):
                    out_line_chunks.extend(block_renders[x, y][by])
                out_lines.append(u''.join(out_line_chunks).rstrip())

        # Then paste together the rows.
        return u'\n'.join(out_lines)
