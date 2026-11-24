import json
import random
import sys

import pygame

from deck import Deck
from utils import (
    card_costs,
    getCardFront,
    getCosts,
    getHalfCardFront,
    loadImage,
    reroll_costs,
)

MUSIC_INTRO = "media/hypnotic_poison_full.ogg"
MUSIC_LOOP = "media/hypnotic_poison_loop.ogg"
MUSIC_LOOP_EVENT = pygame.USEREVENT + 1

#TODO before public release:
    #TODO: Uncomment the playing of music.
    #TODO: Check if the starting deck holds 52 cards.
    #TODO: Set costs back, in utils.


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("My Game")
        self.screen = pygame.display.set_mode((1280, 960))
        self.display = pygame.Surface((640, 480))
        self.clock = pygame.time.Clock()
        self.running = True
        self.play_state = "mainmenu"
        self.old_card = False
        self.selected_add_card = None
        self.selected_remove_card = None
        self.remove_card_rects = []
        self.add_card_rects = []
        self.removed_cards = []
        self.added_cards = []

        self.font = pygame.font.SysFont('Helvetica', 15)
        self.small_font = pygame.font.SysFont('Helvetica', 10)

        self.score = 0
        self.streak = 0
        
        self.width = self.display.get_width()
        self.height = self.display.get_height()
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        
        try:
            with open("media/highscore.json", "r", encoding="utf-8") as file:
                self.highscore = json.load(file)["highscore"]
        except FileNotFoundError:
            self.highscore = 0
        
        try:
            with open("media/savegame.json", "r", encoding="utf-8") as file:
                self.saved = json.load(file)["saved"]
        except FileNotFoundError:
            self.saved = False

        self.deck = Deck()
        self.deck.shuffle()
        self.new_card = self.deck.draw()
        
        self.card_front = loadImage("media/deck_classic_light_4color_1.png")
        self.background = loadImage("media/background.png")
        self.background = pygame.transform.smoothscale(self.background, (640, 480))
        
        self.audio_card_place = pygame.mixer.Sound('media/short-card-place-1.ogg')
        self.audio_card_place.set_volume(0.3)
        self.audio_shuffle = pygame.mixer.Sound('media/short-card-fan-1.ogg')
        self.audio_shuffle.set_volume(0.4)
        self.audio_chip = pygame.mixer.Sound('media/short-chips-handle-1.ogg')
        self.audio_chip.set_volume(0.4)

        pygame.mixer.music.set_endevent(MUSIC_LOOP_EVENT)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.load(MUSIC_INTRO)
        # pygame.mixer.music.play()
    
    
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
    
    
    def drawMainMenu(self):
        self.display.blit(self.background, (0, 0))
        self.display.blit(self.font.render('Main Menu', True, (1, 1, 1)), (self.width / 2 - 38, self.height / 4 - 10))
        
        #New Game button
        self.newgame_button = pygame.Rect(self.width / 2 - 40, self.height / 4 + 10, 80, 30)
        pygame.draw.rect(self.display, (100, 255, 100), self.newgame_button)
        self.display.blit(self.font.render('New Game', True, (1, 1, 1)), (self.width / 2 - 38, self.height / 4 + 15))
        
        #Continue button
        self.continue_button = pygame.Rect(self.width / 2 - 40, self.height / 4 + 50, 80, 30)
        if self.saved:
            pygame.draw.rect(self.display, (100, 255, 100), self.continue_button)
        else:
            pygame.draw.rect(self.display, (100, 100, 100), self.continue_button)
        self.display.blit(self.font.render('Continue', True, (1, 1, 1)), (self.width / 2 - 38, self.height / 4 + 55))
    
    def handleMainMenuClick(self, mouse_pos: list):
        mouse_x = mouse_pos[0] * self.width / self.screen_width
        mouse_y = mouse_pos[1] * self.height / self.screen_height
        
        #New Game button
        if self.newgame_button.collidepoint(mouse_x, mouse_y):
            self.previous_state = "play"
            self.play_state = "play"
        
        #Continue button
        if self.continue_button.collidepoint(mouse_x, mouse_y) and self.saved:
            with open("media/savegame.json", "r", encoding="utf-8") as file:
                save_data = json.load(file)
                self.score = save_data["score"]
                self.deck.cards = save_data["deck"]
                card_costs["times added"] = save_data["times added"]
                card_costs["times removed"] = save_data["times removed"]
                self.cards_to_remove = save_data["cards to remove"]
                self.cards_to_add = save_data["cards to add"]
            self.previous_state = "shop"
            self.play_state = "shop"
        
    
    def drawGame(self):
        self.display.blit(self.background, (0, 0))
        
        #Display rules
        self.display.blit(self.small_font.render('Choose wether the next card is higher, lower or same in rank.', True, (1,1,1)), (self.width / 4 + 50, self.height - 55))
        self.display.blit(self.small_font.render('Ace is the lowest card, King the highest.', True, (1,1,1)), (self.width / 4 + 50, self.height - 45))
        self.display.blit(self.small_font.render('Streak of 2 = 2 Score, streak 5 = 3, streak 10 = 5.', True, (1,1,1)), (self.width / 4 + 50, self.height - 35))
        self.display.blit(self.small_font.render('Correct "same" bet gives 10 Score times streak multiplier.', True, (1,1,1)), (self.width / 4 + 50, self.height - 25))
        self.display.blit(self.small_font.render('You can spend Score in the shop for upgrades.', True, (1,1,1)), (self.width / 4 + 50, self.height - 15))
        
        #Old card underneath the new card
        if self.old_card is not False:
            self.display.blit(
                self.card_front,
                dest=(self.width / 2 - 20, self.height / 4),
                area=getHalfCardFront(self.deck.get_suit(self.old_card), self.deck.get_rank(self.old_card)))
        #New card second, so its on top of old card
        self.display.blit(
            self.card_front,
            dest=(self.width / 2 - 20, self.height / 4 + 15),
            area=getCardFront(self.deck.get_suit(self.new_card), self.deck.get_rank(self.new_card)))
        
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
        self.display.blit(
            self.font.render(f'Highscore: {"69 nice" if self.highscore == 69 else self.highscore}',
                             True, (1, 1, 1)), (self.width / 2 - 63, 20))
        
        #Cards left display
        self.display.blit(
            self.font.render(f'Cards left: {len(self.deck.cards) - len(self.deck.played_cards)}',
                             True, (1, 1, 1)), (self.width / 2 - 59, 40))
        
        #Score display
        self.display.blit(
            self.font.render(f'Score: {"69 nice" if self.score == 69 else self.score}',
                             True, (1, 1, 1)), (self.width / 2 - 35, 60))
        
        #Streak display
        self.display.blit(self.font.render(f'Streak: {self.streak}', True, (1, 1, 1)), (self.width / 2 - 38, 80))
        
        #Played cards displayed from top left to bottom left
        if self.deck.played_cards:
            sorted_played_cards = sorted(self.deck.played_cards)
            for i, value in enumerate(sorted_played_cards[:-1]):
                if i < 32:
                    self.display.blit(
                        self.card_front,
                        dest=(0, i * 15),
                        area=getHalfCardFront(self.deck.get_suit(value), self.deck.get_rank(value)))
                else:
                    self.display.blit(
                        self.card_front,
                        dest=(40, (i * 15) - 32 * 15),
                        area=getHalfCardFront(self.deck.get_suit(value), self.deck.get_rank(value)))
            if len(self.deck.played_cards) > 32:
                self.display.blit(
                    self.card_front,
                    dest=(40, len(self.deck.played_cards) * 15 - 32 * 15 - 15),
                    area=getCardFront(self.deck.get_suit(sorted_played_cards[-1]), self.deck.get_rank(sorted_played_cards[-1])))
            else:
                self.display.blit(
                    self.card_front,
                    dest=(0, len(self.deck.played_cards) * 15 - 15),
                    area=getCardFront(self.deck.get_suit(sorted_played_cards[-1]), self.deck.get_rank(sorted_played_cards[-1])))
        
        #Next button
        if len(self.deck.cards) - len(self.deck.played_cards) == 0:
            self.next_button = pygame.Rect(self.width / 2 - 25, self.height / 2 - 25, 50, 50)
            pygame.draw.rect(self.display, (100, 100, 255), self.next_button)
            self.display.blit(self.font.render('Next', True, (1, 1, 1)), (self.width / 2 - 17, self.height / 2 - 10))
        
        #View Deck button
        self.view_deck_button = pygame.Rect(self.width / 2 - 40, self.height / 2 + 105, 80, 30)
        pygame.draw.rect(self.display, (255, 255, 100), self.view_deck_button)
        self.display.blit(self.font.render('View Deck', True, (1, 1, 1)), (self.width / 2 - 35, self.height / 2 + 110))


    def handleGameClick(self, mouse_pos: list):
        mouse_x = mouse_pos[0] * self.width / self.screen_width
        mouse_y = mouse_pos[1] * self.height / self.screen_height
        
        #Next Button
        #Needs to be first to properly check you are out of cards.
        if len(self.deck.cards) - len(self.deck.played_cards) == 0: #noqa
            if self.next_button.collidepoint(mouse_x, mouse_y):
                self.old_card = False
                self.streak = 0
                self.audio_shuffle.play()
                self.highscore = max(self.highscore, self.score)
                self.cards_to_remove = random.sample(self.deck.cards, 4)
                self.cards_to_add = random.sample(range(52), 4)
                self.times_cards_rerolled = 1
                self.times_upgrades_rerolled = 1
                #Save the game
                with open("media/savegame.json", "w", encoding="utf-8") as file:
                    json.dump({
                        "saved": True,
                        "score": self.score,
                        "deck": self.deck.cards,
                        "times added": card_costs["times added"],
                        "times removed": card_costs["times removed"],
                        "cards to remove": self.cards_to_remove,
                        "cards to add": self.cards_to_add
                            }, file)
                self.play_state = "shop"
        
        #Higher button
        if self.higher_button.collidepoint(mouse_x, mouse_y) and len(self.deck.cards) - len(self.deck.played_cards) > 0:
            self.gameBetClick("higher")

        #Lower button
        if self.lower_button.collidepoint(mouse_x, mouse_y) and len(self.deck.cards) - len(self.deck.played_cards) > 0:
            self.gameBetClick("lower")
        
        #Same button
        if self.same_button.collidepoint(mouse_x, mouse_y) and len(self.deck.cards) - len(self.deck.played_cards) > 0:
            self.gameBetClick("same")
        
        #View Deck button
        if self.view_deck_button.collidepoint(mouse_x, mouse_y):
            self.deck_background = self.display.copy()
            self.previous_state = self.play_state
            self.play_state = "deck"
    
    
    def gameBetClick(self, bet: str):
        if self.new_card is not None:
            self.old_card = self.new_card
        self.new_card = self.deck.draw()
        self.audio_card_place.play()
        self.compare(bet)
        if len(self.deck.cards) - len(self.deck.played_cards) == 0 and self.highscore < self.score:
            with open("media/highscore.json", "w", encoding="utf-8") as file:
                file.write(json.dumps({"highscore": self.score}))
        

    def drawShop(self):
        self.display.blit(self.background, (0, 0))

        #Needs to be reset each time, otherwise it will keep growing forever.
        self.remove_card_rects = []
        self.add_card_rects = []
        
        #Score display
        self.display.blit(self.font.render(f'Score: {self.score}', True, (1, 1, 1)), (self.width / 2 - 30, 20))
        
        #Deck size display
        self.display.blit(self.font.render(f'Deck size: {len(self.deck.cards)}', True, (1, 1, 1)), (self.width / 2 - 57, 40))

        #Cards to remove display
        for i, card in enumerate(self.cards_to_remove):
            card_rect = pygame.Rect(10 + 50 * i, 30, 40, 60)
            self.remove_card_rects.append(card_rect)
            if i == self.selected_remove_card:
                pygame.draw.rect(self.display, (255, 220, 40), card_rect.inflate(4, 4), 2)
            if card in self.removed_cards:
                self.display.blit(self.card_front, dest=card_rect.topleft, area=getCardFront(self.deck.get_suit(card), self.deck.get_rank(card)))
                overlay = pygame.Surface(card_rect.size, pygame.SRCALPHA)
                overlay.fill((128, 128, 128, 150))
                self.display.blit(overlay, card_rect.topleft)
            else:
                self.display.blit(self.card_front, dest=card_rect.topleft, area=getCardFront(self.deck.get_suit(card), self.deck.get_rank(card)))
        self.display.blit(self.font.render('Select a card to remove from the deck', True, (1, 1, 1)), (5, 5))
        
        #Remove card button
        self.remove_button = pygame.Rect(65, 100, 84, 30)
        if getCosts("remove") > self.score:
            pygame.draw.rect(self.display, (100, 100, 100), self.remove_button)
            self.display.blit(self.small_font.render('Not enough Score', True, (1, 1, 1)), (65, 130))
        elif len(self.deck.cards) <= 4:
            pygame.draw.rect(self.display, (100, 100, 100), self.remove_button)
            self.display.blit(self.small_font.render('Deck cannot be smaller than 4 cards', True, (1, 1, 1)), (25, 130))
        else:
            pygame.draw.rect(self.display, (255, 0, 0), self.remove_button)
        self.display.blit(self.font.render(f'Remove: {getCosts("remove")}', True, (1, 1, 1)), (67, 105))
        
        #Cards to add display
        for i, card in enumerate(self.cards_to_add):
            card_rect = pygame.Rect(10 + 50 * i, 170, 40, 60)
            self.add_card_rects.append(card_rect)
            if i == self.selected_add_card:
                pygame.draw.rect(self.display, (255, 220, 40), card_rect.inflate(4, 4), 2)
            if card in self.added_cards:
                self.display.blit(self.card_front, dest=card_rect.topleft, area=getCardFront(self.deck.get_suit(card), self.deck.get_rank(card)))
                overlay = pygame.Surface(card_rect.size, pygame.SRCALPHA)
                overlay.fill((128, 128, 128, 150))
                self.display.blit(overlay, card_rect.topleft)
            else:
                self.display.blit(self.card_front, dest=card_rect.topleft, area=getCardFront(self.deck.get_suit(card), self.deck.get_rank(card)))
        self.display.blit(self.font.render('Select a card to add to the deck', True, (1, 1, 1)), (5, 145))
        
        #Add card button
        self.add_button = pygame.Rect(65, 240, 84, 30)
        if getCosts("add") > self.score:
            pygame.draw.rect(self.display, (100, 100, 100), self.add_button)
            self.display.blit(self.small_font.render('Not enough Score', True, (1, 1, 1)), (65, 270))
        elif len(self.deck.cards) >= 64:
            pygame.draw.rect(self.display, (100, 100, 100), self.add_button)
            self.display.blit(self.small_font.render('Deck cannot be larger than 64 cards', True, (1, 1, 1)), (25, 270))
        else:
            pygame.draw.rect(self.display, (0, 255, 0), self.add_button)
        self.display.blit(self.font.render(f'Add: {getCosts("add")}', True, (1, 1, 1)), (82, 245))
        
        #Reroll Cards button
        self.reroll_cards_button = pygame.Rect(80, 290, 50, 50)
        if reroll_costs["cards"] * self.times_cards_rerolled > self.score:
            pygame.draw.rect(self.display, (100, 100, 100), self.reroll_cards_button)
        else:
            pygame.draw.rect(self.display, (100, 100, 255), self.reroll_cards_button)
        self.display.blit(self.font.render('Reroll:', True, (1, 1, 1)), (84, 294))
        self.display.blit(self.font.render(f'{reroll_costs["cards"] * self.times_cards_rerolled}', True, (1, 1, 1)), (94, 310))
        
        #View Deck button
        self.view_deck_button = pygame.Rect(self.width / 2 - 40, self.height - 120, 80, 30)
        pygame.draw.rect(self.display, (255, 255, 100), self.view_deck_button)
        self.display.blit(self.font.render('View Deck', True, (1, 1, 1)), (self.width / 2 - 34, self.height - 115))
        
        #Rules display
        self.display.blit(
            self.small_font.render('Your deck can never be smaller than 4 cards or larger than 64 cards.', True, (1,1,1)),
            (self.width / 4 + 5, self.height - 90))
        
        #Next button
        self.next_button = pygame.Rect(self.width / 2 - 25, self.height - 75, 50, 50)
        pygame.draw.rect(self.display, (100, 100, 255), self.next_button)
        self.display.blit(self.font.render('Next', True, (1, 1, 1)), (self.width / 2 - 17, self.height - 60))


    def handleShopClick(self, mouse_pos: list):
        mouse_x = mouse_pos[0] * self.width / self.screen_width
        mouse_y = mouse_pos[1] * self.height / self.screen_height

        #Selecting card to add
        for index, card_rect in enumerate(self.add_card_rects):
            if card_rect.collidepoint(mouse_x, mouse_y):
                self.selected_add_card = index
                return
        
        #Selecting card to remove
        for index, card_rect in enumerate(self.remove_card_rects):
            if card_rect.collidepoint(mouse_x, mouse_y):
                self.selected_remove_card = index
                return
        
        #Add button
        if self.add_button.collidepoint(mouse_x, mouse_y): #noqa
            if (self.selected_add_card is not None and
            self.score >= getCosts("add") and
            len(self.deck.cards) <= 64):  # Ensure deck size doesn't exceed 64
                card_to_add = self.cards_to_add[self.selected_add_card]
                if card_to_add not in self.added_cards:
                    self.added_cards.append(card_to_add)
                    self.deck.cards.append(card_to_add)
                    self.selected_add_card = None
                    self.score -= getCosts("add")
                    card_costs["times added"] += 1
                    self.audio_chip.play()
        
        #Remove button
        if self.remove_button.collidepoint(mouse_x, mouse_y): #noqa
            if (self.selected_remove_card is not None and
            self.score >= getCosts("remove") and
            len(self.deck.cards) > 4):  # Ensure deck size doesn't go below 4
                card_to_remove = self.cards_to_remove[self.selected_remove_card]
                if card_to_remove in self.deck.cards and card_to_remove not in self.removed_cards:
                    self.deck.cards.remove(card_to_remove)
                    self.removed_cards.append(card_to_remove)
                    self.selected_remove_card = None
                    self.score -= getCosts("remove")
                    card_costs["times removed"] += 1
                    self.audio_chip.play()
        
        #Next button
        if self.next_button.collidepoint(mouse_x, mouse_y):
            #Clear variables for next round.
            self.deck.played_cards = []
            self.removed_cards = []
            self.added_cards = []
            self.selected_add_card = None
            self.selected_remove_card = None
            
            #Prepare the deck for the next round.
            self.deck.shuffle()
            self.new_card = self.deck.draw()
            self.play_state = "play"
            self.audio_shuffle.play()
        
        #View Deck button
        if self.view_deck_button.collidepoint(mouse_x, mouse_y):
            self.deck_background = self.display.copy()
            self.previous_state = self.play_state
            self.play_state = "deck"
        
        #Reroll Cards button
        if self.reroll_cards_button.collidepoint(mouse_x, mouse_y): # noqa
            if self.score >= reroll_costs["cards"] * self.times_cards_rerolled:
                self.cards_to_remove = random.sample(self.deck.cards, 4)
                self.cards_to_add = random.sample(range(52), 4)
                self.selected_add_card = None
                self.selected_remove_card = None
                self.removed_cards = []
                self.added_cards = []
                self.score -= reroll_costs["cards"] * self.times_cards_rerolled
                self.times_cards_rerolled += 1
                self.audio_shuffle.play()


    def drawDeck(self):
        #Display whole deck from top right to bottom right
        sorted_deck = sorted(self.deck.cards)
        
        self.display.blit(self.deck_background, (0, 0))
        
        self.display.blit(self.background, (self.width - 80, 0), area=(self.width - 80, 0, 80, self.height))
        overlay = pygame.Surface((self.width - 80, self.height), pygame.SRCALPHA)
        overlay.fill((128, 128, 128, 150))
        self.display.blit(overlay, (0, 0))
        
        for i, value in enumerate(sorted_deck[:-1]):
            if i < 32:
                self.display.blit(
                    self.card_front,
                    dest=(self.width - 80, i * 15),
                    area=getHalfCardFront(self.deck.get_suit(value), self.deck.get_rank(value)))
            else:
                self.display.blit(
                    self.card_front,
                    dest=(self.width - 40, (i * 15) - 32 * 15),
                    area=getHalfCardFront(self.deck.get_suit(value), self.deck.get_rank(value)))

        if len(sorted_deck) > 32:
            self.display.blit(
                self.card_front,
                dest=(self.width - 40, len(sorted_deck) * 15 - 32 * 15 - 15),
                area=getCardFront(self.deck.get_suit(sorted_deck[-1]), self.deck.get_rank(sorted_deck[-1])))
        else:
            self.display.blit(
                self.card_front,
                dest=(self.width - 80, len(sorted_deck) * 15 - 15),
                area=getCardFront(self.deck.get_suit(sorted_deck[-1]), self.deck.get_rank(sorted_deck[-1])))


    def handleDeckClick(self, mouse_pos: list):
        if mouse_pos[0] * self.width / self.screen_width < self.width - 80:
            if self.previous_state == "play":
                self.play_state = "play"
            elif self.previous_state == "shop":
                self.play_state = "shop"


    def run(self):
        while self.running:
            if self.play_state == "mainmenu":
                self.drawMainMenu()
            elif self.play_state == "play":
                self.drawGame()
            elif self.play_state == "shop":
                self.drawShop()
            elif self.play_state == "deck":
                self.drawDeck()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()

                if event.type == MUSIC_LOOP_EVENT:
                    pygame.mixer.music.load(MUSIC_LOOP)
                    pygame.mixer.music.play(-1)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play_state == "mainmenu":
                        self.handleMainMenuClick(event.pos)
                    elif self.play_state == "play":
                        self.handleGameClick(event.pos)
                    elif self.play_state == "shop":
                        self.handleShopClick(event.pos)
                    elif self.play_state == "deck":
                        self.handleDeckClick(event.pos)
            
            #Scale the display to the screen size
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()  #Update the display
            self.clock.tick(30)  #Limit to 30 frames per second


Game().run()
