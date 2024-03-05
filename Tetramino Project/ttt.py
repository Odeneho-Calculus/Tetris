import tkinter as tk
import random
import time

class Tetris:
    def __init__(self, master, width=10, height=20):
        self.master = master
        self.master.title("Tetris")
        self.width = width
        self.height = height
        self.canvas_size = 30
        self.canvas = tk.Canvas(self.master, width=width * self.canvas_size, height=height * self.canvas_size)
        self.canvas.pack()
        self.shapes = [
            [[1, 1, 1, 1]],
            [[1, 1, 1], [1]],
            [[1, 1, 1], [0, 0, 1]],
            [[1, 1, 1], [0, 1]],
            [[1, 1], [1, 1]],
            [[1, 1, 0], [0, 1, 1]]
        ]
        self.current_shape = self.new_shape()
        self.game_over = False
        self.draw()

    def new_shape(self):
        shape = random.choice(self.shapes)
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        return {"shape": shape, "color": color, "x": self.width // 2 - len(shape[0]) // 2, "y": 0}

    def draw(self):
        self.canvas.delete("all")
        for i in range(self.width):
            for j in range(self.height):
                if self.current_shape["y"] <= j < self.current_shape["y"] + len(self.current_shape["shape"]):
                    row = j - self.current_shape["y"]
                    for k in range(len(self.current_shape["shape"][row])):
                        if self.current_shape["shape"][row][k]:
                            x = self.current_shape["x"] + k
                            y = j
                            self.canvas.create_rectangle(
                                x * self.canvas_size, y * self.canvas_size,
                                (x + 1) * self.canvas_size, (y + 1) * self.canvas_size,
                                fill=self.current_shape["color"], outline="black"
                            )

    def move_shape(self, dx, dy):
        new_x = self.current_shape["x"] + dx
        new_y = self.current_shape["y"] + dy

        if self.is_valid_position(new_x, new_y, self.current_shape["shape"]):
            self.current_shape["x"] = new_x
            self.current_shape["y"] = new_y
            self.draw()
        else:
            if dy > 0:  # Check if the move was downward
                self.merge_shape()
                self.clear_lines()
                self.current_shape = self.new_shape()
                if not self.is_valid_position(self.current_shape["x"], self.current_shape["y"], self.current_shape["shape"]):
                    self.game_over = True
                    self.canvas.create_text(
                        self.width * self.canvas_size / 2, self.height * self.canvas_size / 2,
                        text="Game Over", font=("Helvetica", 16), fill="red"
                    )
            else:
                self.draw()

    def merge_shape(self):
        for i in range(len(self.current_shape["shape"])):
            for j in range(len(self.current_shape["shape"][i])):
                if self.current_shape["shape"][i][j]:
                    x = self.current_shape["x"] + j
                    y = self.current_shape["y"] + i
                    self.canvas.create_rectangle(
                        x * self.canvas_size, y * self.canvas_size,
                        (x + 1) * self.canvas_size, (y + 1) * self.canvas_size,
                        fill=self.current_shape["color"], outline="black"
                    )

    def is_valid_position(self, x, y, shape):
    for i in range(len(shape)):
        for j in range(len(shape[i])):
            if shape[i][j]:
                if (
                    x + j < 0 or x + j >= self.width or
                    y + i >= self.height or
                    (y + i >= 0 and self.get_fill_color(x, y) != "")
                ):
                    return False
    return True

def get_fill_color(self, x, y):
    enclosed = self.canvas.find_enclosed(x * self.canvas_size, y * self.canvas_size, (x + 1) * self.canvas_size, (y + 1) * self.canvas_size)
    if enclosed:
        return self.canvas.itemcget(enclosed[0], "fill")
    return ""


    def rotate_shape(self):
        rotated_shape = list(zip(*reversed(self.current_shape["shape"])))
        if self.is_valid_position(self.current_shape["x"], self.current_shape["y"], rotated_shape):
            self.current_shape["shape"] = rotated_shape
            self.draw()

    def clear_lines(self):
        for i in range(self.height - 1, -1, -1):
            if all(self.canvas.itemcget(self.canvas.find_enclosed(0, i * self.canvas_size, self.width * self.canvas_size, (i + 1) * self.canvas_size)[0], "fill") != "" for _ in range(self.width)):
                self.canvas.delete(self.canvas.find_enclosed(0, i * self.canvas_size, self.width * self.canvas_size, (i + 1) * self.canvas_size)[0])
                for j in range(i, 0, -1):
                    for k in range(self.width):
                        fill_color = self.canvas.itemcget(self.canvas.find_enclosed(k * self.canvas_size, j * self.canvas_size, (k + 1) * self.canvas_size, (j + 1) * self.canvas_size)[0], "fill")
                        self.canvas.create_rectangle(
                            k * self.canvas_size, (j + 1) * self.canvas_size,
                            (k + 1) * self.canvas_size, (j + 2) * self.canvas_size,
                            fill=fill_color, outline="black"
                        )
if __name__ == "__main__":
    root = tk.Tk()
    tetris = Tetris(root)
    
    def key(event):
        if event.keysym == "Left":
            tetris.move_shape(-1, 0)
        elif event.keysym == "Right":
            tetris.move_shape(1, 0)
        elif event.keysym == "Down":
            tetris.move_shape(0, 1)
        elif event.keysym == "Up":
            tetris.rotate_shape()

    root.bind("<Key>", key)

    while not tetris.game_over:
        root.update_idletasks()
        root.update()
        tetris.move_shape(0, 1)
        time.sleep(0.5)

    root.mainloop()
