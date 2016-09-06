from sgftools.board import Board


class ProblemsBookGenerator(object):
    def __init__(self):
        pass

    def generate(self, game):
        size = game.game_info.board_size

        for node in [x for x in game.root.next_nodes if x.move is None]:
            board = Board(size)
            board.apply(node)
            yield board
        return []
