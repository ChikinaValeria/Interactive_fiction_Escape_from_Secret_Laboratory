# data.py

from classes import Item, Location

# Initialization of items

# Key items
item_blue_card = Item("Blue Key Card", "Grants access to Zone C.", usage="key_blue", points=5)
item_red_card = Item("Red Key Card", "Grants access to Zone B.", usage="key_red", points=5)
item_flash_drive = Item("Flash Drive with Code", "Contains data to reactivate the server.", usage="upload", points=10)
item_antidote = Item("Antidote", "Salvation from the gas. Essential for winning.", usage="antidote", points=40)

# Gear
item_suit = Item("Hazmat Suit", "Protects against biohazard.", usage="wear", points=10)

# Additional items
item_water_canister = Item("Water Canister", "Heavy, but holds clean water.", usage="drink", points=1)
item_accident_report = Item("Accident Report", "A full log of the Omega Project failure.", usage="read", points=1)
item_wire = Item("Wire", "A standard server wire, likely useful.", usage="connect", points=1)

# List of items
ALL_ITEMS = {item.name: item for item in [
    item_blue_card, item_red_card, item_flash_drive, item_antidote,
    item_suit, item_water_canister, item_accident_report, item_wire,
    Item("Battery", "A standard AA battery.", points=1),
]}

# Initialization of locations

# Zone D
loc_1 = Location("Reception Area", "You stand in an empty reception. Main doors are locked.",
                 exits={"north": "D-4 Corridor", "east": "Cloakroom", "south": "Cafeteria"})
loc_2 = Location("Cloakroom", "Rows of lockers, some are open. A blue card is visible.",
                 exits={"west": "Reception Area", "east": "D-4 Corridor"},
                 items=[ALL_ITEMS["Blue Key Card"]])
loc_3 = Location("Cafeteria", "The mess hall. The air is stale. There is a water canister.",
                 exits={"north": "Reception Area", "east": "Waste Lab"},
                 items=[ALL_ITEMS["Water Canister"]])
loc_4 = Location("D-4 Corridor", "A connecting corridor between Zone D.",
                 exits={"north": "Ventilation Access", "south": "Reception Area", "west": "Cloakroom"})
loc_5 = Location("Waste Lab", "Smells of chemicals and burnt trash.",
                 exits={"west": "Cafeteria"})
loc_6 = Location("Ventilation Access", "A grate leads to the ventilation system, continuing to Zone C.",
                 exits={"south": "D-4 Corridor"},
                 required_key={"east": "Blue Key Card"},
                 exits_with_key={"east": "C-2 Laboratory"})

# Research zone C
loc_7 = Location("C-2 Laboratory", "A sterile lab with a wounded guard on the floor.",
                 exits={"west": "Ventilation Access", "north": "Reagent Storage", "south": "Server Room"},
                 npc="Injured Guard")
loc_8 = Location("Server Room", "The room buzzes with power. The Main Server Terminal is here.",
                 exits={"north": "C-2 Laboratory", "east": "Data Storage"},
                 special_action="server_terminal",
                 items=[ALL_ITEMS["Wire"]])
loc_9 = Location("Doctor's Office", "A messy office. Looks like someone left in a hurry.",
                 exits={"north": "Rest Area", "east": "Reagent Storage"},
                 items=[ALL_ITEMS["Flash Drive with Code"]])
loc_10 = Location("Reagent Storage", "Shelves full of chemicals. Better not touch anything.",
                  exits={"west": "Doctor's Office", "south": "C-2 Laboratory"})
loc_11 = Location("Data Storage", "Rows of secure cabinets for project archives.",
                  exits={"west": "Server Room", "south": "Elevator (C-B)"},
                  items=[ALL_ITEMS["Accident Report"]])
loc_12 = Location("Rest Area", "A small room with a coffee machine.",
                  exits={"south": "Doctor's Office", "east": "Elevator (C-B)"})
loc_13 = Location("Elevator (C-B)", "An old freight lift, leading to Zone B.",
                  exits={"west": "Rest Area", "north": "Data Storage"},
                  required_key={"east": "Red Key Card"},
                  exits_with_key={"east": "B-1 Corridor"})

# Zone B (bio-zone) and exit
loc_14 = Location("B-1 Corridor", "WARNING: High levels of biohazard gas detected.",
                  exits={"west": "Elevator (C-B)", "east": "Bio-Isolation Chamber", "south": "Guard Post B"},
                  special_action="gas_hazard")
loc_15 = Location("Bio-Isolation Chamber", "A decontamination area, currently inactive.",
                  exits={"west": "B-1 Corridor", "north": "Sample Cooler"})
loc_16 = Location("Sample Cooler", "Below-freezing temperatures for biological samples.",
                  exits={"south": "Bio-Isolation Chamber", "east": "Antidote Sector"})
loc_17 = Location("Antidote Sector", "The final lockbox. The Antidote is inside.",
                  exits={"west": "Sample Cooler"},
                  items=[ALL_ITEMS["Antidote"]])
loc_18 = Location("Guard Post B", "A deserted security post. A Hazmat Suit hangs here.",
                  exits={"north": "B-1 Corridor", "east": "Emergency Exit", "south": "Technical Access"},
                  items=[ALL_ITEMS["Hazmat Suit"]])
loc_19 = Location("Emergency Exit", "The final door. The main objective door.",
                  exits={"west": "Guard Post B"})
loc_20 = Location("Technical Access", "A service area leading nowhere important.",
                  exits={"north": "Guard Post B"})

# Game world dictionary
GAME_WORLD = {loc.name: loc for loc in [
    loc_1, loc_2, loc_3, loc_4, loc_5, loc_6, loc_7, loc_8, loc_9, loc_10,
    loc_11, loc_12, loc_13, loc_14, loc_15, loc_16, loc_17, loc_18, loc_19, loc_20
]}