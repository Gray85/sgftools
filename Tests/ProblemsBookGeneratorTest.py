import unittest

from sgftools.DiagramGenerators.ProblemsBookGenerator import ProblemsBookGenerator
from sgftools.board import Board
from sgftools.game import GameNode, Point, Game, GameInfo


class ProblemsBookGeneratorTest(unittest.TestCase):
    def test_simple_book_generator(self):
        child1 = GameNode()
        child1.add_black = [Point(7, 7)]

        child2 = GameNode()
        child2.add_white = [Point(3, 3)]
        child2.add_black = [Point(5, 5)]

        child3 = GameNode()
        child3.add_black = [Point(11, 11)]

        root = GameNode()
        root.add_next_node(child1)
        root.add_next_node(child2)
        root.add_next_node(child3)

        game = Game(13)
        game.game_info = GameInfo()
        game.game_info.board_size = 13
        game.root = root

        board1 = Board(13).black(7, 7)
        board2 = Board(13).white(3, 3).black(5, 5)
        board3 = Board(13).black(11, 11)

        expected = [board1, board2, board3]

        generator = ProblemsBookGenerator()

        actual = [x for x in generator.generate(game)]
        self.assertEqual(expected, actual)




