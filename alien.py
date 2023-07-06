import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""
    
    def __init__(self,ai_game):
        super().__init__()
        self.screen = ai_game.screen

        # Load the alien image and set its rect attribute.
        DEFAULT_IMAGE_SIZE = (50, 50)
        self.image = pygame.image.load('images/alien.png')
        self.image = pygame.transform.scale(self.image, DEFAULT_IMAGE_SIZE)
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)