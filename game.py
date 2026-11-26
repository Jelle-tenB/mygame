import json
import random

import pygame

from deck import get_rank, get_suit
from utils import card_costs, compare, getCardFront, getHalfCardFront


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
            area=getHalfCardFront(get_suit(self.old_card), get_rank(self.old_card)))
    #New card second, so its on top of old card
    self.display.blit(
        self.card_front,
        dest=(self.width / 2 - 20, self.height / 4 + 15),
        area=getCardFront(get_suit(self.new_card), get_rank(self.new_card)))
    
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
                    area=getHalfCardFront(get_suit(value), get_rank(value)))
            else:
                self.display.blit(
                    self.card_front,
                    dest=(40, (i * 15) - 32 * 15),
                    area=getHalfCardFront(get_suit(value), get_rank(value)))
        if len(self.deck.played_cards) > 32:
            self.display.blit(
                self.card_front,
                dest=(40, len(self.deck.played_cards) * 15 - 32 * 15 - 15),
                area=getCardFront(get_suit(sorted_played_cards[-1]), get_rank(sorted_played_cards[-1])))
        else:
            self.display.blit(
                self.card_front,
                dest=(0, len(self.deck.played_cards) * 15 - 15),
                area=getCardFront(get_suit(sorted_played_cards[-1]), get_rank(sorted_played_cards[-1])))
    
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
        gameBetClick(self, "higher")

    #Lower button
    if self.lower_button.collidepoint(mouse_x, mouse_y) and len(self.deck.cards) - len(self.deck.played_cards) > 0:
        gameBetClick(self, "lower")
    
    #Same button
    if self.same_button.collidepoint(mouse_x, mouse_y) and len(self.deck.cards) - len(self.deck.played_cards) > 0:
        gameBetClick(self, "same")
    
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
    self.score, self.streak = compare(self, bet)
    if len(self.deck.cards) - len(self.deck.played_cards) == 0 and self.highscore < self.score:
        with open("media/highscore.json", "w", encoding="utf-8") as file:
            file.write(json.dumps({"highscore": self.score}))
