import random

class Card:
    def __init__(self, value):
        self.value = value

class Shoe:
    def __init__(self, decks):
        self.cards = [
            Card(v) for v in 4*decks*["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        ]
        random.shuffle(self.cards)

        self.history = {"A": 0, "2": 0, "3": 0, "4": 0,
                        "5": 0, "6": 0, "7": 0, "8": 0,
                        "9": 0, "10": 0, "J": 0, "Q": 0, "K": 0}

    def pull_card(self):
        if len(self.cards) >= 1:
            new_card = self.cards.pop(0)
            self.history[new_card.value] += 1
            return new_card.value

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.hand_type = 'Hard'

    def add_card(self, card):
        self.cards.append(card)

    def calculate_value(self):
        self.value = 0
        has_ace = False
        for card in self.cards:
            if card.isnumeric():
                self.value += int(card)
            else:
                if card == "A":
                    has_ace = True
                    self.hand_type = 'Soft'
                    self.value += 11
                else:
                    self.value += 10

            if has_ace and self.value > 21:
                self.value -= 10
                self.hand_type = 'Hard'

    def get_value(self):
        self.calculate_value()
        return self.value

    def display(self):
        for card in self.cards:
            print(card)
        print("Total Value", self.get_value())

class Game:
    def __init__(self, decks, pen):
        self.decks = decks
        self.pen = pen

    def play(self):
        playing = True
        self.shoe = Shoe(self.decks)

        while playing:
            #Reshuffle the shoe if it has been penetrated
            if False:
                self.shoe = Shoe(self.decks)
            self.p_hand = [Hand()]
            self.d_hand = Hand()

            for i in range(2):
                self.p_hand[0].add_card(self.shoe.pull_card())
                self.d_hand.add_card(self.shoe.pull_card())

            print("Player hand:")
            self.p_hand[0].display()
            print("Dealer hand:")
            self.d_hand.display()

            game_over = False
            while not game_over:
                p_bj, d_bj = self.check_for_blackjack()
                if p_bj or d_bj:
                    game_over = True
                    self.show_blackjack_results(p_bj, d_bj)
                    continue

            #Decision matrix comes in here - you know if the hand is soft, hard and you know what you have
            #The decision output SHOULD COME HERE
            #Possible Decisions

                #find hand split it, call decision matrix again on everything.
            #SPLIT happens first - split all hands and refill them as needed

            #HIT

            #STAND

            #DOUBLE

            #SPLIT

            #SURRENDER

            #is surrender allowed, is doubling after split allowed

    def check_for_blackjack(self):
        p_bj = False
        d_bj = False
        if self.p_hand[0].get_value() == 21:
            p_bj = True
        if self.d_hand.get_value() == 21:
            d_bj = True
        return p_bj, d_bj

    def decision(self):
        decisions = []
        for hand in p_hand:
            hand.value, d_hand[0].value
        return decisions


    def show_blackjack_results(selfself, p_bj, d_bj):
        if p_bj and d_bj:
            print("Draw!")
        elif p_bj:
            print("You win!")
        elif d_bj:
            print("Dealer win!")

