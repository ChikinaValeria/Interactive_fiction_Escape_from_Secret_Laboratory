# data.py

from classes import Item, Location

# --- ITEMS INITIALIZATION ---

# Key items for progression and victory
item_blue_card = Item("Blue Key Card", "Grants access to Zone C.", usage="key_blue", points=5)
item_red_card = Item("Red Key Card", "Grants access to Zone B.", usage="key_red", points=5)
item_flash_drive = Item("Flash Drive with Code", "Contains data to reactivate the server.", usage="upload", points=10)
item_antidote = Item("Antidote", "Salvation from the gas. Essential for winning.", usage="antidote", points=50)

# Gear
item_suit = Item("Hazmat Suit", "Protects against biohazard.", usage="wear", points=10)

# --- GLOBAL ITEM LIST ---
ALL_ITEMS = {item.name: item for item in [
    item_blue_card, item_red_card, item_flash_drive, item_antidote,
    item_suit, Item("Accident Report", "Nothing important written here.", usage="read"),
    Item("Battery", "A standard AA battery.", points=1),
    Item("Water Canister", "Heavy and currently useless.", points=1)
]}

# --- LOCATIONS INITIALIZATION ---
# (Using the map structure discussed previously)

# Zone D Locations
loc_1 = Location("Reception Area", "You stand in an empty reception. Main doors are locked.",
                 exits={"north": "D-4 Corridor", "east": "Cloakroom", "south": "Cafeteria"},
                 special_action="exit_door")
loc_2 = Location("Cloakroom", "Rows of lockers, some are open.",
                 exits={"west": "Reception Area"},
                 items=[ALL_ITEMS["Blue Key Card"]])
# ...
# loc_6 needs specific parameters for locked doors:
loc_6 = Location("Ventilation Access", "A grate leads to the ventilation system, continuing to Zone C.",
                 exits={"south": "D-4 Corridor"},
                 required_key={"east": "Blue Key Card"},
                 exits_with_key={"east": "C-2 Laboratory"},
                 items=[ALL_ITEMS["Accident Report"]])
# ... (Continue defining all 20 locations)

# --- GAME WORLD DICTIONARY ---
GAME_WORLD = {loc.name: loc for loc in [
    loc_1, loc_2, loc_6, # Add all 20 loc_ objects here
    # ...
]}