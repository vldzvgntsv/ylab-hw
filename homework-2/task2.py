import random
import tkinter as tk
from itertools import cycle, islice
from tkinter import font, messagebox
from typing import NamedTuple


class Player(NamedTuple):
    name: str
    label: str
    color: str


class Move(NamedTuple):
    row: int
    col: int
    label: str = ""


BOARD_SIZE = 5
SYMBOLS_FOR_LOOSE = 3
DEFAULT_PLAYERS = (
    Player(name="Human being", label="X", color="blue"),
    Player(name="Computer", label="O", color="green"),
)


class TicTacToeGame:
    def __init__(self, players=DEFAULT_PLAYERS, board_size=BOARD_SIZE, symbols_for_loose=SYMBOLS_FOR_LOOSE):
        self._players = cycle(players)
        self.board_size = board_size
        self.symbols_for_loose = symbols_for_loose
        self.current_player = next(self._players)
        self.winner_combo = []
        self._current_moves = []
        self._has_winner = False
        self._winning_combos = []
        self._setup_board()

    def _setup_board(self):
        self._current_moves = [
            [Move(row, col) for col in range(self.board_size)]
            for row in range(self.board_size)
        ]
        self._winning_combos = self._get_winning_combos()

    def _get_winning_combos(self):
        all_rows = [[(move.row, move.col) for move in row] for row in self._current_moves]
        all_columns = [list(col) for col in zip(*all_rows)]

        winning_rows_combo = [
            [(row, col) for row, col in islice(row, i, self.symbols_for_loose + i)]
            for row in all_rows for i in range(self.board_size - self.symbols_for_loose + 1)
        ]

        winning_columns_combo = [
            [(row, col) for row, col in islice(column, i, self.symbols_for_loose + i)]
            for column in all_columns for i in range(self.board_size - self.symbols_for_loose + 1)
        ]

        all_diagonals = []
        for k in range(self.board_size):
            diagonal_below_main = [(i, j) for i in range(self.board_size) for j in range(self.board_size) if i - j == k]
            if len(diagonal_below_main) < self.symbols_for_loose:
                break
            all_diagonals.append(diagonal_below_main)
        for diagonal in reversed(all_diagonals):
            if len(diagonal) < self.board_size:
                mirrored_diagonal = [(j, i) for i, j in diagonal]
                all_diagonals.append(mirrored_diagonal)
        for k in range(-self.board_size, self.board_size):
            side_diagonals = [
                (i, j) for i in range(self.board_size)
                for j in range(self.board_size)
                if i + j == self.board_size - k
            ]
            all_diagonals.append(side_diagonals)
        winning_diagonals_combo = []
        for diagonal in all_diagonals:
            for i in range(len(diagonal) - self.symbols_for_loose + 1):
                winning_diagonals_combo.append([(row, col) for row, col in diagonal[i:i+self.symbols_for_loose]])
        winning_combos = winning_rows_combo+winning_columns_combo+winning_diagonals_combo
        return winning_combos

    def possible_ai_moves(self):
        return list(move for row in self._current_moves for move in row if move.label == "")

    def is_valid_move(self, move):
        """Return True if move is valid, and False otherwise."""
        row, col = move.row, move.col
        move_was_not_played = self._current_moves[row][col].label == ""
        no_winner = not self._has_winner
        return no_winner and move_was_not_played

    def process_move(self, move):
        """Process the current move and check if it's a win."""
        row, col = move.row, move.col
        self._current_moves[row][col] = move
        for combo in self._winning_combos:
            results = set(
                self._current_moves[n][m].label
                for n, m in combo
            )
            is_win = (len(results) == 1) and ("" not in results)
            if is_win:
                self._has_winner = True
                self.winner_combo = combo
                break

    def has_winner(self):
        """Return True if the game has a winner, and False otherwise."""
        return self._has_winner

    def is_tied(self):
        """Return True if the game is tied, and False otherwise."""
        no_winner = not self._has_winner
        played_moves = (
            move.label for row in self._current_moves for move in row
        )
        return no_winner and all(played_moves)

    def toggle_player(self):
        """Return a toggled player."""
        self.current_player = next(self._players)


