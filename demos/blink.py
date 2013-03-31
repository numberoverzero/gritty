import pygame
from gritty.lib.grid import Grid

rows = 9
columns = 9
cell_width = 50
cell_height = 50
COLOR_OFF = [000, 000, 255, 255]
COLOR_ON = [255, 255, 51, 255]

args = [
    rows,
    columns,
    cell_width,
    cell_height
]

kwargs = {
    'cell_color_default': COLOR_OFF,
    'cell_border_color': (000, 000, 000, 255),
    'cell_border_size': 5,
    'cell_radius': 0,
}

grid = Grid(*args, **kwargs)
grid_pos = (0, 0)
pygame.init()
pygame.display.set_caption("Blink example")
screen = pygame.display.set_mode(grid.render_dimensions)
background_color = (255, 255, 255)

blink_selection = grid[1:10:3, 1:10:3]
blink_selection.color = COLOR_ON


def clear():
    screen.fill(background_color)


def draw_grid():
    screen.blit(grid.surface, grid_pos)

alpha = 255
offset = 1
while True:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        break
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            break

    alpha += offset
    if alpha >= 256:
        offset = -1
        alpha = 255
    if alpha <= 0:
        offset = 1
        alpha = 0

    color = list(COLOR_ON)
    color[-1] = alpha
    blink_selection.color = color

    clear()
    draw_grid()
    pygame.display.update()
    pygame.time.delay(5)


pygame.quit()
