from classes import Player
from data import GAME_WORLD, ALL_ITEMS

# --- GLOBAL GAME STATE ---
# Player initialization (assuming 'Reception Area' is defined in GAME_WORLD)
PLAYER = Player("Reception Area")
SERVER_ACTIVATED = False

# --- HELPER FUNCTIONS ---

def get_current_location():
    """Returns the current location object."""
    # This might raise a KeyError if the starting location name is wrong in Player.__init__
    return GAME_WORLD[PLAYER.current_location]

def get_item_by_name(item_name_part: str, inventory_only: bool = False):
    """
    Searches for an item by partial name in inventory or current location.
    Returns the Item object if found, otherwise None.
    """
    items_list = PLAYER.inventory[:] # Start with a copy of inventory
    if not inventory_only:
        items_list += get_current_location().items

    # Lowercase input for robust search
    item_name_part = item_name_part.lower().strip()

    for item in items_list:
        if item_name_part in item.name.lower():
            return item
    return None

def display_location_info():
    """Displays information about the current location (look/explore command)."""
    location = get_current_location()

    # Description
    print(f"\n--- You are in: {location.name} ---")
    print(location.description)

    # Items
    if location.items:
        items_names = [item.name for item in location.items]
        print(f"Items here: {', '.join(items_names)}")

    # NPC
    if location.npc:
        print(f"Character: {location.npc} is here.")

    # Exits
    exits_list = []
    for direction, target in location.exits.items():
        if location.required_key and direction in location.required_key:
            # Locked exit
            exits_list.append(f"{direction} (locked)")
        else:
            exits_list.append(f"{direction}")

    print(f"You can go: {', '.join(exits_list)}")

    # Gas hazard check and score penalty
    if location.special_action == "gas_hazard" and not PLAYER.has_worn_suit:
        print("\n❗️ DANGER: Toxic gas in the air. You lose points without protection.\n")
        PLAYER.add_score(-5)

def check_win_condition():
    """Checks the victory conditions (Emergency Exit, Antidote, Server Activated)."""
    global SERVER_ACTIVATED
    location = get_current_location()

    # Note: 'Antidote' check uses partial match, assuming its full name is 'Antidote'
    antidote = get_item_by_name("Antidote", inventory_only=True)

    # Victory condition: Must be at Emergency Exit, possess Antidote, and Server must be activated.
    if location.name == "Emergency Exit" and antidote and SERVER_ACTIVATED:
        PLAYER.add_score(100) # Victory bonus
        print("\n\n*** VICTORY! ***")
        print("You successfully reactivated the server, disabled the security, and escaped the complex.")
        print(f"You took the Antidote and are safe! Your final score: {PLAYER.score}/{PLAYER.max_score}")
        return True

    # Feedback if at the exit but conditions aren't met
    if location.name == "Emergency Exit":
        if not SERVER_ACTIVATED:
            print("❌ The main exit is still locked. You must activate the Server to disable the security system.")
        elif not antidote:
            print("⚠️ The exit is open, but the toxic gas is spreading. You must find the Antidote first!")

    return False

# --- COMMAND INTERPRETER ---

