import pygame
from gritty.lib.grid import Grid

rows = 20
columns = 20
cell_width = 20
cell_height = 20

args = [
    rows,
    columns,
    cell_width,
    cell_height
]

kwargs = {
    'color_cell_on':  (255, 255, 051),
    'color_cell_off': (000, 000, 255),
    'color_border':   (000, 000, 000),
    'border_size': 5,
    'cell_radius': 0,
}

grid = Grid(*args, **kwargs)
grid_pos = (0, 0)
pygame.init()
pygame.display.set_caption("Select example")
screen = pygame.display.set_mode((800, 800))
background_color = (255, 255, 255)


selected = (rows/2, columns/2)
grid.on(selected)

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
    grid.off(selected)
    selected = new_pos
    grid.on(selected)

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
    elif event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        new_pos = grid.hit_check(pos)

    new_pos = new_pos or move()
    if new_pos:
        grid.off(selected)
        selected = new_pos
        grid.on(selected)
        new_pos = None
    pygame.display.update()
    pygame.time.delay(20)


pygame.quit()
