
#TODO: Make 52 cards, 4 suits, 13 ranks deck
    #TODO: Keep track of which cards have been drawn
    #TODO: Draw random card from deck
    #TODO: Choose a spot to display card
    #TODO: Display new card next to previous card
        #TODO: When new bet is placed, switch card placement
        #TODO: Keep track of all drawn cards??

#TODO: Bet higher or lower
#TODO: Track score
#TODO: Handle user input for betting, with arrow keys and/or mouse clicks

import pygame

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("My Game")
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.card_front = pygame.image.load("card_fronts.png").convert()
        self.card_front.set_colorkey((0, 0, 0))  # Set black as the transparent color
        
        
    def getCardFront(self, suit: int, rank: int) -> tuple:
        """
        Suits: 1 = Diamonds, 2 = Clubs, 3 = Hearts, 4 = Spades,
        Ranks: 1 = Ace, 2 = 2, ..., 11 = Jack, 12 = Queen, 13 = King
        """
        
        # Starting position for the card front (3, 3, 71, 97)
        left = (3 * min(rank - 1, 1)) + (71 * (rank - 1))
        top = (3 * min(suit - 1, 1)) + (97 * (suit - 1))
        width = 71
        height = 97
        return (left, top, width, height)


    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((0, 0, 0))  # Clear the screen with black
            self.screen.blit(self.card_front, area=pygame.Rect(self.getCardFront(suit=2, rank=2)))  # Draw the card front
            pygame.display.flip()  # Update the display
            self.clock.tick(60)  # Limit to 60 frames per second

        pygame.quit()


Game().run()