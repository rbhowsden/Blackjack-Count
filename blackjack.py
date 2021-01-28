import random

class Shoe:
    def __init__(self, decks=6, penetration=.75,
                 ranks=['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']):
        self.decks = decks
        self.penetration = penetration
        self.ranks = ranks
        self.cards = ranks*decks*4
        #Problem here is that it only reshuffles what is currently in the shoe
        self.size = len(self.cards)
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def pull_card(self):
        #Basically will need a trigger that tells to reshuffle
        return self.cards.pop(0)







import random

ranks=['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
decks=7
penetration=.75

def shuffle


https://github.com/suhasgaddam/blackjack-python/tree/master/blackjack