def handle_command(command: str):
    """Interprets the user input command."""
    global SERVER_ACTIVATED

    parts = command.lower().split()
    if not parts:
        return True

    verb = parts[0]
    noun = " ".join(parts[1:]) if len(parts) > 1 else None
    location = get_current_location()

    if verb in ["quit", "exit"]:
        print("Quitting the game...")
        return False # Stops the main loop

    elif verb in ["look", "explore"]:
        display_location_info()

    # --- COMMAND INVENTORY/WITH ---
    elif verb in ["with", "inventory", "inv"]:
        if PLAYER.inventory:
            print("--- Your inventory: ---")
            for item in PLAYER.inventory:
                print(f"- {item.name} ({item.description})")
        else:
            print("Your inventory is empty.")
        print(f"Current score: {PLAYER.score}")

    # --- COMMAND GO (Movement) ---
    elif verb == "go":
        if noun in location.exits:
            target_direction = noun

            # Check if exit is locked and requires a key
            if location.required_key and target_direction in location.required_key:
                required_key_name = location.required_key[target_direction]
                key_item = get_item_by_name(required_key_name, inventory_only=True)

                if key_item:
                    # Successful passage with key
                    target_location_name = location.exits_with_key.get(target_direction)
                    if target_location_name:
                        PLAYER.current_location = target_location_name
                        PLAYER.add_score(5)
                        print(f"✅ You used the {key_item.name} and moved to {target_location_name}.")
                        display_location_info()
                else:
                    print(f"❌ The passage {target_direction} is locked. You need the {required_key_name}.")

            # Unlocked passage
            else:
                PLAYER.current_location = location.exits[target_direction]
                PLAYER.add_score(1)
                display_location_info()
        else:
            print(f"Cannot go in that direction, or '{noun}' is not a valid exit.")

    # --- COMMAND TAKE (Take) ---
    elif verb == "take":
        item_to_take = get_item_by_name(noun)
        if item_to_take and item_to_take in location.items:
            location.items.remove(item_to_take)
            PLAYER.inventory.append(item_to_take)
            PLAYER.add_score(item_to_take.points or 1)
            print(f"✅ You took: {item_to_take.name}")
        else:
            print(f"❌ Item '{noun}' is not here.")

    # --- COMMAND DROP (Drop) ---
    elif verb == "drop":
        item_to_drop = get_item_by_name(noun, inventory_only=True)
        if item_to_drop:
            PLAYER.inventory.remove(item_to_drop)
            location.items.append(item_to_drop)
            print(f"✅ You dropped: {item_to_drop.name}")
        else:
            print(f"❌ Item '{noun}' is not in your inventory.")

    # --- COMMAND USE (Use) ---
    elif verb == "use":
        item_to_use = get_item_by_name(noun, inventory_only=True)
        if not item_to_use:
            print(f"❌ You don't have item '{noun}'.")
            return

        # Use: Upload Flash Drive at Server Terminal
        if item_to_use.usage == "upload" and location.special_action == "server_terminal":
            global SERVER_ACTIVATED
            SERVER_ACTIVATED = True
            PLAYER.inventory.remove(item_to_use)
            PLAYER.add_score(20)
            print("✅ Flash Drive connected. Server reactivated! Emergency Exit unlocked.")

        # Use: Wear Hazmat Suit
        elif item_to_use.usage == "wear" and item_to_use.name == "Hazmat Suit":
            PLAYER.has_worn_suit = True
            PLAYER.add_score(5)
            # Remove from inventory since it is now "worn"
            PLAYER.inventory.remove(item_to_use)
            print("✅ You put on the Hazmat Suit. You can now safely enter hazardous zones.")

        # Use: Antidote (only confirms usage for victory condition)
        elif item_to_use.usage == "antidote":
             print("✅ You used the Antidote. This will save you from the gas upon exit.")

        else:
            print(f"❌ Cannot use '{item_to_use.name}' here in this way.")

    # --- ADDITIONAL COMMANDS ---

    elif verb == "talk":
        if location.npc == "Injured Guard":
            print("Guard: 'They... they took... the Red Key Card, it must be somewhere... oh wait, it's on me! Take it!'")
            PLAYER.add_score(2)
        else:
            print("There is no one here to talk to.")

    elif verb == "examine":
        item_to_examine = get_item_by_name(noun, inventory_only=True)
        if item_to_examine:
            print(f"Examining {item_to_examine.name}: {item_to_examine.description}")
        else:
            print(f"❌ Item '{noun}' is not available to examine.")

    elif verb == "help":
        print("Available commands: quit, look/explore, inventory/with, go [direction], take [item], drop [item], use [item], talk, examine.")

    elif verb == "score":
        print(f"Your current score: {PLAYER.score}/{PLAYER.max_score}")

    # Unknown command or invalid format
    else:
        if len(parts) > 2:
            print("❌ Too many words. Enter a one or two-word command (e.g., 'go north' or 'look').")
        else:
            print(f"❌ Unknown command: '{command}'.")

    return True # Continue game loop


# --- MAIN GAME LOOP ---

def play_game():
    """The main game loop."""

    print("=========================================")
    print(" | SECRET LABORATORY 'PROJECT OMEGA' |")
    print("=========================================")
    print("Goal: Activate the Server and escape with the Antidote via the Emergency Exit.")

    # Initial location description
    display_location_info()

    running = True
    while running:
        # Check victory condition before prompting for new command
        if check_win_condition():
            break

        command = input("\n> Enter command: ").strip()
        if not command:
            continue

        # Process the command
        running = handle_command(command)

    print("\nGame over. Thank you for playing!")

# --- EXECUTION ---
if __name__ == "__main__":
    try:
        play_game()
    except KeyError as e:
        print("\n--- FATAL ERROR ---")
        print(f"A location key error occurred. Check if '{e.args[0]}' exists in GAME_WORLD or if it's the correct starting location.")