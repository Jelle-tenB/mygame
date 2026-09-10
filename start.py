
#TODO: Make 52 cards, 4 suits, 13 ranks deck
    #TODO: Keep track of which cards have been drawn
    #TODO: Draw random card from deck
    #TODO: Choose a spot to display card
    #TODO: Display new card next to previous card
        #TODO: When new bet is placed, switch card placement
        #TODO: Keep track of all drawn cards??

#TODO: Bet higher or lower
    #TODO: Handle user input for betting, with arrow keys and/or mouse clicks

#TODO: Track score
    #TODO: Display score on screen
    #TODO: Streak bonus system??

import pygame
from deck import Deck

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("My Game")
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))
        self.clock = pygame.time.Clock()
        self.running = True

        self.card_front = self.load_image("card_fronts.png")
        
        self.deck = Deck()
        self.deck.shuffle()
        self.current_card = self.deck.draw()
        
        self.background = self.load_image("background.png")


    def load_image(self, imgName: str) -> pygame.Surface:
        img = pygame.image.load(imgName).convert()
        img.set_colorkey((0, 0, 0))
        return img
        
        
    def getCardFront(self, suit: int, rank: int) -> tuple:
        """
        Suits: 0 = Diamonds, 1 = Clubs, 2 = Hearts, 3 = Spades,
        Ranks: 0 = Ace, 1 = 2, ..., 11 = Queen, 12 = King
        """
        
        # Starting position for the card front (3, 3, 71, 97)
        left = 3 + rank * 71
        top = 3 + suit * 97
        return (left, top, 71, 97)  # Return the rectangle area for the card front


    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.display.fill((0, 0, 0, 0))  # Clear the screen with black
            self.display.blit(self.background, (0, 0))

            self.display.blit(self.card_front, area=self.getCardFront(self.deck.get_suit(self.current_card), self.deck.get_rank(self.current_card)))  # Draw the card front
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))  # Scale the display to the screen size
            pygame.display.update()  # Update the display
            self.clock.tick(60)  # Limit to 60 frames per second

        pygame.quit()


Game().run()