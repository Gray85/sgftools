import unittest

from sgftools.DiagramGenerators.ProblemsBookGenerator import ProblemsBookGenerator
from sgftools.board import Board
from sgftools.parser import SgfParser


class IntegrationTests(unittest.TestCase):

    def test_simple_9x9_board(self):
        parser = SgfParser()
        actual = parser.load_game('testdata/test9x9.sgf')

        board = Board(9)
        node = actual.root
        while node is not None:
            board.apply(node)
            node = node.next_node

        expected_board = Board(9)\
            .black(7, 9).white(8, 9)\
            .black(6, 8).black(7, 8).white(8, 8)\
            .black(3, 7).black(5, 7).black(7, 7).white(8, 7)\
            .black(5, 6).black(6, 6).white(7, 6)\
            .black(1, 5).black(2, 5).black(3, 5).black(4, 5).white(5, 5).white(6, 5).white(7, 5).white(9, 5)\
            .black(1, 4).white(2, 4).black(3, 4).black(4, 4).black(5, 4).black(6, 4).white(7, 4).white(8, 4)\
            .white(9, 4)\
            .black(1, 3).white(2, 3).black(3, 3).white(4, 3).white(5, 3).black(6, 3).black(7, 3).black(8, 3)\
            .white(9, 3)\
            .white(1, 2).white(2, 2).white(3, 2).white(5, 2).black(6, 2).black(7, 2).white(8, 2)\
            .white(4, 1).white(5, 1).white(6, 1).black(7, 1).white(9, 1)

        self.assertEqual(expected_board, board)

    def test_simple_problem_book_9x9(self):
        parser = SgfParser()
        game = parser.load_game('testdata/problems9x9.sgf')

        board1 = Board(9).white(5, 1).white(7, 1).white(3, 2)
        board2 = Board(9).white(5, 1).white(7, 1).white(3, 1)
        board3 = Board(9).white(3, 1).white(5, 1).white(3, 2)
        board4 = Board(9).white(1, 1).white(2, 2).white(3, 1)

        expected_boards = [board1, board2, board3, board4]

        generator = ProblemsBookGenerator()

        actual = [x for x in generator.generate(game)]
        self.assertEqual(expected_boards, actual)

