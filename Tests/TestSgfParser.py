import sys
sys.path.append('..')

import unittest
from sgftools.game import GameInfo
from sgftools.parser import SgfParser, SgfPyParser, UnsupportedGameException


class TestSgfParser(unittest.TestCase):
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
        info.gamename = 'impossible'
        info['GC'] = u'только для тестирования'
        info['KM'] = '0.00'
        info['ST'] = '2'
        info['GM'] = '1'
        info['AP'] = 'CGoban:3'
        info['FF'] = '4'
        info['CA'] = 'UTF-8'
        info['RU'] = 'Japanese'

        return info

    def test_unsupported_game(self):
        sgf = "(;FF[4]C[root]GM[2])"
        with self.assertRaises(UnsupportedGameException):
            parser = SgfParser()
            parser.load_game_from_string(sgf)

    def test_wrong_value_in_node(self):
        # для тех вершин, где нужны конкретные значения
        self.assertFalse(True, 'тест не реализован')

    def test_error_in_parsing(self):
        # обработка ошибок в файле
        self.assertFalse(True, 'тест не реализован')

    def test_read_cp1251_encoding(self):
        self.assertFalse(True, 'тест не реализован')

    def test_load_GameInfo(self):
        expected = self.get_expected_GameInfo()
        parser = SgfParser()

        actual = parser.load_game('testdata/test_gameinfo.sgf')

        self.assertDictEqual(actual.game_info._info, expected._info)
        # self.assertEqual(expected, actual.game_info, "Информация об игре загрузилась неверно")

    def test_SgfPyParser(self):
        sgf = "(;FF[4]C[root](;C[a];C[b](;C[c])(;C[d];C[e]))(;C[f](;C[g];C[h];C[i])\r\n(;C[j])))"

        variation1 = [
            [['C', 'a']],
            [['C', 'b']],
            ['variations',
             [[['C', 'c']]],  # subvariant1
             [[['C', 'd']], [['C', 'e']]]  # subvariant2
             ]
        ]

        variation2 = [
            [['C', 'f']],
            ['variations',
             [[['C', 'g']], [['C', 'h']], [['C', 'i']]],
             [[['C', 'j']]]
             ],
        ]

        expected = [
            [['FF', '4'], ['C', 'root']],  # node1
            ['variations',
             variation1,
             variation2
             ]
        ]
        parser = SgfPyParser()
        actual = parser.parseString(sgf)

        self.assertSequenceEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
