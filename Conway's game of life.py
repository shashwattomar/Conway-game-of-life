import tkinter as tk

CELL_SIZE = 10
BOARD_WIDTH = 100
BOARD_HEIGHT = 66

class GameOfLife:
    def __init__(self, root):
        self.root = root
        self.root.title("Conway's Game of Life")

        self.board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.generation = 0
        self.running = False

        self.canvas = tk.Canvas(self.root, width=CELL_SIZE * BOARD_WIDTH, height=CELL_SIZE * BOARD_HEIGHT, bg="white")
        self.canvas.pack()

        self.start_button = tk.Button(self.root, text="Start", command=self.start_game)
        self.start_button.pack()

        self.generation_label = tk.Label(self.root, text="Generation: 0")
        self.generation_label.pack()

        self.canvas.bind("<Button-1>", self.handle_click)

    def draw_board(self):
        self.canvas.delete("all")

        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                if self.board[row][col] == 1:
                    x1 = col * CELL_SIZE
                    y1 = row * CELL_SIZE
                    x2 = x1 + CELL_SIZE
                    y2 = y1 + CELL_SIZE
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="black")

    def count_live_neighbors(self, row, col):
        count = 0

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue

                neighbor_row = (row + i + BOARD_HEIGHT) % BOARD_HEIGHT
                neighbor_col = (col + j + BOARD_WIDTH) % BOARD_WIDTH
                count += self.board[neighbor_row][neighbor_col]

        return count

    def update_board(self):
        new_board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                neighbors = self.count_live_neighbors(row, col)

                if self.board[row][col] == 1:
                    if neighbors < 2 or neighbors > 3:
                        new_board[row][col] = 0
                    else:
                        new_board[row][col] = 1
                else:
                    if neighbors == 3:
                        new_board[row][col] = 1

        self.board = new_board
        self.generation += 1
        self.generation_label.config(text="Generation: {}".format(self.generation))
        self.draw_board()

        if self.running:
            self.root.after(100, self.update_board)

    def handle_click(self, event):
        if not self.running:
            col = event.x // CELL_SIZE
            row = event.y // CELL_SIZE

            if self.board[row][col] == 0:
                self.board[row][col] = 1
            else:
                self.board[row][col] = 0

            self.draw_board()

    def start_game(self):
        if not self.running:
            self.running = True
            self.start_button.config(text="Stop")
            self.update_board()
        else:
            self.running = False
            self.start_button.config(text="Start")

# Create the main window
root = tk.Tk()
game = GameOfLife(root)

# Run the Tkinter event loop
root.mainloop()
