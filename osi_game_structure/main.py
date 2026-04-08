import pygame
import time  # ← ADD THIS
import atexit
import os
import signal
from ui.inventory import Inventory
from ui.start_menu import run_start_menu

from floors.physical_layer import run_physical_layer
from floors.data_link_layer import run_data_layer
from floors.network_layer import run_network_layer
from floors.transport_layer import run_transport_layer
from floors.session_layer import run_session_layer, run_stairs_transition
from floors.presentation_layer import run_presentation_layer
from floors.application_layer import run_application_layer

import base64

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCORE_FILE = os.path.join(BASE_DIR, "leaderboard.dat")

player_name = None
score_saved = False
game_start_time = None

# Keep a reference so Windows does not garbage collect the callback.
_windows_console_handler_ref = None

def save_score(name, time_taken):
    data = f"{name}:{time_taken}"
    encoded = base64.b64encode(data.encode()).decode()

    with open(SCORE_FILE, "a", encoding="utf-8") as file:
        file.write(encoded + "\n")
        file.flush()
        os.fsync(file.fileno())

def save_score_once(force=False):
    global score_saved

    if score_saved:
        return None

    if game_start_time is None:
        if not force:
            return None
        total_time = 0
    else:
        total_time = int(time.time() - game_start_time)

    name_to_save = player_name if player_name else "Unknown"
    save_score(name_to_save, total_time)
    score_saved = True
    return total_time


def _graceful_shutdown(signum, frame):
    save_score_once(force=True)
    pygame.quit()
    raise SystemExit(0)


def _register_signal_handlers():
    for sig_name in ("SIGINT", "SIGTERM", "SIGBREAK"):
        sig = getattr(signal, sig_name, None)
        if sig is not None:
            try:
                signal.signal(sig, _graceful_shutdown)
            except (OSError, ValueError):
                pass


def _register_windows_console_close_handler():
    global _windows_console_handler_ref

    if os.name != "nt":
        return

    try:
        import ctypes
        from ctypes import wintypes
    except Exception:
        return

    CTRL_CLOSE_EVENT = 2
    CTRL_LOGOFF_EVENT = 5
    CTRL_SHUTDOWN_EVENT = 6

    HANDLER_ROUTINE = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.DWORD)

    @HANDLER_ROUTINE
    def _console_handler(ctrl_type):
        if ctrl_type in (CTRL_CLOSE_EVENT, CTRL_LOGOFF_EVENT, CTRL_SHUTDOWN_EVENT):
            try:
                save_score_once(force=True)
            except Exception:
                pass
        return False

    try:
        ok = ctypes.windll.kernel32.SetConsoleCtrlHandler(_console_handler, True)
        if ok:
            _windows_console_handler_ref = _console_handler
    except Exception:
        pass


atexit.register(save_score_once)
_register_signal_handlers()
_register_windows_console_close_handler()

pygame.init()

SCREEN_WIDTH = 1152
SCREEN_HEIGHT = 768

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("OSI Mystery Escape")

inventory = Inventory()
timer_font = pygame.font.SysFont(None, 32)  # ← ADD THIS





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
# starts after start menu
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

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Window closed → saving...")

            save_score_once(force=True)   # ✅ FORCE SAVE

            pygame.quit()
            exit()

    if previous_scene and current_scene != previous_scene:
        skip_transition = (
            current_scene == "game_over" or
            (previous_scene == "physical" and current_scene == "data") or
            (previous_scene == "data" and current_scene == "physical")
        )
        if not skip_transition:
            run_stairs_transition(screen)

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

        print("GAME OVER TRIGGERED")   # debug

        total_time = save_score_once()
        if total_time is None:
            total_time = int(time.time() - game_start_time)

        from floors.application_layer import play_game_over
        play_game_over(screen, player_name, total_time)

        running = False

    # -------- DRAW HUD ON TOP --------   # ← ADD THIS
    # result = 
    draw_hud(screen)

    pygame.display.update()

pygame.quit()

