import random

deck = [
    "A♠️", "2♠️", "3♠️", "4♠️", "5♠️", "6♠️", "7♠️", "8♠️", "9♠️", "10♠️", "J♠️", "Q♠️", "K♠️",

    "A♥️", "2♥️", "3♥️", "4♥️", "5♥️", "6♥️", "7♥️", "8♥️", "9♥️", "10♥️", "J♥️", "Q♥️", "K♥️",

    "A♦️", "2♦️", "3♦️", "4♦️", "5♦️", "6♦️", "7♦️", "8♦️", "9♦️", "10♦️", "J♦️", "Q♦️", "K♦️",

    "A♣️", "2♣️", "3♣️", "4♣️", "5♣️", "6♣️", "7♣️", "8♣️", "9♣️", "10♣️", "J♣️", "Q♣️", "K♣️"
]

random.shuffle(deck)

player_hand = []
dealer_hand = []

player_cards = []
dealer_cards = []


def calculate(hand):
    count = 0
    aces = 0
    for value in hand:
        count += value
        if value == 1:
            aces += 1
            
    while aces > 0 and count + 10 <= 21:
        count += 10
        aces -= 1

    return count

def check(rank):
    if rank in ['Q','K','J']:
        return 10
    elif rank == 'A':
         return 1
    else:
        return int(rank)
    
def player_draws():
    card = deck.pop() # take a card from deck

    player_cards.append(card)

    rank = card[:-2] # extract Rank

    rank = check(rank) # validate the rank into numbers

    player_hand.append(rank)



def dealer_draws():
    card = deck.pop()

    dealer_cards.append(card)

    rank = card[:-2]

    rank = check(rank)

    dealer_hand.append(rank)


player_draws()
dealer_draws()

player_draws()
dealer_draws()


player_count = calculate(player_hand)
dealer_count = calculate(dealer_hand)


player_turn = True

while player_turn:

    choice = input("hit or Stand: ").lower()

    match choice:
        case "hit":
            player_draws()
            player_count = calculate(player_hand)
            
            print("player cards", player_cards)
            print("player_count", player_count)

            if player_count > 21:
                print("Bust! player lose!")
                player_turn = False
                exit()

        case "stand":
            player_count = calculate(player_hand)
            
            print("player cards", player_cards)
            print("player_count", player_count)
            print("player stands...")
            break
            

while dealer_count < 17:
    dealer_draws()

    dealer_count = calculate(dealer_hand)


# final result

if dealer_count > 21:
    print("dealer Bust! player wins!")
elif player_count == dealer_count:
    print("draw!")
elif player_count > dealer_count:
    print("player wins!")
else:
    print("dealer wins!")

print("dealer cards", dealer_cards)
print("player cards", player_cards)


print("dealer_count", dealer_count, " \n player_count", player_count)


