import turtle
import random
import time

# ================= SCREEN SETUP =================

screen = turtle.Screen()
screen.title("Advanced Snake Game")
screen.bgcolor("#0A0A0A")
screen.setup(width=0.8, height=0.9)
screen.tracer(0)

# ================= BORDER =================

border = turtle.Turtle()
border.hideturtle()
border.speed(0)
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

title_text.write(
    "SNAKE GAME",
    align="center",
    font=("Arial", 28, "bold")
)

# ================= INSTRUCTIONS =================

instruction = turtle.Turtle()
instruction.hideturtle()
instruction.color("white")
instruction.penup()
instruction.goto(0, -340)

instruction.write(
    "Use Arrow Keys To Move",
    align="center",
    font=("Arial", 14, "normal")
)

# ================= GAME CONSTANTS =================

GRID_SIZE = 15
GRID_RANGE = 18 # Number of steps from center to border
BORDER_LIMIT = 280

# ================= SNAKE HEAD =================

head = turtle.Turtle()
head.shape("circle")
head.color("#00FF66")
head.shapesize(1.3, 1.3)
head.penup()
head.goto(0, 0)
head.direction = "stop"

# ================= EYES =================

left_eye = turtle.Turtle()
left_eye.shape("circle")
left_eye.color("black")
left_eye.shapesize(0.25, 0.25)
left_eye.penup()

right_eye = turtle.Turtle()
right_eye.shape("circle")
right_eye.color("black")
right_eye.shapesize(0.25, 0.25)
right_eye.penup()

# ================= FOOD =================

food = turtle.Turtle()
food.penup()

food_types = [
    {"shape": "circle", "color": "#FF4444", "size": 1.2, "points": 1},
    {"shape": "square", "color": "#FFD700", "size": 1.3, "points": 2},
    {"shape": "triangle", "color": "#00BFFF", "size": 1.4, "points": 3},
]

current_food = None

# ================= BODY PARTS =================

parts = []

green_shades = [
    "#66FF99",
    "#55EE88",
    "#44DD77",
    "#33CC66",
    "#22BB55"
]

# ================= SCORE =================

score = 0
high_score = 0

score_text = turtle.Turtle()
score_text.hideturtle()
score_text.speed(0)
score_text.color("white")
score_text.penup()
score_text.goto(0, 295)

# ================= GAME OVER TEXT =================

game_text = turtle.Turtle()
game_text.hideturtle()
game_text.color("red")
game_text.penup()
game_text.goto(0, 0)

# ================= EFFECT TEXT =================

effect_text = turtle.Turtle()
effect_text.hideturtle()
effect_text.color("#FFD700")
effect_text.penup()

# ================= UPDATE SCORE =================

def update_score():

    score_text.clear()

    score_text.write(
        f"SCORE: {score}    HIGH SCORE: {high_score}",
        align="center",
        font=("Courier New", 18, "bold")
    )

update_score()

# ================= GENERATE FOOD =================

def generate_food():

    global current_food

    current_food = random.choice(food_types)

    food.shape(current_food["shape"])
    food.color(current_food["color"])
    food.shapesize(current_food["size"])

    max_attempts = 100
    attempt = 0
    
    while attempt < max_attempts:
        x = random.randint(-GRID_RANGE, GRID_RANGE) * GRID_SIZE
        y = random.randint(-GRID_RANGE, GRID_RANGE) * GRID_SIZE
        
        # Check if the coordinate is occupied by the snake's head
        if head.distance(x, y) < GRID_SIZE:
            attempt += 1
            continue
            
        # Check if the coordinate is occupied by any body part
        occupied = False
        for part in parts:
            if part.distance(x, y) < GRID_SIZE:
                occupied = True
                break
        
        if not occupied:
            food.goto(x, y)
            return
        
        attempt += 1

    # Fallback: If no space found after max attempts, game is likely won or grid is full
    # Reset game or show win message (for now, we'll reset to avoid freeze)
    reset_game()

generate_food()

# ================= FOOD EFFECT =================

