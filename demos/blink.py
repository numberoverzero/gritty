import pygame
from gritty.lib.grid import Grid

rows = 3
columns = 3
cell_width = 50
cell_height = 50

args = [
    rows,
    columns,
    cell_width,
    cell_height
]

kwargs = {
    'color_cell_on':  (255, 255, 051, 255),
    'color_cell_off': (000, 000, 255, 255),
    'color_border':   (000, 000, 000, 255),
    'border_size': 5,
    'cell_radius': 0,
}

grid = Grid(*args, **kwargs)
grid_pos = (0, 0)
pygame.init()
pygame.display.set_caption("Blink example")
screen = pygame.display.set_mode((400, 400))
background_color = (255, 255, 255)


blink_pos = (1, 1)
grid.on(blink_pos)


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

    color = grid[blink_pos].color
    color[3] = alpha
    grid[blink_pos].color = color

    pygame.display.update()
    pygame.time.delay(5)


pygame.quit()
