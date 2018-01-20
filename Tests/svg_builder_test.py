import tempfile
import unittest
import filecmp

import os

from sgftools.board import Board, Node
from sgftools.game import Circle, Triangle, Square, Cross, Label, Stone
from sgftools.svgdiagrambuilder import SvgDiagramBuilder


class SvgDiagramBuilderTest(unittest.TestCase):
    def test_emty_board(self):
        builder = SvgDiagramBuilder()
        builder.build(Board())

    def test_simple_board(self):
        builder = SvgDiagramBuilder()
        markers = [None, Circle(), Triangle(), Square(), Cross(), Label("A7")]
        board = Board()
        y = 1
        for marker in markers:
            board[1, y] = Node(Stone.Black, marker)
            board[3, y] = Node(Stone.White, marker)
            board[5, y] = Node(None, marker)
            y += 2

        board.black(16, 3).label(16, 3, "1") \
            .white(16, 5).label(16, 5, "2") \
            .black(17, 5).label(17, 5, "3") \
            .white(17, 6).label(17, 6, "4") \
            .black(17, 4).label(17, 4, "5") \
            .white(16, 6).label(16, 6, "6") \
            .black(14, 3).label(14, 3, "7") \
            .white(16, 10).label(16, 10, "8")

        tmp = tempfile.mkstemp()
        os.close(tmp[0])

        try:
            builder.build(board, file=tmp[1])
            self.assertTrue(filecmp.cmp("svg_expected/simple_expected.svg", tmp[1]))
        finally:
            os.remove(tmp[1])
            pass