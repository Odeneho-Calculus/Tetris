import os
import sys
from typing import List, Tuple

# Define the Tetramino type
Tetramino = Tuple[List[Tuple[int, int]], Tuple[int, int, int]]

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
        blocks, color = tetramino  # Updated this line
        for block in blocks:
            x, y = block
            grid[y][x] = f'\x1b[0;{color[0]};{color[1]}m* \x1b[0m'  # Updated color handling

    return grid, tetraminos


def place_tetraminos(tetraminos: List[Tuple[List[Tuple[int, int, int]], int, Tuple[int, int]]], 
                      grid: List[List[str]]) -> List[List[str]]:
    """Places tetraminos on the given grid."""
    new_grid = [row.copy() for row in grid]
    
    for idx, tetramino in enumerate(tetraminos):
        blocks, _, offset = tetramino
        for block in blocks:
            x, y, _ = block
            new_grid[x + offset[0]][y + offset[1]] = f'{idx + 1:02}'
    
    return new_grid

def rotate_tetramino(tetramino: Tuple[List[Tuple[int, int, int]], int, Tuple[int, int]], 
                     clockwise: bool = True) -> Tuple[List[Tuple[int, int, int]], int, Tuple[int, int]]:
    """Rotates the tetramino clockwise or counter-clockwise."""
    blocks, color, offset = tetramino
    rotated_blocks = [(y, -x, z) if clockwise else (-y, x, z) for x, y, z in blocks]
    return rotated_blocks, color, offset

def check_move(tetramino: Tuple[List[Tuple[int, int, int]], int, Tuple[int, int]], 
                grid: List[List[str]]) -> bool:
    """Checks if the current position of the tetramino is valid."""
    for block in tetramino[0]:
        x, y, _ = block
        if not (0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] == ' ' * 2):
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
    for row in grid:
        print(''.join(row[1:-1]))  # Omit borders for better display

def move_tetramino(tetramino: Tuple[List[Tuple[int, int, int]], int, Tuple[int, int]], direction: str) -> Tuple[List[Tuple[int, int, int]], int, Tuple[int, int]]:
    """Moves the tetramino in the specified direction."""
    blocks, color, offset = tetramino
    moved_blocks = [(x + dx, y + dy, z) for x, y, z in blocks]
    
    if direction == 'left':
        moved_offset = (offset[0], offset[1] - 1)
    elif direction == 'right':
        moved_offset = (offset[0], offset[1] + 1)
    elif direction == 'up':
        moved_offset = (offset[0] - 1, offset[1])
    elif direction == 'down':
        moved_offset = (offset[0] + 1, offset[1])
    else:
        moved_offset = offset
    
    return moved_blocks, color, moved_offset


def main():
    if len(sys.argv) != 2:
        print("Usage: python tetramino.py <map_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    # Read file and import tetraminos
    dimensions, tetraminos = import_card(file_path)

    # Create initial grid
    grid = create_grid(*dimensions)

    # Set up tetraminos on the grid
    grid, tetraminos = setup_tetraminos(tetraminos, grid)

    # Main game loop
    while not check_win(grid):
        print_grid(grid)

        # Example: Move the first tetramino to the right
        tetraminos[0] = move_tetramino(tetraminos[0], 'right')

        # Implement more player moves and rotations as needed
        # Update grid and tetraminos accordingly
        # Use functions like place_tetraminos, rotate_tetramino, etc.
        # Make sure to break out of the loop if the game is unwinnable

    print("Congratulations! You've won!")

if __name__ == "__main__":
    main()
