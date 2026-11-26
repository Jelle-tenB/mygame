import pygame

from deck import get_rank

#add 10, remove 10
card_costs = {
        'add' : 10,
        'remove' : 10,
        'times added' : 0,
        'times removed' : 0
        }

reroll_costs = {
                'cards' : 0,
                'upgrades' : 50,
                }

def loadImage(imgName: str) -> pygame.Surface:
    img = pygame.image.load(imgName).convert()
    img.set_colorkey((0, 0, 0))
    return img
    
    
def getCardFront(suit: int, rank: int) -> tuple:
    """
    Suits: 0 = Diamonds, 1 = Clubs, 2 = Hearts, 3 = Spades,
    Ranks: 0 = Ace, 1 = 2, ..., 11 = Queen, 12 = King
    """
    left = 12 + rank * 64
    top = 2 + suit * 64

    return (left, top, 40, 60)


def getHalfCardFront(suit: int, rank: int) -> tuple:
    """
    Suits: 0 = Diamonds, 1 = Clubs, 2 = Hearts, 3 = Spades,
    Ranks: 0 = Ace, 1 = 2, ..., 11 = Queen, 12 = King
    """
    left = 12 + rank * 64
    top = 2 + suit * 64

    return (left, top, 40, 18)


def getCosts(action: str) -> int:
    if action == "add":
        return card_costs["add"] + card_costs["times added"] * 5
    elif action == "remove":
        return card_costs["remove"] + card_costs["times removed"] * 5
    else:
        raise ValueError("Invalid action. Must be 'add' or 'remove'.")


def compare(self, bet: str):
    if ((bet == "higher" and get_rank(self.new_card) > get_rank(self.old_card)) or
    (bet == "lower" and get_rank(self.new_card) < get_rank(self.old_card))):
        if self.streak >= 10:
            self.score += 5
        elif self.streak >= 5:
            self.score += 3
        elif self.streak >= 2:
            self.score += 2
        else:
            self.score += 1
        self.streak += 1
    elif bet == "same" and get_rank(self.new_card) == get_rank(self.old_card):
        if self.streak >= 10:
            self.score += 50
        elif self.streak >= 5:
            self.score += 30
        elif self.streak >= 2:
            self.score += 20
        else:
            self.score += 10
        self.streak += 1
    else:
        self.streak = 0
    return self.score, self.streak
