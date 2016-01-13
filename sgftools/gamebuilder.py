from collections import defaultdict

from sgftools.game import Circle, Triangle, Square, Cross, Label, GoodForBlack, GoodForWhite, PositionIsUnclear, \
    PositionIsEven, Game, GameNode


class UnsupportedGameException(Exception):
    def __init__(self, game_no):
        self._game_no = game_no

    def __str__(self):
        return "Не поддерживаемый тип игры: {}. Поддерживается только го (1)".format(self._game_no)


class GameBuilder:
    def __init__(self):
        self._property_parsers = self._create_property_parsers_map()
        self._node_map = self._create_node_map()
        self._only_root_properties = ['GC', 'FF', 'GM', 'AP', 'ST', 'SZ', 'CA', 'AN', 'BR', 'BT', 'MULTIGOGM',
                                      'BP', 'WR', 'WT', 'WP', 'RO', 'EV', 'PC', 'OV', 'DT', 'CP', 'RU', 'RE', 'US',
                                      'TM', 'US', 'SO']

        self._non_root_properties = ['B', 'BL', 'BM', 'DO', 'IT', 'KO', 'MN', 'OB',
                                     'OW', 'TE', 'W', 'WL', 'AB', 'AE', 'AW', 'PL', 'AR', 'C', 'CR', 'DD', 'DM',
                                     'FG', 'GB', 'GW', 'HO', 'LB', 'LN', 'MA', 'N', 'PM', 'SQ', 'TR', 'UC', 'V', 'VW']

        self.markconstructors = {
            'CR': Circle,
            'TR': Triangle,
            'SQ': Square,
            'MA': Cross,
            'LB': Label
        }

    def _create_node_map(self):
        return {
            'GC': 'game_comment',
            'PB': 'black_player',
            'BR': 'black_rank',
            'BT': 'black_team',
            'PW': 'white_player',
            'WR': 'white_rank',
            'WT': 'white_team',
            'DT': 'date',
            'RO': 'round',
            'AN': 'author',
            'EV': 'event',
            'GN': 'game_name',
            'RE': 'result',
            'CP': 'copyright',
            'W': 'move',
            'B': 'move',
            'C': 'comment',
            'AB': 'add_black',
            'AW': 'add_white',
            'AE': 'empty',
            'MN': 'move_number',
            'PL': 'turn_to_play',
            'N': 'node_name',
            'GB': 'annotation',
            'DM': 'annotation',
            'GW': 'annotation',
            'UC': 'annotation',
            'MARK': 'markups'
        }

    def _create_property_parsers_map(self):
        return {
            # x: str
            "SZ": int,
            'GM': lambda x: self.check_game_number(x),
            # x: list
            'W': lambda x: ('W', self.parse_coordinate(x[0])),
            'B': lambda x: ('B', self.parse_coordinate(x[0])),
            'AB': self.parse_coordinates,
            'AW': self.parse_coordinates,
            'AE': self.parse_coordinates,
            'MN': lambda x: int(x[0]),
            'GB': lambda x: GoodForBlack(),
            'GW': lambda x: GoodForWhite(),
            'UC': lambda x: PositionIsUnclear(),
            'DM': lambda x: PositionIsEven(),
            'MARK': lambda x: list(self.parse_markups(x))
        }

    def parse_markups(self, markslist):
        for marks in markslist:
            mark = self.markconstructors[marks[0]]
            for point in marks[1:]:
                data = point.split(':')
                yield ((mark(*data[1:])), self.parse_coordinate(data[0]))

    def parse_coordinates(self, xylist):
        result = []
        for xy in xylist:
            xydata = xy.split(":")
            if (len(xydata) == 1):
                result.append(self.parse_coordinate(xydata[0]))
            else:
                upperleft = self.parse_coordinate(xydata[0])
                bottomright = self.parse_coordinate(xydata[1])
                for x in range(upperleft[0], bottomright[0] + 1):
                    for y in range(upperleft[1], bottomright[1] + 1):
                        result.append((x, y))

        return result;

    def parse_coordinate(self, xy):
        if xy == '':
            return None
        if xy == 'tt':  # специальный случай
            return None

        x = ord(xy[0]) - ord('a') + 1
        y = ord(xy[1]) - ord('a') + 1
        return (x, y)

    def check_game_number(self, no):
        if no != '1':
            raise UnsupportedGameException(no)
        else:
            return no

    def Build(self, tokenlist):
        game = Game()
        self._fill_game_info(game.game_info, tokenlist[0])
        tokenlist[0] = [x for x in tokenlist[0] if x[0] not in self._only_root_properties]
        game.root = self.load_game_nodes(tokenlist)[0]

        return game

    def load_game_nodes(self, nodes):
        if len(nodes) == 0:
            return [None]

        if len(nodes[0]) == 0:
            return [None]

        if nodes[0][0] == 'variations':  # TODO: использовать специальный тип списка
            return [self.load_game_nodes(x)[0] for x in nodes[0][1:]]

        gamenode = self.create_game_node(nodes[0])
        gamenode.next_nodes = self.load_game_nodes(nodes[1:])
        return [gamenode]

    def group_by_key(self, properties):
        keyvalues = defaultdict(list)
        for prop in properties:
            keyvalues[prop[0]].extend(prop[1:])

        markupkeys = ['TR', 'CR', 'LB', 'MA', 'SQ']
        for key in markupkeys:
            values = keyvalues[key]
            if len(values) != 0:
                values.insert(0, key)
                keyvalues['MARK'].append(values)
            del keyvalues[key]

        return keyvalues

    def create_game_node(self, properties):
        keyvalues = self.group_by_key(properties)
        node = GameNode()
        for key in keyvalues:
            parser = self._property_parsers.get(key, lambda x: x[0])
            parsed = parser(keyvalues[key])
            self.set_node_value(node, key, parsed)

        return node

    def set_node_value(self, node, key, value):
        attrname = self._node_map.get(key)
        if (attrname is None):
            node[key] = value
        else:
            setattr(node, attrname, value)

    def _fill_game_info(self, info, properties):
        nonrootproperties = (x for x in properties if x[0] not in self._non_root_properties)
        for prop in nonrootproperties:
            key, value = self.get_header_key_value(prop)
            self.set_node_value(info, key, value)

    def get_header_key_value(self, alist):
        key = alist[0]
        value = alist[1]

        parser = self._property_parsers.get(key, lambda x: x)
        return key, parser(value)