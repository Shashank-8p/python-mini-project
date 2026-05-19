import turtle

class Scoreboard:
    def __init__(self):
        self.score = 0
        self.display = turtle.Turtle()
        self.display.hideturtle()
        self.display.color("white")
        self.display.penup()
        self.display.goto(0, 320)
        self.update_display()

    def update_display(self):
        self.display.clear()
        self.display.write(
            f"Score: {self.score}", 
            align="center", 
            font=("Arial", 18, "normal")
        )

    def increase(self):
        self.score += 1
        self.update_display()

    def reset(self):
        self.score = 0
        self.update_display()
