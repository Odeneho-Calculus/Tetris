import os
import sys
from getkey import getkey

def create_grid(w, h):
    # Create a grid of size (3w+2) × (3h +2)
    grid = [[' ' * 2 for _ in range(3 * w + 2)] for _ in range(3 * h + 2)]

    # Fill in the boundaries of the central area
    for i in range(3 * h + 2):
        grid[i][w * 3] = '|'
        grid[i][w * 3 + 1] = '| *'

    for j in range(3 * w + 2):
        grid[h * 3][j] = '--'

    return grid

def import_card(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    dimensions = tuple(map(int, lines[0].strip().split(',')))

    tetraminos = []
    for line in lines[1:]:
        data = line.strip().split(';;')
        coordinates = [tuple(map(int, pair.strip('()').split(','))) for pair in data[0].split(';')]
        color = '\x1b[' + data[1] + 'm'
        tetraminos.append([coordinates, color, (0, 0)])

    return dimensions, tetraminos

def setup_tetraminos(tetraminos, grid):
    for i, tetramino in enumerate(tetraminos):
        for block in tetramino[0]:
            x, y = block
            grid[y][x] = f'{i + 1}'

    return grid

def place_tetraminos(tetraminos, grid):
    for tetramino in tetraminos:
        for block in tetramino[0]:
            x, y = block[0] + tetramino[2][0], block[1] + tetramino[2][1]
            grid[y][x] = tetramino[1] + '*'

    return grid

def rotate_tetramino(tetramino, clockwise=True):
    if clockwise:
        tetramino[0] = [(y, -x) for x, y in tetramino[0]]
    else:
        tetramino[0] = [(-y, x) for x, y in tetramino[0]]

    return tetramino

def check_move(tetramino, grid):
    for block in tetramino[0]:
        x, y = block[0] + tetramino[2][0], block[1] + tetramino[2][1]
        if grid[y][x] != ' ' * 2:
            return False
    return True

def check_win(grid):
    # Check if the central area is completely filled
    for i in range(1, len(grid) - 1):
        for j in range(1, len(grid[i]) - 1):
            if grid[i][j] == ' ' * 2:
                return False
    return True

def print_grid(grid, no_number=False):
    os.system('cls' if os.name == 'nt' else 'clear')

    for row in grid:
        print(''.join(row))

def main():
    if len(sys.argv) != 2:
        print("Usage: python tetra.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    dimensions, tetraminos = import_card(file_path)
    w, h = dimensions
    grid = create_grid(w, h)
    selected_tetramino = tetraminos[0]  # Initialize with the first tetramino

    setup_tetraminos(tetraminos, grid)
    print_grid(grid)

    while True:
        key = getkey()
        if key == 'q':
            break
        elif key.isdigit() and 1 <= int(key) <= len(tetraminos):
            selected_tetramino = tetraminos[int(key) - 1]
            print_grid(place_tetraminos([selected_tetramino], grid))
            move_tetramino(selected_tetramino, grid, w, h)
        elif key == 'i':
            rotate_tetramino(selected_tetramino, True)
            print_grid(place_tetraminos([selected_tetramino], grid))
        elif key == 'u':
            rotate_tetramino(selected_tetramino, False)
            print_grid(place_tetraminos([selected_tetramino], grid))
        elif key == 'j':
            move_tetramino(selected_tetramino, grid, w, h, direction='left')
            print_grid(place_tetraminos([selected_tetramino], grid))
        elif key == 'k':
            move_tetramino(selected_tetramino, grid, w, h, direction='down')
            print_grid(place_tetraminos([selected_tetramino], grid))
        elif key == 'l':
            move_tetramino(selected_tetramino, grid, w, h, direction='right')
            print_grid(place_tetraminos([selected_tetramino], grid))

    print("Game Over")

if __name__ == '__main__':
    main()
