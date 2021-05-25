import random
import pandas as pd


class Card:
    def __init__(self, value):
        self.value = value


class Shoe:
    def __init__(self, decks):
        self.cards = [
            Card(v) for v in 4*decks*["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        ]
        self.shoe_size = len(self.cards)
        self.current_size = len(self.cards)
        random.shuffle(self.cards)

        self.history = {"A": 0, "2": 0, "3": 0, "4": 0,
                        "5": 0, "6": 0, "7": 0, "8": 0,
                        "9": 0, "10": 0, "J": 0, "Q": 0, "K": 0}

    def pull_card(self):
        self.current_size -= 1
        new_card = self.cards.pop(0)
        self.history[new_card.value] += 1
        return new_card.value


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.bet = 1
        self.hand_type = 'Hard'

    def add_card(self, card):
        self.cards.append(card)

    def calculate_value(self):
        self.value = 0
        ace_count = 0
        for card in self.cards:
            if card.isnumeric():
                self.value += int(card)
            else:
                if card == "A":
                    ace_count += 1
                    self.hand_type = 'Soft'
                    self.value += 11
                else:
                    self.value += 10

            if ace_count > 0 and self.value > 21:
                ace_count -= 1
                self.value -= 10
                if ace_count == 0:
                    self.hand_type = 'Hard'

    def get_value(self):
        self.calculate_value()
        return self.value


class Game:
    def __init__(self, decks, pen, rounds):
        self.decks = decks
        self.pen = pen
        self.rounds = rounds
        self.shoe = Shoe(self.decks)
        self.outcome = None
        self.p_hands = None
        self.d_hand = None
        self.dataset = pd.DataFrame()
        self.pre_history = None

    def simulate(self):

        for r in range(self.rounds):
            self.pre_history = self.shoe.history.copy()
            self.outcome = 0
            self.p_hands = [Hand()]
            self.d_hand = Hand()

            if r % 1000 == 0:
                print(r)

            if (self.shoe.current_size/self.shoe.shoe_size) < 1 - self.pen:
                self.shoe = Shoe(self.decks)

            for i in range(2):
                self.p_hands[0].add_card(self.shoe.pull_card())
                self.d_hand.add_card(self.shoe.pull_card())

            end_round = False
            while not end_round:
                bj = self.blackjack()
                if bj:
                    end_round = True
                    self.log_results(r)
                    continue

                self.splitter()

                hard_set = {
                    (11, "2"), (11, "3"), (11, "4"), (11, "5"), (11, "6"), (11, "7"), (11, "8"), (11, "9"), (11, "10"),
                    (10, "2"), (10, "3"), (10, "4"), (10, "5"), (10, "6"), (10, "7"), (10, "8"), (10, "9"),
                    (9, "3"), (9, "4"), (9, "5"), (9, "6"),
                }

                soft_set = {
                    (18, "3"), (18, "4"), (18, "5"), (18, "6"),
                    (17, "3"), (17, "4"), (17, "5"), (17, "6"),
                    (16, "4"), (16, "5"), (16, "6"),
                    (15, "4"), (15, "5"), (15, "6"),
                    (14, "5"), (14, "6"),
                    (13, "5"), (13, "6")
                }

                hit_list = {
                    "Hard": {
                        (16, "7"), (16, "8"), (16, "9"), (16, "10"), (16, "J"), (16, "Q"), (16, "K"), (16, "A"),
                        (15, "7"), (15, "8"), (15, "9"), (15, "10"), (15, "J"), (15, "Q"), (15, "K"), (15, "A"),
                        (14, "7"), (14, "8"), (14, "9"), (14, "10"), (14, "J"), (14, "Q"), (14, "K"), (14, "A"),
                        (13, "7"), (13, "8"), (13, "9"), (13, "10"), (13, "J"), (13, "Q"), (13, "K"), (13, "A"),
                        (12, "2"), (12, "3"),
                        (12, "7"), (12, "8"), (12, "9"), (12, "10"), (12, "J"), (12, "Q"), (12, "K"), (12, "A"),
                        (11, "A"),
                        (10, "10"), (10, "A"),
                        (9, "2"),
                        (9, "7"), (9, "8"), (9, "9"), (9, "10"), (9, "J"), (9, "Q"), (9, "K"), (9, "A"),
                        (8, "2"), (8, "3"), (8, "4"), (8, "5"), (8, "6"), (8, "7"), (8, "8"),
                        (8, "9"), (8, "10"), (8, "J"), (8, "Q"), (8, "K"), (8, "A"),
                        (7, "2"), (7, "3"), (7, "4"), (7, "5"), (7, "6"), (7, "7"), (7, "8"),
                        (7, "9"), (7, "10"), (7, "J"), (7, "Q"), (7, "K"), (7, "A"),
                        (6, "2"), (6, "3"), (6, "4"), (6, "5"), (6, "6"), (6, "7"), (6, "8"),
                        (6, "9"), (6, "10"), (6, "J"), (6, "Q"), (6, "K"), (6, "A"),
                        (5, "2"), (5, "3"), (5, "4"), (5, "5"), (5, "6"), (5, "7"), (5, "8"),
                        (5, "9"), (5, "10"), (5, "J"), (5, "Q"), (5, "K"), (5, "A"),
                    },
                    "Soft": {
                        (18, "9"), (18, "10"), (18, "J"), (18, "Q"), (18, "K"), (18, "A"),
                        (17, "2"), (17, "7"), (17, "8"), (17, "9"),
                        (17, "10"), (17, "J"), (17, "Q"), (17, "K"), (17, "A"),
                        (16, "2"), (16, "3"), (16, "7"), (16, "8"), (16, "9"),
                        (16, "10"), (16, "J"), (16, "Q"), (16, "K"), (16, "A"),
                        (15, "2"), (15, "3"), (15, "7"), (15, "8"), (15, "9"),
                        (15, "10"), (15, "J"), (15, "Q"), (15, "K"), (15, "A"),
                        (14, "2"), (14, "3"), (14, "4"), (14, "7"), (14, "8"), (14, "9"),
                        (14, "10"), (14, "J"), (14, "Q"), (14, "K"), (14, "A"),
                        (13, "2"), (13, "3"), (13, "4"), (13, "7"), (13, "8"), (13, "9"),
                        (13, "10"), (13, "J"), (13, "Q"), (13, "K"), (13, "A"),
                    }
                }

                for hand in self.p_hands:
                    if hand.hand_type == 'Hard' and (hand.get_value(), self.d_hand.cards[0]) in hard_set:
                        hand.add_card(self.shoe.pull_card())
                        hand.bet *= 2
                    elif hand.hand_type == 'Soft' and (hand.get_value(), self.d_hand.cards[0]) in soft_set:
                        hand.add_card(self.shoe.pull_card())
                        hand.bet *= 2
                    else:
                        while (hand.get_value(), self.d_hand.cards[0]) in hit_list[hand.hand_type]:
                            hand.add_card(self.shoe.pull_card())

                while self.d_hand.get_value() < 17:
                    self.d_hand.add_card(self.shoe.pull_card())

                dealer_final = self.d_hand.get_value()
                for hand in self.p_hands:
                    hand_final = hand.get_value()
                    if hand_final > 21:
                        self.outcome -= hand.bet
                    elif (dealer_final > 21) or (hand_final > dealer_final):
                        self.outcome += hand.bet
                    else:
                        self.outcome -= hand.bet

                self.log_results(r)
                end_round = True
        self.dataset.to_parquet("blackjack.parquet.gzip", compression="gzip")

    def blackjack(self):
        bj = False
        if self.p_hands[0].get_value() == 21 and self.d_hand.get_value() == 21:
            bj = True
        elif self.p_hands[0].get_value() == 21:
            bj = True
            self.outcome += 1.5*self.p_hands[0].bet
        elif self.d_hand.get_value() == 21:
            bj = True
            self.outcome += self.p_hands[0].bet
        return bj

    def splitter(self):
        split_set = {
            ("A", "2"), ("A", "3"), ("A", "4"), ("A", "5"), ("A", "6"), ("A", "7"), ("A", "8"), ("A", "9"), ("A", "10"),
            ("A", "J"), ("A", "Q"), ("A", "K"), ("A", "A"),
            ("9", "2"), ("9", "3"), ("9", "4"), ("9", "5"), ("9", "6"), ("9", "8"), ("9", "9"),
            ("8", "2"), ("8", "3"), ("8", "4"), ("8", "5"), ("8", "6"), ("8", "7"), ("8", "8"), ("8", "9"), ("8", "10"),
            ("8", "J"), ("8", "Q"), ("8", "K"), ("8", "A"),
            ("7", "2"), ("7", "3"), ("7", "4"), ("7", "5"), ("7", "6"), ("7", "7"),
            ("6", "2"), ("6", "3"), ("6", "4"), ("6", "5"), ("6", "6"),
            ("4", "5"), ("4", "6"),
            ("3", "2"), ("3", "3"), ("3", "4"), ("3", "5"), ("3", "6"), ("3", "7"),
            ("2", "2"), ("2", "3"), ("2", "4"), ("2", "5"), ("2", "6"), ("2", "7")
        }

        splitting = True
        while splitting:
            splitting = False
            for i, hand in enumerate(self.p_hands):
                # Different "10" values will not match here but it doesn't matter given strategy
                if hand.cards[0] == hand.cards[1]:
                    if (hand.cards[0], self.d_hand.cards[0]) in split_set:
                        splitting = True
                        new_hand = Hand()
                        new_hand.add_card(hand.cards.pop())
                        new_hand.add_card(self.shoe.pull_card())
                        hand.add_card(self.shoe.pull_card())
                        self.p_hands.append(new_hand)

    def log_results(self, r):
        row = self.pre_history
        row['outcome'] = self.outcome
        row['round'] = r
        self.dataset = self.dataset.append([row])


