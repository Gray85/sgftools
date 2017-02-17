import sys
sys.path.append('..')

import unittest
from sgftools.parser import SgfParser, SgfPyParser


class TestSgfParser(unittest.TestCase):

    def test_wrong_value_in_node(self):
        # для тех вершин, где нужны конкретные значения
        raise NotImplementedError('тест не реализован')

    def test_error_in_parsing(self):
        """ Обработка неверного файла """
        parser = SgfParser()
        sgf = "This is not sgf"
        with self.assertRaises(ValueError):
            parser.load_game_from_string(sgf)

    def test_read_cp1251_encoding(self):
        parser = SgfParser()

        actual = parser.load_game('testdata/test_cp1251.sgf')
        self.assertEqual(actual.game_info.game_comment, 'Комментарий')

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
        actual = parser.parse_string(sgf)

        self.assertSequenceEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
