
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
    def __init__(self, string):
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


class Game:
    def __init__(self):
        self.game_info = GameInfo()
        self.root = None


#############################################
class GameInfo:
    def __init__(self):
        self._info = dict()

    @property
    def author(self):
        return self._info.get('AN')

    @author.setter
    def author(self, author):
        self._info['AN'] = author

    @property
    def black_rank(self):
        return self._info.get('BR')

    @black_rank.setter
    def black_rank(self, rank):
        self._info['BR'] = rank

    @property
    def black_team(self):
        return self._info.get('BT')

    @black_team.setter
    def black_team(self, team):
        self._info['BT'] = team

    @property
    def black_player(self):
        return self._info.get('PB')

    @black_player.setter
    def black_player(self, name):
        self._info['PB'] = name

    @property
    def white_rank(self):
        return self._info.get('WR')

    @white_rank.setter
    def white_rank(self, rank):
        self._info['WR'] = rank

    @property
    def white_team(self):
        return self._info.get('WT')

    @white_team.setter
    def white_team(self, team):
        self._info['WT'] = team

    @property
    def white_player(self):
        return self._info.get('PW')

    @white_player.setter
    def white_player(self, name):
        self._info['PW'] = name

    @property
    def copyright(self):
        return self._info.get('CP')

    @copyright.setter
    def copyright(self, copyright):
        self._info['CP'] = copyright

    @property
    def date(self):
        return self._info.get['DT']

    @date.setter
    def date(self, date):
        self._info['DT'] = date

    @property
    def event(self):
        return self._info.get('EV')

    @event.setter
    def event(self, event):
        self._info['EV'] = event

    @property
    def gamename(self):
        return self._info.get('GN')

    @gamename.setter
    def gamename(self, name):
        self._info['GN'] = name

    @property
    def result(self):
        return self._info.get('RE')

    @result.setter
    def result(self, result):
        self._info['RE'] = result

    @property
    def round(self):
        return self._info.get('RO')

    @round.setter
    def round(self, round):
        self._info['RO'] = round

    @property
    def board_size(self):
        return self._info.get('SZ', 19)

    @board_size.setter
    def board_size(self, size):
        self._info['SZ'] = size

    def __getitem__(self, key):
        return self._info[key]

    def __setitem__(self, key, value):
        self._info[key] = value

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
                self._info == other._info)

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
        self.nextnodes = []

    @property
    def markups(self):
        return self._markups

    @markups.setter
    def markups(self, marks):
        self._markups = set(marks)

    @property
    def nextnode(self):
        if len(self.nextnodes) == 0:
            return None
        return self.nextnodes[0]

    def __setitem__(self, key, value):
        self.extra[key] = value

    def __getitem__(self, key):
        return self.extra.get(key)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        info = []
        if self.move is not None:
            info.append("{}: {}".format(self.move[0], self.move[1]))

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












