import os
from getkey import getkey

def create_grid(w, h):
    grid = [[' ' * 2] * (3 * w + 2) for _ in range(3 * h + 2)]
    # Add vertical borders
    for i in range(3 * h + 2):
        grid[i][w * 3] = '|'
        grid[i][-1] = '|'
    # Add horizontal borders
    for i in range(2, w * 3, 3):
        grid[0][i] = '--'
        grid[-1][i] = '--'
    return grid

def import_card(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    dimensions = tuple(map(int, lines[0].split(', ')))

    tetraminos = []
    for line in lines[1:]:
        coords_color = line.strip().split(';;')
        coordinates = [tuple(map(int, coord.split(', '))) for coord in coords_color[0].split(';')]
        color = '\x1b[' + coords_color[1] + 'm'

        tetramino = [coordinates, color, (0, 0)]
        tetraminos.append(tetramino)

    return dimensions, tetraminos

def setup_tetraminos(tetraminos, grid):
    new_tetraminos = []
    for i, tetramino in enumerate(tetraminos):
        offset = (3 * i, 0)
        new_tetramino = [list((x + offset[0], y + offset[1]) for x, y in tetramino[0]), tetramino[1], offset]
        new_tetraminos.append(new_tetramino)
        place_tetraminos(new_tetraminos, grid)
    return grid, new_tetraminos

def place_tetraminos(tetraminos, grid):
    for tetramino in tetraminos:
        for x, y in tetramino[0]:
            grid[y][x] = tetramino[1] + '* '

def rotate_tetramino(tetramino, clockwise=True):
    rotation_matrix = lambda x, y: (y, -x) if clockwise else (-y, x)
    tetramino[0] = [rotation_matrix(x, y) for x, y in tetramino[0]]
    return tetramino

def check_move(tetramino, grid):
    for x, y in tetramino[0]:
        if not (0 <= x < len(grid[0]) and 0 <= y < len(grid)):
            return False
        if grid[y][x] != ' ' * 2:
            return False
    return True

def check_win(grid):
    for row in grid:
        if ' ' * 2 in row:
            return False
    return True

def print_grid(grid, no_number):
    os.system('clear' if os.name == 'posix' else 'cls')
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if no_number and cell[0].isdigit():
                print(' ' * 2, end='')
            else:
                print(cell, end='')
        print()

def main():
    dimensions, tetraminos = import_card('map_1.txt')
    w, h = dimensions
    grid = create_grid(w, h)
    grid, tetraminos = setup_tetraminos(tetraminos, grid)
    print_grid(grid, False)

    while True:
        key = getkey()
        if key.isdigit() and 1 <= int(key) <= len(tetraminos):
            selected_tetramino = tetraminos[int(key) - 1]
            print_grid(grid, True)
            print(f"Selected Tetramino: {key}")
            print(f"Move: i (up), k (down), j (left), l (right), o (rotate clockwise), u (rotate counter-clockwise), v (validate)")

            move_key = getkey()
            if move_key == 'i':
                selected_tetramino[0] = [(x, y - 1) for x, y in selected_tetramino[0]]
            elif move_key == 'k':
                selected_tetramino[0] = [(x, y + 1) for x, y in selected_tetramino[0]]
            elif move_key == 'j':
                selected_tetramino[0] = [(x - 1, y) for x, y in selected_tetramino[0]]
            elif move_key == 'l':
                selected_tetramino[0] = [(x + 1, y) for x, y in selected_tetramino[0]]
            elif move_key == 'o':
                rotate_tetramino(selected_tetramino)
            elif move_key == 'u':
                rotate_tetramino(selected_tetramino, clockwise=False)
            elif move_key == 'v':
                if check_move(selected_tetramino, grid):
                    place_tetraminos([selected_tetramino], grid)
                    print_grid(grid, False)
                    if check_win(grid):
                        print("Congratulations! You won!")
                        return
                else:
                    print("Invalid move! Try again.")

if __name__ == '__main__':
    main()
