from fpdf import FPDF

from sgftools.game import Stone, Label


class ProblemsPdfWriter:
    @property
    def working_width(self):
        return self._pdf.w - 2 * self.margin

    @property
    def board_width(self):
        return (self.working_width - 2 * self.board_indent)/2

    @property
    def working_height(self):
        return self._pdf.h - 2 * self.margin

    def __init__(self,  trim_board=True, draw_diagram_caption=True):
        self.label_font_size = 5
        self.font_size = 8
        self.margin = 18
        self.board_indent = 5
        self.font_name = 'Arial'
        self.trim_board = trim_board
        self.draw_diagram_caption = draw_diagram_caption
        self.caption_height = 6
        self.problem_num = 1

        self._curr_x = self.margin
        self._curr_y = self.margin
        self._pdf = FPDF('P', 'mm')
        self._pdf.set_auto_page_break(False)
        self._pdf.add_page()
        self._add_pagenum(self._pdf)

    def add_diagrams(self, boards):
        for board in boards:
            self.draw_board(board, self._pdf)
            self._move_y(self.board_indent)
            self.problem_num += 1

    def save(self, output_file_name):
        self._pdf.output(output_file_name, 'F')

    def _move_y(self, height):
        self._curr_y += height
        self._ensure_height(0)

    def _next_column(self):
        self._curr_x = self._curr_x + self.board_width + 2 * self.board_indent
        if self._curr_x + self.board_width > self.working_width + self.margin:
            self._curr_x = self.margin
            self._curr_y = self.margin
            self._pdf.add_page()
            self._add_pagenum(self._pdf)

    def _ensure_height(self, height):
        if self._curr_y + height > self.working_height + self.margin:
            self._curr_y = self.margin
            self._next_column()

    def _add_pagenum(self, pdf):
        pdf.set_font(self.font_name, '', self.font_size)
        pdf.set_text_color(0)
        pdf.set_xy(self.margin, self.margin / 4)
        pdf.cell(pdf.w - 2 * self.margin, self.margin/2, "{}".format(pdf.page_no()), 0, 0, 'C')
        pdf.set_xy(0, 0)

    def _get_last_line_to_draw(self, board):
        if not self.trim_board:
            return board.size

        for y in reversed(range(1, board.size + 1)):
            if any(not board[x, y].is_empty() for x in range(1, board.size + 1)):
                return y
        return 1

    def draw_board(self, board, pdf):
        pdf.set_font(self.font_name, '', self.label_font_size)
        pdf.set_draw_color(0)
        cell_size = self.board_width / board.size

        self._move_y(cell_size/2)

        last_line_to_draw = self._get_last_line_to_draw(board)
        coeff = 0.6 if (last_line_to_draw < board.size) else 0
        board_line_height = cell_size * (last_line_to_draw - 1 + coeff)
        board_height = board_line_height + cell_size * (0 if (last_line_to_draw < board.size) else 0.5)
        self._ensure_height(board_height + (self.caption_height if self.draw_diagram_caption else 0))

        # draw grid
        for i in range(0, board.size):
            step_size = i * cell_size
            pdf.line(self._curr_x + step_size, self._curr_y, self._curr_x + step_size,
                     self._curr_y + board_line_height)

        for i in range(0, last_line_to_draw):
            step_size = i * cell_size
            pdf.line(self._curr_x, self._curr_y + step_size, self._curr_x + cell_size * (board.size - 1),
                     self._curr_y + step_size)

        # draw nodes
        for x in range(1, board.size + 1):
            for y in range(1, last_line_to_draw + 1):
                node = board[x, y]
                if node.is_empty():
                    continue

                myx = self._curr_x + (x - 1) * cell_size
                myy = self._curr_y + (y - 1) * cell_size
                self.draw_node(myx, myy, cell_size, node, pdf)

        self._move_y(board_height)
        if self.draw_diagram_caption:
            self._draw_caption(pdf)

    def draw_node(self, myx, myy, cell_size, node, pdf):
        radius = cell_size / 2 - 0.05
        text_color = 0
        fill_color = 255
        if node.stone == Stone.Black:
            fill_color = 0
            text_color = 255
        pdf.set_text_color(text_color)
        pdf.set_fill_color(fill_color)
        if node.stone is not None:
            pdf.ellipse(myx - radius, myy - radius, 2 * radius, 2 * radius, 'F')
            pdf.set_fill_color(0)
            pdf.ellipse(myx - radius, myy - radius, 2 * radius, 2 * radius, '')

        if isinstance(node.marker, Label):
            text = str(node.marker)
            if len(text) <= 2:
                pdf.set_xy(myx - cell_size/2, myy - cell_size/2)
                pdf.cell(cell_size, cell_size, text, 0, 0, 'C')

    def _draw_caption(self, pdf):
        pdf.set_font(self.font_name, '', self.font_size)
        pdf.set_text_color(0)
        pdf.set_xy(self._curr_x, self._curr_y)

        pdf.cell(self.board_width, self.caption_height, "Problem {}".format(self.problem_num), 0, 0, 'C')
        self._move_y(self.caption_height)
