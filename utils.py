import pygame

#add 10, remove 20
costs = {
            'add' : 0,
            'remove' : 0,
            'times added' : 1,
            'times removed' : 1
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
        return costs["add"] * costs["times added"]
    elif action == "remove":
        return costs["remove"] * costs["times removed"]
    else:
        raise ValueError("Invalid action. Must be 'add' or 'remove'.")
