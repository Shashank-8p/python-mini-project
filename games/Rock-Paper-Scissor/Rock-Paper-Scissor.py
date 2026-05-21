import random

class Rock_Paper_Scissors:
    def __init__(self):
        """Initializes the game state without blocking execution."""
        self.user_score = 0
        self.computer_score = 0
        self.rounds_played = 0 
        # Perfectly mirrors the JS choices array ['rock', 'paper', 'scissors']
        self.choices = ["rock", "paper", "scissors"]

    def users_play(self):
        """Handles a single round of interaction."""
        user_choice = ""
        while user_choice not in self.choices:
            user_choice = input("Enter your choice (rock, paper, or scissors): ").lower()
            if user_choice not in self.choices:
                print("Invalid choice. Please choose rock, paper, or scissors.")

        computer_choice = random.choice(self.choices)
        print(f"Computer chose: {computer_choice}")

        if user_choice == computer_choice:
            print("It's a Tie! 🤝")
            return "tie"
        elif (user_choice == "rock" and computer_choice == "scissors") or \
             (user_choice == "paper" and computer_choice == "rock") or \
             (user_choice == "scissors" and computer_choice == "paper"):
            print("You Win this round! 🎉")
            return "user"
        else:
            print("Computer Wins this round! 🤖")
            return "computer"

    def statistics(self):
        """Displays performance statistics matching the web dashboard metrics."""
        print("\n--- Game Statistics ---")
        print(f"Rounds Played: {self.rounds_played}")
        print(f"Your Score: {self.user_score}")
        print(f"Computer Score: {self.computer_score}")

    def save_game(self):
        """Appends the final game results to a local tracking log."""
        name = input("Enter your name to save the results (optional): ")
        if not name:
            name = "Anonymous"
        result_string = f"Player: {name}, Final Score: {self.user_score} - {self.computer_score} (User-Computer), Rounds: {self.rounds_played}\n"
        try:
            with open("game_results.txt", "a") as f:
                f.write(result_string)
            print("Game results saved successfully.")
        except IOError:
            print("Error: Could not save game results to file.")

    def play_game(self): 
        """Launches the primary interactive gameplay loop."""
        print("Welcome to Rock, Paper, Scissors!")
        while True:
            self.rounds_played += 1
            print(f"\n--- Round {self.rounds_played} ---")
            
            round_winner = self.users_play()

            if round_winner == "user":
                self.user_score += 1
            elif round_winner == "computer":
                self.computer_score += 1

            self.statistics()
            play_again_input = input("Do you want to play again? (yes/no): ").lower()
            if play_again_input != "yes":
                print("\nThanks for playing! Final results:")
                self.statistics()
                self.save_game()
                break

# Standard execution block ensuring clean instantiation
if __name__ == "__main__":
    game = Rock_Paper_Scissors()
    game.play_game()