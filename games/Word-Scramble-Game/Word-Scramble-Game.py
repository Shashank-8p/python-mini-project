#!/usr/bin/env python3
"""
🔤 Word Scramble Game
=====================
A terminal-based word guessing game where players unscramble shuffled letters.

Features:
  - Random word selection from a categorised built-in word list
  - Scrambled letter display
  - Hint system (reveals the word's category)
  - 3 lives per game
  - Score tracking across rounds
  - Zero external dependencies (pure Python)
"""

import random
import time
import os
import sys

# ── Word bank ────────────────────────────────────────────────────────────────

WORD_BANK: dict[str, list[str]] = {
    "🐾 Animals": [
        "elephant", "penguin", "dolphin", "cheetah", "giraffe",
        "kangaroo", "crocodile", "flamingo", "panther", "squirrel",
    ],
    "🍎 Fruits": [
        "mango", "papaya", "cherry", "apricot", "banana",
        "guava", "lychee", "peach", "plum", "strawberry",
    ],
    "🌍 Countries": [
        "brazil", "france", "canada", "japan", "kenya",
        "norway", "mexico", "india", "egypt", "sweden",
    ],
    "🔬 Science": [
        "gravity", "nucleus", "photon", "proton", "molecule",
        "quantum", "enzyme", "plasma", "neuron", "voltage",
    ],
    "🎵 Music": [
        "rhythm", "melody", "chorus", "octave", "guitar",
        "violin", "harmony", "trumpet", "bassoon", "symphony",
    ],
    "🏅 Sports": [
        "cricket", "tennis", "hockey", "soccer", "rowing",
        "karate", "boxing", "cycling", "archery", "fencing",
    ],
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def scramble(word: str) -> str:
    """Shuffle letters until the result differs from the original."""
    letters = list(word)
    for _ in range(100):          # give up after 100 tries (very short words)
        random.shuffle(letters)
        scrambled = "".join(letters)
        if scrambled != word:
            return scrambled
    return "".join(letters)       # best effort


def fancy_scramble(word: str) -> str:
    """Return the scrambled word with spaces between letters for readability."""
    return "  ".join(scramble(word).upper())


def slow_print(text: str, delay: float = 0.03) -> None:
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def draw_lives(lives: int, max_lives: int = 3) -> str:
    return "❤️ " * lives + "🖤 " * (max_lives - lives)


def draw_header(score: int, round_num: int, lives: int) -> None:
    print("╔══════════════════════════════════════════════╗")
    print("║          🔤  W O R D  S C R A M B L E  🔤         ║")
    print("╠══════════════════════════════════════════════╣")
    print(f"║  Round: {round_num:<5}  Score: {score:<6}  Lives: {draw_lives(lives):<14}║")
    print("╚══════════════════════════════════════════════╝")
    print()


# ── Game logic ────────────────────────────────────────────────────────────────

def pick_word() -> tuple[str, str]:
    """Return (word, category)."""
    category = random.choice(list(WORD_BANK))
    word = random.choice(WORD_BANK[category])
    return word, category


def play_round(score: int, round_num: int, lives: int) -> tuple[int, int, bool]:
    """
    Run one round.
    Returns (new_score, new_lives, still_playing).
    """
    word, category = pick_word()
    scrambled = fancy_scramble(word)
    hint_used = False
    attempts = 0
    max_attempts = 3       # attempts before a life is lost

    while attempts < max_attempts:
        clear()
        draw_header(score, round_num, lives)

        print(f"  🔀  Unscramble this word:\n")
        print(f"      ✨  {scrambled}  ✨\n")
        print(f"  Letters: {len(word)}   |   Attempts left this round: {max_attempts - attempts}")
        if hint_used:
            print(f"  💡 Hint: {category}")
        print()
        print("  Commands: [answer] · 'hint' · 'skip' · 'quit'")
        print()

        try:
            raw = input("  ➤  Your guess: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            return score, lives, False

        if raw == "quit":
            return score, lives, False

        if raw == "skip":
            print(f"\n  ⏭️  Skipped! The word was: {word.upper()}")
            time.sleep(1.5)
            return score, lives, True          # no penalty for skip

        if raw == "hint":
            if not hint_used:
                hint_used = True
                print(f"\n  💡 Hint unlocked: {category}")
            else:
                print("\n  💡 You already used your hint!")
            time.sleep(1)
            continue                           # don't count as an attempt

        attempts += 1

        if raw == word:
            bonus = 10 if not hint_used else 5
            score += bonus
            clear()
            draw_header(score, round_num, lives)
            slow_print(f"\n  🎉 Correct! +{bonus} points {'(hint used: half points)' if hint_used else ''}\n")
            time.sleep(1.5)
            return score, lives, True

        else:
            remaining = max_attempts - attempts
            if remaining > 0:
                print(f"\n  ❌ Nope! Try again. ({remaining} attempt{'s' if remaining != 1 else ''} left)")
                time.sleep(1)
            else:
                lives -= 1
                clear()
                draw_header(score, round_num, lives)
                slow_print(f"\n  💔 Out of attempts! The word was: {word.upper()}\n")
                time.sleep(2)
                return score, lives, lives > 0

    # should not reach here
    return score, lives, lives > 0


def game_over_screen(score: int, rounds_played: int) -> None:
    clear()
    print()
    print("  ╔══════════════════════════════════╗")
    print("  ║         💀  GAME  OVER  💀          ║")
    print("  ╚══════════════════════════════════╝")
    print()
    slow_print(f"  You survived {rounds_played} round{'s' if rounds_played != 1 else ''}.")
    slow_print(f"  Final score: {score} points")
    print()
    grade = (
        "🏆 Wordsmith Supreme!" if score >= 80 else
        "🥇 Excellent!"         if score >= 60 else
        "🥈 Good effort!"       if score >= 40 else
        "🥉 Keep practising!"   if score >= 20 else
        "📚 Hit the dictionary!"
    )
    slow_print(f"  {grade}")
    print()


def welcome_screen() -> None:
    clear()
    print()
    slow_print("  ╔══════════════════════════════════════════════╗", 0.005)
    slow_print("  ║       🔤  W O R D  S C R A M B L E  🔤        ║", 0.005)
    slow_print("  ╚══════════════════════════════════════════════╝", 0.005)
    print()
    slow_print("  Unscramble the letters to guess the hidden word!", 0.02)
    print()
    print("  📋  Rules:")
    print("      • 3 lives per game — lose one each time you run out of attempts")
    print("      • 3 attempts per word before losing a life")
    print("      • Type 'hint'  to reveal the word's category  (5 pts instead of 10)")
    print("      • Type 'skip'  to skip a word with no penalty")
    print("      • Type 'quit'  to end the game at any time")
    print()
    input("  Press Enter to start… ")


def main() -> None:
    welcome_screen()

    score = 0
    lives = 3
    round_num = 1

    while lives > 0:
        score, lives, still_playing = play_round(score, round_num, lives)
        if not still_playing:
            break
        round_num += 1

    game_over_screen(score, round_num)

    try:
        again = input("  Play again? (y/n): ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        again = "n"

    if again == "y":
        main()
    else:
        slow_print("\n  Thanks for playing! 👋\n", 0.02)


if __name__ == "__main__":
    main()