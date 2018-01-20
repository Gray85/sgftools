
import itertools
from collections import namedtuple

from sgftools.game import Point, Stone, Circle, Square, Cross, Triangle, Label

_Cell = namedtuple("Cell", "x y node")

class ImpossibleMove(Exception):
    def __init__(self, message=None):
        self.message = message

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if self.message is None:
            return "Impossible move"

        return self.message


class Node:
    def __init__(self, stone=None, marker=None):
        self.marker = marker
        self.stone = stone

    def __repr__(self):
        return self.__str__()

    def is_empty(self):
        return (self.marker is None) and (self.stone is None)

    def __eq__(self, other):
        if other is None:
            return self.is_empty()

        if not isinstance(other, type(self)):
            return False

        return self.marker == other.marker and self.stone == other.stone

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        if self.is_empty():
            return '<empty>'

        if self.stone is None:
            return str(self.marker)

        if self.marker is None:
            return str(self.stone)

        return "{}/{}".format(self.stone, self.marker)


class Board:
    def __init__(self, size:int=19):
        self.name = ''
        self._size = size
        self._grid = dict()
        self.comment = ''

    @property
    def size(self):
        return self._size

    def black(self, x, y):
        return self._node(x, y, Stone.Black)

    def white(self, x, y):
        return self._node(x, y, Stone.White)

    def circle(self, x, y):
        return self._marker(x, y, Circle())

    def square(self, x, y):
        return self._marker(x, y, Square())

    def cross(self, x, y):
        return self._marker(x, y, Cross())

    def triangle(self, x, y):
        return self._marker(x, y, Triangle())

    def label(self, x: int, y: int, label: str):
        return self._marker(x, y, Label(label))

    def _marker(self, x, y, marker):
        node = self[x, y]
        node.marker = marker
        self[x, y] = node
        return self

    def _node(self, x, y, color):
        node = self[x, y]
        node.stone = color
        self[x, y] = node
        return self

    def apply(self, game_node):
        for point in game_node.empty:
            del self._grid[point]

        for point in game_node.add_black:
            self.black(point.x, point.y)

        for point in game_node.add_white:
            self.white(point.x, point.y)

        for markup in game_node.markups:
            point = markup[1]
            node = self[point]
            node.marker = markup[0]
            self[point] = node

        if game_node.move is None:
            return

        # pass
        if game_node.move.point is None:
            return

        node = self[game_node.move.point]
        if node.stone is not None:
            raise ImpossibleMove("Here already is the stone: {}".format(game_node.move.point))

        node.stone = game_node.move.stone
        self[game_node.move.point] = node
        self._execute_take_stones(game_node.move.point, game_node.move.stone)

    def _execute_take_stones(self, point, stone):
        # 1. Собрать соседние группы камней другого цвета
        groups = []
        neighbor_points = self._get_neighbours(point)
        for pnt in neighbor_points:
            already_in_any_group = any(pnt in grp for grp in groups)
            if self[pnt].stone is not None and self[pnt].stone != stone and not already_in_any_group:
                group = self._find_stone_group(pnt)
                if len(group) > 0:
                    groups.append(group)

        # 2. Подсчитать дамэ групп
        for grp in groups:
            cnt = self._count_dame(grp)
            # 3. Снять группы с дамэ = 0
            if cnt == 0:
                self._remove_group(grp)

    def _remove_group(self, group):
        for x in group:
            self[x].stone = None

    def _count_dame(self, group):
        dame_set = set(y for y in
                       itertools.chain.from_iterable(self._get_neighbours(x) for x in group)
                       if self[y].stone is None)

        return len(dame_set)

    def _find_stone_group(self, pnt):
        result = set()
        stone = self[pnt].stone
        candidates = [pnt]
        while len(candidates) > 0:
            result.update(candidates)
            candidates = list(itertools.chain.from_iterable([self._get_neighbours(x) for x in candidates]))
            candidates = [x for x in set(candidates) if not self._out_of_board(x)]
            candidates = [x for x in candidates if self[x].stone == stone]
            candidates = [x for x in candidates if x not in result]

        return result

    def _get_neighbours(self, point):
        points = [Point(point.x - 1, point.y),
                  Point(point.x + 1, point.y),
                  Point(point.x, point.y - 1),
                  Point(point.x, point.y + 1)]
        return [pnt for pnt in points if not self._out_of_board(pnt)]

    def __setitem__(self, pos, value):
        if isinstance(pos, Point):
            point = pos
        else:
            point = Point(*pos)

        if self._out_of_board(point):
            raise IndexError("point {} out of board. Board size: {}".format(point, self.size))

        self._grid[point] = value

    def __getitem__(self, pos):
        if isinstance(pos, Point):
            point = pos
        else:
            point = Point(*pos)

        if self._out_of_board(point):
            raise IndexError("point {} out of board. Board size: {}".format(point, self.size))

        return self._grid.get(point, Node())

    def _out_of_board(self, point):
        return point.x <= 0 or point.x > self._size or point.y <= 0 or point.y > self._size

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        if other is None:
            return False

        if not isinstance(other, type(self)):
            return False

        return other.size == self._size and \
               other.name == self.name and \
               other.comment == self.comment and \
               self._grid_eq(other)

    def _grid_eq(self, other):
        node_set = set(self._grid.keys()).union(other._grid.keys())

        return all(self[point] == other[point] for point in node_set)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self._grid.__str__()

    def __iter__(self):
        return self._iteration()

    def _iteration(self):
        for x in range(1, self.size  +1):
            for y in range(1, self.size + 1):
                node = self[x, y]
                if not node.is_empty():
                    yield _Cell(x, y, node)




