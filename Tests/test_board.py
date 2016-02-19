import unittest

import functools

from sgftools.board import Board, Node, ImpossibleMove
from sgftools.game import Stone, Point, Square, GameNode, Move, Triangle, Circle


class TestBoard(unittest.TestCase):
    def create_board_13x13(self):
        board = Board(13)
        board.comment = "Board for test"
        board.name = "Board 13x13"
        node = Node()
        node.stone = Stone.Black
        node.marker = Square()
        board[1, 1] = node

        return board

    def test_set_get_node_value(self):
        board = Board()
        node = Node()
        node.stone = Stone.Black
        board[1, 1] = node

        self.assertEqual(board[1, 1], node)

    def test_set_get_node_value_by_point(self):
        board = Board()
        node = Node()
        node.stone = Stone.Black
        board[Point(1, 1)] = node

        self.assertEqual(board[Point(1, 1)], node)

    def test_out_of_range_index(self):
        board = Board()

        self.assertRaises(IndexError, lambda: board[0, 1])
        self.assertRaises(IndexError, lambda: board[1, 0])
        self.assertRaises(IndexError, lambda: board[20, 1])
        self.assertRaises(IndexError, lambda: board[1, 20])

    def test_equals(self):
        board_1 = self.create_board_13x13()
        board_2 = self.create_board_13x13()

        self.assertEqual(board_1, board_2)

    def test_not_equals(self):
        board_1 = self.create_board_13x13()
        board_2 = self.create_board_13x13().white(7, 7)

        self.assertNotEqual(board_1, board_2)

    def test_equals_None_node_as_empty(self):
        board_1 = self.create_board_13x13()
        board_2 = self.create_board_13x13()

        board_1[3, 3] = Node()  # empty node
        board_1[4, 4] = None  # empty node

        self.assertEqual(board_1, board_2)

    def test_equals_set_None(self):
        board_1 = self.create_board_13x13()
        board_2 = self.create_board_13x13()

        board_1[3, 3] = Node()  # empty node
        board_2[3, 3] = None  # empty node
        self.assertEqual(board_1, board_2)

    def test_equals_set_None_None(self):
        board_1 = self.create_board_13x13()
        board_2 = self.create_board_13x13()

        board_1[3, 3] = None  # empty node
        board_2[3, 3] = None  # empty node
        self.assertEqual(board_1, board_2)

    def test_equals_set_Node_Node(self):
        board_1 = self.create_board_13x13()
        board_2 = self.create_board_13x13()

        board_1[3, 3] = Node()  # empty node
        board_2[3, 3] = Node()  # empty node
        self.assertEqual(board_1, board_2)

    def test_apply_move(self):
        game_node = GameNode()
        game_node.add_black = [Point(2, 2), Point(12, 12)]
        game_node.add_white = [Point(3, 3), Point(11, 11)]
        game_node.empty = [Point(1, 1)]
        game_node.move = Move(Stone.Black, Point(7, 7))
        game_node.markups = [(Triangle(), Point(7, 7)), (Circle(), Point(5, 5))]

        board = self.create_board_13x13()
        board.apply(game_node)

        board_expected = self.create_board_13x13()
        board_expected[1, 1] = None
        board_expected[2, 2] = Node(stone=Stone.Black)
        board_expected[12, 12] = Node(stone=Stone.Black)
        board_expected[3, 3] = Node(stone=Stone.White)
        board_expected[11, 11] = Node(stone=Stone.White)
        board_expected[5, 5] = Node(marker=Circle())
        board_expected[7, 7] = Node(stone=Stone.Black, marker=Triangle())

        self.assertEqual(board_expected, board)

    def test_apply_move_replace_stone(self):
        game_node = GameNode()
        game_node.add_white = [Point(1, 1)]
        board = self.create_board_13x13()
        board.apply(game_node)

        board_expected = self.create_board_13x13()
        board_expected[1, 1] = Node(stone=Stone.White, marker=Square())

        self.assertEqual(board_expected, board)

    def test_impossible_move_stone_already_here(self):
        game_node = GameNode()
        game_node.move = Move(Stone.Black, Point(1, 1))
        board = self.create_board_13x13()

        self.assertRaises(ImpossibleMove, functools.partial(board.apply, game_node))

    def test_empty_node_first(self):
        game_node = GameNode()
        game_node.empty = [Point(1, 1)]
        game_node.move = Move(Stone.White, Point(1, 1))
        board = self.create_board_13x13()
        board.apply(game_node)

        board_expected = self.create_board_13x13()
        board_expected[1, 1] = Node(stone=Stone.White)
        self.assertEqual(board_expected, board)

    def test_снятие_камней_1_камень(self):
        board = self.create_board_13x13()\
            .black(7, 7)\
            .white(6, 7)\
            .white(8, 7)\
            .white(7, 8)

        game_node = GameNode()
        game_node.move = Move(Stone.White, Point(7, 6))
        board.apply(game_node)

        board_expected = self.create_board_13x13()\
            .white(7, 6)\
            .white(6, 7)\
            .white(8, 7)\
            .white(7, 8)
        self.assertEqual(board_expected, board)

    def test_снятие_камней_4_камня_в_центре(self):
        board = Board(13)\
            .white(7, 6).white(6, 7).white(8, 7).white(7, 8)\
            .black(7, 5).black(5, 7).black(9, 7).black(7, 9)\
            .black(8, 8).black(6, 6).black(8, 6).black(6, 8)

        game_node = GameNode()
        game_node.move = Move(Stone.Black, Point(7, 7))
        board.apply(game_node)

        board_expected = Board(13)\
            .black(7, 5).black(5, 7).black(9, 7).black(7, 9)\
            .black(8, 8).black(6, 6).black(8, 6).black(6, 8).black(7, 7)

        self.assertEqual(board_expected, board)

    def test_снятие_камней_2_группы_в_центре(self):
        board = Board(13)\
            .white(6, 8).white(6, 7).white(7, 8).white(8, 6).white(7, 6).white(8, 7)\
            .black(6, 6).black(8, 8)\
            .black(5, 7).black(5, 8).black(6, 9).black(7, 9)\
            .black(7, 5).black(8, 5).black(9, 6).black(9, 7)

        game_node = GameNode()
        game_node.move = Move(Stone.Black, Point(7, 7))
        board.apply(game_node)

        board_expected = Board(13)\
            .black(6, 6).black(8, 8).black(7, 7)\
            .black(5, 7).black(5, 8).black(6, 9).black(7, 9)\
            .black(7, 5).black(8, 5).black(9, 6).black(9, 7)

        self.assertEqual(board_expected, board)

    def test_снятие_камней_группа_в_углу(self):
        board = Board(13)\
            .white(1, 2).white(2, 2).white(2, 1)\
            .black(1, 3).black(2, 3).black(3, 1).black(3, 2)\

        game_node = GameNode()
        game_node.move = Move(Stone.Black, Point(1, 1))
        board.apply(game_node)

        board_expected = Board(13)\
            .black(1, 1)\
            .black(1, 3).black(2, 3).black(3, 1).black(3, 2)\

        self.assertEqual(board_expected, board)

    def test_toString(self):
        raise NotImplementedError()

    def test_как_очищать_маркеры(self):
        raise NotImplementedError()


if __name__ == '__main__':
    unittest.main()
