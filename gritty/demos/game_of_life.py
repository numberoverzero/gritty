import pygame
import itertools
from gritty import Grid, CellCollection

# gritty demo
# Copyright 2013 Joe Cross
# This is free software, released under The GNU Lesser General Public License, version 3.
# You are free to use, distribute, and modify pyGrid. If modification is your game,
# it is recommended that you read the GNU LGPL license: http://www.gnu.org/licenses/

rows = 30
columns = 30
cell_width = 20
cell_height = 20
COLOR_OFF = (000, 000, 255)
COLOR_ON = (255, 255, 51)

args = [
    rows,
    columns,
    cell_width,
    cell_height
]

kwargs = {
    'cell_color_default': COLOR_OFF,
    'cell_border_color': (000, 000, 000),
    'cell_border_size': 3,
    'cell_radius': 0,
}

grid = Grid(*args, **kwargs)
grid_pos = (0, 0)
pygame.init()
pygame.display.set_caption("Click and drag to select!")
screen = pygame.display.set_mode(grid.render_dimensions)
background_color = (255, 255, 255)
screen.fill(background_color)

paused = True

# Initialize the grid used to calc the next iteration
copy_grid = [False] * rows * columns


def wrap(val, L1, L2):
    """Returns the wrapped integer in [min(L1, L2), max(L1, L2)]"""
    low, high = min(L1, L2), max(L1, L2)
    nlow = -low
    return ((val + nlow) % (high + nlow)) - nlow


def update_cell_color(value, cell):
    cell.color = COLOR_ON if value else COLOR_OFF
    return value


grid.cell_attr['alive'] = False
grid.cell_attr_coercion_funcs['alive'] = update_cell_color

offsets = list(itertools.product([-1, 0, 1], [-1, 0, 1]))
offsets.remove((0, 0))


def update_cell(pos):
    global copy_grid
    x, y = pos
    neighbors = []
    for xo, yo in offsets:
        neighbor_x = wrap(x + xo, 0, rows)
        neighbor_y = wrap(y + yo, 0, columns)
        neighbors.append((neighbor_x, neighbor_y))
    count = sum(int(grid[pos].alive) for pos in neighbors)
    if grid[pos].alive:
        if count < 2:
            copy_grid[x + columns * y] = False
        elif count > 3:
            copy_grid[x + columns * y] = False
        else:
            copy_grid[x + columns * y] = True
    elif count == 3:
        copy_grid[x + columns * y] = True


def update_grid():
    for x in range(columns):
        for y in range(rows):
            update_cell((x, y))


def apply_grid():
    for x in range(columns):
        for y in range(rows):
            grid[x, y].alive = copy_grid[x + columns * y]


def draw_grid():
    screen.blit(grid.surface, grid_pos)


while True:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        break
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            break
        elif event.key == pygame.K_p:
            paused = not paused
    elif event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:  # Left button only
            if paused:
                cell = grid[grid.hit_check(pygame.mouse.get_pos())]
                cell.alive = not cell.alive
    if not paused:
        update_grid()
        apply_grid()

    draw_grid()
    pygame.display.update()


pygame.quit()
