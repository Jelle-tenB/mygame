
# TODO: Change first card position to the left

#TODO: Track score
    #TODO: Streak bonus system??

import pygame
from deck import Deck
import sys
import json

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("My Game")
        self.screen = pygame.display.set_mode((1280, 960))
        self.display = pygame.Surface((640, 480))
        self.clock = pygame.time.Clock()
        self.running = True

        self.score = 0
        self.old_card = False
        
        
        
        try:
            with open("highscore.json", "r") as file:
                self.highscore = json.load(file)["highscore"]
        except FileNotFoundError:
            self.highscore = 0
        self.save = False
        self.out_of_cards = False
        
        self.deck = Deck()
        self.deck.shuffle()
        self.new_card = self.deck.draw()
        
        self.card_front = self.load_image("deck_classic_light_4color_1.png")
        self.background = self.load_image("background.png")
        self.background = pygame.transform.smoothscale(self.background, (640, 480))


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
        left = 12 + rank * 64
        top = 2 + suit * 64

        return (left, top, 40, 60)
    
    
    def getHalfCardFront(self, suit: int, rank: int) -> tuple:
            """
            Suits: 0 = Diamonds, 1 = Clubs, 2 = Hearts, 3 = Spades,
            Ranks: 0 = Ace, 1 = 2, ..., 11 = Queen, 12 = King
            """
            
            # Starting position for the card front (3, 3, 71, 97)
            left = 12 + rank * 64
            top = 2 + suit * 64
    
            return (left, top, 40, 18)
    
    
    def compare(self, bet):
        if bet == "higher" and self.deck.get_rank(self.new_card) > self.deck.get_rank(self.old_card):
            self.score += 1
        elif bet == "lower" and self.deck.get_rank(self.new_card) < self.deck.get_rank(self.old_card):
            self.score += 1


    def run(self):
        while self.running:

            self.display.fill((0, 0, 0, 0))  # Clear the screen with black
            self.display.blit(self.background, (0, 0))
            width = self.display.get_width()
            height = self.display.get_height()
            
            # Old card underneath the new card
            if self.old_card:
                self.display.blit(self.card_front, dest=(width / 2 - 20, height / 4 - 15), area=self.getHalfCardFront(self.deck.get_suit(self.old_card), self.deck.get_rank(self.old_card)))
            # New card second, so its on top of old card
            self.display.blit(self.card_front, dest=(width / 2 - 20, height / 4), area=self.getCardFront(self.deck.get_suit(self.new_card), self.deck.get_rank(self.new_card)))
            
            #Higher button
            higher_button = pygame.Rect(width / 2 - 50, height / 2 + 50, 50, 50)
            pygame.draw.rect(self.display, (100, 255, 100), higher_button)
            font = pygame.font.SysFont('Helvetica', 15)
            self.display.blit(font.render('Higher', True, (1, 1, 1)), (width / 2 - 47, height / 2 + 65))
            
            #Lower button
            lower_button = pygame.Rect(width / 2 + 5, height / 2 + 50, 50, 50)
            pygame.draw.rect(self.display, (255, 100, 100), lower_button)
            self.display.blit(font.render('Lower', True, (1, 1, 1)), (width / 2 + 10, height / 2 + 65))
            
            #Score display
            self.display.blit(font.render(f'Score: {self.score}', True, (1, 1, 1)), (width / 2 - 25, 20))
            
            #Highscore display
            self.display.blit(font.render(f'Highscore: {self.highscore}', True, (1, 1, 1)), (width / 2 - 53, 40))
            
            # Display played cards from top left to bottom left
            if self.deck.played_cards:
                for i, value in enumerate(self.deck.played_cards[:-1]):
                    if i > 29:
                        self.display.blit(self.card_front, dest=(40, (i * 15) - 30 * 15), area=self.getHalfCardFront(self.deck.get_suit(value), self.deck.get_rank(value)))
                    else:
                        self.display.blit(self.card_front, dest=(0, i * 15), area=self.getHalfCardFront(self.deck.get_suit(value), self.deck.get_rank(value)))
                if len(self.deck.played_cards) > 30:
                    self.display.blit(self.card_front, dest=(40, (len(self.deck.played_cards) - 15 * 30) * 15 - 15), area=self.getCardFront(self.deck.get_suit(self.deck.played_cards[-1]), self.deck.get_rank(self.deck.played_cards[-1])))
                else:
                    self.display.blit(self.card_front, dest=(0, len(self.deck.played_cards) * 15 - 15), area=self.getCardFront(self.deck.get_suit(self.deck.played_cards[-1]), self.deck.get_rank(self.deck.played_cards[-1])))
            
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
                    
                    # Restart Button
                    # Needs to be first to properly check you are out of cards.
                    if self.out_of_cards:
                        if restart_button.collidepoint(mouse_x, mouse_y):
                            self.out_of_cards = False
                            self.score = 0
                            self.old_card = False
                            self.deck = Deck()
                            self.deck.shuffle()
                            self.old_card = self.deck.draw()
                            self.highscore = max(self.highscore, self.score)
                    
                    # Higher button
                    if higher_button.collidepoint(mouse_x, mouse_y) and not self.out_of_cards:
                        if self.new_card:
                            self.old_card = self.new_card
                        try:
                            self.new_card = self.deck.draw()
                            print(self.new_card)
                            self.compare("higher")
                        except IndexError:
                            if self.highscore < self.score:
                                with open("highscore.json", "w") as file:
                                    file.write(json.dumps({"highscore": self.score}))
                            self.out_of_cards = True

                    # Lower button
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
            
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))  # Scale the display to the screen size
            pygame.display.update()  # Update the display
            self.clock.tick(30)  # Limit to 30 frames per second


Game().run()
