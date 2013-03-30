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
selection = None


def calc_rect((x0, y0), (x1, y1)):
    return min(x0, x1), max(x0, x1), min(y0, y1), max(y0, y1)


def clear():
    screen.fill(background_color)


def draw_grid():
    screen.blit(grid.surface, grid_pos)


def update_selection(new_selection):
    global selection
    if selection:
        xmin, xmax, ymin, ymax = selection
        grid[xmin:xmax+1, ymin:ymax+1].color = COLOR_OFF
    selection = new_selection
    if selection:
        xmin, xmax, ymin, ymax = selection
        grid[xmin:xmax+1, ymin:ymax+1].color = COLOR_ON


while True:

    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        break
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            break
    elif event.type == pygame.MOUSEBUTTONDOWN:
        if not is_dragging:
            top_left = grid.hit_check(pygame.mouse.get_pos())
            # Don't start dragging unless we've actually got a top left
            if top_left:
                is_dragging = True
                x, y = top_left
                new_selection = ((x, x, y, y))
                update_selection(new_selection)

    elif event.type == pygame.MOUSEBUTTONUP:
        if is_dragging:
            is_dragging = False

    if is_dragging:
        bottom_right = grid.hit_check(pygame.mouse.get_pos())
        if bottom_right:
            # Basic selection - can't select backwards
            if bottom_right[0] >= selection[0] or bottom_right[1] >= selection[2]:
                if bottom_right[0] < selection[0]:
                    bottom_right[0] = selection[0]
                if bottom_right[1] < selection[2]:
                    bottom_right[1] = selection[2]
                new_selection = calc_rect((selection[0], selection[2]), bottom_right)
                update_selection(new_selection)

    clear()
    draw_grid()
    pygame.display.update()
    #pygame.time.delay(29)


pygame.quit()
