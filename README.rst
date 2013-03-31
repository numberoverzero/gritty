===================
Gritty
===================

Gritty is designed to provide an easy-to-use grid component, with
reasonable performance for small grids (~ 100x100).  gritty supports
custom cell attributes, including default values and coercion functions,
and tries to provide an easy interface for manipulating multiple cells at once.
Typical setup often looks like this::

    #!/usr/bin/env python

    import pygame
    from gritty import grid

    # Set up args and kwargs

    pygame.init()
    grid = Grid(*args, **kwargs)
    grid_pos = (0, 0)
    screen = pygame.display.set_mode(grid.render_dimensions)

    while True:
        # Do stuff to the grid
        screen.blit(grid.surface, grid_pos)


Note the ``grid.surface`` in the while loop: gritty caches the grid surface and only redraws cells that have changed since the last time it was rendered.


Grid Initialization
===================

Grid has 4 required arguments - number of rows, number of columns, and cell width in pixels, and cell height in pixels.  Beyond that, you can specify values for cell color, cell border color, cell border size, and cell radius.  All of these are optional, and will use default settings as specified in ``Grid.__init__()``.  Note that these are a mix of grid properties and cell attribute defaults - see the following sections for more info on how to use each.

From the previous section, "set up args and kwargs" may look something like this::

    rows = 20
    columns = 20
    cell_width = 25
    cell_height = 25
    COLOR_OFF = (000, 000, 255)
    COLOR_ON = (255, 255, 51)

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

    pygame.init()
    grid = Grid(*args, **kwargs)

Cell Attributes
===================

Attribute Defaults
----------------------------

grid.cell_attr holds the list of default values for cell attributes.
Note that you can still adjust arbitrary attributes of cells without adding a default ot grid.cell_attr.  However, empty cells will not have a value for that attribute.

Adding, removing, or updating defaults will trigger a full redraw the next time the surface is rendered.

To change the default color::

    grid = Grid(10, 10, 2, 2)
    grid.cel_attr['color'] = [255, 0, 0]  # Set default color to red

To add an 'alive' attribute, such as for the Game of Life::

    grid = Grid(10, 10, 2, 2)
    grid.cell_attr['alive'] = False  # By default, cells are dead


Attribute Coercion Functions
----------------------------

Color values can be specified as (R,G,B) or (R,G,B,A).  Instead of manually checking the length each time we get or set the value, we can add an intercepting coercion function.  The color coercion function below is included by default::

    def coerce_alpha(input):
        '''Default to full opacity'''
        if len(input) == 3:
            input = list(input)
            input.append(255)
        return input
    
    grid = Grid(10, 10, 2, 2)
    grid.cell_attr_coercion_funcs['color'] = coerce_alpha
    grid[1,1].color = (0, 1, 2)
    print grid[1,1]

Currently, one coercion function is used for both set and get, so a function which doubled the red value of a color would double it when set, and double the return value of get.  This feature hasn't been fully designed out yet, so it could change significantly (or be cut altogether).

Grid Properties
===================

Changing a grid property will trigger a full redraw the next time the surface is rendered.  Be aware that ``grid.hit_check`` will use the new values immediately - be sure to check input **after** drawing the grid so that the mouse interaction you are testing is against the correct dimensions.

Grid properties are:

* ``rows`` - number of rows of cells in the grid

* ``columns`` - number of columns of cells in the grid

* ``cell_width`` - width in pixels of a cell (interior, without border)

* ``cell_height`` - height in pixels of a cell (interior, without border)

* ``cell_border_size`` - thickness in pixels of the border between cells and around the grid

