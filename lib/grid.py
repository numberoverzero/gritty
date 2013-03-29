import itertools
import pygame
from gritty.padlib import rrect
from cell_collection import CellCollection

DEFAULT_OFF_COLOR = (0, 0, 0, 255)
DEFAULT_ON_COLOR = (255, 255, 255, 255)
DEFAULT_BORDER_COLOR = (0, 0, 0, 255)
DEFAULT_BORDER_SIZE = 0
DEFAULT_CELL_RADIUS = 0


def color_eq(color1, color2):
    if len(color1) != len(color2):
        return False
    for c1, c2 in zip(color1, color2):
        if c1 != c2:
            return False
    return True


class Grid(object):
    def __init__(self, rows, columns, cell_width, cell_height, **kwargs):
        '''
        rows:: the number of rows in the grid
        columns:: the number of columns in the grid

        keyword arguments:
        color_cell_on  :: color used when a cell is set to 'on'
        color_cell_off :: color used when a cell is set to 'off'
        color_border   :: border color for the grid (exterior edges and border between cells)

        border_size    :: thickness of the border
        cell_radius    :: curvature of the cell corners.  Use 0 for square corners
        '''
        self._rows = rows
        self._columns = columns
        self._cells = [None] * rows * columns

        self._color_cell_off = kwargs.get('color_cell_off', DEFAULT_OFF_COLOR)
        self._color_cell_on = kwargs.get('color_cell_on', DEFAULT_ON_COLOR)
        self._color_border = kwargs.get('color_border', DEFAULT_BORDER_COLOR)

        self._border_size = kwargs.get('border_size', DEFAULT_BORDER_SIZE)

        self._cell_radius = kwargs.get('cell_radius', DEFAULT_CELL_RADIUS)
        self._cell_width = cell_width
        self._cell_height = cell_height

        self._dirty = []
        self._surf_cache = pygame.Surface(self._render_dimensions, pygame.SRCALPHA)
        self.all.off()

    def _index(self, pos):
        x, y = pos
        return x + self._columns * y

    @property
    def _render_dimensions(self):
        width = self._columns * self._cell_width + (self._columns + 1) * self._border_size
        height = self._rows * self._cell_height + (self._rows + 1) * self._border_size
        return width, height

    def _cell_rect(self, (x, y)):
        '''Returns the (x, y, width, height) rectangle of the given cell'''
        x = self._border_size * (1 + x) + self._cell_width * x
        y = self._border_size * (1 + y) + self._cell_height * y
        return (x, y, self._cell_width, self._cell_height)

    def _draw_cell(self, surface, pos):
        x, y = pos
        x *= (self._border_size + self._cell_width)
        y *= (self._border_size + self._cell_height)

        #Border
        rect = (x, y,
                self._cell_width + 2 * self._border_size,
                self._cell_height + 2 * self._border_size
                )
        rrect(surface, self._color_border, rect, 0, 0)

        #Cell
        x += self._border_size
        y += self._border_size
        color = self.get_color_at(pos)
        rect = (x, y, self._cell_width, self._cell_height)
        rrect(surface, color, rect, self._cell_radius, 0)

    @property
    def surface(self):
        if self._dirty:
            for pos in self._dirty:
                self._draw_cell(self._surf_cache, pos)
            self._dirty = []
        return self._surf_cache

    def hit_check(self, pos):
        '''Returns the cell pos that contains pos, or None'''
        cell_width, cell_height = self._cell_width, self._cell_height
        width, height = self._render_dimensions
        border_size = self._border_size
        pos_x, pos_y = pos

        if pos_x < 0 or pos_y < 0:
                    return None

        if pos_x > width or pos_y > height:
            return None

        x, rx = divmod(pos_x, cell_width + border_size)
        y, ry = divmod(pos_y, cell_height + border_size)
        if rx <= border_size or ry <= border_size:
            return None
        return x, y

    @property
    def all(self):
        return CellCollection(self, self)

    def on(self, pos):
        self.set_color_at(pos, self._color_cell_on)

    def off(self, pos):
        self.set_color_at(pos, self._color_cell_off)

    def get_color_at(self, pos):
        '''Gets the color at a position'''
        pos = self._index(pos)
        return self._cells[pos]

    def set_color_at(self, pos, value):
        '''Sets the color at a position'''
        index = self._index(pos)
        old_value = self.get_color_at(pos)
        self._cells[index] = tuple(value)
        if not old_value or not color_eq(value, old_value):
            self._dirty.append(pos)

    def __iter__(self):
        for pair in itertools.product(range(self._rows), range(self._columns)):
            yield pair[::-1]

    def __getitem__(self, x, y):
        if isinstance(x, slice):
            xs = range(*x.indices(self._columns))
        else:
            xs = [x]
        if isinstance(y, slice):
            ys = range(*y.indices(self._rows))
        else:
            ys = [y]
        pairs = itertools.product(ys, xs)
        pairs = (tuple(reversed(pair)) for pair in pairs)
        return CellCollection(self, pairs)
