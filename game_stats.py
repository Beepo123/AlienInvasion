class GameStats:
    """Track statistics for Alien Invasion"""

    def __init__(self, ai_game):
        # Read high score from score file
        with open("scores.txt", 'r') as file:
            self.high_score = int(file.read())
        self.settings = ai_game.settings
        self.game_active = False
        self.reset_stats()

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
