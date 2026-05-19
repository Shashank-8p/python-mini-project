import random
import math
import time

# ─────────────────────────────────────────
#  🎮 Tic Tac Toe — Smart AI Edition
# ─────────────────────────────────────────

EMPTY = "⬜"
X = "❌"
O = "⭕"


# ─────────────────────────────────────────
# BOARD FUNCTIONS
# ─────────────────────────────────────────

def create_board():
    return [EMPTY] * 9


def display_board(board):
    print()
    for i in range(0, 9, 3):
        print(f"  {board[i]}  {board[i+1]}  {board[i+2]}")
    print()


def display_position_guide():
    print("\n  📌 Position guide:")
    for i in range(1, 10, 3):
        print(f"  {i}  {i+1}  {i+2}")
    print()


def available_moves(board):
    return [i for i, cell in enumerate(board) if cell == EMPTY]


# ─────────────────────────────────────────
# GAME LOGIC
# ─────────────────────────────────────────

def check_winner(board, symbol):
    wins = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],

        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],

        [0, 4, 8],
        [2, 4, 6]
    ]

    return any(
        board[a] == board[b] == board[c] == symbol
        for a, b, c in wins
    )


def check_draw(board):
    return all(cell != EMPTY for cell in board)


# ─────────────────────────────────────────
# PLAYER INPUT
# ─────────────────────────────────────────

def get_player_move(board, symbol, name):
    while True:
        try:
            pos = int(input(
                f"  {symbol} {name}'s turn!\n"
                f"  ➡️ Enter position (1-9): "
            ))

            if pos < 1 or pos > 9:
                print("  ⚠️ Enter a number between 1 and 9.\n")

            elif board[pos - 1] != EMPTY:
                print("  ⚠️ Position already taken.\n")

            else:
                return pos - 1

        except ValueError:
            print("  ⚠️ Invalid input.\n")


# ─────────────────────────────────────────
# EASY AI
# ─────────────────────────────────────────

def easy_ai(board):
    return random.choice(available_moves(board))


# ─────────────────────────────────────────
# MEDIUM AI
# ─────────────────────────────────────────

def medium_ai(board):
    # Try to win
    for move in available_moves(board):
        board[move] = O

        if check_winner(board, O):
            board[move] = EMPTY
            return move

        board[move] = EMPTY

    # Block player win
    for move in available_moves(board):
        board[move] = X

        if check_winner(board, X):
            board[move] = EMPTY
            return move

        board[move] = EMPTY

    # Otherwise random
    return random.choice(available_moves(board))


# ─────────────────────────────────────────
# HARD AI (MINIMAX)
# ─────────────────────────────────────────

def minimax(board, depth, is_maximizing):

    if check_winner(board, O):
        return 1

    if check_winner(board, X):
        return -1

    if check_draw(board):
        return 0

    if is_maximizing:
        best_score = -math.inf

        for move in available_moves(board):
            board[move] = O

            score = minimax(board, depth + 1, False)

            board[move] = EMPTY

            best_score = max(score, best_score)

        return best_score

    else:
        best_score = math.inf

        for move in available_moves(board):
            board[move] = X

            score = minimax(board, depth + 1, True)

            board[move] = EMPTY

            best_score = min(score, best_score)

        return best_score


def hard_ai(board):
    best_score = -math.inf
    best_move = None

    for move in available_moves(board):
        board[move] = O

        score = minimax(board, 0, False)

        board[move] = EMPTY

        if score > best_score:
            best_score = score
            best_move = move

    return best_move


# ─────────────────────────────────────────
# AI CONTROLLER
# ─────────────────────────────────────────

def get_computer_move(board, difficulty):

    if difficulty == "easy":
        return easy_ai(board)

    elif difficulty == "medium":
        return medium_ai(board)

    else:
        return hard_ai(board)


# ─────────────────────────────────────────
# GAME MODE
# ─────────────────────────────────────────

def choose_difficulty():
    while True:

        print("\n  🎯 Choose Difficulty:")
        print("  1️⃣ Easy")
        print("  2️⃣ Medium")
        print("  3️⃣ Hard")

        choice = input("  ➡️ Enter choice (1/2/3): ").strip()

        if choice == "1":
            return "easy"

        elif choice == "2":
            return "medium"

        elif choice == "3":
            return "hard"

        else:
            print("  ⚠️ Invalid choice.\n")


def play_vs_computer():

    board = create_board()

    difficulty = choose_difficulty()

    print(f"\n  👤 You = {X}  |  🤖 Computer = {O}")
    print(f"  🎯 Difficulty: {difficulty.upper()}")

    display_position_guide()

    while True:

        # PLAYER TURN
        display_board(board)

        move = get_player_move(board, X, "You")

        board[move] = X

        if check_winner(board, X):
            display_board(board)
            print("  🎉 You win! 🏆\n")
            return

        if check_draw(board):
            display_board(board)
            print("  🤝 It's a draw!\n")
            return

        # COMPUTER TURN
        print("\n  🤖 Computer is thinking...")
        time.sleep(1)

        comp_move = get_computer_move(board, difficulty)

        board[comp_move] = O

        print(f"  🤖 Computer chose position {comp_move + 1}")

        if check_winner(board, O):
            display_board(board)
            print("  😔 Computer wins!\n")
            return

        if check_draw(board):
            display_board(board)
            print("  🤝 It's a draw!\n")
            return


# ─────────────────────────────────────────
# TWO PLAYER MODE
# ─────────────────────────────────────────

def play_two_players():

    board = create_board()

    players = [
        {"name": "Player 1", "symbol": X},
        {"name": "Player 2", "symbol": O}
    ]

    print(f"\n  👤 Player 1 = {X} | Player 2 = {O}")

    display_position_guide()

    turn = 0

    while True:

        display_board(board)

        player = players[turn % 2]

        move = get_player_move(
            board,
            player["symbol"],
            player["name"]
        )

        board[move] = player["symbol"]

        if check_winner(board, player["symbol"]):
            display_board(board)

            print(
                f"  🎉 {player['name']} wins! 🏆\n"
            )

            return

        if check_draw(board):
            display_board(board)
            print("  🤝 It's a draw!\n")
            return

        turn += 1


# ─────────────────────────────────────────
# MENU
# ─────────────────────────────────────────

def choose_mode():

    while True:

        print("\n  Choose mode:")
        print("  1️⃣ 2 Players")
        print("  2️⃣ vs Computer")

        choice = input(
            "  ➡️ Enter choice (1/2): "
        ).strip()

        if choice == "1":
            return "two"

        elif choice == "2":
            return "computer"

        else:
            print("  ⚠️ Invalid choice.\n")


def play_again():

    while True:

        answer = input(
            "  🔄 Play again? (y/n): "
        ).strip().lower()

        if answer in ("y", "yes"):
            return True

        elif answer in ("n", "no"):
            return False

        else:
            print("  ⚠️ Enter y or n.\n")


# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────

def main():

    print("\n" + "=" * 42)
    print("      🎮 TIC TAC TOE — SMART AI")
    print("=" * 42)

    while True:

        mode = choose_mode()

        if mode == "two":
            play_two_players()

        else:
            play_vs_computer()

        if not play_again():
            print("\n  👋 Thanks for playing!\n")
            break


if __name__ == "__main__":
    main()
