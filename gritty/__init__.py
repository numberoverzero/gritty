import itertools
import pygame
from padlib import rrect
from gritty.color import Color

DEFAULT_CELL_COLOR = Color(0, 0, 0, 255)
DEFAULT_BORDER_COLOR = Color(255, 255, 255, 255)
DEFAULT_BORDER_SIZE = 0
DEFAULT_CELL_RADIUS = 0


class Grid(object):
    def __init__(self, rows, columns, cell_width, cell_height, **kwargs):
        '''
        rows:: the number of rows in the grid
        columns:: the number of columns in the grid

        cell_width         :: width in pixels of a cell
        cell_height        :: height in pixels of a cell

        cell_radius        :: curvature of the cell corners.  Use 0 for square corners
        cell_border_size   :: thickness in pixels of the border
        cell_border_color  :: border color for the grid (exterior edges and border between cells)
        cell_default_color :: default colorof a cell (this value is used when calling cell.off)

        Updating any of these attributes will force a redraw of the entire grid.
        '''

        self._rows = rows
        self._columns = columns

        self._cell_width = cell_width
        self._cell_height = cell_height

        self._cell_radius = kwargs.get('cell_radius', DEFAULT_CELL_RADIUS)
        self._cell_border_size = kwargs.get('cell_border_size', DEFAULT_BORDER_SIZE)
        self._cell_border_color = kwargs.get('cell_border_color', DEFAULT_BORDER_COLOR)
        self._cell_default_color = kwargs.get('cell_default_color', DEFAULT_CELL_COLOR)

        self._cells = {}
        self._dirty = []
        self.force_redraw()
        self.surface  # Accessing the surface to cache it

    @property
    def render_dimensions(self):
        width = self._columns * self.cell_width + (self._columns + 1) * self.cell_border_size
        height = self._rows * self.cell_height + (self._rows + 1) * self.cell_border_size
        return width, height

    @property
    def surface(self):
        if self._forced_redraw:
            self._surf_cache = pygame.Surface(self.render_dimensions, pygame.SRCALPHA)
            dirty = self
        elif self._dirty:
            dirty = self._dirty
        else:
            dirty = []

        map(lambda c: self._draw_cell(c), dirty)
        self._forced_redraw = False
        self._dirty = []
        return self._surf_cache

    def _draw_cell(self, cell, surface=None):
        surface = surface or self._surf_cache
        rect = self.cell_rect(cell.pos)

        #Border
        rrect(surface, self._cell_border_color, rect, 0, self.cell_border_size)

        #Cell
        rrect(surface, cell.color, rect, self._cell_radius, 0)

    @property
    def rows(self):
        return self._rows

    @rows.setter
    def rows(self, value):
        self._rows = value
        self.force_redraw()
        # TODO: Delete cells outside the new bounds

    @property
    def columns(self):
        return self._columns

    @columns.setter
    def columns(self, value):
        self._columns = value
        self.force_redraw()
        # TODO: Delete cells outside the new bounds

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
    def cell_radius(self):
        return self._cell_radius

    @cell_radius.setter
    def cell_radius(self, value):
        self._cell_radius = value
        self.force_redraw()

    @property
    def cell_border_size(self):
        return self._cell_border_size

    @cell_border_size.setter
    def cell_border_size(self, value):
        self._cell_border_size = value
        self.force_redraw()

    @property
    def cell_border_color(self):
        return self._cell_border_color

    @cell_border_color.setter
    def cell_border_color(self, value):
        self._cell_border_color = value
        self.force_redraw()

    @property
    def cell_default_color(self):
        return self._cell_default_color

    @cell_default_color.setter
    def cell_default_color(self, value):
        self._cell_default_color = value
        self.force_redraw()

    def hit_check(self, pos, use_nearest=True, clip_to_render=False):
        '''
        Returns the cell pos that contains pos.
        If use_nearest, returns the closest pos to the target.
        Otherwise, returns None when a cell is not exactly clicked.

        If clip_to_render, returns None when the position is outside of the rendered area.
        This setting has no effect when use_nearest is False.
        '''
        grid_width, grid_height = self.render_dimensions
        pos_x, pos_y = pos

        if pos_x < 0 or pos_y < 0:
            if clip_to_render or not use_nearest:
                return None

        if pos_x > grid_width or pos_y > grid_height:
            if clip_to_render or not use_nearest:
                return None

        cell_width, cell_height = self.cell_width, self.cell_height
        border = self.cell_border_size

        x, rx = divmod(pos_x, cell_width + border)
        y, ry = divmod(pos_y, cell_height + border)
        if rx <= border or ry <= border:
            if use_nearest:
                if rx < border:
                    x -= rx < border/2
                if ry < border:
                    y -= ry < border/2
            else:
                return None
        return [x, y]

    def update_cell(self, cell):
        self._cells[cell.pos] = cell
        self._dirty.append(cell)

    def reset(self):
        self._cells = {}
        self.force_redraw()

    def force_redraw(self):
        self._forced_redraw = True

    def cell_at(self, pos):
        # This could just be self._cells.get(pos, ...)
        # but that fully generates the cell, which includes a bunch of work.
        if pos in self._cells:
            return self._cells[pos]
        return Cell(self, pos, Color(self.cell_default_color))

    def cell_rect(self, pos):
        '''Returns the (x, y, width, height) rectangle of the given cell'''
        border_size = self.cell_border_size
        width = self.cell_width
        height = self.cell_height
        x, y = pos
        x = border_size * (1 + x) + width * x
        y = border_size * (1 + y) + height * y
        return [x, y, width, height]

    def __iter__(self):
        for revpos in itertools.product(range(self._rows), range(self._columns)):
            yield self.cell_at(revpos[::-1])

    def __getitem__(self, (x, y)):
        if isinstance(x, slice):
            xs = range(*x.indices(self.rows))
        else:
            xs = [x]
        if isinstance(y, slice):
            ys = range(*y.indices(self.rows))
        else:
            ys = [y]
        pairs = (pos[::-1] for pos in itertools.product(ys, xs))
        cells = map(self.cell_at, pairs)
        if len(cells) == 1:
            return cells[0]
        return CellCollection(self, cells)


