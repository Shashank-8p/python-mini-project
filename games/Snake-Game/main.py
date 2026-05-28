import turtle
import time
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, COLLISION_DISTANCE, SLEEP_TIME
from snake import Snake
from food import Food
from scoreboard import Scoreboard

try:
    import pygame
    pygame_installed = True
except ImportError:
    pygame_installed = False
    print("⚠️ Warning: pygame module not found. Game will run without sound effects.")

class SnakeGame:
    def __init__(self):
        # Game state
        self.paused = False
        self.delay = SLEEP_TIME
        self.level = 1

        # Screen setup
        self.screen = turtle.Screen()
        self.screen.title("Snake Game (Modular OOP)")
        self.screen.bgcolor("black")
        self.screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.screen.tracer(0)

        self._draw_borders()

        # Game objects
        self.snake = Snake()
        self.food = Food()
        self.scoreboard = Scoreboard()

        # Sound setup
        self.pygame_installed = pygame_installed
        if self.pygame_installed:
            try:
                pygame.mixer.init()
                self.eat_sound = pygame.mixer.Sound("sounds/Apple_Eating.mp3")
                self.gameover_sound = pygame.mixer.Sound("sounds/Game_over.mp3")
            except Exception as e:
                print(f"⚠️ Warning: Could not initialize pygame mixer: {e}")
                self.pygame_installed = False

        # Keyboard bindings
        self.screen.listen()
        self.screen.onkeypress(self.snake.move_up, "Up")
        self.screen.onkeypress(self.snake.move_down, "Down")
        self.screen.onkeypress(self.snake.move_left, "Left")
        self.screen.onkeypress(self.snake.move_right, "Right")
        self.screen.onkeypress(self.toggle_pause, "p")   # Pause key

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

    # Countdown before game starts
    def countdown(self):
        for text in ["3", "2", "1", "GO!"]:
            self.scoreboard.show_message(text)
            self.screen.update()
            time.sleep(1)

        self.scoreboard.update_display()

    # Pause toggle
    def toggle_pause(self):
        self.paused = not self.paused

        if self.paused:
            self.scoreboard.show_message("PAUSED")
        else:
            self.scoreboard.update_display()

    def run(self):
        self.countdown()  # Start countdown

        while True:
            self.screen.update()

            # Pause check
            if self.paused:
                continue

            # Boundary collision
            if self.snake.check_boundary_collision():
                if self.pygame_installed:
                    self.gameover_sound.play()
                self.snake.reset()
                self.scoreboard.reset()
                self.delay = SLEEP_TIME
                self.level = 1

            # Food collision
            if self.snake.head.distance(self.food.item) < COLLISION_DISTANCE:
                self.food.reposition(self.snake)
                self.snake.add_part()

                self.scoreboard.increase()
                if self.pygame_installed:
                    self.eat_sound.play()

                # Level system
                if self.scoreboard.score % 5 == 0:
                    self.level += 1
                    self.delay -= 0.01

                    # Optional level message
                    self.scoreboard.show_message(f"LEVEL {self.level}")
                    self.screen.update()
                    time.sleep(0.5)
                    self.scoreboard.update_display()

            # Move snake
            self.snake.move()

            # Self collision
            if self.snake.check_self_collision():
                if self.pygame_installed:
                    self.gameover_sound.play()
                self.snake.reset()
                self.scoreboard.reset()
                self.delay = SLEEP_TIME
                self.level = 1

            # Game speed
            time.sleep(self.delay)


if __name__ == "__main__":
    game = SnakeGame()
    try:
        game.run()
    except turtle.Terminator:
        pass
