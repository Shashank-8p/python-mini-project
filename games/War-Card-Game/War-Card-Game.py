import random


# =========================
# Card Class
# =========================
class Card:
    def __init__(self, suit, rank, value):
        self.suit = suit
        self.rank = rank
        self.value = value

    def __str__(self):
        return f"{self.rank} of {self.suit}"


# =========================
# Deck Class
# =========================
class Deck:
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]

    ranks = {
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "Jack": 11,
        "Queen": 12,
        "King": 13,
        "Ace": 14
    }

    def __init__(self):
        self.cards = []
        self.create_deck()

    def create_deck(self):
        for suit in self.suits:
            for rank, value in self.ranks.items():
                self.cards.append(Card(suit, rank, value))

    def shuffle_deck(self):
        random.shuffle(self.cards)

    def deal_cards(self):
        mid = len(self.cards) // 2
        return self.cards[:mid], self.cards[mid:]


# =========================
# Player Class
# =========================
class Player:
    def __init__(self, name, cards):
        self.name = name
        self.cards = cards
        self.score = 0

    def play_card(self):
        if self.cards:
            return self.cards.pop(0)
        return None

    def add_point(self):
        self.score += 1


# =========================
# War Game Class
# =========================
class WarGame:
    def __init__(self):
        self.deck = Deck()
        self.player1 = None
        self.player2 = None

    def setup_game(self):
        print("\n===== Welcome to War Card Game =====\n")

        name1 = input("Enter Player 1 Name: ")
        name2 = input("Enter Player 2 Name: ")

        self.deck.shuffle_deck()
        cards1, cards2 = self.deck.deal_cards()

        self.player1 = Player(name1, cards1)
        self.player2 = Player(name2, cards2)

        print("\nDeck shuffled successfully!")
        print("Cards distributed equally to both players.\n")

    def play_round(self, round_number):
        card1 = self.player1.play_card()
        card2 = self.player2.play_card()

        print(f"\n========== Round {round_number} ==========")
        print(f"{self.player1.name} draws: {card1}")
        print(f"{self.player2.name} draws: {card2}")

        if card1.value > card2.value:
            self.player1.add_point()
            print(f"🏆 Round Winner: {self.player1.name}")
        elif card2.value > card1.value:
            self.player2.add_point()
            print(f"🏆 Round Winner: {self.player2.name}")
        else:
            print("🤝 It's a Tie!")

        print(
            f"Current Score -> {self.player1.name}: {self.player1.score} | "
            f"{self.player2.name}: {self.player2.score}"
        )

    def declare_winner(self):
        print("\n========== Final Result ==========")
        print(
            f"{self.player1.name}: {self.player1.score} points\n"
            f"{self.player2.name}: {self.player2.score} points"
        )

        if self.player1.score > self.player2.score:
            print(f"\n🏆 {self.player1.name} wins the game!")
        elif self.player2.score > self.player1.score:
            print(f"\n🏆 {self.player2.name} wins the game!")
        else:
            print("\n🤝 The game ends in a Tie!")

    def start_game(self):
        self.setup_game()

        round_number = 1

        while self.player1.cards and self.player2.cards:
            choice = input(
                f"\nDo you want to play Round {round_number}? (yes/no): "
            ).lower()

            if choice != "yes":
                print("\nGame stopped by user.")
                break

            self.play_round(round_number)
            round_number += 1

        self.declare_winner()


# =========================
# Main Program
# =========================
if __name__ == "__main__":
    game = WarGame()
    game.start_game()