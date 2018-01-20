from enum import Enum


class GameAnnotation:
    def __init__(self):
        pass

    def __eq__(self, other):
        if other is None:
            return False

        return isinstance(other,  type(self))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return self.__str__()


class GoodForBlack(GameAnnotation):
    def __str__(self):
        return "Good for black"


class GoodForWhite(GameAnnotation):
    def __str__(self):
        return "Good for white"


class PositionIsEven(GameAnnotation):
    def __str__(self):
        return "Position is even"


class PositionIsUnclear(GameAnnotation):
    def __str__(self):
        return "Position is unclear"


#
# Пометки точек на доске
#
class Markup:
    def __init__(self):
        pass

    def __eq__(self, other):
        if other is None:
            return False

        return isinstance(other,  type(self))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(self.__str__())


class Circle(Markup):
    def __str__(self):
        return 'Circle'


class Square(Markup):
    def __str__(self):
        return 'Square'


class Cross(Markup):
    def __str__(self):
        return 'Cross'


class Triangle(Markup):
    def __str__(self):
        return 'Triangle'


class Label(Markup):
    def __init__(self, string: str):
        super(Label, self).__init__()
        self.label = string

    def __str__(self):
        return self.label

    def __eq__(self, other):
        if other is None:
            return False

        if not isinstance(other, type(self)):
            return False

        return self.label == other.label

    def __hash__(self):
        return hash(self.label)


class Stone(Enum):

    def __str__(self):
        return self._name_

    White = 1
    Black = 2


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if other is None:
            return False

        if not isinstance(other, type(self)):
            return False

        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "(x:{}, y:{})".format(self.x, self.y)

    def __hash__(self):
        return (self.x << 8) + self.y


class Move:
    def __init__(self, stone, point):
        self.stone = stone
        self.point = point

    def __str__(self):
        return "{}: {}".format(self.stone, self.point)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if other is None:
            return False

        if not isinstance(other, type(self)):
            return False

        return self.point == other.point and self.stone == other.stone


class Game:
    def __init__(self, board_size=19):
        self.game_info = GameInfo()
        self.game_info.board_size = board_size
        self.root = None


#############################################
class GameInfo:
    def __init__(self):
        self._info = dict()
        self.author = ''
        self.black_player = ''
        self.black_rank = ''
        self.black_team = ''
        self.white_player = ''
        self.white_rank = ''
        self.white_team = ''
        self.copyright = ''
        self.date = ''
        self.event = ''
        self.game_name = ''
        self.result = ''
        self.round = ''
        self.game_comment = ''
        self.place = ''

    @property
    def board_size(self):
        return self._info.get('SZ', 19)

    @board_size.setter
    def board_size(self, size):
        self._info['SZ'] = size

    def __getitem__(self, key):
        if key in self._info:
            return self._info[key]
        return None

    def __setitem__(self, key, value):
        self._info[key] = value

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return self._info == other._info and \
            self.place == other.place and \
            self.date == other.date and \
            self.author == other.author and \
            self.black_player == other.black_player and \
            self.black_rank == other.black_rank and \
            self.black_team == other.black_team and \
            self.copyright == other.copyright and \
            self.event == other.event and \
            self.game_comment == other.game_comment and \
            self.game_name == other.game_name and \
            self.result == other.result and \
            self.round == other.round and \
            self.white_player == other.white_player and \
            self.white_rank == other.white_rank and \
            self.white_team == other.white_team

    def __ne__(self, other):
        return not self.__eq__(other)


class GameNode:
    def __init__(self):
        self.extra = dict()
        self.move = None
        self.add_black = []
        self.add_white = []
        self.empty = []
        self.move_number = None
        self.turn_to_play = None
        self.node_name = ''
        self.comment = ''
        self.annotation = None
        self._markups = set()
        self.next_nodes = []

    @property
    def markups(self):
        return self._markups

    @markups.setter
    def markups(self, marks):
        self._markups = set(marks)

    @property
    def next_node(self):
        if len(self.next_nodes) == 0:
            return None
        return self.next_nodes[0]

    def add_next_node(self, next_node):
        self.next_nodes.append(next_node)

    def __setitem__(self, key, value):
        self.extra[key] = value

    def __getitem__(self, key):
        if key in self.extra:
            return self.extra.get(key)
        return None

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        info = []
        if self.move is not None:
            info.append("{}".format(self.move))

        if len(self.add_black) != 0:
            info.append("Add black: {}".format(self.add_black))

        if len(self.add_white) != 0:
            info.append("Add white: {}".format(self.add_white))

        if len(self.empty) != 0:
            info.append("Clear stones: {}".format(self.empty))

        if len(self.markups) != 0:
            info.append("Markups: {}".format(self.markups))

        if self.move_number is not None:
            info.append("Move number: {}".format(self.move_number))

        if self.turn_to_play is not None:
            info.append("Turn to play: {}".format(self.turn_to_play))

        if self.node_name != '' and self.node_name is not None:
            info.append("Node name: {}".format(self.node_name))

        if self.annotation is not None:
            info.append("Annotation: {}".format(self.annotation))

        if self.comment != '':
            info.append("Comment: {}".format(self.comment))

        return "\n".join(info + ["{}: {}".format(key, value) for key, value in self.extra])

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        if other is None:
            return False

        if not isinstance(other,  type(self)):
            return False

        return self.add_black == other.add_black and \
               self.add_white == other.add_white and \
               self.comment == other.comment and \
               self.empty == other.empty and \
               self.move == other.move and \
               self.annotation == other.annotation and \
               self.markups == other.markups and \
               self.node_name == other.node_name and \
               self.move_number == other.move_number and \
               self.turn_to_play == other.turn_to_play and \
               self.extra == other.extra












