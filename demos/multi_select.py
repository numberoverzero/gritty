import pygame
from gritty.lib.grid import Grid

rows = 45
columns = 45
cell_width = 12
cell_height = 12
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
    'cell_border_size': 3,
    'cell_radius': 5,
}

grid = Grid(*args, **kwargs)
grid_pos = (0, 0)
pygame.init()
pygame.display.set_caption("Click and drag to select!")
screen = pygame.display.set_mode((800, 800))
background_color = (255, 255, 255)

is_dragging = False
origin = None
selection = None


def get_selection((x1, y1)):
    if origin is None:
        return None
    xstep = 1 if origin[0] <= x1 else -1
    ystep = 1 if origin[1] <= y1 else -1
    xslice = slice(origin[0], x1+xstep, xstep)
    yslice = slice(origin[1], y1+ystep, ystep)
    return grid[xslice, yslice]


def clear():
    screen.fill(background_color)


def draw_grid():
    screen.blit(grid.surface, grid_pos)


def update_selection(new_selection):
    global selection
    if selection:
        to_clear = selection - new_selection
        to_clear.color = COLOR_OFF
        to_add = new_selection - to_clear
        to_add.color = COLOR_ON
    else:
        new_selection.color = COLOR_ON
    selection = new_selection


while True:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        break
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            break
    elif event.type == pygame.MOUSEBUTTONDOWN:
        origin = grid.hit_check(pygame.mouse.get_pos())
        # Don't start dragging unless we've actually got a top left
        if origin:
            new_selection = get_selection(origin)
            update_selection(new_selection)
            is_dragging = True

    elif event.type == pygame.MOUSEBUTTONUP:
        if is_dragging:
            is_dragging = False

    if is_dragging:
        bottom_right = grid.hit_check(pygame.mouse.get_pos())
        if bottom_right:
            new_selection = get_selection(bottom_right)
            update_selection(new_selection)

    clear()
    draw_grid()
    pygame.display.update()
    #pygame.time.delay(29)


pygame.quit()
