import itertools


class CellCollection(object):
    def __init__(self, grid, cells=None):
            self.grid = grid
            if cells:
                self.cells = list(cells)

    @property
    def color(self):
        if len(self.cells) > 1:
            raise ValueError("Cannot return a single color for multiple cells")
        return self.grid.get_attr_at('color', self.cells[0])

    @color.setter
    def color(self, c):
        for pos in self.cells:
            self.grid.set_attr_at('color', pos, c)

    def __iter__(self):
        for pair in itertools.product(range(self.rows), range(self.columns)):
            yield pair[::-1]

    def __add__(self, other):
        cells = sorted(set(self.cells + other.cells))
        return CellCollection(self.grid, cells)

    def __sub__(self, other):
        cells = sorted(set(self.cells) - set(other.cells))
        return CellCollection(self.grid, cells)
