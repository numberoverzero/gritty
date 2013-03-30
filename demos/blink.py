import pygame
from gritty.lib.grid import Grid

rows = 9
columns = 9
cell_width = 50
cell_height = 50
COLOR_OFF = [000, 000, 255, 255]
COLOR_ON = [255, 255, 051, 255]

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
screen = pygame.display.set_mode((500, 500))
background_color = (255, 255, 255)


blink = (slice(1, 10, 3), slice(1, 10, 3))
grid[blink].color = COLOR_ON


def clear():
    screen.fill(background_color)


def draw_grid():
    screen.blit(grid.surface, grid_pos)

alpha = 255
offset = 1
while True:
    clear()
    draw_grid()

    event = pygame.event.poll()
    if event.type == pygame.QUIT:
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
    grid[blink].color = color

    pygame.display.update()
    pygame.time.delay(5)


pygame.quit()
