import itertools
import pygame
from cell_collection import Cell, CellCollection
from notify_dict import NotifiableDict

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

        self._cell_width = cell_width
        self._cell_height = cell_height
        self._cell_border_size = kwargs.get('cell_border_size', DEFAULT_BORDER_SIZE)

        self.cell_attr = NotifiableDict(
            {'color': kwargs.get('cell_color_default', DEFAULT_CELL_COLOR),
             'radius': kwargs.get('cell_radius', DEFAULT_CELL_RADIUS),
             'border_color': kwargs.get('cell_border_color', DEFAULT_BORDER_COLOR)
             }
        )
        self.cell_attr.set_notify_func(lambda *a, **kw: self.force_redraw())

        self._cells = {}
        self._dirty = []
        self.force_redraw()
        self.surface

    @property
    def render_dimensions(self):
        width = self._columns * self.cell_width + (self._columns + 1) * self.cell_border_size
        height = self._rows * self.cell_height + (self._rows + 1) * self.cell_border_size
        return width, height

    @property
    def surface(self):
        if self._forced_redraw:
            self._surf_cache = pygame.Surface(self.render_dimensions, pygame.SRCALPHA)
            self._forced_redraw = False
            self._dirty = []
            for cell in self:
                cell.draw(self._surf_cache)
        elif self._dirty:
            for cell in self._dirty:
                cell.draw(self._surf_cache)
            self._dirty = []
        return self._surf_cache

    @property
    def cell_width(self):
        return self._cell_width

    @cell_width.setter
    def cell_width(self, value):
        self._cell_width = value
        self.force_redraw()

    @property
    def cell_height(self):
        return self._cell_height

    @cell_height.setter
    def cell_height(self, value):
        self._cell_height = value
        self.force_redraw()

    @property
    def cell_border_size(self):
        return self._cell_border_size

    @cell_border_size.setter
    def cell_border_size(self, value):
        self._cell_border_size = value
        self.force_redraw()

    def hit_check(self, pos):
        '''Returns the cell pos that contains pos, or None'''
        grid_width, grid_height = self.render_dimensions
        pos_x, pos_y = pos

        if pos_x < 0 or pos_y < 0:
            return None

        if pos_x > grid_width or pos_y > grid_height:
            return None

        cell_width, cell_height = self.cell_width, self.cell_height
        border = self.cell_border_size

        x, rx = divmod(pos_x, cell_width + border)
        y, ry = divmod(pos_y, cell_height + border)
        if rx <= border or ry <= border:
            return None
        return x, y

    def update_cell(self, cell):
        self._cells[cell.pos] = cell
        self._dirty.append(cell)

    def force_redraw(self):
        self._forced_redraw = True

    def cell_at(self, pos):
        return self._cells.get(pos, Cell(self, pos, self.cell_attr))

    def set_cell_attr(self, name, value):
        self._cell_attributes[name] = value
        self.force_redraw()

    def get_cell_attr(self, name):
        return self._cell_attributes[name]

    def has_cell_attr(self, name):
        return name in self._cell_attributes

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
