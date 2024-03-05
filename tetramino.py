import tkinter as tk
import random

class Tetris:
    def __init__(self, master, width=10, height=20, block_size=30):
        self.master = master
        self.width = width
        self.height = height
        self.block_size = block_size
        self.canvas_size = block_size
        self.canvas = tk.Canvas(master, width=width * block_size, height=height * block_size, bg="white")
        self.canvas.pack()
        self.shapes = [
            [[1, 1, 1, 1]],
            [[1, 1, 1], [1]],
            [[1, 1, 1], [0, 0, 1]],
            [[1, 1, 1], [0, 1]],
            [[1, 1], [1, 1]],
            [[1, 1, 1], [0, 1, 0]],
            [[1, 1, 1], [1, 0]],
        ]
        self.current_shape = {"shape": [], "color": ""}
        self.new_shape()
        self.master.after(500, self.update)
        self.master.bind("<Left>", lambda event: self.move_left())
        self.master.bind("<Right>", lambda event: self.move_right())
        self.master.bind("<Up>", lambda event: self.rotate())
        self.master.bind("<Down>", lambda event: self.move_down())

    def new_shape(self):
        self.current_shape["shape"] = random.choice(self.shapes)
        self.current_shape["color"] = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        self.current_x = self.width // 2 - len(self.current_shape["shape"][0]) // 2
        self.current_y = 0
        self.draw_shape()

    def draw_shape(self):
        self.canvas.delete("current_shape")
        for i in range(len(self.current_shape["shape"])):
            for j in range(len(self.current_shape["shape"][i])):
                if self.current_shape["shape"][i][j]:
                    x = (self.current_x + j) * self.canvas_size
                    y = (self.current_y + i) * self.canvas_size
                    self.canvas.create_rectangle(
                        x, y, x + self.canvas_size, y + self.canvas_size, fill=self.current_shape["color"], tags="current_shape"
                    )

    def clear_lines(self):
        lines_to_clear = []
        for i in range(self.current_y, self.current_y + len(self.current_shape["shape"])):
            if all(self.canvas.itemcget(item, "fill") != "" for item in self.canvas.find_enclosed(0, i * self.canvas_size, self.width * self.canvas_size, (i + 1) * self.canvas_size)):
                lines_to_clear.append(i)

        for line in lines_to_clear:
            for item in self.canvas.find_enclosed(0, 0, self.width * self.canvas_size, line * self.canvas_size):
                self.canvas.move(item, 0, self.canvas_size)

    def move_left(self):
        if self.is_valid_position(self.current_x - 1, self.current_y, self.current_shape["shape"]):
            self.current_x -= 1
            self.draw_shape()

    def move_right(self):
        if self.is_valid_position(self.current_x + 1, self.current_y, self.current_shape["shape"]):
            self.current_x += 1
            self.draw_shape()

    def move_down(self):
        if self.is_valid_position(self.current_x, self.current_y + 1, self.current_shape["shape"]):
            self.current_y += 1
            self.draw_shape()
        else:
            self.clear_lines()
            self.new_shape()

    def rotate(self):
        rotated_shape = [list(row) for row in zip(*self.current_shape["shape"][::-1])]
        if self.is_valid_position(self.current_x, self.current_y, rotated_shape):
            self.current_shape["shape"] = rotated_shape
            self.draw_shape()

    def is_valid_position(self, x, y, shape):
        for i in range(len(shape)):
            for j in range(len(shape[i])):
                if shape[i][j]:
                    x_pos = x + j
                    y_pos = y + i
                    if (
                        x_pos < 0 or x_pos >= self.width or
                        y_pos >= self.height or
                        (y_pos >= 0 and x_pos >= 0 and self.canvas.itemcget(self.canvas.find_overlapping(x_pos * self.canvas_size, y_pos * self.canvas_size, (x_pos + 1) * self.canvas_size, (y_pos + 1) * self.canvas_size)[0], "fill") != "")
                    ):
                        return False
        return True

    def update(self):
        self.move_down()
        self.master.after(500, self.update)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Tetris")
    game = Tetris(root)
    root.mainloop()
