import unittest

from sgftools.ProblemsPdfBuilder import ProblemsPdfBuilder
from sgftools.board import Board


class ProblemsPdfWriterTest(unittest.TestCase):

    def TestGenerateOneTask(self):
        board = Board(19)
        board\
            .black(1, 1, '12')\
            .white(1, 2, '44')\
            .black(13, 13)\
            .white(1, 13)\
            .white(13, 1)

        board13 = Board(13)
        board13 \
            .black(1, 1, '12') \
            .white(1, 2) \
            .black(13, 13) \
            .white(1, 13) \
            .white(13, 1)

        generator = ProblemsPdfBuilder(trim_board=True)
        generator.add_diagrams([board, board13, board, board13, board, board, board, board])
        generator.save('output.pdf')
