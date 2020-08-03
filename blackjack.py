from cards import Card, Hand, Deck
import games, random

removed = []

def card_sum(hand):
    total = 0
    for card in hand.cards:
        total += card.value
    return total

def has_ace(hand):
    for card in hand.cards:
        if card.rank == "A":
            return True
    return False

def change_ace(hand):
    for x in range(len(hand.cards)):
        if hand.cards[x].value == 11:
            hand.cards[x].value = 1
            break

def natural_bj(hand, hands):
    if hand.cards[0].value + hand.cards[1].value == 21:
        print("You got natural blackjack!\n")
        hand.bank = hand.bank + hand.bet + 15
        removed.append(hand)

def wallet(hands, dealer):
    print("\nHere are people's remaining money and cards:")
    print(dealer)
    for hand in hands:
        print(hand)
        if len(hand.cards)>1:
            if dealer.cards[0].rank!="A":
                natural_bj(hand, hands)

def remove():
    for removes in removed:
        if removes in hands:
            hands.remove(removes)

def output():
    print("\n\nRemoved players:")
    for removes in removed:
        print(removes)
    print("\n\nRemaining players:")
    print(dealer)
    for hand in hands:
        print(hand)


hands = []
num = input("\nHow many players? ")
for i in range(int(num)):
    name = input("Player name: ")
    bank = input("How much money do you have? ")
    hands.append(Hand(name.title(), int(bank)))            
again = None
while again != "n":
    deck = Deck()
    deck.populate()
    deck.shuffle()
    print("\n")
    print(deck)
    dealer = Hand('Dealer')
    deck.give(deck.cards[0], dealer)
    deck.give(deck.cards[0], dealer)
    dealer.cards[1].is_face_up = False
    for removes in removed:
        hands.append(removes)
    removed.clear()
    for hand in hands:
        hand.clear()
        hand.bank = hand.bank - 10
        hand.bet = 10
        hand.insurance = False
    deck.deal(hands, per_hand = 2)
    wallet(hands, dealer)
    remove()
    output()
    if dealer.cards[0].value==10 and dealer.cards[1].value==11:
        dealer.cards[1].is_face_up = True
        output()
        print("Dealer has 21. Round over.")
    else:
        x = 0 
        while x != len(hands):
            if card_sum(hands[x])>21:
                print("You busted!")
                removed.append(hands[x])
            else:
                cont = "y"
                print("\n" + hands[x].owner + ", it's your turn: ")
                if dealer.cards[0].rank=="A": 
                    if (card_sum(hands[x])==21):
                        insurance = input("Do you want even-money insurance? (y/n): ")
                        if insurance == 'y':
                            hands[x].bank = hands[x].bank + 2 * hands[x].bet
                            removed.append(hands[x])
                            cont = "n"
                        else:
                            hands[x].natbj = True
                    else:
                        insurance = input("Do you want insurance? (y/n): ")
                        if insurance == 'y':
                            hands[x].bank = hands[x].bank - 5
                            hands[x].insurance = True
                if cont == "y":
                    if hands[x].cards[0].rank==hands[x].cards[1].rank:
                        choice = input("Do you want to hit, stand, double down, surrender, or split? ")    
                    else:
                        choice = input("Do you want to hit, stand, double down, or surrender? ")
                    if choice == "split":
                        hands.insert(hands.index(hands[x])+1, Hand(hands[x].owner.title(), hands[x].bank - 10))
                        hands[x].bank = hands[x].bank - 10
                        hands[x].give(hands[x].cards[1], hands[x+1])
                        deck.give(deck.cards[0], hands[x])
                        deck.give(deck.cards[0], hands[x+1])
                        print(hands[x])
                        print(hands[x+1])
                        x = x - 1
                        cont = "n"
                    if choice == "surrender":
                        hands[x].bank = hands[x].bank + .5 * hands[x].bet
                        removed.append(hands[x])
                        cont = "n"
                    if choice == "double down": 
                        hands[x].bank = hands[x].bank - hands[x].bet
                        hands[x].bet = 2 * hands[x].bet
                        deck.give(deck.cards[0], hands[x])
                        print(hands[x])
                        if has_ace(hands[x]):
                            while (card_sum(hands[x])>21):
                                change_ace(hands[x])
                        if card_sum(hands[x])>21:
                            print("You busted!")
                            print(hands[x])
                            removed.append(hands[x])
                        cont = "n"
                while cont=="y":
                    if choice == "stand":
                        cont = "n"
                    else:
                        deck.give(deck.cards[0], hands[x])
                        print(hands[x])
                        if has_ace(hands[x]):
                            while (card_sum(hands[x])>21):
                                change_ace(hands[x])
                        if card_sum(hands[x])>21:
                            print("You busted!")
                            print(hands[x])
                            removed.append(hands[x])
                            cont = "n"
                        else:
                            cont = input("Do you want to hit or stand? (y for hit/n for stand): ")
            x = x + 1
        remove()
        dealer.cards[1].is_face_up = True
        while card_sum(dealer)<17:
            deck.give(deck.cards[0], dealer)
            if has_ace(dealer):
                while (card_sum(dealer)>21):
                    change_ace(dealer)
        output()
        if card_sum(dealer)>21:
            print("\nDealer busted!")
            for hand in hands:
                hand.bank = hand.bank + 2 * hand.bet
                print("\n" + hand.owner + ", you have $" + str(hand.bank))
        else:
            for hand in hands:
                if card_sum(hand)>card_sum(dealer):
                    print("\n" + hand.owner + ", you won!")
                    hand.bank = hand.bank + 2 * hand.bet
                    if hand.natbj:
                        hand.bank = hand.bank + 5
                    print("You have $" + str(hand.bank))
                elif card_sum(hand)==card_sum(dealer):
                    print("\n" + hand.owner + ", it's a tie.")
                    hand.bank = hand.bank + hand.bet
                    print("You have $" + str(hand.bank)) 
                else:
                    print("\n" + hand.owner + ", you lost.")
                    if (hand.insurance) and (card_sum(dealer)==21): 
                        hand.bank = hand.bank + hand.bet
                    print("You have $" + str(hand.bank)) 
            
    again = games.ask_yes_no("\nDo you want to play again? (y/n): ")

