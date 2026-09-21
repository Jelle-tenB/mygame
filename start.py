
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
import sys
import json

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("My Game")
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))
        self.clock = pygame.time.Clock()
        self.running = True

        self.score = 0
        self.new_card = False
        
        try:
            with open("highscore.json", "r") as file:
                self.highscore = json.load(file)["highscore"]
        except FileNotFoundError:
            self.highscore = 0
        self.save = False
        self.out_of_cards = False
        
        self.deck = Deck()
        self.deck.shuffle()
        self.old_card = self.deck.draw()
        
        self.card_front = self.load_image("card_fronts.png")
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
    
    
    def compare(self, bet):
        if bet == "higher" and self.deck.get_rank(self.new_card) > self.deck.get_rank(self.old_card):
            self.score += 1
        elif bet == "lower" and self.deck.get_rank(self.new_card) < self.deck.get_rank(self.old_card):
            self.score += 1


    def run(self):
        while self.running:

            self.display.fill((0, 0, 0, 0))  # Clear the screen with black
            self.display.blit(self.background, (0, 0))

            # Display old card left
            self.display.blit(self.card_front, dest=(0,0), area=self.getCardFront(self.deck.get_suit(self.old_card), self.deck.get_rank(self.old_card)))
            # Display new card right
            if self.new_card:
                self.display.blit(self.card_front, dest=(320 - 68, 0), area=self.getCardFront(self.deck.get_suit(self.new_card), self.deck.get_rank(self.new_card)))
            
            width = self.display.get_width()
            height = self.display.get_height()
            
            #Higher button
            higher_button = pygame.Rect(width / 2 - 50, height / 2 + 50, 50, 50)
            pygame.draw.rect(self.display, (100, 255, 100), higher_button)
            font = pygame.font.SysFont('Corbel', 15)
            self.display.blit(font.render('Higher', True, (1, 1, 1)), (width / 2 - 47, height / 2 + 65))
            
            #Lower button
            lower_button = pygame.Rect(width / 2 + 5, height / 2 + 50, 50, 50)
            pygame.draw.rect(self.display, (255, 100, 100), lower_button)
            self.display.blit(font.render('Lower', True, (1, 1, 1)), (width / 2 + 11, height / 2 + 65))
            
            #Score display
            self.display.blit(font.render(f'Score: {self.score}', True, (1, 1, 1)), (width / 2 - 25, 20))
            
            #Highscore display
            self.display.blit(font.render(f'Highscore: {self.highscore}', True, (1, 1, 1)), (width / 2 - 53, 40))
            
            #Restart button
            if self.out_of_cards:
                restart_button = pygame.Rect(width / 2 - 25, 60, 50, 50)
                pygame.draw.rect(self.display, (100, 100, 255), restart_button)
                self.display.blit(font.render('Restart', True, (1, 1, 1)), (width / 2 - 21, 75))
            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x = event.pos[0] * width / self.screen.get_width()
                    mouse_y = event.pos[1] * height / self.screen.get_height()
                    if higher_button.collidepoint(mouse_x, mouse_y) and not self.out_of_cards:
                        if self.new_card:
                            self.old_card = self.new_card
                        try:
                            self.new_card = self.deck.draw()
                            self.compare("higher")
                        except IndexError:
                            if self.highscore < self.score:
                                with open("highscore.json", "w") as file:
                                    file.write(json.dumps({"highscore": self.score}))
                            self.out_of_cards = True

                    if lower_button.collidepoint(mouse_x, mouse_y) and not self.out_of_cards:
                        if self.new_card:
                            self.old_card = self.new_card
                        try:
                            self.new_card = self.deck.draw()
                            self.compare("lower")
                        except IndexError:
                            if self.highscore < self.score:
                                with open("highscore.json", "w") as file:
                                    file.write(json.dumps({"highscore": self.score}))
                            self.out_of_cards = True
                    
                    try:
                        if restart_button.collidepoint(mouse_x, mouse_y):
                            self.out_of_cards = False
                            self.score = 0
                            self.new_card = False
                            self.deck = Deck()
                            self.deck.shuffle()
                            self.old_card = self.deck.draw()
                            self.highscore = max(self.highscore, self.score)
                    except UnboundLocalError:
                        pass
            
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))  # Scale the display to the screen size
            pygame.display.update()  # Update the display
            self.clock.tick(30)  # Limit to 30 frames per second


Game().run()