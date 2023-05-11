import tkinter as tk

# Constants
CELL_SIZE = 10
BOARD_WIDTH = 100
BOARD_HEIGHT = 66

# Class: This class represents the Game of Life. It has an initializer method __init__ that takes the root window as a parameter.
class GameOfLife:
    # This method initializes the GameOfLife object. It assigns the root window to self.root and sets the window title to "Conway's Game of Life".
    def __init__(self, root):
        self.root = root
        self.root.title("Conway's Game of Life")

        # These instance variables represent the game board, the current generation, and the running state of the game. self.board is a 2D list initialized with zeros, self.generation is set to 0, and self.running is set to False initially.
        self.board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.generation = 0
        self.running = False

        # This creates a Tkinter canvas widget inside the root window. The canvas is used to draw the game board. Its size is determined by multiplying the cell size with the board width and height. The canvas is also given a white background color.
        self.canvas = tk.Canvas(self.root, width=CELL_SIZE * BOARD_WIDTH, height=CELL_SIZE * BOARD_HEIGHT, bg="red")
        self.canvas.pack()

        # This creates a Tkinter button widget inside the root window. The button is labeled "Start" and its command parameter is set to the start_game method. When clicked, the button will invoke the start_game method.
        self.start_button = tk.Button(self.root, text="Start", command=self.start_game)
        self.start_button.pack()

        # This creates a Tkinter label widget inside the root window. The label displays the current generation number, which is initially set to 0.
        self.generation_label = tk.Label(self.root, text="Generation: 0")
        self.generation_label.pack()

        # This line binds the left mouse button click event to the handle_click method. When the left mouse button is clicked on the canvas, the handle_click method will be called.
        self.canvas.bind("<Button-1>", self.handle_click)


# This method is responsible for drawing the game board on the canvas. It clears the canvas and then iterates over each cell in the board, drawing a black rectangle for live cells (represented by 1) and leaving empty for dead cells (represented by 0).
    def draw_board(self):
        self.canvas.delete("all")

        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                if self.board[row][col] == 1:
                    x1 = col * CELL_SIZE
                    y1 = row * CELL_SIZE
                    x2 = x1 + CELL_SIZE
                    y2 = y1 + CELL_SIZE
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="yellow")

# This method takes the row and column indices of a cell as input and returns the count of live neighbors around that cell. It iterates over the neighboring cells (including diagonal neighbors) and counts the number of live cells (cells with a value of 1) in the board.
# The method uses modular arithmetic to handle the wrapping around the edges of the board. If a neighboring cell is outside the board boundaries, it wraps around to the opposite side. For example, if the cell is at the top row and its neighbor is in the row above, the neighbor will be considered as the bottom row.
# The count of live neighbors is accumulated in the count variable and returned at the end.
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

# This method updates the game board to the next generation. It creates a new empty board new_board to hold the updated state.
# It iterates over each cell in the current board and counts the number of live neighbors using the count_live_neighbors method. Based on the rules of the Game of Life, it determines whether the cell should live, die, or be born in the next generation and updates the corresponding cell in new_board.
# After updating the entire board, the self.board is replaced with new_board, the generation counter is incremented, the generation label is updated, and the board is redrawn on the canvas using the draw_board method.
# If the game is running (self.running is True), it schedules the update_board method to be called again after a delay of 100 milliseconds using the after method of the root window. This creates a continuous animation loop, updating the board at regular intervals.
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

# This method handles the left mouse button click event on the canvas. It is only active when the game is not running (self.running is False). It calculates the row and column indices of the clicked cell based on the mouse coordinates.
# If the clicked cell is currently dead (value is 0), it changes it to live (value 1), and vice versa. Then, it redraws the board on the canvas using the draw_board method.
    def handle_click(self, event):
        if not self.running:
            col = event.x // CELL_SIZE
            row = event.y // CELL_SIZE

            if self.board[row][col] == 0:
                self.board[row][col] = 1
            else:
                self.board[row][col] = 0

            self.draw_board()


# This method is invoked when the start button is clicked. If the game is not currently running, it sets self.running to True, changes the button text to "Stop," and starts the game loop by calling the update_board method. If the game is already running, it stops the game by setting self.running to False and changes the button text to "Start."
    def start_game(self):
        if not self.running:
            self.running = True
            self.start_button.config(text="Stop")
            self.update_board()
        else:
            self.running = False
            self.start_button.config(text="Start")

# Create the main window: These lines create the main window using the Tkinter Tk class and assign it to root. Then, an instance of the GameOfLife class is created with root as an argument, initializing the game.
root = tk.Tk()
game = GameOfLife(root)

# Run the Tkinter event loop: This line starts the Tkinter event loop, which handles user input and updates the GUI. The program remains in this loop until the window is closed.
root.mainloop()
