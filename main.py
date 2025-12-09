# main.py

from classes import Player
from data import GAME_WORLD, ALL_ITEMS

# --- GLOBAL GAME STATE ---
PLAYER = Player("Reception Area")
SERVER_ACTIVATED = False

# --- HELPER FUNCTIONS ---

def get_current_location():
    """Returns the current location object."""
    return GAME_WORLD[PLAYER.current_location]

def get_item_by_name(item_name_part: str, inventory_only: bool = False):
    """Searches for an item by partial name in inventory or current location."""
    # ... (Implementation of get_item_by_name from the previous response)

def display_location_info():
    """Displays information about the current location (look/explore command)."""
    # ... (Implementation of display_location_info)
    location = get_current_location()

    # Gas hazard check
    if location.special_action == "gas_hazard" and not PLAYER.has_worn_suit:
        print("\n❗️ DANGER: Toxic gas in the air. You lose points without protection.\n")
        PLAYER.add_score(-5)


def check_win_condition():
    """Checks the victory conditions."""
    # ... (Implementation of check_win_condition)
    global SERVER_ACTIVATED
    location = get_current_location()
    antidote = get_item_by_name("Antidote", inventory_only=True)

    if location.name == "Emergency Exit" and antidote and SERVER_ACTIVATED:
        PLAYER.add_score(100) # Victory bonus
        print("\n\n*** VICTORY! ***")
        # ... (Winning message)
        return True
    return False

# --- COMMAND INTERPRETER ---

def handle_command(command: str):
    """Interprets the user input command."""
    # ... (Implementation of handle_command, including all verbs: quit, look, go, take, drop, use, talk, examine, etc.)
    # IMPORTANT: Ensure the command processing (verb/noun splitting) and logic (especially 'go' and 'use')
    # correctly handle the imported classes and data structures.
    # ...

    return True # Continue game loop


# --- MAIN GAME LOOP ---

def play_game():
    """The main game loop."""
    print("=========================================")
    print(" | SECRET LABORATORY 'PROJECT OMEGA' |")
    print("=========================================")
    print("Goal: Activate the Server and escape with the Antidote via the Emergency Exit.")

    display_location_info()

    running = True
    while running:
        if check_win_condition():
            break

        command = input("\n> Enter command: ").strip()
        if not command:
            continue

        running = handle_command(command)

    print("\nGame over. Thank you for playing!")

if __name__ == "__main__":
    play_game()