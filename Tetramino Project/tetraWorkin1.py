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
    for row in grid:
        print(''.join(row[1:-1]))  # Omit borders for better display


def rotate_or_move_tetramino(tetramino: Tetramino, move: str) -> Tetramino:
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


def update_grid(grid, tetraminos):
    """Update the grid based on the current state of tetraminos."""
    # Clear the grid
    grid = create_grid(len(grid[0]) // 3, len(grid) // 3)

    # Place the tetraminos on the grid with ANSI escape codes
    for idx, tetramino in enumerate(tetraminos):
        blocks, offset = tetramino
        for block in blocks:
            x, y, _ = block[:3]  # Unpack only the first two values (x, y) from block
            grid[y + offset[0] * 3][x + offset[1] * 3] = f'\x1b[0;{tetramino[1][0]};{tetramino[1][1]}m* \x1b[0m'

    return grid


def on_key_event(e):
    """Callback function for keyboard events."""
    key = e.name
    if key in ["left", "right", "up", "down"]:
        # Update tetraminos based on the pressed key
        for idx, tetramino in enumerate(tetraminos):
            # Remove existing tetramino from the grid
            for block in tetramino[0]:
                x, y, _ = block[:3]  # Unpack only the first two values (x, y) from block
                grid[y + tetramino[1][0] * 3][x + tetramino[1][1] * 3] = ' ' * 2

            # Move or rotate the tetramino
            tetraminos[idx] = rotate_or_move_tetramino(tetramino, key)

        # Update the grid based on the current state of tetraminos
        updated_grid = update_grid(grid, tetraminos)

        # Print the updated grid
        print_grid(updated_grid)


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

    # Print the initial grid
    print_grid(grid)

    # Register the callback function for keyboard events
    keyboard.hook(on_key_event)

    # Use a flag to control the game loop
    game_running = True

    # Main game loop
    while game_running:
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
