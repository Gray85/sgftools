import sys
sys.path.append('..')

import unittest
from sgftools.game import *
from sgftools.parser import SgfParser
from sgftools.gamebuilder import UnsupportedGameException


class GameBuilderTest(unittest.TestCase):

    def load_root_node(self, sgf):
        parser = SgfParser()
        game = parser.load_game_from_string(sgf)
        return game.root

    def test_load_gamenode_comment(self):
        expected = GameNode()
        expected.comment = 'root'
        root = self.load_root_node("(;FF[4]C[root]GM[1];W[cd])")
        self.assertEqual(expected, root)

    def test_load_gamenode_pass(self):
        expected = GameNode()
        expected.move = Move(Stone.White, None)

        expectedblack = GameNode()
        expectedblack.move = Move(Stone.Black, None)

        root = self.load_root_node("(;W[];B[tt])")

        self.assertEqual(expected, root)
        self.assertEqual(expectedblack, root.next_node)

    def test_load_gamenode_move(self):
        expectedwhite = GameNode()
        expectedwhite.move = Move(Stone.White, Point(3, 4))

        expectedblack = GameNode()
        expectedblack.move = Move(Stone.Black, Point(5, 4))

        root = self.load_root_node("(;W[cd];B[ed])")

        self.assertEqual(expectedwhite, root)
        self.assertEqual(expectedblack, root.next_node)

    def test_addstones(self):
        expected = GameNode()
        expected.add_black = [Point(3, 4), Point(5, 3)]
        expected.add_white = [Point(2, 4)]
        expected.empty = [Point(1, 1), Point(2, 2)]

        root = self.load_root_node("(;AW[bd]AB[cd][ec]AE[aa][bb])")
        self.assertEqual(expected, root)

    def test_addstones_repeated(self):
        expected = GameNode()
        expected.add_black = [Point(3, 4), Point(5, 3)]
        expected.add_white = [Point(2, 4)]

        root = self.load_root_node("(;AW[bd]AB[cd]AB[ec])")
        self.assertEqual(expected, root)

    def test_nodename_turntomove_movenumber(self):
        expected = GameNode()
        expected.move_number = 13
        expected.node_name = 'devil move'
        expected.turn_to_play = Stone.Black

        root = self.load_root_node("(;MN[13]N[devil move]PL[B])")
        self.assertEqual(expected, root)

    def test_annotation(self):
        expected = GameNode()
        root = self.load_root_node("(;GB[];GW[];DM[];UC[])")

        expected.annotation = GoodForBlack()
        self.assertEqual(expected, root)

        root = root.next_node
        expected.annotation = GoodForWhite()
        self.assertEqual(expected, root)

        root = root.next_node
        expected.annotation = PositionIsEven()
        self.assertEqual(expected, root)

        root = root.next_node
        expected.annotation = PositionIsUnclear()
        self.assertEqual(expected, root)

    def test_markups(self):
        expected = GameNode()
        expected.markups = [
            (Circle(), Point(3, 3)),
            (Label('A'), Point(4, 4)),
            (Cross(), Point(5, 5)),
            (Square(), Point(1, 1)),
            (Triangle(), Point(2, 2)),
            (Circle(), Point(6, 6))
        ]

        root = self.load_root_node("(;CR[cc]LB[dd:A]MA[ee]SQ[aa]TR[bb]CR[ff])")
        self.assertEqual(expected, root)

    def test_variations(self):
        expected = GameNode()
        expected.comment = 'start'
        expected.next_nodes = [GameNode(), GameNode()]
        expected.next_nodes[0].move = Move(Stone.Black, Point(4, 4))
        expected.next_nodes[0].next_nodes = [GameNode()]
        expected.next_nodes[0].next_nodes[0].move = Move(Stone.White, Point(3, 6))

        expected.next_nodes[1].move = Move(Stone.Black, Point(3, 4))

        root = self.load_root_node("(;C[start](;B[dd];W[cf])(;B[cd]))")

        self.assertEqual(expected, root)
        self.assertListEqual(expected.next_nodes, root.next_nodes)
        self.assertEqual(expected.next_nodes[0].next_node, root.next_nodes[0].next_node)

    def test_compressed_pointlist(self):
        expected = GameNode()
        expected.add_black = [
            Point(1, 1), Point(1, 2), Point(2, 1), Point(2, 2), Point(4, 4)
        ]
        root = self.load_root_node("(;AB[aa:bb][dd])")
        self.assertEqual(expected, root)

    def get_expected_GameInfo(self):
        info = GameInfo()
        info.author = 'gamer'
        info.event = 'just game'
        info.date = '2015-12-31'
        info.result = 'B+3'
        info.copyright = '(c)'
        info.black_player = 'Shusaku'
        info.black_team = 'Japan'
        info.black_rank = '9p'
        info.white_player = 'Gu Li'
        info.white_team = 'China'
        info.white_rank = '9p'
        info.round = '1'
        info.board_size = 19
        info.game_name = 'impossible'
        info.game_comment = u'только для тестирования'
        info['KM'] = '0.00'
        info['ST'] = '2'
        info['GM'] = '1'
        info['AP'] = 'CGoban:3'
        info['FF'] = '4'
        info['CA'] = 'UTF-8'
        info['RU'] = 'Japanese'

        return info

    def test_load_GameInfo(self):
        expected = self.get_expected_GameInfo()
        parser = SgfParser()

        actual = parser.load_game('testdata/test_gameinfo.sgf')

        self.assertDictEqual(actual.game_info._info, expected._info)
        self.assertEqual(expected, actual.game_info, "Информация об игре загрузилась неверно")

    def test_unsupported_game(self):
        sgf = "(;FF[4]C[root]GM[2])"
        with self.assertRaises(UnsupportedGameException):
            parser = SgfParser()
            parser.load_game_from_string(sgf)


if __name__ == '__main__':
    unittest.main()
