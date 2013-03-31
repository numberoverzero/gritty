import pygame

# Copyright 2013 Joe Cross
# This is free software, released under The GNU Lesser General Public License,
# version 3.
# You are free to use, distribute, and modify gritty. If modification is your
# game, it is recommended that you read the GNU LGPL license:
# http://www.gnu.org/licenses/
#
# This is a modified version of some functionality from the
# Pygame Advanced Graphics Library,
# by Ian Mallett: www.geometrian.com


def circle(surface, color, point, radius, width):
    pygame.draw.circle(surface, color, point, radius, width)


def rrect(surface, color, rect, radius, width):
    '''
    color is either (R,G,B) or (R,G,B,A) with each value between [0, 255]
    rect is of the form (x, y, width, height) where x, y is the position of the upper left corner
    radius is the curvature of the corners
    '''
    if radius == 0:
        pygame.draw.rect(surface, color, rect, 0)
        return

    if color[0] + color[1] + color[2] == 0:
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

    if width != 0:
        rrect(surf_temp, colorkey, (width, width, rect[2]-2*width, rect[3]-2*width), radius-width, 0)

    surf_temp.set_colorkey(colorkey)
    surface.blit(surf_temp, (rect[0], rect[1]))
