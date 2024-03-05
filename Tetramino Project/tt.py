import os
import sys
from typing import List, Tuple
import keyboard 

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
        blocks, color = tetramino
        for block in blocks:
            x, y = block
            grid[y][x] = f'\x1b[0;{color[0]};{color[1]}m* \x1b[0m'  # Updated color handling

    return grid, tetraminos

def place_tetraminos(tetraminos: List[Tuple[List[Tuple[int, int]], Tuple[int, int, int]]], 
                      grid: List[List[str]]) -> List[List[str]]:
    """Places tetraminos on the given grid."""
    new_grid = [row.copy() for row in grid]
    
    for idx, tetramino in enumerate(tetraminos):
        blocks, offset = tetramino
        for block in blocks:
            x, y, _ = block
            new_grid[x + offset[0]][y + offset[1]] = f'{idx + 1:02}'
    
    return new_grid

def rotate_tetramino(tetramino: Tuple[List[Tuple[int, int, int]], Tuple[int, int, int]]) -> Tuple[List[Tuple[int, int, int]], Tuple[int, int, int]]:
    """Rotates the tetramino clockwise."""
    blocks, offset = tetramino
    rotated_blocks = [(-y, x, z) for x, y, z in blocks]
    return rotated_blocks, offset

def move_tetramino(tetramino: Tuple[List[Tuple[int, int, int]], Tuple[int, int, int]], direction: str) -> Tuple[List[Tuple[int, int, int]], Tuple[int, int, int]]:
    """Moves the tetramino in the specified direction."""
    blocks, offset = tetramino
    if direction == 'left':
        offset = (offset[0], offset[1] - 1, offset[2])
    elif direction == 'right':
        offset = (offset[0], offset[1] + 1, offset[2])
    elif direction == 'up':
        offset = (offset[0] - 1, offset[1], offset[2])
    elif direction == 'down':
        offset = (offset[0] + 1, offset[1], offset[2])
    return blocks, offset

def check_move(tetraminos, grid):
    """Check if a move is valid."""
    for tetramino in tetraminos:
        for block in tetramino[0]:
            x, y = block  # Unpack two values (x, y) from block
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
    for row in grid:
        print(''.join(row[1:-1]))  # Omit borders for better display

def rotate_or_move_tetramino(tetramino: Tuple[List[Tuple[int, int, int]], Tuple[int, int, int]], move: str) -> Tuple[List[Tuple[int, int, int]], Tuple[int, int, int]]:
    """Moves or rotates the tetramino based on the player's choice."""
    if move.lower() in ['left', 'right', 'up', 'down']:
        # Move the tetramino
        return move_tetramino(tetramino, move.lower())
    elif move.lower() == 'rotate':
        # Rotate the tetramino
        return rotate_tetramino(tetramino)
    else:
        # No valid move or rotate command
        return tetramino

def on_key_event(e):
    """Callback function for keyboard events."""
    key = e.name
    if key in ["left", "right", "up", "down"]:
        # Update grid and tetraminos based on the pressed key
        for idx, tetramino in enumerate(tetraminos):
            # Remove existing tetramino from the grid
            for block in tetramino[0]:
                x, y, _ = block
                grid[x][y] = ' ' * 2

            # Move or rotate the tetramino
            tetraminos[idx] = rotate_or_move_tetramino(tetramino, key)

            # Place the updated tetramino on the grid
            for block in tetraminos[idx][0]:
                x, y, _ = block
                grid[x][y] = f'\x1b[0;{tetraminos[idx][1][0]};{tetraminos[idx][1][1]}m* \x1b[0m'

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

    # Attach the on_key_event function to the keyboard listener
    keyboard.hook(on_key_event)

    # Use a flag to control the game loop
    game_running = True

    # Main game loop
    while game_running:
        # Print debug information
        print("Grid:")
        print_grid(grid)
        print("Current Tetraminos:")
        for idx, tetramino in enumerate(tetraminos):
            print(f"Tetramino {idx + 1}: {tetramino}")

        # Implement more player moves and rotations as needed
        # Update grid and tetraminos accordingly
        # Use functions like place_tetraminos, rotate_tetramino, etc.

        # Example condition to end the game (you can modify this based on your game logic)
        if check_win(grid) or not check_move(tetraminos, grid):
            game_running = False

    print("Game Over!")
    if check_win(grid):
        print("Congratulations! You've won!")
    else:
        print("You've reached an unwinnable state. Better luck next time.")

if __name__ == "__main__":
    main()
