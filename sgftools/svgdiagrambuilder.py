from svgwrite import Drawing
from svgwrite.shapes import Circle, Rect, Polygon, Line
import svgwrite
from svgwrite.text import Text

from sgftools import game
from sgftools.board import Board
from sgftools.game import Stone


class SvgDiagramBuilder:
    picture_size = 42000

    def __init__(self):

        self.default_style = "font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;" \
                             "text-align:center;writing-mode:lr-tb;text-anchor:middle;line-height:100%"
        self.unit = svgwrite.px
        self._margin = SvgDiagramBuilder.picture_size / 50
        self._line_width = SvgDiagramBuilder.picture_size / 420
        #todo: передавать размеры в конструкторе
        #todo: научиться обрезать доску до указанных размеров или по области где есть камни

    def build(self, board: Board, file=None):
        board_size = board.size
        stone_size = ((SvgDiagramBuilder.picture_size - 2 * self._margin) / board_size)

        drw = svgwrite.Drawing(size=(SvgDiagramBuilder.picture_size * self.unit, SvgDiagramBuilder.picture_size * self.unit))
        self._draw_grid(drw, board_size, stone_size)

        for cell in board:
            self._draw_cell(drw, cell, stone_size)

        if isinstance(file, str):
            drw.saveas(filename=file)
        elif file is not None:
            drw.write(file)
        else:
            #todo: возвращать file-like object?
            pass

    def _draw_grid(self, drw, board_size, stone_size):
        #todo: уметь рисовать переданный фон
        from_grid_to_edge = stone_size / 2 + self._margin
        grid = drw.add(drw.g(id='grid', stroke=svgwrite.rgb(0, 0, 0)))
        for i in range(board_size):
            grid.add(
                drw.line(
                    start=(
                        (from_grid_to_edge - self._line_width / 2) * self.unit,
                        (i * stone_size + from_grid_to_edge) * self.unit
                    ),
                    end=(
                        (SvgDiagramBuilder.picture_size - from_grid_to_edge + self._line_width / 2) * self.unit,
                        (i * stone_size + from_grid_to_edge) * self.unit
                    ),
                    stroke_width=self._line_width * self.unit
                )
            )

            grid.add(
                drw.line(
                    start=(
                        (i * stone_size + from_grid_to_edge) * self.unit,
                        (from_grid_to_edge - self._line_width / 2) * self.unit
                    ),
                    end=(
                        (i * stone_size + from_grid_to_edge) * self.unit,
                        (SvgDiagramBuilder.picture_size - from_grid_to_edge + self._line_width / 2) * self.unit
                    ),
                    stroke_width=self._line_width * self.unit
                )
            )

        for point in self._get_dot_points(board_size):
            grid.add(
                Circle(
                    (
                      ((point[0] - 1) * stone_size + from_grid_to_edge) * self.unit,
                      ((point[1] - 1) * stone_size + from_grid_to_edge) * self.unit
                    ),
                    self._line_width * 2.5 * self.unit,
                    fill=svgwrite.rgb(0, 0, 0)
                )
            )

    def _draw_cell(self, drw: Drawing, cell, stone_size):
        from_grid_to_edge = stone_size / 2 + self._margin
        x = (from_grid_to_edge + (cell.x - 1) * stone_size)
        y = (from_grid_to_edge + (cell.y - 1) * stone_size)
        node = cell.node
        cell = drw.add(drw.g(id=f'cell{cell.x}-{cell.y}'))

        if node.stone is not None:
            self._put_stone(cell, x, y, node.stone, stone_size)

        if node.stone is None:
            half_size = 3 * stone_size / 8
            cell.add(Rect(
                ((x - half_size) * self.unit, (y - half_size) * self.unit),
                (2 * half_size * self.unit, 2 * half_size * self.unit),
                fill="white"
            ))

        fill = "white" if node.stone == Stone.Black else "black"
        if isinstance(node.marker, game.Label):
            self._put_label(cell, x, y, node.marker.label, fill, stone_size)
        elif isinstance(node.marker, game.Square):
            self._put_square(cell, fill, stone_size, x, y)
        elif isinstance(node.marker, game.Circle):
            self._put_circle(cell, x, y, fill, stone_size)
        elif isinstance(node.marker, game.Cross):
            self._put_cross(cell, x, y, fill, stone_size)
        elif isinstance(node.marker, game.Triangle):
            self._put_triangle(cell, x, y, fill, stone_size)

    def _put_stone(self, cell, x, y, stone, stone_size):
        #todo: уметь рисовать камни переданные изображениеми
        fill = "white" if stone == Stone.White else "black"
        cell.add(
            Circle(
                (x * self.unit, y * self.unit),
                stone_size / 2 * self.unit,
                stroke="black",
                fill=fill,
                stroke_width=self._line_width / 5
            )
        )

    def _put_triangle(self, cell, x, y, fill, stone_size):
        cell.add(
            Polygon(
                [
                    (x, (y - stone_size / 4)),
                    ((x - stone_size / 4), (y + stone_size / 4)),
                    ((x + stone_size / 4), (y + stone_size / 4))
                ],
                fill=fill,
                stroke=fill
            ))

    def _put_cross(self, cell, x, y, fill, stone_size):
        offset = stone_size / 4
        cell.add(
            Line(
                start=((x - offset) * self.unit, (y - offset) * self.unit),
                end=((x + offset) * self.unit, (y + offset) * self.unit),
                fill=fill,
                stroke=fill,
                stroke_width=self._line_width * 3
            )
        )
        cell.add(
            Line(
                start=((x - offset) * self.unit, (y + offset) * self.unit),
                end=((x + offset) * self.unit, (y - offset) * self.unit),
                fill=fill,
                stroke=fill,
                stroke_width=self._line_width * 3
            )
        )

    def _put_circle(self, cell, x, y, fill, stone_size):
        radius = stone_size / 4
        cell.add(Circle(
            (x * self.unit, y * self.unit),
            radius * self.unit,
            fill=fill
        ))

    def _put_square(self, cell, fill, stone_size, x, y):
        half_size = stone_size / 4
        cell.add(Rect(
            ((x - half_size) * self.unit, (y - half_size) * self.unit),
            (2 * half_size * self.unit, 2 * half_size * self.unit),
            fill=fill
        ))

    def _put_label(self, cell, x, y, label: str, fill, stone_size):
        cell.add(
            Text(
                label,
                x=[(x) * self.unit],
                y=[(y + 3 * stone_size / 16) * self.unit],
                stroke=fill,
                fill=fill,
                style=f"font-size: {stone_size / 2 * self.unit};{self.default_style}"
            )
        )

    def _get_dot_points(self, board_size):
        hosi = 4 if board_size >= 13 else 3
        xy = board_size - hosi + 1

        yield (hosi, hosi)
        yield (hosi, xy)
        yield (xy, hosi)
        yield (xy, xy)

        if board_size % 2 == 1:
            center = board_size // 2 + 1
            yield (center, center)

            if board_size >= 19:
                yield (hosi, center)
                yield (center, xy)
                yield (xy, center)
                yield (center, hosi)


