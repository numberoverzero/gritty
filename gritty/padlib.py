import pygame

# This is a modified version of some functionality from the
# Pygame Advanced Graphics Library,
# by Ian Mallett: www.geometrian.com


def circle(surface, color, point, radius, width):
    pygame.draw.circle(surface, color, point, radius, width)


def rrect(surface, color, rect, radius, width):
    '''
    color is either (R,G,B) or (R,G,B,A) with each value in [0, 255]
    rect is of the form (x, y, width, height) where x, y is the position of the upper left corner
    radius is the curvature of the corners
    '''
    #outline_rect(surface, color, rect, width)
    #return
    if not radius:
        if width:
            outline_rect(surface, color, rect, width)
        else:
            pygame.draw.rect(surface, color, rect, 0)
        return

    if sum(color[:3]) == 0:
        colorkey = (1, 1, 1)
    else:
        colorkey = (0, 0, 0)

    surf_temp = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
    surf_temp.fill(colorkey)
    pygame.draw.rect(surf_temp, color, (0, radius, rect[2], rect[3]-2*radius), 0)
    pygame.draw.rect(surf_temp, color, (radius, 0, rect[2]-2*radius, rect[3]), 0)

    draw_circle = lambda point: circle(surf_temp, color, point, radius, 0)
    points = [
        [radius, radius],
        [rect[2]-radius, radius],
        [radius, rect[3]-radius],
        [rect[2]-radius, rect[3]-radius]
    ]
    map(draw_circle, points)

    if width:
        rrect(surf_temp, colorkey, (width, width, rect[2]-2*width, rect[3]-2*width), radius-width, 0)

    surf_temp.set_colorkey(colorkey)
    surface.blit(surf_temp, (rect[0], rect[1]))


def outline_rect(surface, color, rect, width):
    '''
    This is to fix the fact that the width argument doesn't work in pygame when
    drawing rectangles.

    Note that this method will draw the border AROUND the rectangle specified.
    So if (10, 10, 50, 50) is passed with a thickness of 5, the smallest rectangle
    that would contain the drawn border would be (5, 5, 55, 55)
    '''

    # Bail early on 0 width
    if not width:
        return

    X, Y, L, H = rect
    W = width

    surf_temp = pygame.Surface((L + 2 * W, H + 2 * W), pygame.SRCALPHA)
    sides = [
        [W, 0, L+W, W],
        [L+W, W, W, H+W],
        [0, H+W, L+W, W],
        [0, 0, W, H+W]
    ]
    draw = lambda side: pygame.draw.rect(surf_temp, color, side, 0)
    map(draw, sides)
    surface.blit(surf_temp, (X-W, Y-W))
