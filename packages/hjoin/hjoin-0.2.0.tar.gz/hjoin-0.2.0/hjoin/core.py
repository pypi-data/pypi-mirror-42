# -*- coding: utf-8 -*-

from ansiwrap import ansilen, ansi_terminate_lines

def string_shape(s):
    """
    Return the height, width of a string, in lines/scharacters.
    h,w order chosen to be compatible with rows, columns standard of
    NumPy and and its shape method.
    """
    lines = s.splitlines()
    lengths = [ansilen(l) for l in lines]
    return (len(lengths), max(lengths or [0]))


def ansi_ljust(s, width):
    needs = width - ansilen(s)
    if needs > 0:
        return s + ' ' * needs
    else:
        return s



def hjoin(strings, sep=' '):
    """
    Horizontal join. Concatenates strings horizontally. Like
    join, but considers nth line of each string to be another column
    and concatenates it appropriately.
    """
    if not strings:
        return ''
    ncols = len(strings)
    slines = [ansi_terminate_lines(s.splitlines()) for s in strings]
    shapes = [string_shape(s) for s in strings]
    heights, widths = zip(*shapes)
    height = max(heights)
    lines = []
    for row_index in range(height):
        row = []
        for col_index in range(ncols):
            col_lines = slines[col_index]
            if row_index < heights[col_index]:
                cell = col_lines[row_index]
            else:
                cell = ''
            celljust = ansi_ljust(cell, widths[col_index])
            row.append(celljust)
        lines.append(sep.join(row))
    return '\n'.join(lines)
