from gritty.padlib import rrect


class Cell(object):
    def __init__(self, grid, pos, attrs):
        self.grid = grid
        self.pos = pos
        for name, value in attrs.iteritems():
            setattr(self, name, value)

    @property
    def _rect(self):
        '''Returns the (x, y, width, height) rectangle of the given cell'''
        border_size = self.grid.cell_border_size
        width = self.grid.cell_width
        height = self.grid.cell_height
        x, y = self.pos
        x = border_size * (1 + x) + width * x
        y = border_size * (1 + y) + height * y
        return [x, y, width, height]

    def draw(self, surface):
        border_size = self.grid.cell_border_size
        border_color = self.border_color

        #Border
        border_rect = self._rect
        border_rect[0] -= border_size
        border_rect[1] -= border_size
        border_rect[2] += 2 * border_size
        border_rect[3] += 2 * border_size
        rrect(surface, border_color, border_rect, 0, 0)

        #Cell
        color = self.color
        rect = self._rect
        rrect(surface, color, rect, self.radius, 0)

    def __setattr__(self, name, value):
        if name == 'grid':
            object.__setattr__(self, name, value)
        elif self.grid.has_cell_attr(name):
            object.__setattr__(self, name, value)
            self.grid.update_cell(self)
        else:
            object.__setattr__(self, name, value)

    def __str__(self):
        return "Cell({}, {})".format(self.pos, self.color)

    def __repr__(self):
        return str(self)


class CellCollection(object):
    def __init__(self, grid, cells=None):
        self._grid = grid
        if cells:
            self._cells = cells
        else:
            self._cells = []

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
        return self._cells

    def __add__(self, other):
        #Use cell position instead of object in case one of the lists updated a cell value
        positions = set([c.pos for c in self] + [c.pos for c in other])
        cells = [self.grid.cell_at(pos) for pos in positions]
        return CellCollection(self._grid, cells)

    def __sub__(self, other):
        #Use cell position instead of object in case one of the lists updated a cell value
        positions = set(c.pos for c in self) - set(c.pos for c in other)
        cells = [self.grid.cell_at(pos) for pos in set(positions)]
        return CellCollection(self._grid, cells)
