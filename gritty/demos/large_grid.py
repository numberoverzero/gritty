import pygame
from gritty.demos import basic_grid
from gritty.color import Color

caption = "Large grid (400x400)"
grid, display, COLOR_OFF, COLOR_ON = basic_grid(caption)

# Reshape grid
grid.rows = 400
grid.columns = 400
grid.cell_width = 2
grid.cell_height = 2
grid.cell_border_size = 0

COLOR_OFF = Color()
COLOR_ON = Color(255, 255, 255)

# Repaint background black
grid.cell_default_color = COLOR_OFF


grid_pos = (0, 0)
selected = (grid.rows/2, grid.columns/2)
grid[selected].color = COLOR_ON

# Resize the display to match the grid
display.set_mode(grid.render_dimensions)

# Preload surface, since first render takes some time
print "Loading grid..."
grid.surface
print "Grid loaded!"


movement = {
    pygame.K_UP: [False, 0, -1],
    pygame.K_DOWN: [False, 0, 1],
    pygame.K_LEFT: [False, -1, 0],
    pygame.K_RIGHT: [False, 1, 0]
}


def draw_grid():
    display.get_surface().blit(grid.surface, grid_pos)


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
    if new_pos[0] >= grid.columns:
        new_pos[0] = 0
    if new_pos[0] < 0:
        new_pos[0] = grid.columns - 1
    if new_pos[1] >= grid.rows:
        new_pos[1] = 0
    if new_pos[1] < 0:
        new_pos[1] = grid.rows - 1
    return new_pos


def update_selected(new_pos):
    global selected
    if not new_pos:
        return
    grid[selected].color = COLOR_OFF
    selected = new_pos
    grid[selected].color = COLOR_ON

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
    #pygame.time.delay(29)


pygame.quit()
