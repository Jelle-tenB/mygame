import json
import random
import sys

import pygame

from deck import Deck

MUSIC_INTRO = "media/Jankis_Lair_intro.ogg"
MUSIC_LOOP = "media/Jankis_Lair_loop.ogg"
MUSIC_LOOP_EVENT = pygame.USEREVENT + 1


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("My Game")
        self.screen = pygame.display.set_mode((1280, 960))
        self.display = pygame.Surface((640, 480))
        self.clock = pygame.time.Clock()
        self.running = True
        self.play_state = True
        self.selected_menu_card = None
        self.menu_card_rects = []

        self.font = pygame.font.SysFont('Helvetica', 15)
        self.small_font = pygame.font.SysFont('Helvetica', 10)

        self.score = 0
        self.old_card = False
        self.streak = 0
        
        self.width = self.display.get_width()
        self.height = self.display.get_height()
        
        try:
            with open("highscore.json", "r") as file:
                self.highscore = json.load(file)["highscore"]
        except FileNotFoundError:
            self.highscore = 0
        
        self.deck = Deck()
        self.deck.shuffle()
        self.new_card = self.deck.draw()
        self.deck_size = self.deck.deck_size
        
        self.card_front = self.load_image("media/deck_classic_light_4color_1.png")
        self.background = self.load_image("media/background.png")
        self.background = pygame.transform.smoothscale(self.background, (640, 480))
        
        self.audio_card_place = pygame.mixer.Sound('media/short-card-place-1.ogg')
        self.audio_card_place.set_volume(0.3)
        self.audio_shuffle = pygame.mixer.Sound('media/short-card-fan-1.ogg')
        self.audio_shuffle.set_volume(0.4)

        pygame.mixer.music.set_endevent(MUSIC_LOOP_EVENT)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.load(MUSIC_INTRO)
        pygame.mixer.music.play()
        
        


    def load_image(self, imgName: str) -> pygame.Surface:
        img = pygame.image.load(imgName).convert()
        img.set_colorkey((0, 0, 0))
        return img
        
        
    def getCardFront(self, suit: int, rank: int) -> tuple:
        """
        Suits: 0 = Diamonds, 1 = Clubs, 2 = Hearts, 3 = Spades,
        Ranks: 0 = Ace, 1 = 2, ..., 11 = Queen, 12 = King
        """
        left = 12 + rank * 64
        top = 2 + suit * 64

        return (left, top, 40, 60)
    
    
    def getHalfCardFront(self, suit: int, rank: int) -> tuple:
        """
        Suits: 0 = Diamonds, 1 = Clubs, 2 = Hearts, 3 = Spades,
        Ranks: 0 = Ace, 1 = 2, ..., 11 = Queen, 12 = King
        """
        left = 12 + rank * 64
        top = 2 + suit * 64

        return (left, top, 40, 18)
    
    
    def compare(self, bet: str):
        if ((bet == "higher" and self.deck.get_rank(self.new_card) > self.deck.get_rank(self.old_card)) or
        (bet == "lower" and self.deck.get_rank(self.new_card) < self.deck.get_rank(self.old_card))):
            if self.streak >= 10:
                self.score += 5
            elif self.streak >= 5:
                self.score += 3
            elif self.streak >= 2:
                self.score += 2
            else:
                self.score += 1
            self.streak += 1
        elif bet == "same" and self.deck.get_rank(self.new_card) == self.deck.get_rank(self.old_card):
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
    
    
    def draw_game(self):
        self.display.blit(self.background, (0, 0))
        
        #Display rules
        self.display.blit(self.small_font.render('Choose wether the next card is higher, lower or same rank', True, (1,1,1)), (self.width / 4 + 50, self.height - 45))
        self.display.blit(self.small_font.render('Ace is the lowest card, King the highest', True, (1,1,1)), (self.width / 4 + 50, self.height - 35))
        self.display.blit(self.small_font.render('Streak of 2 = 2 points, streak 5 = 3, streak 10 = 5', True, (1,1,1)), (self.width / 4 + 50, self.height - 25))
        self.display.blit(self.small_font.render('Correct "same" bet gives 10 points times streak multiplier', True, (1,1,1)), (self.width / 4 + 50, self.height - 15))
        
        # Old card underneath the new card
        if self.old_card is not False:
            self.display.blit(self.card_front, dest=(self.width / 2 - 20, self.height / 4), area=self.getHalfCardFront(self.deck.get_suit(self.old_card), self.deck.get_rank(self.old_card)))
        # New card second, so its on top of old card
        self.display.blit(self.card_front, dest=(self.width / 2 - 20, self.height / 4 + 15), area=self.getCardFront(self.deck.get_suit(self.new_card), self.deck.get_rank(self.new_card)))
        
        #Higher button
        self.higher_button = pygame.Rect(self.width / 2 - 80, self.height / 2 + 50, 50, 50)
        pygame.draw.rect(self.display, (100, 255, 100), self.higher_button)
        self.display.blit(self.font.render('Higher', True, (1, 1, 1)), (self.width / 2 - 77, self.height / 2 + 65))
        
        #Lower button
        self.lower_button = pygame.Rect(self.width / 2 - 25, self.height / 2 + 50, 50, 50)
        pygame.draw.rect(self.display, (255, 100, 100), self.lower_button)
        self.display.blit(self.font.render('Lower', True, (1, 1, 1)), (self.width / 2 - 20, self.height / 2 + 65))
        
        #Same button
        self.same_button = pygame.Rect(self.width / 2 + 30, self.height / 2+ 50, 50, 50)
        pygame.draw.rect(self.display, (128, 50, 128), self.same_button)
        self.display.blit(self.font.render('Same', True, (1, 1, 1)), (self.width / 2 + 35, self.height / 2 + 65))
        
        #Highscore display
        self.display.blit(self.font.render(f'Highscore: {"69 nice" if self.highscore == 69 else self.highscore}', True, (1, 1, 1)), (self.width / 2 - 63, 20))
        
        #Cards left display
        self.display.blit(self.font.render(f'Cards left: {self.deck_size - len(self.deck.played_cards)}', True, (1, 1, 1)), (self.width / 2 - 59, 40))
        
        #Score display
        self.display.blit(self.font.render(f'Score: {"69 nice" if self.score == 69 else self.score}', True, (1, 1, 1)), (self.width / 2 - 35, 60))
        
        #Streak display
        self.display.blit(self.font.render(f'Streak: {self.streak}', True, (1, 1, 1)), (self.width / 2 - 38, 80))
        
        #Played cards displayed from top left to bottom left
        if self.deck.played_cards:
            sorted_played_cards = sorted(self.deck.played_cards)
            for i, value in enumerate(sorted_played_cards[:-1]):
                if i < 32:
                    self.display.blit(self.card_front, dest=(0, i * 15), area=self.getHalfCardFront(self.deck.get_suit(value), self.deck.get_rank(value)))
                else:
                    self.display.blit(self.card_front, dest=(40, (i * 15) - 32 * 15), area=self.getHalfCardFront(self.deck.get_suit(value), self.deck.get_rank(value)))
            if len(self.deck.played_cards) > 32:
                self.display.blit(self.card_front, dest=(40, len(self.deck.played_cards) * 15 - 32 * 15 - 15), area=self.getCardFront(self.deck.get_suit(sorted_played_cards[-1]), self.deck.get_rank(sorted_played_cards[-1])))
            else:
                self.display.blit(self.card_front, dest=(0, len(self.deck.played_cards) * 15 - 15), area=self.getCardFront(self.deck.get_suit(sorted_played_cards[-1]), self.deck.get_rank(sorted_played_cards[-1])))
        
        #Next button
        if self.deck_size - len(self.deck.played_cards) == 0:
            self.next_button = pygame.Rect(self.width / 2 - 25, self.height / 2 - 25, 50, 50)
            pygame.draw.rect(self.display, (100, 100, 255), self.next_button)
            self.display.blit(self.font.render('Next', True, (1, 1, 1)), (self.width / 2 - 17, self.height / 2 - 10))
        

    def draw_menu(self):
        self.display.blit(self.background, (0, 0))
        self.remove_card_rects = []
        self.add_card_rects = []

        #Cards to remove display
        for i, card in enumerate(self.cards_to_remove):
            card_rect = pygame.Rect(10 + 50 * i, 10, 40, 60)
            self.remove_card_rects.append(card_rect)
            if i == self.selected_menu_card:
                pygame.draw.rect(self.display, (255, 220, 40), card_rect.inflate(4, 4), 2)
            self.display.blit(self.card_front, dest=card_rect.topleft, area=self.getCardFront(self.deck.get_suit(card), self.deck.get_rank(card)))
        
        #Cards to add display
        for i, card in enumerate(self.cards_to_add):
                    card_rect = pygame.Rect(10 + 50 * i, 100, 40, 60)
                    self.add_card_rects.append(card_rect)
                    if i == self.selected_menu_card:
                        pygame.draw.rect(self.display, (255, 220, 40), card_rect.inflate(4, 4), 2)
                    self.display.blit(self.card_front, dest=card_rect.topleft, area=self.getCardFront(self.deck.get_suit(card), self.deck.get_rank(card)))
    
    
    def handle_game_click(self, mouse_pos: list):
        mouse_x = mouse_pos[0] * self.width / self.screen.get_width()
        mouse_y = mouse_pos[1] * self.height / self.screen.get_height()
        
        # Next Button
        # Needs to be first to properly check you are out of cards.
        if self.deck_size - len(self.deck.played_cards) == 0:
            if self.next_button.collidepoint(mouse_x, mouse_y):
                self.old_card = False
                self.streak = 0
                # self.deck = Deck()
                # self.deck.shuffle()
                # self.new_card = self.deck.draw()
                self.audio_shuffle.play()
                self.highscore = max(self.highscore, self.score)
                self.score = 0
                self.cards_to_remove = random.sample(self.deck.cards, 4)
                self.cards_to_add = random.sample(range(self.deck.deck_size), 4)
                self.play_state = False
        
        # Higher button
        if self.higher_button.collidepoint(mouse_x, mouse_y) and self.deck_size - len(self.deck.played_cards) > 0:
            self.game_bet_click("higher")

        # Lower button
        if self.lower_button.collidepoint(mouse_x, mouse_y) and self.deck_size - len(self.deck.played_cards) > 0:
            self.game_bet_click("lower")
        
        # Same button
        if self.same_button.collidepoint(mouse_x, mouse_y) and self.deck_size - len(self.deck.played_cards) > 0:
            self.game_bet_click("same")
    
    
    def game_bet_click(self, bet: str):
        if self.new_card is not None:
            self.old_card = self.new_card
        self.new_card = self.deck.draw()
        self.audio_card_place.play()
        self.compare(bet)
        if self.deck_size - len(self.deck.played_cards) == 0 and self.highscore < self.score:
                with open("highscore.json", "w") as file:
                    file.write(json.dumps({"highscore": self.score}))
    
    
    def handle_menu_click(self, mouse_pos: list):
        mouse_x = mouse_pos[0] * self.width / self.screen.get_width()
        mouse_y = mouse_pos[1] * self.height / self.screen.get_height()

        for index, card_rect in enumerate(self.menu_card_rects):
            if card_rect.collidepoint(mouse_x, mouse_y):
                self.selected_menu_card = index
                return


    def run(self):
        while self.running:
            if self.play_state:
                self.draw_game()
            else:
                self.draw_menu()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()

                if event.type == MUSIC_LOOP_EVENT:
                    pygame.mixer.music.load(MUSIC_LOOP)
                    pygame.mixer.music.play(-1)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play_state:
                        self.handle_game_click(event.pos)
                    else:
                        self.handle_menu_click(event.pos)
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))  # Scale the display to the screen size
            pygame.display.update()  # Update the display
            self.clock.tick(30)  # Limit to 30 frames per second


Game().run()
