import os
import sys
from typing import List, Tuple
import keyboard

# Define the Tetramino type
Tetramino = Tuple[List[Tuple[int, int, int]], Tuple[int, int, int]]


def create_grid(w: int, h: int) -> List[List[str]]:
    """Creates a grid of size (3w + 2) × (3h + 2), including the boundaries of the central area."""
    grid = [[' ' * 2 for _ in range(3 * w + 2)] for _ in range(3 * h + 2)]
    # Add vertical boundaries
    for i in range(3 * h + 2):
        grid[i][w * 3] = '| '
        grid[i][-1] = '| '
    # Add horizontal boundaries
    for j in range(3 * w + 2):
        grid[0][j] = '--'
        grid[-1][j] = '--'
    return grid


def import_card(file_path: str) -> Tuple[Tuple[int, int], List[Tetramino]]:
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Parse dimensions
    dimensions = tuple(map(int, lines[0].split(', ')))

    # Parse tetraminos
    tetraminos = []
    for line in lines[1:]:
        blocks_info, color_info = map(str.strip, line.split(';;'))
        blocks = [tuple(map(int, coord.split(', '))) for coord in blocks_info.split(';')]
        color = tuple(map(int, color_info.split(', ')))
        tetraminos.append((blocks, color))

    return dimensions, tetraminos


def setup_tetraminos(tetraminos: List[Tetramino], grid: List[List[str]]) -> Tuple[List[List[str]], List[Tetramino]]:
    for tetramino in tetraminos:
        blocks, color = tetramino
        for block in blocks:
            x, y, *_ = block[:3]  # Unpack only the first two values (x, y) from block
            grid[y][x] = f'\x1b[0;{color[0]};{color[1]}m* \x1b[0m'  # Updated color handling

    return grid, tetraminos


def rotate_tetramino(tetramino: Tetramino) -> Tetramino:
    """Rotates the tetramino clockwise."""
    blocks, offset = tetramino
    rotated_blocks = [(-y, x, *block[2:]) for x, y, *block in blocks]
    return rotated_blocks, offset


def move_tetramino(tetramino: Tetramino, direction: str) -> Tetramino:
    """Moves the tetramino in the specified direction."""
    blocks, offset = tetramino
    new_blocks = []

    for block in blocks:
        x, y, *_ = block[:3]  # Unpack only the first two values (x, y) from block
        if direction == 'left':
            new_blocks.append((x, y - 1, *block[2:]))
        elif direction == 'right':
            new_blocks.append((x, y + 1, *block[2:]))
        elif direction == 'up':
            new_blocks.append((x - 1, y, *block[2:]))
        elif direction == 'down':
            new_blocks.append((x + 1, y, *block[2:]))

    return new_blocks, offset


def check_move(tetraminos, grid):
    """Check if a move is valid."""
    for tetramino in tetraminos:
        for block in tetramino[0]:
            x, y, *_ = block + (0,)  # Unpack only the first two values (x, y) from block
            # Check if the block is out of bounds or collides with other blocks
            if (
                x < 0 or x >= len(grid) or
                y < 0 or y >= len(grid[0]) or
                grid[x][y] != ' ' * 2
            ):
                return False
    return True


def check_win(grid: List[List[str]]) -> bool:
    """Checks if the current position of the pieces corresponds to a winning configuration."""
    for row in grid[1:-1]:
        for cell in row[1:-1]:
            if cell == ' ' * 2:
                return False
    return True


def print_grid(grid: List[List[str]], no_number: bool = False):
    """Prints the game board."""
    # Move the cursor to the top-left corner of the console
    print("\033[H", end="")

    for row in grid:
        print(''.join(row[1:-1]))  # Omit borders for better display


def main():
    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')

    # Import tetraminos from file
    file_path = input("Enter the path to the tetramino file: ")
    dimensions, tetraminos = import_card(file_path)
    w, h = dimensions

    # Create the game grid
    grid = create_grid(w, h)

    # Setup initial tetraminos
    grid, tetraminos = setup_tetraminos(tetraminos, grid)

    # Initial tetramino index
    tetramino_index = 0
    current_tetramino = tetraminos[tetramino_index]

    # Game loop
    while True:
        # Clear the console
        os.system('cls' if os.name == 'nt' else 'clear')

        # Print the game board
        print_grid(grid)

        # Handle keyboard input
        if keyboard.is_pressed('q'):
            sys.exit()

        if keyboard.is_pressed('left'):
            new_tetramino = move_tetramino(current_tetramino, 'left')
            if check_move([new_tetramino], grid):
                current_tetramino = new_tetramino

        if keyboard.is_pressed('right'):
            new_tetramino = move_tetramino(current_tetramino, 'right')
            if check_move([new_tetramino], grid):
                current_tetramino = new_tetramino

        if keyboard.is_pressed('up'):
            new_tetramino = rotate_tetramino(current_tetramino)
            if check_move([new_tetramino], grid):
                current_tetramino = new_tetramino

        if keyboard.is_pressed('down'):
            new_tetramino = move_tetramino(current_tetramino, 'down')
            if check_move([new_tetramino], grid):
                current_tetramino = new_tetramino

        # Update the grid with the current tetramino
        grid, _ = setup_tetraminos([current_tetramino], grid)

        # Check for a win
        if check_win(grid):
            print("Congratulations! You won!")
            break


if __name__ == "__main__":
    main()
