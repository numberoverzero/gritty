import pygame
from gritty.demos import basic_grid

# gritty demo
# Copyright 2013 Joe Cross
# This is free software, released under The GNU Lesser General Public License, version 3.
# You are free to use, distribute, and modify pyGrid. If modification is your game,
# it is recommended that you read the GNU LGPL license: http://www.gnu.org/licenses/

caption = "Blink example"
grid, display, COLOR_OFF, COLOR_ON = basic_grid(caption)

background_color = (255, 255, 255)
blink_selection = grid[2:grid.rows:6, 2:grid.columns:6]

# Add some yellow lines for the hell of it
(grid[2::12, :] + grid[:, 2::12]).color = COLOR_ON


def clear():
    display.get_surface().fill(background_color)


def draw_grid():
    display.get_surface().blit(grid.surface, (0, 0))

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
        factor = 0.95
        alpha = 200
    if alpha < 20:
        factor = 1.05
        alpha = 20

    COLOR_OFF[-1] = int(alpha)
    blink_selection.color = COLOR_OFF

    clear()
    draw_grid()
    pygame.display.update()
    pygame.time.delay(5)


pygame.quit()
