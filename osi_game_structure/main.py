import sys
import atexit
import pygame
import time  # ← ADD THIS
from ui.inventory import Inventory
from ui.start_menu import run_start_menu

from floors.physical_layer import run_physical_layer
from floors.data_link_layer import run_data_layer
from floors.network_layer import run_network_layer
from floors.transport_layer import run_transport_layer
from floors.session_layer import run_session_layer
from floors.presentation_layer import run_presentation_layer
from floors.application_layer import run_application_layer

import base64

def safe_exit():
    global game_saved

    print("Saving before exit...")

    total_time = int(time.time() - game_start_time)

    if not game_saved:
        save_score(player_name, total_time)
        game_saved = True

    pygame.quit()
    sys.exit()

def save_score(name, time_taken):

    minutes = time_taken // 60
    seconds = time_taken % 60
    formatted_time = f"{minutes:02}:{seconds:02}"

    with open("leaderboard.txt", "a") as file:
        file.write(f"{name} - {formatted_time}\n")

# def save_score(name, time_taken):
#     data = f"{name}:{time_taken}"
#     encoded = base64.b64encode(data.encode()).decode()

#     with open("leaderboard.dat", "a") as file:
#         file.write(encoded + "\n")

pygame.init()

SCREEN_WIDTH = 1152
SCREEN_HEIGHT = 768

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("OSI Mystery Escape")

inventory = Inventory()
timer_font = pygame.font.SysFont(None, 32)  # ← ADD THIS

# ---------- LOAD STAIRS IMAGES ----------
stairs_img = pygame.image.load("assets/stairs.jpg")
stairs1_img = pygame.image.load("assets/stairs1.jpg")

stairs_img = pygame.transform.scale(stairs_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
stairs1_img = pygame.transform.scale(stairs1_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# ---------- TRANSITION FUNCTION ----------
def play_stairs_transition(screen):
    screen.blit(stairs_img, (0, 0))
    pygame.display.flip()
    pygame.time.delay(250)

    screen.blit(stairs1_img, (0, 0))
    pygame.display.flip()
    pygame.time.delay(250)

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

# ---------- TIMER STATE ----------        # ← ADD THIS BLOCK
game_start_time = None                     # starts after start menu
countdown_active = False                   # wall puzzle triggered
countdown_start = None
COUNTDOWN_LIMIT = 420                      # 7 minutes

# ---------- START MENU ----------
player_name = run_start_menu(screen)
game_start_time = time.time()              # ← clock starts after menu

# ---------- DRAW HUD ----------           # ← ADD THIS FUNCTION
def draw_hud(surface, panel_x=10, start_y=10):
    elapsed = int(time.time() - game_start_time)
    e_min, e_sec = elapsed // 60, elapsed % 60
    elapsed_txt = timer_font.render(f"{e_min:02}:{e_sec:02}", True, (200, 200, 200))
    surface.blit(elapsed_txt, (panel_x, start_y))

    if countdown_active:
        remaining = max(0, COUNTDOWN_LIMIT - int(time.time() - countdown_start))
        r_min, r_sec = remaining // 60, remaining % 60
        color = (255, 50, 50) if remaining <= 60 else (255, 200, 0)
        txt = timer_font.render(f"⚠ {r_min:02}:{r_sec:02}", True, color)
        surface.blit(txt, (panel_x, start_y - 25))
        if remaining <= 0:
            return "game_over"
    return None


    # Elapsed clock (always running)
    elapsed = int(time.time() - game_start_time)
    e_min = elapsed // 60
    e_sec = elapsed % 60
    elapsed_txt = timer_font.render(f"Time: {e_min:02}:{e_sec:02}", True, (200, 200, 200))
    screen.blit(elapsed_txt, (10, 10))

    # Countdown (only when active)
    if countdown_active:
        remaining = max(0, COUNTDOWN_LIMIT - int(time.time() - countdown_start))
        r_min = remaining // 60
        r_sec = remaining % 60
        color = (255, 50, 50) if remaining <= 60 else (255, 200, 0)
        countdown_txt = timer_font.render(f"ALERT: {r_min:02}:{r_sec:02}", True, color)
        screen.blit(countdown_txt, (10, 40))

        if remaining <= 0:
            return "game_over"

    return None

# ---------- SCENE LOOP ----------
current_scene = "physical"
previous_scene = None
running = True

game_saved = False

atexit.register(lambda: save_score(player_name, int(time.time() - game_start_time)))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            safe_exit()

    if previous_scene and current_scene != previous_scene:
        skip_transition = (
            (previous_scene == "physical" and current_scene == "data") or
            (previous_scene == "data" and current_scene == "physical")
        )
        if not skip_transition:
            play_stairs_transition(screen)

    previous_scene = current_scene

    # -------- PHYSICAL --------
    if current_scene == "physical":
        current_scene = run_physical_layer(screen, inventory, game_state["physical"],draw_hud)

    elif current_scene == "data":
        current_scene = run_data_layer(screen, inventory, game_state["physical"], game_state["data_link"],draw_hud)

    elif current_scene == "network":
        current_scene = run_network_layer(screen, inventory, game_state["data_link"], game_state["network"],draw_hud)

    elif current_scene == "transport":
        current_scene = run_transport_layer(screen, inventory, game_state["transport"],draw_hud)

    elif current_scene == "session":
        current_scene = run_session_layer(screen, inventory, game_state["session"],draw_hud)

        # ← CHECK if wall puzzle started the countdown
        if game_state["session"].get("timer_active") and not countdown_active:
            countdown_active = True
            countdown_start = game_state["session"]["timer_start"]

    elif current_scene == "presentation":
        current_scene = run_presentation_layer(screen, inventory, game_state["presentation"],draw_hud)

    elif current_scene == "application":
        current_scene = run_application_layer(screen, inventory, game_state["application"],draw_hud)

    elif current_scene == "game_over":

        print("GAME OVER TRIGGERED")

        total_time = int(time.time() - game_start_time)

        if not game_saved:
            save_score(player_name, total_time)
            game_saved = True

        from floors.application_layer import play_game_over
        play_game_over(screen, player_name, total_time)

        running = False

    # -------- DRAW HUD ON TOP --------   # ← ADD THIS
    # result = 
    draw_hud(screen)

    pygame.display.update()



pygame.quit()