import random
import os
import json
import time
import copy

EMPTY = " "
X = "X"
O = "O"

SAVE_FILE = "tic_tac_toe_save.json"
WINS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6)
]

while True:
    os.system("cls" if os.name == "nt" else "clear")
    print("\033[96m\033[1m")
    print("╔══════════════════════════════════════╗")
    print("║       🎮  TIC  TAC  TOE  🎮          ║")
    print("╚══════════════════════════════════════╝")
    print("\033[0m")

    print("\033[1m\n  Choose Game Mode:\033[0m")
    print("  1 → Two Players")
    print("  2 → vs Computer")

    while True:
        mode = input("\n  ➜ Your choice (1/2): ").strip()
        if mode in ["1", "2"]:
            break
        print("\033[93m  ⚠ Enter 1 or 2.\033[0m")

    difficulty = "easy"
    if mode == "2":
        print("\033[1m\n  Choose Difficulty:\033[0m")
        print("  1 → Easy")
        print("  2 → Medium")
        print("  3 → Hard")
        while True:
            diff_choice = input("\n  ➜ Your choice (1/2/3): ").strip()
            if diff_choice == "1":
                difficulty = "easy"
                break
            elif diff_choice == "2":
                difficulty = "medium"
                break
            elif diff_choice == "3":
                difficulty = "hard"
                break
            print("\033[93m  ⚠ Enter 1, 2 or 3.\033[0m")

    os.system("cls" if os.name == "nt" else "clear")
    if mode == "1":
        p1_name = input("\033[1m  Player 1 name: \033[0m").strip() or "Player 1"
        p2_name = input("\033[1m  Player 2 name: \033[0m").strip() or "Player 2"
        players = [
            {"name": p1_name, "symbol": X, "is_human": True},
            {"name": p2_name, "symbol": O, "is_human": True},
        ]
    else:
        p1_name = input("\033[1m  Your name: \033[0m").strip() or "You"
        players = [
            {"name": p1_name, "symbol": X, "is_human": True},
            {"name": "Computer", "symbol": O, "is_human": False},
        ]

    scores = {"p1": 0, "p2": 0, "draws": 0}

    print("\033[1m\n  Best of how many rounds?\033[0m")
    print("  1 → 1 round")
    print("  2 → Best of 3")
    print("  3 → Best of 5")

    while True:
        rc = input("\n  ➜ Your choice (1/2/3): ").strip()
        if rc in ["1", "2", "3"]:
            break
        print("\033[93m  ⚠ Enter 1, 2 or 3.\033[0m")

    max_rounds = {"1": 1, "2": 3, "3": 5}[rc]
    rounds_played = 0

    while rounds_played < max_rounds:
        board = [EMPTY] * 9
        turn = 0
        undo_stack = []
        redo_stack = []
        move_history = []
        round_over = False
        winner = None

        while not round_over:
            os.system("cls" if os.name == "nt" else "clear")
            print("\033[96m\033[1m")
            print("╔══════════════════════════════════════╗")
            print("║       🎮  TIC  TAC  TOE  🎮          ║")
            print("╚══════════════════════════════════════╝")
            print("\033[0m")

            print("\033[1m  ┌─── SCOREBOARD ───────────────┐\033[0m")
            print(f"  │  \033[91m{players[0]['name']:<20}\033[0m \033[1m{scores['p1']:>3}\033[0m  │")
            print(f"  │  \033[94m{players[1]['name']:<20}\033[0m \033[1m{scores['p2']:>3}\033[0m  │")
            print(f"  │  {'Draws':<20} \033[1m{scores['draws']:>3}\033[0m  │")
            print("\033[1m  └───────────────────────────────┘\033[0m\n")

            # Format board
            formatted = []
            for i in range(9):
                if board[i] == X:
                    formatted.append("\033[1m\033[91m X \033[0m")
                elif board[i] == O:
                    formatted.append("\033[1m\033[94m O \033[0m")
                else:
                    formatted.append(f"\033[2m {i+1} \033[0m")
            
            print(f"  {formatted[0]}│{formatted[1]}│{formatted[2]}")
            print("  ───┼───┼───")
            print(f"  {formatted[3]}│{formatted[4]}│{formatted[5]}")
            print("  ───┼───┼───")
            print(f"  {formatted[6]}│{formatted[7]}│{formatted[8]}\n")

            current = players[turn % 2]

            if current["is_human"]:
                print("\033[2m  Commands:\033[0m")
                print("\033[2m  u → undo, r → redo, s → save, l → load, h → history\033[0m")
                print("\033[2m  Enter → continue normally\n\033[0m")
                
                command = input("\033[2m  Optional command: \033[0m").strip().lower()
                
                if command == "u":
                    if undo_stack:
                        redo_stack.append(copy.deepcopy(board))
                        board = undo_stack.pop()
                        if move_history:
                            move_history.pop()
                        turn -= 1
                        if mode == "2":  # Undo computer move too
                            if undo_stack:
                                redo_stack.append(copy.deepcopy(board))
                                board = undo_stack.pop()
                                if move_history:
                                    move_history.pop()
                                turn -= 1
                        continue
                    else:
                        print("\033[93m\n  ⚠ Nothing to undo.\n\033[0m")
                        time.sleep(1.2)
                        continue
                elif command == "r":
                    if redo_stack:
                        undo_stack.append(copy.deepcopy(board))
                        board = redo_stack.pop()
                        turn += 1
                        if mode == "2" and redo_stack:
                            undo_stack.append(copy.deepcopy(board))
                            board = redo_stack.pop()
                            turn += 1
                        continue
                    else:
                        print("\033[93m\n  ⚠ Nothing to redo.\n\033[0m")
                        time.sleep(1.2)
                        continue
                elif command == "s":
                    try:
                        with open(SAVE_FILE, "w") as f:
                            json.dump({"board": board, "scores": scores, "move_history": move_history, "turn": turn}, f, indent=4)
                        print("\033[92m\033[1m\n  💾 Game saved successfully!\n\033[0m")
                    except Exception:
                        print("\033[93m\n  ⚠ Error saving game.\n\033[0m")
                    time.sleep(1.2)
                    continue
                elif command == "l":
                    if not os.path.exists(SAVE_FILE):
                        print("\033[93m\033[1m\n  ⚠ No saved game found.\n\033[0m")
                    else:
                        try:
                            with open(SAVE_FILE, "r") as f:
                                data = json.load(f)
                            board = data["board"]
                            scores.update(data["scores"])
                            move_history = data["move_history"]
                            turn = data["turn"]
                            undo_stack.clear()
                            redo_stack.clear()
                            print("\033[92m\033[1m\n  ✅ Saved game loaded!\n\033[0m")
                        except Exception:
                            print("\033[93m\n  ⚠ Error loading game.\n\033[0m")
                    time.sleep(1.2)
                    continue
                elif command == "h":
                    print("\033[1m\n  📜 MATCH HISTORY\n\033[0m")
                    if not move_history:
                        print("\033[93m  ⚠ No moves recorded.\n\033[0m")
                    else:
                        for idx, m in enumerate(move_history, start=1):
                            print(f"  {idx}. {m['player']} → position {m['position']}")
                    input("\n  Press Enter to continue...")
                    continue

                sym_colored = "\033[91m" + current["symbol"] + "\033[0m" if current["symbol"] == X else "\033[94m" + current["symbol"] + "\033[0m"
                
                valid_move = False
                while not valid_move:
                    try:
                        raw = input(f"  {sym_colored} \033[1m{current['name']}\033[0m → enter position (1-9): ").strip()
                        pos = int(raw)
                        if not 1 <= pos <= 9:
                            print("\033[93m  ⚠ Enter number from 1 to 9.\n\033[0m")
                        elif board[pos - 1] != EMPTY:
                            print("\033[93m  ⚠ Cell already occupied.\n\033[0m")
                        else:
                            move = pos - 1
                            valid_move = True
                    except ValueError:
                        print("\033[93m  ⚠ Please enter valid number.\n\033[0m")
            else:
                print(f"  🤖 \033[1m{current['name']}\033[0m is thinking", end="", flush=True)
                for _ in range(3):
                    time.sleep(0.35)
                    print(".", end="", flush=True)
                print()
                time.sleep(0.2)
                
                avail = [i for i, c in enumerate(board) if c == EMPTY]
                move = -1
                
                if difficulty == "easy":
                    move = random.choice(avail)
                else:
                    opponent = X if current["symbol"] == O else O
                    # Try to win
                    for m in avail:
                        board[m] = current["symbol"]
                        win = False
                        for a, b, c in WINS:
                            if board[a] == board[b] == board[c] == current["symbol"]: win = True
                        board[m] = EMPTY
                        if win:
                            move = m
                            break
                    
                    if move == -1:
                        # Try to block
                        for m in avail:
                            board[m] = opponent
                            win = False
                            for a, b, c in WINS:
                                if board[a] == board[b] == board[c] == opponent: win = True
                            board[m] = EMPTY
                            if win:
                                move = m
                                break
                                
                    if move == -1:
                        if difficulty == "hard":
                            if board[4] == EMPTY: move = 4
                            elif board[0] == opponent and board[8] == EMPTY: move = 8
                            elif board[8] == opponent and board[0] == EMPTY: move = 0
                            elif board[2] == opponent and board[6] == EMPTY: move = 6
                            elif board[6] == opponent and board[2] == EMPTY: move = 2
                            else:
                                for p in [0, 2, 6, 8, 1, 3, 5, 7]:
                                    if board[p] == EMPTY:
                                        move = p
                                        break
                        else:
                            # Medium
                            for p in [4, 0, 2, 6, 8, 1, 3, 5, 7]:
                                if board[p] == EMPTY:
                                    move = p
                                    break
                
                print(f"  🤖 {current['name']} chose position \033[1m{move + 1}\033[0m\n")
                time.sleep(0.5)

            undo_stack.append(copy.deepcopy(board))
            redo_stack.clear()
            
            board[move] = current["symbol"]
            move_history.append({"player": current["symbol"], "position": move + 1})
            
            # Check win
            has_won = False
            for a, b, c in WINS:
                if board[a] == board[b] == board[c] == current["symbol"]:
                    has_won = True
                    break
            
            if has_won:
                os.system("cls" if os.name == "nt" else "clear")
                print("\033[96m\033[1m")
                print("╔══════════════════════════════════════╗")
                print("║       🎮  TIC  TAC  TOE  🎮          ║")
                print("╚══════════════════════════════════════╝")
                print("\033[0m")
                
                formatted = []
                for i in range(9):
                    if board[i] == X: formatted.append("\033[1m\033[91m X \033[0m")
                    elif board[i] == O: formatted.append("\033[1m\033[94m O \033[0m")
                    else: formatted.append(f"\033[2m {i+1} \033[0m")
                print(f"  {formatted[0]}│{formatted[1]}│{formatted[2]}")
                print("  ───┼───┼───")
                print(f"  {formatted[3]}│{formatted[4]}│{formatted[5]}")
                print("  ───┼───┼───")
                print(f"  {formatted[6]}│{formatted[7]}│{formatted[8]}\n")
                
                print(f"\033[92m\033[1m  🏆 {current['name']} wins this round!\n\033[0m")
                
                winner = "p1" if turn % 2 == 0 else "p2"
                round_over = True
            
            # Check draw
            elif EMPTY not in board:
                os.system("cls" if os.name == "nt" else "clear")
                print("\033[96m\033[1m")
                print("╔══════════════════════════════════════╗")
                print("║       🎮  TIC  TAC  TOE  🎮          ║")
                print("╚══════════════════════════════════════╝")
                print("\033[0m")
                
                formatted = []
                for i in range(9):
                    if board[i] == X: formatted.append("\033[1m\033[91m X \033[0m")
                    elif board[i] == O: formatted.append("\033[1m\033[94m O \033[0m")
                    else: formatted.append(f"\033[2m {i+1} \033[0m")
                print(f"  {formatted[0]}│{formatted[1]}│{formatted[2]}")
                print("  ───┼───┼───")
                print(f"  {formatted[3]}│{formatted[4]}│{formatted[5]}")
                print("  ───┼───┼───")
                print(f"  {formatted[6]}│{formatted[7]}│{formatted[8]}\n")
                
                print("\033[93m\033[1m  🤝 It's a draw!\n\033[0m")
                winner = "draw"
                round_over = True

            turn += 1

            if round_over:
                print("\033[1m\n  📜 MATCH HISTORY\n\033[0m")
                for idx, m in enumerate(move_history, start=1):
                    print(f"  {idx}. {m['player']} → position {m['position']}")
                print()
                time.sleep(1.5)

        if winner == "p1": scores["p1"] += 1
        elif winner == "p2": scores["p2"] += 1
        else: scores["draws"] += 1
        rounds_played += 1

    os.system("cls" if os.name == "nt" else "clear")
    print("\033[96m\033[1m")
    print("╔══════════════════════════════════════╗")
    print("║       🎮  TIC  TAC  TOE  🎮          ║")
    print("╚══════════════════════════════════════╝")
    print("\033[0m")

    print("\033[1m  ┌─── FINAL SCOREBOARD ─────────┐\033[0m")
    print(f"  │  \033[91m{players[0]['name']:<20}\033[0m \033[1m{scores['p1']:>3}\033[0m  │")
    print(f"  │  \033[94m{players[1]['name']:<20}\033[0m \033[1m{scores['p2']:>3}\033[0m  │")
    print(f"  │  {'Draws':<20} \033[1m{scores['draws']:>3}\033[0m  │")
    print("\033[1m  └──────────────────────────────┘\033[0m\n")

    if scores["p1"] > scores["p2"]:
        print(f"\033[92m\033[1m  🏆 {players[0]['name']} wins the match!\n\033[0m")
    elif scores["p2"] > scores["p1"]:
        print(f"\033[92m\033[1m  🏆 {players[1]['name']} wins the match!\n\033[0m")
    else:
        print("\033[93m\033[1m  🤝 Match tied!\n\033[0m")

    while True:
        again = input("  ➜ Play again? (y/n): ").strip().lower()
        if again in ["y", "n"]:
            break
        print("\033[93m  ⚠ Enter 'y' or 'n'.\033[0m")

    if again == "n":
        os.system("cls" if os.name == "nt" else "clear")
        print("\033[96m\033[1m\n  👋 Thanks for playing!\n\033[0m")
        break