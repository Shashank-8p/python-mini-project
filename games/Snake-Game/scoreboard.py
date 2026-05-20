import turtle
class Scoreboard:
    def __init__(self):
        self.score = 0
        self.level = 1
        self.high_score = 0

        self.display = turtle.Turtle()
        self.display.hideturtle()
        self.display.color("white")
        self.display.penup()
        self.display.goto(0, 320)

        self.update_display()

    def update_display(self):
        self.display.clear()
        self.display.write(
            f"Score: {self.score}  |  Level: {self.level}  |  High Score: {self.high_score}",
            align="center",
            font=("Arial", 18, "normal")
        )

    def increase(self):
        self.score += 1

        # Update high score
        if self.score > self.high_score:
            self.high_score = self.score

        self.update_display()

    def level_up(self):
        self.level += 1
        self.update_display()

    def reset(self):
        self.score = 0
        self.level = 1
        self.update_display()

    def show_message(self, text):
        self.display.goto(0, 0)
        self.display.write(text, align="center", font=("Arial", 30, "bold"))
        self.display.goto(0, 320)
