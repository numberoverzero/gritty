import itertools
import pygame
from cell_collection import Cell, CellCollection

DEFAULT_CELL_COLOR = (0, 0, 0, 255)
DEFAULT_BORDER_COLOR = (0, 0, 0, 255)
DEFAULT_BORDER_SIZE = 0
DEFAULT_CELL_RADIUS = 0


class Grid(object):
    def __init__(self, rows, columns, cell_width, cell_height, **kwargs):
        '''
        rows:: the number of rows in the grid
        columns:: the number of columns in the grid

        keyword arguments are split into Global attributes and Cell attributes.

        Global attributes are features applicable to the grid as a whole, or apply to every cell.
        Adding, removing, or updating global attributes will force a redraw of the grid.

        Cell attributes are features whose value can change per-cell.
        Adding, removing, or updating a cell attribute will force a redraw of that cell.
        Changing a cell attribute default will force a redraw of the grid.

        GLOBAL
        cell_width         :: width in pixels of a cell
        cell_height        :: height in pixels of a cell
        cell_border_size   :: thickness in pixels of the border

        CELL
        cell_color_default :: default color a cell is rendered with
        cell_radius        :: curvature of the cell corners.  Use 0 for square corners
        border_color       :: border color for the grid (exterior edges and border between cells)
        '''
        self._rows = rows
        self._columns = columns

        self._global_attributes = {
            'cell_width': cell_width,
            'cell_height': cell_height,
            'cell_border_size': kwargs.get('cell_border_size', DEFAULT_BORDER_SIZE)
        }

        self._cell_attributes = {
            'color': kwargs.get('cell_color_default', DEFAULT_CELL_COLOR),
            'radius': kwargs.get('cell_radius', DEFAULT_CELL_RADIUS),
            'border_color': kwargs.get('cell_border_color', DEFAULT_BORDER_COLOR)
        }

        self._cells = {}
        self._dirty = []
        self._surf_cache = pygame.Surface(self.render_dimensions, pygame.SRCALPHA)
        self._forced_redraw = False
        self.force_redraw()

    @property
    def render_dimensions(self):
        cell_width = self.get_global_attribute('cell_width')
        cell_height = self.get_global_attribute('cell_height')
        border_size = self.get_global_attribute('cell_border_size')
        width = self._columns * cell_width + (self._columns + 1) * border_size
        height = self._rows * cell_height + (self._rows + 1) * border_size
        return width, height

    @property
    def surface(self):
        if self._dirty:
            self._forced_redraw = False
            for cell in self._dirty:
                cell.draw(self._surf_cache)
            self._dirty = []
        return self._surf_cache

    def hit_check(self, pos):
        '''Returns the cell pos that contains pos, or None'''
        cell_width, cell_height = self._cell_width, self._cell_height
        width, height = self.render_dimensions
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

    def update_cell(self, cell):
        self._cells[cell.pos] = cell
        self._dirty.append(cell)

    def force_redraw(self):
        if not self._forced_redraw:
            for cell in self:
                self.update_cell(cell)

    def cell_at(self, pos):
        return self._cells.get(pos, Cell(self, pos, self._cell_attributes))

    def set_cell_attribute_default(self, name, default):
        self._cell_attributes[name] = default
        self.force_redraw()

    def get_cell_attribute_default(self, name):
        return self._cell_attributes[name]

    def has_cell_attribute(self, name):
        return name in self._cell_attributes

    def set_global_attribute(self, name, value):
        self._global_attributes[name] = value
        self.force_redraw()

    def get_global_attribute(self, name):
        return self._global_attributes[name]

    def del_global_attribute(self, name):
        del self._global_attributes[name]
        self.force_redraw()

    def __iter__(self):
        for revpos in itertools.product(range(self._rows), range(self._columns)):
            yield self.cell_at(revpos[::-1])

    def __getitem__(self, (x, y)):
        if isinstance(x, slice):
            xs = range(*x.indices(self._columns))
        else:
            xs = [x]
        if isinstance(y, slice):
            ys = range(*y.indices(self._rows))
        else:
            ys = [y]
        pairs = (pos[::-1] for pos in itertools.product(ys, xs))
        cells = map(self.cell_at, pairs)
        return CellCollection(self, cells)
