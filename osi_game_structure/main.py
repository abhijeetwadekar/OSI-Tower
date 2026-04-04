# import pygame
# from ui.inventory import Inventory
# from ui.start_menu import run_start_menu

# from floors.physical_layer import run_physical_layer
# from floors.data_link_layer import run_data_layer
# from floors.network_layer import run_network_layer
# from floors.transport_layer import run_transport_layer
# from floors.session_layer import run_session_layer
# from floors.presentation_layer import run_presentation_layer
# from floors.application_layer import run_application_layer   # ✅ NEW

# pygame.init()

# SCREEN_WIDTH = 1152
# SCREEN_HEIGHT = 768

# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption("OSI Mystery Escape")

# inventory = Inventory()

# # ---------- LOAD STAIRS IMAGES ----------
# stairs_img = pygame.image.load("assets/stairs.jpg")
# stairs1_img = pygame.image.load("assets/stairs1.jpg")

# stairs_img = pygame.transform.scale(stairs_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
# stairs1_img = pygame.transform.scale(stairs1_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# # ---------- TRANSITION FUNCTION ----------
# def play_stairs_transition(screen):
#     screen.blit(stairs_img, (0, 0))
#     pygame.display.flip()
#     pygame.time.delay(250)

#     screen.blit(stairs1_img, (0, 0))
#     pygame.display.flip()
#     pygame.time.delay(250)

# # ---------- STATE ----------
# game_state = {
#     "physical": {},
#     "data_link": {},
#     "network": {},
#     "transport": {},
#     "session": {},
#     "presentation": {},
#     "application": {}   # ✅ NOW USED
# }

# # ---------- START MENU ----------
# run_start_menu(screen)

# # ---------- SCENE LOOP ----------
# current_scene = "physical"
# previous_scene = None

# running = True

# while running:

#     # 🎯 PLAY TRANSITION
#     if previous_scene and current_scene != previous_scene:
#         skip_transition = (
#             (previous_scene == "physical" and current_scene == "data") or
#             (previous_scene == "data" and current_scene == "physical")
#         )

#         if not skip_transition:
#             play_stairs_transition(screen)

#     previous_scene = current_scene

#     # -------- PHYSICAL --------
#     if current_scene == "physical":
#         current_scene = run_physical_layer(screen, inventory, game_state["physical"])

#     # -------- DATA LINK --------
#     elif current_scene == "data":
#         current_scene = run_data_layer(
#             screen, inventory,
#             game_state["physical"],
#             game_state["data_link"]
#         )

#     # -------- NETWORK --------
#     elif current_scene == "network":
#         current_scene = run_network_layer(
#             screen, inventory,
#             game_state["data_link"],
#             game_state["network"]
#         )

#     # -------- TRANSPORT --------
#     elif current_scene == "transport":
#         current_scene = run_transport_layer(
#             screen, inventory,
#             game_state["transport"]
#         )

#     # -------- SESSION --------
#     elif current_scene == "session":
#         current_scene = run_session_layer(
#             screen, inventory,
#             game_state["session"]
#         )

#     # -------- PRESENTATION --------
#     elif current_scene == "presentation":
#         current_scene = run_presentation_layer(
#             screen,
#             inventory,
#             game_state["presentation"]
#         )

#     # -------- APPLICATION ✅ FULLY CONNECTED --------
#     elif current_scene == "application":
#         current_scene = run_application_layer(
#             screen,
#             inventory,
#             game_state["application"]
#         )

#     # -------- EXIT --------
#     elif current_scene == "quit":
#         running = False

# pygame.quit()


# ==================================================================================
# 🔧 DEBUG MODE: RUN APPLICATION LAYER ONLY (KEEP COMMENTED)
# ==================================================================================

import pygame
from ui.inventory import Inventory
from floors.application_layer import run_application_layer

pygame.init()

WIDTH, HEIGHT = 1152, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Test Application Layer")

inventory = Inventory()
application_state = {}

while True:
    next_scene = run_application_layer(screen, inventory, application_state)

    if next_scene == "presentation":
        print("Back to presentation (loop continues)")

    elif next_scene == "underground":
        print("Going underground (test loop continues)")

    elif next_scene == "quit":
        break

pygame.quit()