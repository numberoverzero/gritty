import pygame
from gritty import Grid


def basic_grid(caption):
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
    pygame.display.set_caption(caption)
    screen = pygame.display.set_mode(grid.render_dimensions)
    background_color = (255, 255, 255)
    screen.fill(background_color)
    return grid, pygame.display, COLOR_OFF, COLOR_ON
