import itertools


class Cell(object):
    def __init__(self, grid, pos):
        self.grid = grid
        self.pos = pos

    @property
    def color(self):
        return self.grid.color_at(self.pos)

    @color.setter
    def color(self, w):
        self.grid.color_at(self.pos, w)


class CellCollection(object):
    def __init__(self, grid, cells=None):
            self.grid = grid
            if cells:
                self.cells = list(cells)

    @property
    def color(self):
        if len(self.cells) > 1:
            raise ValueError("Cannot return a single color for multiple cells")
        return self.grid.get_color_at(self.cells[0])

    @color.setter
    def color(self, c):
        for pos in self.cells:
            self.grid.set_color_at(pos, c)

    def on(self):
        for pos in self.cells:
            self.grid.on(pos)

    def off(self):
        for pos in self.cells:
            self.grid.off(pos)

    def __iter__(self):
        for pair in itertools.product(range(self.rows), range(self.columns)):
            yield pair[::-1]

    def __add__(self, other):
        cells = sorted(set(self.cells + other.cells))
        return CellCollection(self.grid, cells)

    def __sub__(self, other):
        cells = sorted(set(self.cells) - set(other.cells))
        return CellCollection(self.grid, cells)
