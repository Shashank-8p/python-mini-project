import random
import time
import os

emojis = ["🍎", "🚗", "⚽", "🐍", "🎧", "🔥", "🌈", "🚀"]
HIGH_SCORE_FILE = "highscore.txt"

while True:
    print("\n🎮 Welcome to Emoji Memory Game!")

    if not os.path.exists(HIGH_SCORE_FILE):
        try:
            with open(HIGH_SCORE_FILE, "w") as file:
                file.write("0")
        except Exception:
            pass

    high_score = 0
    try:
        with open(HIGH_SCORE_FILE, "r") as file:
            high_score = int(file.read().strip() or "0")
    except Exception:
        high_score = 0

    print(f"🏅 High Score: {high_score}\n")

    print("🎯 Select Difficulty")
    print("1. Easy (5 sec)")
    print("2. Medium (4 sec)")
    print("3. Hard (2 sec)")

    while True:
        choice = input("Enter choice (1/2/3): ").strip()
        if choice in ['1', '2', '3']:
            break
        print("⚠️ Invalid input. Enter 1, 2, or 3.")

    display_time = 4
    if choice == "1":
        display_time = 5
    elif choice == "3":
        display_time = 2

    print("\n⏳ Get Ready!")
    for i in range(3, 0, -1):
        print(i)
        time.sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')

    score = 0
    level = 1

    while True:
        sequence = random.choices(emojis, k=level + 2)

        print("🧠 MEMORIZE THESE EMOJIS:")
        print(" ".join(sequence))

        time.sleep(display_time)
        os.system('cls' if os.name == 'nt' else 'clear')

        user_input_raw = input("Type the emojis in order (separated by spaces):\n> ").strip()
        user_input = [emoji.strip() for emoji in user_input_raw.split()]

        if not user_input:
            print("⚠️ Empty input detected!")
            print("❌ Wrong!")
            print("Correct sequence was:", " ".join(sequence))
            break

        if user_input == sequence:
            score += level * 10
            print("✅ Correct!")
            level += 1
            print(f"🏆 Score: {score}\n")
        else:
            print("❌ Wrong!")
            print("Correct sequence was:", " ".join(sequence))
            break

    print("\n🎯 Game Over!")
    print(f"🏆 Final Score: {score}")

    if score > high_score:
        print("🔥 NEW HIGH SCORE!")
        try:
            with open(HIGH_SCORE_FILE, "w") as file:
                file.write(str(score))
        except Exception:
            print("⚠️ Could not save high score.")
    else:
        print(f"🏅 High Score remains: {high_score}")

    while True:
        replay = input("\nPlay again? (y/n): ").strip().lower()
        if replay in ['y', 'yes', 'n', 'no']:
            break
        print("⚠️ Invalid input. Please enter 'y' or 'n'.")

    if replay in ['n', 'no']:
        print("👋 Thanks for playing!")
        break