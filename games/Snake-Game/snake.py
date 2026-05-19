import turtle
import time
from constants import MOVE_DISTANCE, BOUNDARY, BODY_COLLISION_DISTANCE

class Snake:
    def __init__(self):
        self.head = turtle.Turtle()
        self.head.shape("square")
        self.head.color("green")
        self.head.penup()
        self.head.direction = "stop"
        self.parts = []

    def move_up(self):
        if self.head.direction != "down":
            self.head.direction = "up"

    def move_down(self):
        if self.head.direction != "up":
            self.head.direction = "down"

    def move_left(self):
        if self.head.direction != "right":
            self.head.direction = "left"

    def move_right(self):
        if self.head.direction != "left":
            self.head.direction = "right"

    def move(self):
        for i in range(len(self.parts) - 1, 0, -1):
            x = self.parts[i - 1].xcor()
            y = self.parts[i - 1].ycor()
            self.parts[i].goto(x, y)

        if len(self.parts) > 0:
            self.parts[0].goto(self.head.xcor(), self.head.ycor())

        if self.head.direction == "up":
            self.head.sety(self.head.ycor() + MOVE_DISTANCE)
        if self.head.direction == "down":
            self.head.sety(self.head.ycor() - MOVE_DISTANCE)
        if self.head.direction == "left":
            self.head.setx(self.head.xcor() - MOVE_DISTANCE)
        if self.head.direction == "right":
            self.head.setx(self.head.xcor() + MOVE_DISTANCE)

    def add_part(self):
        new_part = turtle.Turtle()
        new_part.shape("square")
        new_part.color("lightgreen")
        new_part.penup()
        self.parts.append(new_part)

    def check_boundary_collision(self) -> bool:
        return (
            self.head.xcor() > BOUNDARY or
            self.head.xcor() < -BOUNDARY or
            self.head.ycor() > BOUNDARY or
            self.head.ycor() < -BOUNDARY
        )

    def check_self_collision(self) -> bool:
        for p in self.parts:
            if p.distance(self.head) < BODY_COLLISION_DISTANCE:
                return True
        return False

    def reset(self):
        time.sleep(1)
        self.head.goto(0, 0)
        self.head.direction = "stop"
        for p in self.parts:
            p.goto(1000, 1000)
        self.parts.clear()
