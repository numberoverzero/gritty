import pygame
from gritty.demos import basic_grid

# gritty demo
# Copyright 2013 Joe Cross
# This is free software, released under The GNU Lesser General Public License, version 3.
# You are free to use, distribute, and modify pyGrid. If modification is your game,
# it is recommended that you read the GNU LGPL license: http://www.gnu.org/licenses/

caption = "Click and drag to select!"
grid, display, COLOR_OFF, COLOR_ON = basic_grid(caption)

is_dragging = False
origin = None
selection = []


def draw_grid():
    display.get_surface().blit(grid.surface, (0, 0))

constraints = (0, max(grid.rows, grid.columns))


def constrain(value):
    value = min(value, constraints[1])
    value = max(value, constraints[0])
    return value


def minmax(pair):
    min_ = constrain(min(pair))
    max_ = constrain(max(pair))
    return min_, max_


def get_selection((x1, y1)):
    if origin is None:
        return None
    xmin, xmax = minmax((x1, origin[0]))
    ymin, ymax = minmax((y1, origin[1]))
    xslice = slice(xmin, xmax+1, 1)
    yslice = slice(ymin, ymax+1, 1)
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
