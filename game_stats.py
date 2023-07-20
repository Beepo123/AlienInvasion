class GameStats:
    """Track statistics for Alien Invasion"""

    def __init__(self, ai_game):
        # Read high score from score file
        try:
            with open("scores.txt", 'r') as file:
                self.high_score = int(file.read())
        except FileNotFoundError:
            with open("scores.txt",'w') as file:
                file.write("0")
                self.high_score = 0

        self.settings = ai_game.settings
        self.game_active = False
        self.reset_stats()

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
