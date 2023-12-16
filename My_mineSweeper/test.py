"""Use this file as you want to run testcode and play around"""


x_pos=y_pos=0
for a_row in range(amount_of_cells):
    cell = (x_pos, y_pos, CELL_WIDTH, CELL_HEIGHT, bomb_chance)
    x_pos+= CELL_WIDTH
    row.append(cell)
x_pos = 0
y_pos += CELL_HEIGHT
cells.append(row)
