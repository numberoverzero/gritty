import pygame
from gritty import Grid

rows = 45
columns = 45
cell_width = 12
cell_height = 12
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
pygame.display.set_caption("Click and drag to select!")
screen = pygame.display.set_mode(grid.render_dimensions)
background_color = (255, 255, 255)
screen.fill(background_color)

is_dragging = False
origin = None
selection = []


def draw_grid():
    screen.blit(grid.surface, grid_pos)


def get_selection((x1, y1)):
    if origin is None:
        return None
    xstep = 1 if origin[0] <= x1 else -1
    ystep = 1 if origin[1] <= y1 else -1
    xslice = slice(origin[0], x1+xstep, xstep)
    yslice = slice(origin[1], y1+ystep, ystep)
    return grid[xslice, yslice]


def update_selection(new_selection):
    global selection
    if selection == new_selection:
        return

    # Turn off cells in the old selection that aren't in the new selection
    (selection - new_selection).color = COLOR_OFF

    # Turn on cells in the new selection that aren't on in the old selection
    (new_selection - selection).color = COLOR_ON

    selection = new_selection


while True:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        break
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            break
    elif event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:  # Left button only
            origin = grid.hit_check(pygame.mouse.get_pos())
            new_selection = get_selection(origin)
            update_selection(new_selection)
            is_dragging = True
    elif event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:  # Left button only
            if is_dragging:
                is_dragging = False
    elif event.type == pygame.MOUSEMOTION:
        if is_dragging:
            bottom_right = grid.hit_check(pygame.mouse.get_pos())
            if bottom_right:
                new_selection = get_selection(bottom_right)
                update_selection(new_selection)

    draw_grid()
    pygame.display.update()
    #pygame.time.delay(29)


pygame.quit()
