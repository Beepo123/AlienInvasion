import sys
from time import sleep

import pygame
from random import randint

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from star import Star
from game_stats import GameStats
from button import Button


class AlienInvasion:
    """Overall call to manage game assets and behavior"""

    def __init__(self):
        """Initialize the game and create game resources"""
        # Initialize game window
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_w, self.settings.screen_h)
        )
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics.
        self.stats = GameStats(self)

        # Create game resourices
        self.ship = Ship(self)
        self.stars = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_stars()
        self._create_fleet()

        # Make play button
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start the main loop of the game"""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        """respond to key press and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p and self.stats.game_active == False:
            self._start_game()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update the position of bullets and get rid of old bullets."""
        # Update bullet positions
        self.bullets.update()

        # Ger rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # Check for bullets that have hit aliens.
        # if so get rid of bullet and alien
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            # Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

    def _create_fleet(self):
        """Create the fleet of aliens"""
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_w - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of alien that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_h - (3 * alien_height) - ship_height
        number_rows = (available_space_y // (2 * alien_height)) // 2

        # Create full fleet of alien
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond if any aliens reached the edge of screen"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop entire fleet and change fleet direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_stars(self):
        for number_star in range(self.settings.max_stars):
            star = Star(self)
            star.rect.x = randint(0, self.settings.screen_w)
            star.rect.y = randint(0, self.settings.screen_h // 2)
            self.stars.add(star)

    def _update_aliens(self):
        """
        fleet_direction of 1 represents right; -1 represents left.
            self.fleet_direction = 1
        """
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _ship_hit(self):
        # Decrement ship left
        self.stats.ships_left -= 1
        if self.stats.ships_left > 0:
            # Get rid of any remaining aliens and bullets
            self.bullets.empty()
            self.aliens.empty()

            # pause game
            sleep(0.5)

            # Create new fleet and center ship
            self._create_fleet()
            self.ship.center_ship()
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_play_button(self, mouse_pos):
        """Start a new game when player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.stats.game_active == False:
            self._start_game()

    def _start_game(self):
        # Reset game settings.
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.stats.game_active = True
        pygame.mouse.set_visible(False)

        # Get rid of remaining aliens and bullets
        self.aliens.empty()
        self.bullets.empty()

        # Create new fleet and center the ship
        self._create_fleet()
        self.ship.center_ship()

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.stars.draw(self.screen)
        self.aliens.draw(self.screen)

        # Draw the play button if game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == "__main__":
    # make game instance and run game
    ai = AlienInvasion()
    ai.run_game()
