import pygame
from gritty import Grid

# gritty demo
# Copyright 2013 Joe Cross
# This is free software, released under The GNU Lesser General Public License, version 3.
# You are free to use, distribute, and modify pyGrid. If modification is your game,
# it is recommended that you read the GNU LGPL license: http://www.gnu.org/licenses/

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
factor = 0.99
while True:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        break
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            break

    alpha *= factor
    if alpha > 200:
        factor = 0.9
        alpha = 200
    if alpha < 20:
        factor = 1.1
        alpha = 20

    color = list(COLOR_ON)
    color[-1] = int(alpha)
    blink_selection.color = color

    clear()
    draw_grid()
    pygame.display.update()
    pygame.time.delay(5)


pygame.quit()
