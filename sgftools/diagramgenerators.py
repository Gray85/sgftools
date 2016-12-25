from sgftools.board import Board


class ProblemsBookGenerator(object):
    def __init__(self):
        pass

    def generate(self, game, title=None):
        size = game.game_info.board_size
        num = 1
        for node in [x for x in game.root.next_nodes if x.move is None]:
            board = Board(size)
            board.apply(node)
            if title is not None:
                board.name = "{} {}".format(title, num)
            num += 1
            yield board

