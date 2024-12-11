import tkinter as tk
import random
import os

# Constants
BOARD_SIZE = 4
CELL_SIZE = 120
PADDING = 10
BG_COLOR = "#faf8ef"
EMPTY_COLOR = "#cdc1b4"
TILE_COLORS = {
    2: "#eee4da",
    4: "#ede0c8",
    8: "#f2b179",
    16: "#f59563",
    32: "#f67c5f",
    64: "#f65e3b",
    128: "#edcf72",
    256: "#edcc61",
    512: "#edc850",
    1024: "#edc53f",
    2048: "#edc22e",
}

TEXT_COLORS = {
    2: "#776e65",
    4: "#776e65",
    8: "#f9f6f2",
    16: "#f9f6f2",
    32: "#f9f6f2",
    64: "#f9f6f2",
    128: "#f9f6f2",
    256: "#f9f6f2",
    512: "#f9f6f2",
    1024: "#f9f6f2",
    2048: "#f9f6f2",
}

FONT = ("Helvetica", 24, "bold")
HIGH_SCORE_FILE = "highscore.txt"


class Game2048:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("2048 Game")
        self.window.configure(bg=BG_COLOR)
        self.window.resizable(False, False)

        self.board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.score = 0
        self.game_over = False
        self.high_score = self.load_high_score()

        self.create_widgets()
        self.start_game()

        self.window.bind("<Key>", self.handle_keypress)

    def create_widgets(self):
        # Score label
        self.score_label = tk.Label(
            self.window, text=f"Score: 0  |  High Score: {self.high_score}",
            font=("Helvetica", 18), bg=BG_COLOR, fg="#776e65"
        )
        self.score_label.pack(pady=10)

        # Game board canvas
        self.canvas = tk.Canvas(
            self.window, width=BOARD_SIZE * CELL_SIZE + PADDING * (BOARD_SIZE + 1),
            height=BOARD_SIZE * CELL_SIZE + PADDING * (BOARD_SIZE + 1),
            bg=BG_COLOR, highlightthickness=0
        )
        self.canvas.pack()

        # Restart button
        self.restart_button = tk.Button(
            self.window, text="Restart", command=self.start_game,
            font=("Helvetica", 16), bg="#8f7a66", fg="white"
        )
        self.restart_button.pack(pady=10)

    def start_game(self):
        self.board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.score = 0
        self.game_over = False
        self.create_tile()
        self.create_tile()
        self.update_board()

    def create_tile(self):
        empty_cells = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if self.board[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.board[i][j] = random.choice([2, 4])

    def update_board(self):
        self.canvas.delete("tile")
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                value = self.board[i][j]
                x0 = j * CELL_SIZE + PADDING * (j + 1)
                y0 = i * CELL_SIZE + PADDING * (i + 1)
                x1 = x0 + CELL_SIZE
                y1 = y0 + CELL_SIZE

                color = TILE_COLORS.get(value, EMPTY_COLOR)
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="", tags="tile")

                if value:
                    text_color = TEXT_COLORS.get(value, "#f9f6f2")
                    self.canvas.create_text(
                        (x0 + x1) / 2, (y0 + y1) / 2, text=str(value),
                        font=FONT, fill=text_color, tags="tile"
                    )

        self.score_label.config(text=f"Score: {self.score}  |  High Score: {self.high_score}")

    def handle_keypress(self, event):
        moves = {
            "Left": self.move_left,
            "Right": self.move_right,
            "Up": self.move_up,
            "Down": self.move_down,
        }

        if event.keysym in moves:
            previous_board = [row[:] for row in self.board]
            moves[event.keysym]()
            if self.board != previous_board:
                self.create_tile()
                self.update_board()
                if self.is_game_over():
                    self.display_game_over()
                    self.update_high_score()

    def compress(self, row):
        new_row = [num for num in row if num != 0]
        new_row += [0] * (BOARD_SIZE - len(new_row))
        return new_row

    def merge(self, row):
        for i in range(BOARD_SIZE - 1):
            if row[i] == row[i + 1] and row[i] != 0:
                row[i] *= 2
                self.score += row[i]
                row[i + 1] = 0
        return row

    def move_left(self):
        for i in range(BOARD_SIZE):
            self.board[i] = self.compress(self.merge(self.compress(self.board[i])))

    def move_right(self):
        for i in range(BOARD_SIZE):
            self.board[i] = list(reversed(self.compress(self.merge(self.compress(reversed(self.board[i]))))))

    def move_up(self):
        self.board = list(map(list, zip(*self.board)))
        self.move_left()
        self.board = list(map(list, zip(*self.board)))

    def move_down(self):
        self.board = list(map(list, zip(*self.board)))
        self.move_right()
        self.board = list(map(list, zip(*self.board)))

    def is_game_over(self):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == 0:
                    return False
                if j < BOARD_SIZE - 1 and self.board[i][j] == self.board[i][j + 1]:
                    return False
                if i < BOARD_SIZE - 1 and self.board[i][j] == self.board[i + 1][j]:
                    return False
        return True

    def display_game_over(self):
        self.canvas.create_text(
            self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2,
            text="Game Over!", font=("Helvetica", 32, "bold"), fill="red"
        )

    def load_high_score(self):
        if os.path.exists(HIGH_SCORE_FILE):
            with open(HIGH_SCORE_FILE, "r") as file:
                return int(file.read())
        return 0

    def update_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            with open(HIGH_SCORE_FILE, "w") as file:
                file.write(str(self.high_score))

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    game = Game2048()
    game.run()
