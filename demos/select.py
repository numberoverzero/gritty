import pygame
from Gritty import Grid

rows = 20
columns = 20
cell_width = 25
cell_height = 25
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
    'cell_radius': 5,
}

grid = Grid(*args, **kwargs)
grid_pos = (0, 0)
pygame.init()
pygame.display.set_caption("Select example")
screen = pygame.display.set_mode(grid.render_dimensions)
background_color = (255, 255, 255)
screen.fill(background_color)

selected = (rows/2, columns/2)
grid[selected].color = COLOR_ON

movement = {
    pygame.K_UP: [False, 0, -1],
    pygame.K_DOWN: [False, 0, 1],
    pygame.K_LEFT: [False, -1, 0],
    pygame.K_RIGHT: [False, 1, 0]
}


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
    if not new_pos:
        return
    grid[selected].color = COLOR_OFF
    selected = new_pos
    grid[selected].color = COLOR_ON
    print grid[selected]

while True:
    new_pos = None

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

    update_selected(new_pos or move())
    draw_grid()
    pygame.display.update()
    pygame.time.delay(29)


pygame.quit()
