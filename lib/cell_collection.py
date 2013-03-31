

class Cell(object):
    def __init__(self, grid, pos):
        self._grid = grid
        self.pos = pos

    def __setattr__(self, name, value):
        if name == '_grid':
            object.__setattr__(self, name, value)
        elif name in self._grid.cell_attr:
            if name in self._grid.cell_attr_coercion_funcs:
                value = self._grid.cell_attr_coercion_funcs[name](value)
            object.__setattr__(self, name, value)
            self._grid.update_cell(self)
        else:
            object.__setattr__(self, name, value)

    def __getattr__(self, name):
        if name == '_grid':
            return object.__getattr__(self, name)
        elif name in self._grid.cell_attr:
            try:
                value = object.__getattr__(self, name)
            except AttributeError:
                value = self._grid.cell_attr[name]
            if name in self._grid.cell_attr_coercion_funcs:
                value = self._grid.cell_attr_coercion_funcs[name](value)
            return value
        else:
            return object.__getattr__(self, name)

    def __str__(self):
        args = list(self.pos) + list(self.color)
        return "Cell({}:{}, {}:{}:{}:{})".format(*args)

    def __repr__(self):
        return str(self)

    def __iter__(self):
        return iter([self])

    def __sub__(self, other):
        return CellCollection(self._grid, self) - other

    def __add__(self, other):
        return CellCollection(self._grid, self) - other


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

    def __str__(self):
        return str(list(self))

    def __repr__(self):
        return str(self)
