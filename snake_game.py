import tkinter as tk
import random

# Game constants
GAME_WIDTH = 600
GAME_HEIGHT = 400
SPACE_SIZE = 20
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

class Snake:
    def __init__(self, canvas):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
        for i in range(BODY_PARTS):
            self.coordinates.append([0, 0])
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self, canvas):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake, food):
    global direction, score, SPEED

    if not running:
        return

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        score += 1
        label.config(text=f"Score: {score}")
        canvas.delete("food")
        food = Food(canvas)
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction
    opposites = {"up": "down", "down": "up", "left": "right", "right": "left"}
    if new_direction != opposites.get(direction):
        direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False

def game_over():
    global running
    running = False
    canvas.delete(tk.ALL)
    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 - 20,
                       font=("Helvetica", 32), text="GAME OVER!", fill="red")
    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 + 20,
                       font=("Helvetica", 20), text=f"Final Score: {score}", fill="white")
    restart_btn.pack(pady=10)

def restart_game():
    global snake, food, score, direction, running
    canvas.delete(tk.ALL)
    score = 0
    direction = "right"
    label.config(text=f"Score: {score}")
    snake = Snake(canvas)
    food = Food(canvas)
    restart_btn.pack_forget()
    running = True
    next_turn(snake, food)

def set_difficulty(level):
    global SPEED
    if level == "Easy":
        SPEED = 150
    elif level == "Medium":
        SPEED = 100
    elif level == "Hard":
        SPEED = 60
    difficulty_frame.pack_forget()
    start_game()

def start_game():
    global snake, food, running
    running = True
    snake = Snake(canvas)
    food = Food(canvas)
    next_turn(snake, food)

# --- Setup window ---
window = tk.Tk()
window.title("🐍 Snake Game")
window.resizable(False, False)

score = 0
direction = "right"
running = False
SPEED = 100

label = tk.Label(window, text=f"Score: {score}", font=("Arial", 20))
label.pack()

canvas = tk.Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# Center window
window.update()
window.geometry(f"{GAME_WIDTH}x{GAME_HEIGHT + 80}+{(window.winfo_screenwidth()//2) - (GAME_WIDTH//2)}+{(window.winfo_screenheight()//2) - (GAME_HEIGHT//2)}")

# Difficulty selection
difficulty_frame = tk.Frame(window)
difficulty_frame.pack(pady=10)

tk.Label(difficulty_frame, text="Select Difficulty:", font=("Arial", 14)).pack(side="left", padx=10)
for level in ["Easy", "Medium", "Hard"]:
    tk.Button(difficulty_frame, text=level, font=("Arial", 12),
              command=lambda lvl=level: set_difficulty(lvl)).pack(side="left", padx=5)

# Restart button (hidden initially)
restart_btn = tk.Button(window, text="Restart Game", font=("Arial", 14), bg="lightblue", command=restart_game)

# Key bindings
window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))

window.mainloop()
