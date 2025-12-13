# classes.py

class Item:
    # Represents an item in the game
    def __init__(self, name: str, description: str, usage: str = None, points: int = 0):
        self.name = name
        self.description = description
        self.usage = usage
        self.points = points # Points gained for finding/using the item

class Location:
    # Represents a location (room) in the game
    def __init__(self, name: str, description: str, exits: dict, items: list = None,
                 npc: str = None, required_key: dict = None, exits_with_key: dict = None,
                 special_action: str = None):

        self.name = name
        self.description = description
        self.exits = exits          # What direction user can go
        self.items = items if items is not None else []
        self.npc = npc # non-playable character
        self.required_key = required_key # {'direction': 'Required Key Name'}
        self.exits_with_key = exits_with_key # {'direction': 'Target Location Name'}
        self.special_action = special_action # e.g., 'server_terminal', 'gas_hazard', 'exit_door'

class Player:
    # Represents the player and her state
    def __init__(self, start_location_name: str):
        self.current_location = start_location_name
        self.inventory = []
        self.score = 0
        self.max_score = 150
        self.has_worn_suit = False

    def add_score(self, points: int):
        # Adds points to the score and provides feedback
        self.score += points
        print(f"\n✨ You gained {points} points! Current score: {self.score}\n")