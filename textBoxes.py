### text boxes that appear when a player is trying to undo a move, pass the turn
### or reset the game

import pygame
from static import *

# object for using text boxes
class TextBox(pygame.sprite.Sprite):
    bounds = (50, 200, 500, 200)
    
    def __init__(self, action):
        self.action = action
        text = "Are you sure you want to %s?" % action
        self.text = pygame.font.Font(None, 36).render(text, True, (0, 0, 0))
        
    def draw(self, screen):
        pygame.draw.rect(screen, Colors.WHITE, self.bounds)
        pygame.draw.rect(screen, Colors.BLACK, self.bounds, 5)
        screen.blit(self.text, (75, 225))
        BoolBox("Yes").draw(screen)
        BoolBox("No").draw(screen)
      
# the "yes" and "no" buttons on one such text box
class BoolBox(pygame.sprite.Sprite):
    def __init__(self, boolean):
        self.text = pygame.font.Font(None, 36).render(boolean, True, (0, 0, 0))
        if boolean == "Yes":
            self.bounds = GoConstants.YESBOXBOUNDS
            self.textPos = (100, 337)
        elif boolean == "No":
            self.bounds = GoConstants.NOBOXBOUNDS
            self.textPos = (405, 337)
        
    def draw(self, screen):
        pygame.draw.rect(screen, Colors.BLACK, self.bounds, 3)
        screen.blit(self.text, self.textPos)
        
# the "play" button on the start screen
class PlayButton(pygame.sprite.Sprite):
    bounds = (200, 250, 200, 50)
    
    def __init__(self):
        self.text = pygame.font.Font(None, 36).render("PLAY", True, (0, 0, 0))
        self.textPos = (270, 263)
        
    def draw(self, screen):
        pygame.draw.rect(screen, Colors.WHITE, self.bounds)
        pygame.draw.rect(screen, Colors.BLACK, self.bounds, 5)
        screen.blit(self.text, self.textPos)
        
# the "instructions" button on the start screen
class InstructionsButton(pygame.sprite.Sprite):
    bounds = (200, 325, 200, 50)
    
    def __init__(self):
        self.text = pygame.font.Font(None, 36).render("INSTRUCTIONS", True, (0, 0, 0))
        self.textPos = (205, 338)
        
    def draw(self, screen):
        pygame.draw.rect(screen, Colors.WHITE, self.bounds)
        pygame.draw.rect(screen, Colors.BLACK, self.bounds, 5)
        screen.blit(self.text, self.textPos)