import sys
import pygame
from settings import Settings
from ship import Ship
from blimp import Blimp

class AlienInvasion:
    """Overall call to manage game assets and behavior"""

    def __init__(self):
        """Initialize the game and create game resources"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_w, self.settings.screen_h)
        )
        pygame.display.set_caption("Alien Invasion")
        
        self.ship = Ship(self)
        self.blimp = Blimp(self)

    def run_game(self):
        """Start the main loop of the game"""
        while True:
            self._check_events()
            self._update_screen()

    def _check_events(self):
        """respond to key press and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    # Move ship to right
                    self.ship.rect.x += 1
                elif event.key == pygame.K_LEFT:
                    self.ship.rect.x -= 1
                elif event.key == pygame.K_UP:
                    self.ship.rect.y -= 1
                elif event.key == pygame.K_DOWN:
                    self.ship.rect.y += 1

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        self.blimp.blitme()
        pygame.display.flip()


if __name__ == "__main__":
    # make game instance and run game
    ai = AlienInvasion()
    ai.run_game()