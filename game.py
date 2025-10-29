import tkinter as tk
from tkinter import messagebox

# Function to handle a player's move
def on_click(row, col):
    global current_player, board

    if board[row][col] == "" and not game_over:
        board[row][col] = current_player
        buttons[row][col].config(text=current_player, state="disabled")

        if check_winner(current_player):
            messagebox.showinfo("Game Over", f"🎉 Player {current_player} wins!")
            disable_all_buttons()
        elif is_draw():
            messagebox.showinfo("Game Over", "It's a draw! 🤝")
            disable_all_buttons()
        else:
            current_player = "O" if current_player == "X" else "X"

# Function to check for a winner
def check_winner(player):
    # Check rows
    for row in board:
        if all(cell == player for cell in row):
            return True
    # Check columns
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    # Check diagonals
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

# Function to check for draw
def is_draw():
    return all(board[row][col] != "" for row in range(3) for col in range(3))

# Function to disable all buttons when game ends
def disable_all_buttons():
    global game_over
    game_over = True
    for row in buttons:
        for button in row:
            button.config(state="disabled")

# Function to reset the game
def reset_game():
    global board, current_player, game_over
    board = [["" for _ in range(3)] for _ in range(3)]
    current_player = "X"
    game_over = False
    for row in range(3):
        for col in range(3):
            buttons[row][col].config(text="", state="normal")

# Create main window
root = tk.Tk()
root.title("Tic Tac Toe")
root.resizable(False, False)

# Initialize game variables
board = [["" for _ in range(3)] for _ in range(3)]
buttons = [[None for _ in range(3)] for _ in range(3)]
current_player = "X"
game_over = False

# Create buttons for Tic Tac Toe grid
for row in range(3):
    for col in range(3):
        button = tk.Button(
            root,
            text="",
            font=("Helvetica", 24),
            width=5,
            height=2,
            command=lambda r=row, c=col: on_click(r, c)
        )
        button.grid(row=row, column=col)
        buttons[row][col] = button

# Reset button
reset_btn = tk.Button(root, text="Restart Game", font=("Helvetica", 14), bg="lightblue", command=reset_game)
reset_btn.grid(row=3, column=0, columnspan=3, sticky="nsew")

# Start the GUI loop
root.mainloop()
