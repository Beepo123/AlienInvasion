import pygame


class Blimp:
    """A class to manage a blimp"""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect
        DEFAULT_IMAGE_SIZE = (70, 50)
        self.image = pygame.image.load("images/blimp.png")
        self.image = pygame.transform.scale(self.image, DEFAULT_IMAGE_SIZE)
        self.rect = self.image.get_rect()

        # Start ship at the bottom center of the screen
        self.rect.bottomright = self.screen_rect.bottomright

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)
