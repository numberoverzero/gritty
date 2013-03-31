import pygame
from gritty import Grid

# gritty demo
# Copyright 2013 Joe Cross
# This is free software, released under The GNU Lesser General Public License, version 3.
# You are free to use, distribute, and modify pyGrid. If modification is your game,
# it is recommended that you read the GNU LGPL license: http://www.gnu.org/licenses/


def basic_grid():
    rows = 41
    columns = 41
    cell_width = 20
    cell_height = 20
    COLOR_OFF = [000, 000, 255]
    COLOR_ON = [255, 255, 51]

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
        'cell_radius': 0,
    }

    grid = Grid(*args, **kwargs)
    pygame.init()
    pygame.display.set_caption("Click to toggle, space to pause/resume")
    screen = pygame.display.set_mode(grid.render_dimensions)
    background_color = (255, 255, 255)
    screen.fill(background_color)
    return grid, screen, COLOR_OFF, COLOR_ON
