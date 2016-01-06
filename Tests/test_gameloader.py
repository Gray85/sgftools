import sys
sys.path.append('..')

import unittest
from sgftools.game import *
from sgftools.parser import SgfParser


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
        expected.move = ('W', None)

        expectedblack = GameNode()
        expectedblack.move = ('B', None)

        root = self.load_root_node("(;W[];B[tt])")

        self.assertEqual(expected, root)
        self.assertEqual(expectedblack, root.nextnode)


    def test_load_gamenode_move(self):
        expectedwhite = GameNode()
        expectedwhite.move = ('W', (3, 4))

        expectedblack = GameNode()
        expectedblack.move = ('B', (5, 4))

        root = self.load_root_node("(;W[cd];B[ed])")

        self.assertEqual(expectedwhite, root)
        self.assertEqual(expectedblack, root.nextnode)

    def test_addstones(self):
        expected = GameNode()
        expected.add_black = [(3, 4), (5, 3)]
        expected.add_white = [(2,4)]
        expected.empty = [(1, 1), (2, 2)]

        root = self.load_root_node("(;AW[bd]AB[cd][ec]AE[aa][bb])")
        self.assertEqual(expected, root)

    def test_addstones_repeated(self):
        expected = GameNode()
        expected.add_black = [(3, 4), (5, 3)]
        expected.add_white = [(2,4)]

        root = self.load_root_node("(;AW[bd]AB[cd]AB[ec])")
        self.assertEqual(expected, root)

    def test_nodename_turntomove_movenumber(self):
        expected = GameNode()
        expected.move_number = 13
        expected.node_name = 'devil move'
        expected.turn_to_play = 'B'

        root = self.load_root_node("(;MN[13]N[devil move]PL[B])")
        self.assertEqual(expected, root)

    def test_annotation(self):
        expected = GameNode()
        root = self.load_root_node("(;GB[];GW[];DM[];UC[])")

        expected.annotation = GoodForBlack()
        self.assertEqual(expected, root)

        root = root.nextnode
        expected.annotation = GoodForWhite()
        self.assertEqual(expected, root)

        root = root.nextnode
        expected.annotation = PositionIsEven()
        self.assertEqual(expected, root)

        root = root.nextnode
        expected.annotation = PositionIsUnclear()
        self.assertEqual(expected, root)

    def test_markups(self):
        expected = GameNode()
        expected.markups = [
            (Circle(), (3, 3)),
            (Label('A'), (4, 4)),
            (Cross(), (5, 5)),
            (Square(), (1, 1)),
            (Triangle(), (2, 2)),
            (Circle(), (6, 6))
        ]

        root = self.load_root_node("(;CR[cc]LB[dd:A]MA[ee]SQ[aa]TR[bb]CR[ff])")
        self.assertEqual(expected, root)

    def test_variations(self):
        expected = GameNode()
        expected.comment = 'start'
        expected.nextnodes = [GameNode(), GameNode()]
        expected.nextnodes[0].move = ('B', (4, 4))
        expected.nextnodes[0].nextnodes = [GameNode()]
        expected.nextnodes[0].nextnodes[0].move = ('W', (3, 6))

        expected.nextnodes[1].move = ('B', (3, 4))

        root = self.load_root_node("(;C[start](;B[dd];W[cf])(;B[cd]))")

        self.assertEqual(expected, root)
        self.assertListEqual(expected.nextnodes, root.nextnodes)
        self.assertEqual(expected.nextnodes[0].nextnode, root.nextnodes[0].nextnode)

    def test_compressed_pointlist(self):
        expected = GameNode()
        expected.add_black = [
            (1,1), (1, 2), (2, 1), (2, 2), (4, 4)
        ]
        root = self.load_root_node("(;AB[aa:bb][dd])")
        self.assertEqual(expected, root)


if __name__ == '__main__':
    unittest.main()