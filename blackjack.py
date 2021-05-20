import random

class Card:
    def __init__(self, value):
        self.value = value

class Shoe:
    def __init__(self, decks=6, penetration=.75):
        self.decks = decks
        self.penetration = penetration
        self.ranks = [Card(v) for v in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]]
        self.history = {"A": 0, "2": 0, "3": 0, "4": 0,
                        "5": 0, "6": 0, "7": 0, "8": 0,
                        "9": 0, "10": 0, "J": 0, "Q": 0, "K": 0}
        self.cards = 4*self.ranks*self.decks
        self.size = len(self.cards)
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def pull_card(self):
        new_card = self.cards.pop(0)
        self.history[new_card.value] += 1
        return new_card.value

class Hand:
    def __init__(self, split=None):
        if split:
            self.cards = [split]
        else:
            self.cards = []
        while len(self.cards) < 2:
            self.cards.append(card)
        self.value = 0
        self.calculate_value()
        self.soft = False

    def hit(self):
        self.cards.append(card)

    def split(self):
        return Hand(self.cards[0]), Hand(self.cards[0])

    def calculate_value(self):
        self.value = 0
        has_ace = False
        for card in self.cards:
            if card.value.isnumeric():
                self.value += int(card.value)
            else:
                if card.value == "A":
                    has_ace = True
                    self.value += 11
                else:
                    self.value += 10

        if has_ace and self.value > 21:
            self.value -= 10

class Game:
    self.shoe = Shoe()
    self.p_hand = Hand()
    self.d_hand = Hand()