def food_effect(x, y, points):

    effect_text.goto(x, y + 20)

    effect_text.clear()

    effect_text.write(
        f"+{points}",
        align="center",
        font=("Arial", 16, "bold")
    )

    screen.update()

    time.sleep(0.2)

    effect_text.clear()

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

screen.listen()

screen.onkeypress(move_up, "Up")
screen.onkeypress(move_down, "Down")
screen.onkeypress(move_left, "Left")
screen.onkeypress(move_right, "Right")

# ================= MOVE FUNCTION =================

def move():

    if head.direction == "up":
        head.sety(head.ycor() + GRID_SIZE)

    if head.direction == "down":
        head.sety(head.ycor() - GRID_SIZE)

    if head.direction == "left":
        head.setx(head.xcor() - GRID_SIZE)

    if head.direction == "right":
        head.setx(head.xcor() + GRID_SIZE)

# ================= UPDATE EYES =================

def update_eyes():

    x = head.xcor()
    y = head.ycor()

    if head.direction == "up":
        left_eye.goto(x - 5, y + 8)
        right_eye.goto(x + 5, y + 8)

    elif head.direction == "down":
        left_eye.goto(x - 5, y - 8)
        right_eye.goto(x + 5, y - 8)

    elif head.direction == "left":
        left_eye.goto(x - 8, y + 5)
        right_eye.goto(x - 8, y - 5)

    elif head.direction == "right":
        left_eye.goto(x + 8, y + 5)
        right_eye.goto(x + 8, y - 5)

    else:
        left_eye.goto(x - 5, y + 8)
        right_eye.goto(x + 5, y + 8)

# ================= RESET GAME =================

def reset_game():

    global score

    time.sleep(1)

    head.goto(0, 0)
    head.direction = "stop"

    left_eye.goto(-1000, -1000)
    right_eye.goto(-1000, -1000)

    for p in parts:
        p.goto(1000, 1000)

    parts.clear()

    game_text.clear()

    game_text.write(
        "GAME OVER\nPress Any Arrow Key To Restart",
        align="center",
        font=("Arial", 24, "bold")
    )

    screen.update()

    time.sleep(1.5)

    game_text.clear()

    score = 0

    update_score()

# ================= MAIN GAME LOOP =================

pulse_size = 1.2
pulse_direction = 0.03

while True:

    # FOOD ANIMATION

    pulse_size += pulse_direction

    if pulse_size > 1.4:
        pulse_direction = -0.03

    if pulse_size < 1.1:
        pulse_direction = 0.03

    food.shapesize(pulse_size)

    food.setheading(food.heading() + 5)

    # BORDER COLLISION

    if (
        head.xcor() > BORDER_LIMIT or
        head.xcor() < -BORDER_LIMIT or
        head.ycor() > BORDER_LIMIT or
        head.ycor() < -BORDER_LIMIT
    ):
        reset_game()

    # FOOD COLLISION

    if head.distance(food) < GRID_SIZE:

        food_effect(
            food.xcor(),
            food.ycor(),
            current_food["points"]
        )

        generate_food()

        # NEW BODY PART

        new_part = turtle.Turtle()

        new_part.shape("circle")
        new_part.color(random.choice(green_shades))
        new_part.shapesize(1.0, 1.0)
        new_part.penup()

        parts.append(new_part)

        # SNAKE COLOR CHANGE

        head.color(random.choice(green_shades))

        # SCORE UPDATE

        score += current_food["points"]

        if score > high_score:
            high_score = score

        update_score()

    # MOVE BODY

    for i in range(len(parts) - 1, 0, -1):

        x = parts[i - 1].xcor()
        y = parts[i - 1].ycor()

        parts[i].goto(x, y)

    if len(parts) > 0:
        parts[0].goto(head.xcor(), head.ycor())

    # MOVE HEAD

    move()

    # UPDATE EYES

    update_eyes()

    # SELF COLLISION

    for p in parts:

        if p.distance(head) < 12:

            reset_game()

    screen.update()

    time.sleep(0.05)