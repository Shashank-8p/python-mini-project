import turtle
import random
import time
# ================= SOUND =================
try:
    import pygame
    pygame.mixer.init()
    eat_sound = pygame.mixer.Sound("sounds/eat.wav")
    gameover_sound = pygame.mixer.Sound("sounds/gameover.wav")
    pygame_installed = True
except ImportError:
    pygame_installed = False
    print("⚠️ Warning: pygame module not found. Game will run without sound effects.")


# ================= SCREEN SETUP =================

screen = turtle.Screen()
screen.title("Advanced Snake Game")
screen.bgcolor("#0A0A0A")
screen.setup(width=0.8, height=0.9)
screen.tracer(0)

# ================= BORDER =================

border = turtle.Turtle()
border.hideturtle()
border.color("#00FFAA")
border.pensize(4)
border.penup()
border.goto(-300, 300)
border.pendown()

for _ in range(4):
    border.forward(600)
    border.right(90)

# ================= TITLE =================

title_text = turtle.Turtle()
title_text.hideturtle()
title_text.color("#00FFAA")
title_text.penup()
title_text.goto(0, 330)
title_text.write("SNAKE GAME", align="center", font=("Arial", 28, "bold"))

# ================= TEXT =================

game_text = turtle.Turtle()
game_text.hideturtle()
game_text.color("white")
game_text.penup()
game_text.goto(0, 0)

# ================= GAME CONSTANTS =================

GRID_SIZE = 15
GRID_RANGE = 18
BORDER_LIMIT = 280

# ================= SNAKE =================

head = turtle.Turtle()
head.shape("circle")
head.color("#00FF66")
head.penup()
head.direction = "stop"

parts = []

# ================= FOOD =================

food = turtle.Turtle()
food.penup()

food_types = [
    {"shape": "circle", "color": "#FF4444", "size": 1.2, "points": 1},
    {"shape": "square", "color": "#FFD700", "size": 1.3, "points": 2},
    {"shape": "triangle", "color": "#00BFFF", "size": 1.4, "points": 3},
]

current_food = None

def generate_food():
    global current_food

    current_food = random.choice(food_types)
    food.shape(current_food["shape"])
    food.color(current_food["color"])
    food.shapesize(current_food["size"])

    while True:
        x = random.randint(-GRID_RANGE, GRID_RANGE) * GRID_SIZE
        y = random.randint(-GRID_RANGE, GRID_RANGE) * GRID_SIZE

        occupied = False

        if (x, y) == (int(head.xcor()), int(head.ycor())):
            occupied = True

        for p in parts:
            if (int(p.xcor()), int(p.ycor())) == (x, y):
                occupied = True
                break

        if not occupied:
            food.goto(x, y)
            return

generate_food()

# ================= SCORE =================

score = 0
high_score = 0
level = 1
speed = 0.05

score_text = turtle.Turtle()
score_text.hideturtle()
score_text.color("white")
score_text.penup()
score_text.goto(0, 295)

def update_score():
    score_text.clear()
    score_text.write(
        f"SCORE: {score}   LEVEL: {level}   HIGH SCORE: {high_score}",
        align="center",
        font=("Courier New", 16, "bold")
    )

update_score()

# ================= PAUSE =================

paused = False

def toggle_pause():
    global paused
    paused = not paused

    game_text.clear()

    if paused:
        game_text.write("PAUSED", align="center", font=("Arial", 24, "bold"))

screen.listen()
screen.onkeypress(toggle_pause, "p")

# ================= COUNTDOWN =================

def countdown():
    for text in ["3", "2", "1", "GO!"]:
        game_text.clear()
        game_text.write(text, align="center", font=("Arial", 30, "bold"))
        screen.update()
        time.sleep(1)
    game_text.clear()

countdown()

# ================= CONTROLS =================

def move_up():
    if head.direction != "down":
        head.direction = "up"

def move_down():
    if head.direction != "up":
        head.direction = "down"

def move_left():
    if head.direction != "right":
        head.direction = "left"

def move_right():
    if head.direction != "left":
        head.direction = "right"

screen.onkeypress(move_up, "Up")
screen.onkeypress(move_down, "Down")
screen.onkeypress(move_left, "Left")
screen.onkeypress(move_right, "Right")

# ================= MOVE =================

def move():
    if head.direction == "up":
        head.sety(head.ycor() + GRID_SIZE)
    elif head.direction == "down":
        head.sety(head.ycor() - GRID_SIZE)
    elif head.direction == "left":
        head.setx(head.xcor() - GRID_SIZE)
    elif head.direction == "right":
        head.setx(head.xcor() + GRID_SIZE)

# ================= RESET =================

def reset_game():
    global score, level, speed

    if pygame_installed:
        gameover_sound.play()

    time.sleep(1)

    head.goto(0, 0)
    head.direction = "stop"

    for p in parts:
        p.goto(1000, 1000)
    parts.clear()

    score = 0
    level = 1
    speed = 0.05

    update_score()

# ================= MAIN LOOP =================

while True:

    screen.update()

    if paused:
        continue

    # Border collision
    if (
        head.xcor() > BORDER_LIMIT or
        head.xcor() < -BORDER_LIMIT or
        head.ycor() > BORDER_LIMIT or
        head.ycor() < -BORDER_LIMIT
    ):
        reset_game()

    # Food collision
    if head.distance(food) < GRID_SIZE:

        if pygame_installed:
            eat_sound.play()

        score += current_food["points"]

        if score > high_score:
            high_score = score

        # LEVEL SYSTEM
        if score % 5 == 0:
            level += 1
            speed -= 0.005

            game_text.clear()
            game_text.write(f"LEVEL {level}", align="center", font=("Arial", 24, "bold"))
            screen.update()
            time.sleep(0.5)
            game_text.clear()

        generate_food()

        new_part = turtle.Turtle()
        new_part.shape("circle")
        new_part.color("#66FF99")
        new_part.penup()

        parts.append(new_part)

        update_score()

    # Move body
    for i in range(len(parts) - 1, 0, -1):
        x = parts[i - 1].xcor()
        y = parts[i - 1].ycor()
        parts[i].goto(x, y)

    if parts:
        parts[0].goto(head.xcor(), head.ycor())

    move()

    # Self collision
    for p in parts:
        if p.distance(head) < 12:
            reset_game()

    time.sleep(speed)
