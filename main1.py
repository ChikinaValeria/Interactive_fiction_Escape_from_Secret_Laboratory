# main.py (Финальная исправленная версия, гарантирующая продолжение игры)

from classes import Player
from data1 import GAME_WORLD, ALL_ITEMS

# --- GLOBAL GAME STATE ---
PLAYER = Player("Reception Area")
SERVER_ACTIVATED = False

# ... (HELPER FUNCTIONS: get_current_location, get_item_by_name, display_location_info, check_win_condition - без изменений) ...

def get_current_location():
    """Returns the current location object."""
    return GAME_WORLD[PLAYER.current_location]

def get_item_by_name(item_name_part: str, inventory_only: bool = False):
    """
    Searches for an item by partial name in inventory or current location.
    Returns the Item object if found, otherwise None.
    """
    items_list = PLAYER.inventory[:]
    if not inventory_only:
        items_list += get_current_location().items

    if not item_name_part:
        return None

    item_name_part = item_name_part.lower().strip()

    for item in items_list:
        if item_name_part in item.name.lower():
            return item
    return None

def display_location_info():
    """Displays information about the current location (look/explore command)."""
    location = get_current_location()

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

    antidote = get_item_by_name("Antidote", inventory_only=True)

    if location.name == "Emergency Exit" and antidote and SERVER_ACTIVATED:
        PLAYER.add_score(100)
        print("\n\n*** VICTORY! ***")
        print("You successfully reactivated the server, disabled the security, and escaped the complex.")
        print(f"You took the Antidote and are safe! Your final score: {PLAYER.score}/{PLAYER.max_score}")
        return True

    if location.name == "Emergency Exit":
        if not SERVER_ACTIVATED:
            print("❌ The emergency exit is still locked. You must activate the Server to disable the security system.")
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
        return False # Единственный случай, когда возвращаем False

    elif verb in ["look", "explore"]:
        display_location_info()

    # --- COMMAND INVENTORY/WITH ---
    elif verb in ["with", "inventory", "inv"]:
        if PLAYER.inventory:
            print("--- Your inventory: ---")
            for item in PLAYER.inventory:
                print(f"- {item.name} ({item.description})")
            if PLAYER.has_worn_suit:
                print("- Hazmat Suit (Worn)")
        else:
            print("Your inventory is empty.")
        print(f"Current score: {PLAYER.score}")

    # --- COMMAND GO (Movement) ---
    elif verb == "go":
        if not noun:
            print("❌ Go where? Specify a direction (e.g., 'go north').")
            return True

        if noun in location.exits:
            target_direction = noun

            if location.required_key and target_direction in location.required_key:
                required_key_name = location.required_key[target_direction]
                key_item = get_item_by_name(required_key_name, inventory_only=True)

                if key_item:
                    print(f"Hint: The door is locked by a card reader. Try to 'swipe {key_item.name}' to open it.")
                else:
                    print(f"❌ The passage {target_direction} is locked. You need the {required_key_name}.")

            else:
                PLAYER.current_location = location.exits[target_direction]
                PLAYER.add_score(1)
                display_location_info()
        else:
            print(f"Cannot go in that direction, or '{noun}' is not a valid exit.")

    # --- COMMAND TAKE (Take) ---
    elif verb == "take":
        if not noun:
            print("❌ Take what? Specify an item name.")
            return True # ГАРАНТИРУЕТ ПРОДОЛЖЕНИЕ ИГРЫ

        item_to_take = get_item_by_name(noun)
        if item_to_take and item_to_take in location.items:
            location.items.remove(item_to_take)
            PLAYER.inventory.append(item_to_take)
            PLAYER.add_score(item_to_take.points or 1)
            print(f"✅ You took: {item_to_take.name}")
        else:
            print(f"❌ Item '{noun}' is not here or cannot be taken.")

    # --- COMMAND DROP (Drop) ---
    elif verb == "drop":
        if not noun:
            print("❌ Drop what? Specify an item name.")
            return True

        item_to_drop = get_item_by_name(noun, inventory_only=True)
        if item_to_drop:
            PLAYER.inventory.remove(item_to_drop)
            location.items.append(item_to_drop)
            print(f"✅ You dropped: {item_to_drop.name}")
        else:
            print(f"❌ Item '{noun}' is not in your inventory.")

    # --- COMMAND SWIPE (New: Key Cards) ---
    elif verb == "swipe":
        if not noun:
            print("❌ Swipe what? Usage: swipe [key card name]")
            return True

        item_to_swipe = get_item_by_name(noun, inventory_only=True)
        if not item_to_swipe:
            print(f"❌ Item '{noun}' is not in your inventory.")
            return True

        if item_to_swipe.usage not in ["key_blue", "key_red"]:
            print(f"❌ {item_to_swipe.name} is not a Key Card and cannot be swiped.")
            return True

        target_direction = None
        for direction, required_key in location.required_key.items() if location.required_key else {}.items():
            if required_key.lower() == item_to_swipe.name.lower():
                target_direction = direction
                break

        if target_direction and location.exits_with_key and target_direction in location.exits_with_key:
            target_location_name = location.exits_with_key[target_direction]
            PLAYER.current_location = target_location_name
            PLAYER.add_score(5)
            print(f"✅ You successfully swiped the {item_to_swipe.name} and moved to {target_location_name}.")
            display_location_info()
        else:
            print(f"❌ The {item_to_swipe.name} does not open any locked doors here.")

    # --- COMMAND UPLOAD (New: Flash Drive at Server) ---
    elif verb == "upload":
        if location.special_action != "server_terminal":
            print("❌ You can only upload data at the Main Server Terminal in the Server Room.")
            return True

        if not noun:
            print("❌ Upload what? Usage: upload [flash drive name]")
            return True

        item_to_upload = get_item_by_name(noun, inventory_only=True)
        if not item_to_upload:
            print(f"❌ Item '{noun}' is not in your inventory.")
            return True

        if item_to_upload.usage != "upload":
            print(f"❌ {item_to_upload.name} is not a valid data source for the server.")
            return True

        global SERVER_ACTIVATED
        SERVER_ACTIVATED = True
        PLAYER.inventory.remove(item_to_upload)
        PLAYER.add_score(20)
        print(f"✅ {item_to_upload.name} connected. Server reactivated! Emergency Exit unlocked.")
        print("Note: The server has opened a new way.")

    # --- COMMAND WEAR (New: Hazmat Suit) ---
    elif verb == "wear":
        if not noun:
            print("❌ Wear what? Usage: wear [suit name]")
            return True

        item_to_wear = get_item_by_name(noun, inventory_only=True)

        if not item_to_wear:
            print(f"❌ Item '{noun}' is not in your inventory.")
            return True

        if item_to_wear.usage != "wear":
            print(f"❌ You cannot wear '{item_to_wear.name}'.")
            return True

        if PLAYER.has_worn_suit:
            print("You are already wearing a protective suit.")
            return True

        PLAYER.has_worn_suit = True
        PLAYER.add_score(5)
        PLAYER.inventory.remove(item_to_wear) # It's now worn, not in the inventory list
        print("✅ You put on the Hazmat Suit. You can now safely enter hazardous zones.")

    # --- COMMANDS FOR OTHER ITEMS (using generic 'use' logic) ---
    elif verb == "use":
        if not noun:
            print("❌ Use what? Specify an item name.")
            return True

        item_to_use = get_item_by_name(noun, inventory_only=True)
        if not item_to_use:
            print(f"❌ You don't have item '{noun}'.")
            return True

        if item_to_use.usage == "antidote":
            print("✅ You used the Antidote. This will save you from the gas upon exit.")
        elif item_to_use.usage == "drink" and item_to_use.name == "Water Canister":
            print("💧 You take a sip from the Water Canister. You feel refreshed.")
            PLAYER.add_score(1)
        elif item_to_use.usage == "connect" and item_to_use.name == "Wire" and location.special_action == "server_terminal":
            print("You connect the Wire to the server. It buzzes, but nothing happens. You still need the Flash Drive.")
            PLAYER.add_score(1)
        else:
            print(f"❌ Cannot use '{item_to_use.name}' here in this way.")

    # --- ADDITIONAL COMMANDS ---

    elif verb == "read":
        if not noun:
            print("❌ Read what? Specify an item name.")
            return True

        item_to_read = get_item_by_name(noun, inventory_only=True)

        if item_to_read and item_to_read.usage == "read":
            if item_to_read.name == "Accident Report":
                 print(f"Reading the {item_to_read.name}: 'The log details a controlled breach during testing of the Antidote on a new strain of airborne toxin. The server was locked down as a fail-safe.'")
                 PLAYER.add_score(2)
            else:
                print(f"You read the {item_to_read.name}. It contains only technical jargon.")
        else:
             print(f"❌ You cannot read '{noun}'.")

    elif verb == "talk":
        if location.npc == "Injured Guard":
            red_card = ALL_ITEMS["Red Key Card"]
            if red_card not in PLAYER.inventory:
                PLAYER.inventory.append(red_card)
                PLAYER.add_score(5)
                print("Guard: 'They... they took... the Red Key Card, it must be somewhere... oh wait, it's on me! Take it!'")
                print(f"✅ You received: {red_card.name}")
            else:
                 print("Guard: 'I need medical help... just leave me...'")
        else:
            print("There is no one here to talk to.")

    elif verb == "examine":
        if not noun:
            print("❌ Examine what? Specify an item name.")
            return True

        item_to_examine = get_item_by_name(noun, inventory_only=True)
        if item_to_examine:
            print(f"Examining {item_to_examine.name}: {item_to_examine.description}")
        else:
            print(f"❌ Item '{noun}' is not available to examine.")

    elif verb == "help":
        print("\n--- Available commands ---")
        print("Movement: go [north/south/east/west]")
        print("Interaction: take [item], drop [item], talk [npc], examine [item], read [item]")
        print("Special Actions:")
        print("  swipe [card name] (Use key cards on locked doors)")
        print("  upload [flash drive name] (Use at Server Room to activate server)")
        print("  wear [suit name] (Use Hazmat Suit)")
        print("Status: look/explore, inventory/with, score, quit")

    elif verb == "score":
        print(f"Your current score: {PLAYER.score}/{PLAYER.max_score}")

    else:
        if len(parts) > 2:
            print("❌ Too many words. Enter a one or two-word command (e.g., 'go north' or 'look').")
        else:
            print(f"❌ Unknown command: '{command}'. Try 'help'.")

    return True # Возвращение True по умолчанию для продолжения игры

# --- MAIN GAME LOOP ---
# ... (код play_game и EXECUTION без изменений)
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

# --- EXECUTION ---
if __name__ == "__main__":
    try:
        play_game()
    except KeyError as e:
        print("\n--- FATAL ERROR ---")
        print(f"A location key error occurred. Check if '{e.args[0]}' exists in GAME_WORLD or if it's the correct starting location.")