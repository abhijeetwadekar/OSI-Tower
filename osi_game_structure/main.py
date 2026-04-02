import pygame
from ui.inventory import Inventory
from ui.start_menu import run_start_menu

from floors.physical_layer import run_physical_layer
from floors.data_link_layer import run_data_layer
from floors.network_layer import run_network_layer
from floors.transport_layer import run_transport_layer   # ✅ ADDED

# 🔜 future layers
# from floors.session_layer import run_session_layer
# from floors.presentation_layer import run_presentation_layer
# from floors.application_layer import run_application_layer

pygame.init()

SCREEN_WIDTH = 1152
SCREEN_HEIGHT = 768

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("OSI Mystery Escape")

inventory = Inventory()

# ---------- STATE ----------
game_state = {
    "physical": {},
    "data_link": {},
    "network": {},
    "transport": {},   # ✅ already ready
    "session": {},
    "presentation": {},
    "application": {}
}

# ---------- START MENU ----------
run_start_menu(screen)

# ---------- SCENE LOOP ----------
current_scene = "physical"

running = True

while running:

    # -------- PHYSICAL LAYER --------
    if current_scene == "physical":
        current_scene = run_physical_layer(
            screen,
            inventory,
            game_state["physical"]
        )

    # -------- DATA LINK LAYER --------
    elif current_scene == "data":
        current_scene = run_data_layer(
            screen,
            inventory,
            game_state["physical"],
            game_state["data_link"]
        )

    # -------- NETWORK LAYER --------
    elif current_scene == "network":
        current_scene = run_network_layer(
            screen,
            inventory,
            game_state["data_link"],
            game_state["network"]
        )

    # -------- TRANSPORT LAYER ✅ --------
    elif current_scene == "transport":
        current_scene = run_transport_layer(
            screen,
            inventory,
            game_state["transport"]
        )

    # -------- FUTURE LAYERS --------
    elif current_scene == "session":
        print("Session layer not built yet")
        current_scene = "transport"

    elif current_scene == "presentation":
        print("Presentation layer not built yet")
        current_scene = "session"

    elif current_scene == "application":
        print("Application layer not built yet")
        current_scene = "presentation"

    # -------- EXIT GAME --------
    elif current_scene == "quit":
        running = False

pygame.quit()

# ---------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------
# 🔥 TEST ONLY TRANSPORT LAYER (for debugging)

# import pygame
# from ui.inventory import Inventory
# from floors.transport_layer import run_transport_layer

# pygame.init()

# SCREEN_WIDTH = 1152
# SCREEN_HEIGHT = 768

# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption("OSI Mystery Escape - Transport Layer Only")

# inventory = Inventory()

# game_state = {
#     "transport": {}
# }

# run_transport_layer(
#     screen,
#     inventory,
#     game_state["transport"]
# )

# pygame.quit()