class TicTacToeBoard(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.title("Rotten Tic-Tac-Toe")
        self._cells = {}
        self._game = game
        self._create_board_display()
        self._create_board_grid()
        self.show_message()

    def _create_board_display(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text="You start!",
            font=font.Font(size=28, weight="bold"),
        )
        self.display.pack()

    def _create_board_grid(self):
        grid_frame = tk.Frame(master=self)
        grid_frame.pack()
        for row in range(self._game.board_size):
            for col in range(self._game.board_size):
                button = tk.Button(
                    master=grid_frame,
                    text="",
                    font=font.Font(size=10, weight="bold"),
                    fg="black",
                    width=6,
                    height=3,
                    highlightbackground="lightblue",
                )
                self._cells[button] = (row, col)
                button.bind("<ButtonPress-1>", self.play)
                button.grid(
                    row=row,
                    column=col,
                    padx=1,
                    pady=1,
                    sticky="nsew"
                )

    def show_message(self):
        msg = (
            f'You are playing «Rotten Tic-Tac-Toe» versus AI on board size {self._game.board_size}.\n'
            f'Whoever has a vertical, horizontal or diagonal row of {self._game.symbols_for_loose} loses.\n'
        )
        messagebox.showinfo("About", msg)

    def play(self, event):
        """Handle a player's move."""
        clicked_btn = event.widget
        row, col = self._cells[clicked_btn]
        move = Move(row, col, self._game.current_player.label)
        if self._game.is_valid_move(move):
            self.process_move(clicked_btn, move)
            self.ai_play()

    def ai_play(self):
        row, col, clicked_btn = self.find_best_move()
        move = Move(row, col, self._game.current_player.label)
        if self._game.is_valid_move(move):
            self.process_move(clicked_btn, move)

    def find_best_move(self):
        empty_buttons = [button for button in self._cells if button.cget('text') == ""]
        for i in range(len(empty_buttons)):
            clicked_btn = random.choice(empty_buttons)
            row, col = self._cells[clicked_btn]
            self._game._current_moves[row][col] = Move(row, col, self._game.current_player.label)
            for combo in self._game._winning_combos:
                results = set(
                    self._game._current_moves[n][m].label
                    for n, m in combo
                )
                is_win = (len(results) == 1) and ("" not in results)
                if is_win:
                    break
            self._game._current_moves[row][col] = Move(row, col, '')
            if not is_win:
                return row, col, clicked_btn
        return row, col, clicked_btn

    def process_move(self, clicked_btn, move):
        self._update_button(clicked_btn)
        self._game.process_move(move)
        if self._game.is_tied():
            self._update_display(msg="Tied game!", color="red")
        elif self._game.has_winner():
            self._highlight_cells()
            msg = f'{self._game.current_player.name}"{self._game.current_player.label}" loose!'
            color = self._game.current_player.color
            self._update_display(msg, color)
        else:
            self._game.toggle_player()
            msg = f'{self._game.current_player.name} "{self._game.current_player.label}" turn'
            self._update_display(msg)

    def _update_button(self, clicked_btn):
        clicked_btn.config(text=self._game.current_player.label)
        clicked_btn.config(fg=self._game.current_player.color)

    def _update_display(self, msg, color="black"):
        self.display["text"] = msg
        self.display["fg"] = color

    def _highlight_cells(self):
        for button, coordinates in self._cells.items():
            if coordinates in self._game.winner_combo:
                button.config(highlightbackground="red")


def main():
    """Create the game's board and run its main loop."""
    game = TicTacToeGame()
    board = TicTacToeBoard(game)
    board.mainloop()


if __name__ == "__main__":
    main()
