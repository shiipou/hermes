from typing import List

class Story:
    max_player_interaction: int = None
    player_interaction: int = 0
    start: str = None
    story_plot: str = None
    adventures: List[str] = None

    def __init__(self, max_player_interaction: int, start: str, adventures: List[str] = []):
        self.max_player_interaction = max_player_interaction
        self.player_interaction = 0
        self.start = start
        self.adventures = adventures
