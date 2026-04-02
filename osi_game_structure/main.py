import pygame
from ui.inventory import Inventory
from ui.start_menu import run_start_menu

from floors.physical_layer import run_physical_layer
from floors.data_link_layer import run_data_layer
from floors.network_layer import run_network_layer
from floors.transport_layer import run_transport_layer

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
    "transport": {},
    "session": {},
    "presentation": {},
    "application": {}
}

# ---------- TRANSITION FUNCTION ----------
def play_transition(screen):
    WIDTH, HEIGHT = screen.get_size()

    stairs1 = pygame.image.load("assets/stairs.jpg")
    stairs2 = pygame.image.load("assets/stairs1.jpg")

    stairs1 = pygame.transform.scale(stairs1, (WIDTH, HEIGHT))
    stairs2 = pygame.transform.scale(stairs2, (WIDTH, HEIGHT))

    # Show first image
    screen.blit(stairs1, (0,0))
    pygame.display.update()
    pygame.time.delay(500)

    # Show second image
    screen.blit(stairs2, (0,0))
    pygame.display.update()
    pygame.time.delay(500)


# ---------- START MENU ----------
run_start_menu(screen)

# ---------- SCENE LOOP ----------
current_scene = "physical"
prev_scene = None   # 🔥 track previous scene

running = True

while running:

    # 🎬 PLAY TRANSITION ONLY WHEN SCENE CHANGES
    # 🎬 PLAY TRANSITION ONLY WHEN SCENE CHANGES (EXCEPT PHYSICAL ↔ DATA)
    if prev_scene != current_scene and prev_scene is not None:

        skip_transition = (
            (prev_scene == "physical" and current_scene == "data") or
            (prev_scene == "data" and current_scene == "physical")
        )

        if not skip_transition:
            play_transition(screen)

    prev_scene = current_scene

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

    # -------- TRANSPORT LAYER --------
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