import json

import pygame

from utils import card_costs


def drawStartMenu(self):
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

def handleStartMenuClick(self, mouse_pos: list):
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
        
        self.times_cards_rerolled = 1
        self.times_upgrades_rerolled = 1
        
        self.previous_state = "shop"
        self.play_state = "shop"
