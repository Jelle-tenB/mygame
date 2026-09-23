import random


class Deck:
    def __init__(self):
        self.cards = list(range(52))
        self.position = 0
        self.played_cards = []

    def shuffle(self):
        random.shuffle(self.cards)
        self.position = 0

    def draw(self):
        if self.position >= len(self.cards):
            raise IndexError("No cards left in deck")

        card = self.cards[self.position]
        self.played_cards.append(card)
        self.played_cards.sort()
        self.position += 1
        return card

    @staticmethod
    def get_suit(card):
        return card // 13

    @staticmethod
    def get_rank(card):
        return card % 13