import tkinter as tk
import sys

# Define grid as a global variable
grid = None
file_path = None  # Initialize file_path variable
# Initialize current_piece and tetraminos_index as global variables
current_piece = None
tetraminos_index = 0

def import_card(file_path):
    dimensions = None
    tetraminos = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

        # Extract dimensions from the first line
        dimensions = tuple(map(int, lines[0].strip().split(',')))

        # Process Tetraminos data
        for line in lines[1:]:
            data = line.strip().split(';;')

            # Parsing coordinates
            coordinates = []
            for coord in data[0].split(';'):
                coord = coord.strip()
                if coord:
                    coord = tuple(map(int, coord[1:-1].split(',')))
                    coordinates.append(coord)

            # Parsing color
            color = tuple(map(int, data[1].split(';')[1].split(',')))
            tetraminos.append([coordinates, color])

    return dimensions, tetraminos



# Function to initialize game grid
def create_grid(w, h):
    grid = [[' ' for _ in range(3 * w + 2)] for _ in range(3 * h + 2)]
    return grid

# Function to update the display with the current game state
def update_display(grid):
    for widget in root.winfo_children():
        widget.destroy()
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            label = tk.Label(root, text=grid[i][j], borderwidth=1, relief="solid", width=3, height=2)
            label.grid(row=i, column=j)

# Function to place Tetraminos on the grid
def place_tetraminos(grid, current_piece):
    for pos in current_piece[0]:
        x, y = pos
        grid[y][x] = current_piece[1]
    return grid

# Function to check if the current Tetramino position is valid
def check_move(tetramino, grid):
    for pos in tetramino[0]:
        x, y = pos
        if x < 0 or y < 0 or x >= len(grid[0]) or y >= len(grid):
            return False
        if grid[y][x] != ' ':
            return False
    return True

# Function to rotate Tetraminos
def rotate_tetramino(tetramino, clockwise=True):
    new_positions = []
    for x, y in tetramino[0]:
        if clockwise:
            new_positions.append((-y, x))
        else:
            new_positions.append((y, -x))
    tetramino[0] = new_positions
    return tetramino

# Function to check for a win condition
def check_win(grid):
    for row in grid:
        if ' ' in row:
            return False
    return True

# Function to handle user inputs
def handle_input(event):
    global grid, current_piece, tetraminos_index
    key = event.keysym
    if key == 'Right':
        if current_piece:
            temp_piece = [(pos[0] + 1, pos[1]) for pos in current_piece[0]]
            if check_move((temp_piece, current_piece[1]), grid):
                current_piece = (temp_piece, current_piece[1])
                grid = place_tetraminos(grid, current_piece)
    elif key == 'Left':
        if current_piece:
            temp_piece = [(pos[0] - 1, pos[1]) for pos in current_piece[0]]
            if check_move((temp_piece, current_piece[1]), grid):
                current_piece = (temp_piece, current_piece[1])
                grid = place_tetraminos(grid, current_piece)
    elif key == 'Up':
        if current_piece:
            rotated_piece = rotate_tetramino(current_piece, clockwise=True)
            if check_move(rotated_piece, grid):
                current_piece = rotated_piece
                grid = place_tetraminos(grid, current_piece)
    elif key == 'Down':
        if current_piece:
            temp_piece = [(pos[0], pos[1] + 1) for pos in current_piece[0]]
            if check_move((temp_piece, current_piece[1]), grid):
                current_piece = (temp_piece, current_piece[1])
                grid = place_tetraminos(grid, current_piece)
    update_display(grid)
    if check_win(grid):
        print("Congratulations! You won!")

# Function to start the game
def start_game(file_path):
    global grid, tetraminos, tetraminos_index, current_piece
    dimensions, tetraminos = import_card(file_path)
    grid = create_grid(dimensions[0], dimensions[1])
    tetraminos_index = 0
    current_piece = tetraminos[tetraminos_index]
    update_display(place_tetraminos(grid, current_piece))
    root.bind("<Key>", handle_input)
    print("Game is starting...")

root = tk.Tk()
root.title("Tetramino Game")

if len(sys.argv) < 2:
    print("Please provide the game file path as an argument.")
else:
    file_path = sys.argv[1]
    start_game(file_path)

root.mainloop()
