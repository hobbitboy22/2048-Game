# main.py

import random
import tkinter as tk

# Define grid size
# These numbers must be the same
row_number = 4
column_number = 4

def initialise_grid():
    grid = [[0] * column_number for _ in range(row_number)]
    add_random_tile(grid)
    add_random_tile(grid)
    return grid
        
def add_random_tile(grid):
    empty_cells = [(r, c) for r in range(row_number) for c in range(column_number) if grid[r][c] == 0]
    if empty_cells:
        r, c = random.choice(empty_cells)
        grid[r][c] = random.choice([2, 4])
        
def print_grid(grid):
    for r in grid:
        print('+----' * 4 + '+')
        print('|', end = '')
        for tile in r:
            if tile == 0:
                print('    |', end = '')
            else:
                print(f'{tile:4} |', end = '')
        print()
    print('+----' * 4 + '+')

def print_grid_default(grid):
    for row in grid:
        print(row)

def slide_left(row):
    new_row = [i for i in row if i != 0]
    new_row += [0] * (column_number - len(new_row))
    for i in range(column_number - 1):
        if new_row[i] == new_row[i + 1]:
            new_row[i] *= 2
            new_row[i + 1] = 0
    new_row = [i for i in new_row if i != 0]
    new_row += [0] * (column_number - len(new_row))
    return new_row

def move_left(grid):
    return [slide_left(row) for row in grid]

def move_right(grid):
    return [slide_left(row[::-1])[::-1] for row in grid]

def transpose(grid):
    return [list(row) for row in zip(*grid)]

def move_up(grid):
    return transpose(move_left(transpose(grid)))

def move_down(grid):
    return transpose(move_right(transpose(grid)))

def check_game_over(grid):
    # Check if empty space is present
    for row in grid:
        if 0 in row:
            return False
    # Check is adjacent tiles are equal
    for row in grid:
        for i in range(column_number - 1):
            if row[i] == row[i + 1]:
                return False
    # Check if vertical tiles are equal
    for i in range(row_number - 1):
        for j in range(column_number):
            if grid[i][j] == grid[i + 1][j]:
                return False
    # Return true if game is over
    return True

def check_win(grid):
    # Check for 2048 tile
    for row in grid:
        if 2048 in row:
            return True
    return False

def create_window():
    window = tk.Tk()
    window.title('2048')
    return window

def create_grid(window):
    grid_frame = tk.Frame(window, bg = 'lightgray')
    grid_frame.grid(sticky = "nsew")
    cells = [[tk.Label(grid_frame, text = '', width = 4, height = 2, font = ('Helvetica', 24), bg = 'white') for _ in range(row_number)] for _ in range(column_number)]
    for r in range(row_number):
        for c in range(column_number):
            cells[r][c].grid(row = r, column = c, padx = 5, pady = 5)
    return cells

def update_grid_display(cells, grid):
    for r in range(row_number):
        for c in range(column_number):
            value = grid[r][c]
            cells[r][c].config(text = str(value) if value else '', bg = get_tile_colour(value))
            
def get_tile_colour(value):
    colours = {
        0: "white", 2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
        16: "#f59563", 32: "#f67c5f", 64: "#f65e3b",
        128: "#edcf72", 256: "#edcc61", 512: "#edc850",
        1024: "#edc53f", 2048: "#edc22e"
    }
    return colours.get(value, "black")

def handle_key(event):
    global grid
    key = event.keysym
    if key in ['Left', 'Right', 'Up', 'Down']:
        if key == 'Left':
            grid = move_left(grid)
        elif key == 'Right':
            grid = move_right(grid)
        elif key == 'Up':
            grid = move_up(grid)
        elif key == 'Down':
            grid = move_down(grid)
        add_random_tile(grid)
        update_grid_display(cells, grid)
        if check_win(grid):
            print('You win!')
        if check_game_over(grid):
            print('Game over!')

def main():
    global grid, cells
    grid = initialise_grid()
    window = create_window()
    cells = create_grid(window)
    update_grid_display(cells, grid)

    window.bind('<Key>', handle_key)
    window.mainloop()

if __name__ == '__main__':
    main()