import turtle
import random
from constants import COLLISION_DISTANCE
from snake import Snake

class Food:
    """Manages the food item spawning."""
    def __init__(self):
        self.item = turtle.Turtle()
        self.item.shape("circle")
        self.item.color("red")
        self.item.penup()
        self.item.goto(0, 100)

    def reposition(self, snake: Snake):
        attempts = 0
        while attempts < 100:
            x = random.randint(-14, 14) * 20
            y = random.randint(-14, 14) * 20
            overlaps = False
            
            if snake.head.distance(x, y) < COLLISION_DISTANCE:
                overlaps = True
            for p in snake.parts:
                if p.distance(x, y) < COLLISION_DISTANCE:
                    overlaps = True
                    break
            
            if not overlaps:
                self.item.goto(x, y)
                break
            attempts += 1

        if attempts >= 100:
            self.item.goto(2000, 2000)
