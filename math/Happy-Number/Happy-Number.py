import tkinter as tk

# ---------------- HAPPY NUMBER LOGIC ---------------- #

print("🔢 Happy Number Checker 🔢")
print("🎯 A happy number eventually reaches 1.\n")

N = int(input("➡️  Enter a number: "))

seen = set()
sequence = []

num = N

while num != 1 and num not in seen:
    seen.add(num)
    sequence.append(num)

    num = sum(int(digit) ** 2 for digit in str(num))

sequence.append(num)

is_happy = (num == 1)

if is_happy:
    print(f"\n✅ {N} is a HAPPY number!")
else:
    print(f"\n❌ {N} is NOT a happy number!")

print("➡️  Sequence:", " → ".join(map(str, sequence)))


# ---------------- TKINTER VISUALIZER ---------------- #

class HappyVisualizer:

    def __init__(self, root):
        self.root = root
        self.root.title("Happy Number Visualizer")
        self.root.geometry("1000x600")
        self.root.configure(bg="#f4f4f4")

        # Frame
        frame = tk.Frame(root, bg="#f4f4f4")
        frame.pack(fill=tk.BOTH, expand=True)

        # Scrollbars
        self.h_scroll = tk.Scrollbar(
            frame,
            orient=tk.HORIZONTAL
        )
        self.h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        self.v_scroll = tk.Scrollbar(
            frame,
            orient=tk.VERTICAL
        )
        self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Canvas
        self.canvas = tk.Canvas(
            frame,
            bg="white",
            xscrollcommand=self.h_scroll.set,
            yscrollcommand=self.v_scroll.set,
            highlightthickness=2,
            highlightbackground="#cccccc"
        )

        self.canvas.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True
        )

        self.h_scroll.config(command=self.canvas.xview)
        self.v_scroll.config(command=self.canvas.yview)

        # Mouse wheel scrolling
        self.canvas.bind_all(
            "<MouseWheel>",
            self.mouse_scroll
        )

    def mouse_scroll(self, event):
        self.canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    def clear_canvas(self):
        self.canvas.delete("all")

    def draw_arrow(self, x1, y1, x2, y2):
        self.canvas.create_line(
            x1,
            y1,
            x2,
            y2,
            arrow=tk.LAST,
            width=3,
            fill="#444"
        )

    def visualize(self, number, sequence, is_happy):

        self.clear_canvas()

        start_x = 100
        y = 250
        spacing = 180

        for i, value in enumerate(sequence):

            x = start_x + i * spacing

            # Colors
            if value == 1:
                color = "#00C853"

            elif i == len(sequence) - 1 and not is_happy:
                color = "#D50000"

            else:
                color = "#1976D2"

            # Circle
            self.canvas.create_oval(
                x - 45,
                y - 45,
                x + 45,
                y + 45,
                fill=color,
                outline=""
            )

            # Number
            self.canvas.create_text(
                x,
                y,
                text=str(value),
                font=("Arial", 16, "bold"),
                fill="white"
            )

            # Arrow
            if i < len(sequence) - 1:

                next_x = start_x + (i + 1) * spacing

                self.draw_arrow(
                    x + 45,
                    y,
                    next_x - 45,
                    y
                )

        # Result text
        result = (
            f"{number} is a HAPPY Number 🎉"
            if is_happy
            else f"{number} is NOT a Happy Number ❌"
        )

        self.canvas.create_text(
            max(500, start_x + len(sequence) * spacing // 2),
            420,
            text=result,
            font=("Arial", 22, "bold"),
            fill="#222"
        )

        # Dynamic scroll region
        self.canvas.config(
            scrollregion=self.canvas.bbox("all")
        )


# ---------------- RUN APP ---------------- #

root = tk.Tk()

app = HappyVisualizer(root)

app.visualize(
    N,
    sequence,
    is_happy
)

root.mainloop()