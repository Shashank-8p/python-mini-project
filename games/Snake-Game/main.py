import turtle
import time
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, COLLISION_DISTANCE, SLEEP_TIME
from snake import Snake
from food import Food
from scoreboard import Scoreboard

class SnakeGame:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.title("Snake Game (Modular OOP)")
        self.screen.bgcolor("black")
        self.screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.screen.tracer(0)

        self._draw_borders()

        self.snake = Snake()
        self.food = Food()
        self.scoreboard = Scoreboard()

        # Keyboard bindings
        self.screen.listen()
        self.screen.onkeypress(self.snake.move_up, "Up")
        self.screen.onkeypress(self.snake.move_down, "Down")
        self.screen.onkeypress(self.snake.move_left, "Left")
        self.screen.onkeypress(self.snake.move_right, "Right")

    def _draw_borders(self):
        box = turtle.Turtle()
        box.hideturtle()
        box.color("white")
        box.pensize(3)
        box.penup()
        box.goto(-300, 300)
        box.pendown()
        for _ in range(4):
            box.forward(600)
            box.right(90)

    def run(self):
        while True:
            self.screen.update()

            if self.snake.check_boundary_collision():
                self.snake.reset()
                self.scoreboard.reset()

            # Check food collision
            if self.snake.head.distance(self.food.item) < COLLISION_DISTANCE:
                self.food.reposition(self.snake)
                self.snake.add_part()
                self.scoreboard.increase()

            self.snake.move()

            # Check body collision
            if self.snake.check_self_collision():
                self.snake.reset()
                self.scoreboard.reset()

            time.sleep(SLEEP_TIME)

if __name__ == "__main__":
    game = SnakeGame()
    try:
        game.run()
    except turtle.Terminator:
        pass
