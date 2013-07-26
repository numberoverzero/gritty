import pygame
import itertools
from gritty.demos import basic_grid


caption = "Click to toggle, space to pause/resume"
grid, display, COLOR_OFF, COLOR_ON = basic_grid(caption)

paused = True
dimensions = grid.rows * grid.columns
active_grid, buffer_grid = [False] * dimensions, [False] * dimensions
index = lambda x, y: x + grid.columns * y
initial = [
    (11, 15),
    (12, 15),
    (12, 16),
    (16, 16),
    (17, 16),
    (18, 16),
    (17, 14),
]


def alive_to_color(value, cell):
    cell.color = COLOR_ON if value else COLOR_OFF
    return value

grid.cell_attr['alive'] = False
grid.cell_attr_coercion_funcs['alive'] = alive_to_color

for x, y in initial:
    grid[x, y].alive = active_grid[index(x, y)] = True


def wrap(val, L1, L2):
    """Returns the wrapped integer in [min(L1, L2), max(L1, L2)]"""
    low, high = min(L1, L2), max(L1, L2)
    nlow = -low
    return ((val + nlow) % (high + nlow)) - nlow


cells = list(itertools.product(xrange(grid.rows), xrange(grid.columns)))
offsets = list(itertools.product([-1, 0, 1], [-1, 0, 1]))
offsets.remove((0, 0))


def update_cell((x, y)):
    global buffer_grid
    count = 0
    for xo, yo in offsets:
        nx = wrap(x + xo, 0, grid.rows)
        ny = wrap(y + yo, 0, grid.columns)
        count += active_grid[nx + grid.columns * ny]
    alive = active_grid[index(x, y)]
    if alive:
        if count < 2 or count > 3:
            buffer_grid[index(x, y)] = False
        else:
            buffer_grid[index(x, y)] = True
    else:
        if count == 3:
            buffer_grid[index(x, y)] = True
        else:
            buffer_grid[index(x, y)] = False


def calculate_next_frame():
    for x, y in cells:
        update_cell((x, y))


def flip_frames():
    global buffer_grid, active_grid
    tmp = active_grid
    active_grid = buffer_grid
    buffer_grid = tmp


def apply_grid():
    for x, y in cells:
        grid[x, y].alive = active_grid[index(x, y)]


def draw_grid():
    display.get_surface().blit(grid.surface, (0, 0))


while True:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        break
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            break
        elif event.key == pygame.K_SPACE:
            paused = not paused
    elif event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:  # Left button only
            if paused:
                x, y = grid.hit_check(pygame.mouse.get_pos())
                active_grid[index(x, y)] = not active_grid[index(x, y)]
                grid[x, y].alive = active_grid[index(x, y)]

    if not paused:
        calculate_next_frame()
        flip_frames()
        apply_grid()

    draw_grid()
    pygame.display.update()


pygame.quit()
