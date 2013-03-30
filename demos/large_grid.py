import pygame
from gritty.lib.grid import Grid

rows = 400
columns = 400
cell_width = 2
cell_height = 2
COLOR_OFF = (000, 000, 255)
COLOR_ON = (255, 255, 051)

args = [
    rows,
    columns,
    cell_width,
    cell_height
]

kwargs = {
    'cell_color_default': COLOR_OFF,
    'cell_border_color': (000, 000, 000),
    'cell_border_size': 0,
    'cell_radius': 0,
}

grid = Grid(*args, **kwargs)
grid_pos = (0, 0)
pygame.init()
pygame.display.set_caption("Large grid (400x400)")
screen = pygame.display.set_mode((800, 800))
background_color = (255, 255, 255)


selected = (rows/2, columns/2)
grid[selected].color = COLOR_ON

movement = {
    pygame.K_UP: [False, 0, -1],
    pygame.K_DOWN: [False, 0, 1],
    pygame.K_LEFT: [False, -1, 0],
    pygame.K_RIGHT: [False, 1, 0]
}


def clear():
    screen.fill(background_color)


def draw_grid():
    screen.blit(grid.surface, grid_pos)


def move():
    ox, oy = 0, 0
    for key, (toggle, mox, moy) in movement.iteritems():
        if toggle:
            ox += mox
            oy += moy
    if ox == oy == 0:
        return None
    return wrap(selected, (ox, oy))


def wrap((x, y), (ox, oy)):
    new_pos = [x + ox, y + oy]
    if new_pos[0] >= columns:
        new_pos[0] = 0
    if new_pos[0] < 0:
        new_pos[0] = columns - 1
    if new_pos[1] >= rows:
        new_pos[1] = 0
    if new_pos[1] < 0:
        new_pos[1] = rows - 1
    return new_pos


def update_selected(new_pos):
    global selected
    grid[selected].color = COLOR_OFF
    selected = new_pos
    grid[selected].color = COLOR_ON

while True:
    new_pos = None
    clear()
    draw_grid()

    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        break
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            break
        if event.key in movement:
            movement[event.key][0] = True
    elif event.type == pygame.KEYUP:
        if event.key in movement:
            movement[event.key][0] = False

    new_pos = new_pos or move()
    if new_pos:
        update_selected(new_pos)
    pygame.display.update()
    #pygame.time.delay(29)


pygame.quit()
