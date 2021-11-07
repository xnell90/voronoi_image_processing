import math
import random

from .cell_types import *

def get_cells(num_cells, range_x, range_y, alternate_cell_color):
    cells = []

    for i in range(num_cells):
        if (type(range_x) is tuple): cpx = random.randrange(*range_x)
        else: cpx = random.randrange(range_x)

        if (type(range_y) is tuple): cpy = random.randrange(*range_y)
        else: cpy = random.randrange(range_y)

        cp  = (cpx, cpy)

        if alternate_cell_color:
            new_cell = ColorCell(cp, is_gray = (i % 2 == 0))
            cells.append(new_cell)
        else:
            cells.append(StandardCell(cp))

    return cells

def forms_boundary(p1, p2, alternate_cell_color=False):
    if not alternate_cell_color: return p1 != p2

    r1, g1, b1 = p1[0], p1[1], p1[2]
    r2, g2, b2 = p2[0], p2[1], p2[2]

    is_p1_gray = (r1 == g1 and g1 == b1)
    is_p2_gray = (r2 == g2 and g2 == b2)

    return (is_p1_gray and not is_p2_gray) or (not is_p1_gray and is_p2_gray)