class Cell(object):
    __slots__ = ['_grid', '_pos', '_color']

    def __init__(self, grid, pos, color):
        self._grid = grid
        self._pos = pos
        self._color = color

    @property
    def pos(self):
        return list(self._pos)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value
        self._grid.update_cell(self)

    def __str__(self):
        return "Cell({}, [{}, {}], {})".format(self._grid, self.pos[0], self.pos[1], self.color)

    def __repr__(self):
        return str(self)

    def __iter__(self):
        return iter([self])

    @property
    def _as_collection(self):
        return CellCollection(self._grid, self)

    def __sub__(self, other):
        return self._as_collection - other

    def __add__(self, other):
        return self._as_collection - other

    def __rsub__(self, other):
        return other - self._as_collection

    def __radd__(self, other):
        return other + self._as_collection


class CellCollection(object):
    def __init__(self, grid, cells=None):
        self._grid = grid
        self._cells = cells or []

    def __getattr__(self, name):
        if name in ['_grid', '_cells']:
            return object.__getattr__(self, name)
        get = lambda c: getattr(c, name)
        return map(get, self._cells)

    def __setattr__(self, name, value):
        if name in ['_grid', '_cells']:
            object.__setattr__(self, name, value)
        else:
            set = lambda c: setattr(c, name, value)
            map(set, self._cells)

    def __iter__(self):
        return iter(self._cells)

    def __add__(self, other):
        #Use cell position instead of object in case one of the lists updated a cell value
        positions = set([c.pos for c in self] + [c.pos for c in other])
        cells = [self._grid.cell_at(pos) for pos in positions]
        return CellCollection(self._grid, cells)

    def __sub__(self, other):
        #Use cell position instead of object in case one of the lists updated a cell value
        positions = set(c.pos for c in self) - set(c.pos for c in other)
        cells = [self._grid.cell_at(pos) for pos in set(positions)]
        return CellCollection(self._grid, cells)

    def __rsub__(self, other):
        return CellCollection(self._grid, other) - self

    def __radd__(self, other):
        return CellCollection(self._grid, other) + self

    def __iadd__(self, other):
        positions = set([c.pos for c in self] + [c.pos for c in other])
        self._cells = [self._grid.cell_at(pos) for pos in positions]
        return self

    def __str__(self):
        return str(list(self))

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return set(c.pos for c in self) == set(c.pos for c in other)
