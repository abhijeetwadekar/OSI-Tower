import pygame
import sys
import cv2  # for video playback

from game.safe import run_safe_game
from game.underground import run_underground


def play_game_over(screen, player_name, total_time):
    minutes = total_time // 60
    seconds = total_time % 60
    time_text = f"{minutes:02}:{seconds:02}"
    cap = cv2.VideoCapture("assets/game_over.mp4")
    clock = pygame.time.Clock()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame (BGR → RGB)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert to pygame surface
        frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

        # Scale to screen size
        frame = pygame.transform.scale(frame, screen.get_size())

        # Draw on SAME screen
        screen.blit(frame, (0, 0))
        pygame.display.update()

        # Handle quit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                pygame.quit()
                sys.exit()

        clock.tick(30)  # control FPS

    cap.release()
    try:
        end_img = pygame.image.load("assets/end.jpeg")
        end_img = pygame.transform.scale(end_img, screen.get_size())
    except:
        # Fallback if image is missing so the game doesn't crash
        end_img = pygame.Surface(screen.get_size())
        end_img.fill((0, 0, 0))

    # Static loop to keep the end screen visible
    font_big = pygame.font.SysFont(None, 60)
    while True:
        screen.blit(end_img, (0, 0))
        # BLACK COLOR
        name_surface = font_big.render(f"Player: {player_name}", True, (0,0,0))
        time_surface = font_big.render(f"Time: {time_text}", True, (0,0,0))

        # CENTER ALIGN
        name_rect = name_surface.get_rect(center=(screen.get_width()//2, 250))
        time_rect = time_surface.get_rect(center=(screen.get_width()//2, 350))

        screen.blit(name_surface, name_rect)
        screen.blit(time_surface, time_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Optional: Allow them to press any key to exit
            if event.type == pygame.KEYDOWN:
                pygame.quit()
                sys.exit()

        clock.tick(15)


def run_application_layer(screen, inventory, application_state, draw_hud=None):
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 35)
    big_font = pygame.font.SysFont(None, 45)

    # ---------- INITIALIZE STATE ----------
    # Using .get ensures we don't overwrite existing state but fill in missing keys
    default_state = {
        "locker_unlocked": False,
        "siren_active": False,
        "siren_stopped": False,
        "door_unlocked": False,
        "viewing_note": False,
        "axe_replaced": False,
        "viewing_watch": False,
        "axe_collected": False,  
        "entering_password": False,
        "entering_siren_code": False,
        "input_text": "",
        "broken_glass": False,
        "message": "",
        "message_timer": 0
    }
    for key, value in default_state.items():
        if key not in application_state:
            application_state[key] = value

    # ---------- IMAGES ----------
    bg = pygame.image.load("assets/application.png")
    bg = pygame.transform.scale(bg, (WIDTH - 160, HEIGHT))

    locker_open_img = pygame.image.load("assets/locker.png")
    siren_img = pygame.image.load("assets/siren.png")
    open_door_img = pygame.image.load("assets/openeddoor7.png")

    note_img = pygame.image.load("assets/final_note.jpeg")
    watch_img = pygame.image.load("assets/watch.png")
    broken_glass_img = pygame.image.load("assets/brokenglass.png")
    

    # ---------- RECTS ----------
    back_rect = pygame.Rect(20, 150, 100, 400)
    door_rect = pygame.Rect(200, 185, 136, 360)
    locker_rect = pygame.Rect(WIDTH // 2 - 88, 323, 170, 110)
    siren_rect = pygame.Rect(WIDTH // 2 + 160, 200, 100, 100)
    table_rect = pygame.Rect(WIDTH // 2 - 140, HEIGHT - 240, 100, 100)
    window_rect = pygame.Rect(WIDTH - 250, 64, 150, 380)

    back_btn = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 120, 100, 40)
    input_box = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 30, 300, 60)

    flicker = False
    flicker_timer = 0

    while True:
        dt = clock.tick(60)
        flicker_timer += dt

        # message timer
        if application_state["message_timer"] > 0:
            application_state["message_timer"] -= dt
            if application_state["message_timer"] <= 0:
                application_state["message"] = ""

        # ---------- EVENTS ----------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    application_state["entering_password"] = False
                    application_state["entering_siren_code"] = False
                    application_state["input_text"] = ""

                if application_state["entering_password"]:
                    if event.key == pygame.K_RETURN:
                        if application_state["input_text"].lower() == "pineapple":
                            application_state["door_unlocked"] = True
                        application_state["entering_password"] = False
                        application_state["input_text"] = ""
                    elif event.key == pygame.K_BACKSPACE:
                        application_state["input_text"] = application_state["input_text"][:-1]
                    else:
                        application_state["input_text"] += event.unicode

                elif application_state["entering_siren_code"]:
                    if event.key == pygame.K_RETURN:
                        if application_state["input_text"].lower() == "stop":
                            application_state["siren_stopped"] = True
                        application_state["entering_siren_code"] = False
                        application_state["input_text"] = ""
                    elif event.key == pygame.K_BACKSPACE:
                        application_state["input_text"] = application_state["input_text"][:-1]
                    else:
                        if len(application_state["input_text"]) < 4:
                            application_state["input_text"] += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Handle overlays first
                if application_state["entering_password"] or application_state["entering_siren_code"]:
                    if back_btn.collidepoint(event.pos):
                        application_state["entering_password"] = False
                        application_state["entering_siren_code"] = False
                        application_state["input_text"] = ""
                    continue

                if application_state["viewing_note"] or application_state["viewing_watch"]:
                    if back_btn.collidepoint(event.pos):
                        application_state["viewing_note"] = False
                        application_state["viewing_watch"] = False
                    continue
                
                # Check Inventory
                inventory.handle_click(event.pos, screen)

                # World Interactions
                if back_rect.collidepoint(event.pos):
                    return "presentation"

                elif door_rect.collidepoint(event.pos):
                    if not application_state["door_unlocked"]:
                        application_state["entering_password"] = True
                    else:
                        run_underground(screen, inventory,application_state)

                elif locker_rect.collidepoint(event.pos):

                    if not application_state["locker_unlocked"]:
                        if run_safe_game(screen):
                            application_state["locker_unlocked"] = True
                            application_state["siren_active"] = True
                    elif application_state["siren_stopped"]:
                        application_state["viewing_note"] = True
                    else:
                        application_state["message"] = "Alarm is ringing!"
                        application_state["message_timer"] = 1000

                elif siren_rect.collidepoint(event.pos):
                    if application_state["siren_active"] and not application_state["siren_stopped"]:
                        application_state["entering_siren_code"] = True
                    else:
                        application_state["message"] = "Siren is OFF"
                        application_state["message_timer"] = 1000

                elif table_rect.collidepoint(event.pos):
                    application_state["viewing_watch"] = True

                elif window_rect.collidepoint(event.pos):
                    if not application_state["broken_glass"]:
                        if inventory.selected_item == "axe":
                            application_state["broken_glass"] = True
                        else:
                            application_state["message"] = "Glass is sealed pack!"
                            application_state["message_timer"] = 1000
                    else:
                        return "game_over"

        # ---------- DRAWING ----------
        screen.blit(bg, (0, 0))

        if application_state["locker_unlocked"]:
            screen.blit(pygame.transform.scale(locker_open_img, locker_rect.size), locker_rect)

        if application_state["door_unlocked"]:
            screen.blit(pygame.transform.scale(open_door_img, door_rect.size), door_rect)

        if application_state["broken_glass"]:
            screen.blit(pygame.transform.scale(broken_glass_img, window_rect.size), window_rect)

        # ---------- SIREN EFFECTS ----------
        if application_state["siren_active"] and not application_state["siren_stopped"]:
            if flicker_timer > 250:
                flicker = not flicker
                flicker_timer = 0
            if flicker:
                # Flash the siren overlay
                siren_scaled = pygame.transform.scale(siren_img, (WIDTH - 160, HEIGHT))
                screen.blit(siren_scaled, (0, 0))
            
            txt = big_font.render("SAFE TRIGGERED ALARM! TURN IT OFF!", True, (255, 0, 0))
            screen.blit(txt, (WIDTH // 2 - 300, 50))

        # ---------- UI OVERLAYS (Notes/Watch) ----------
        if application_state["viewing_note"]:
            screen.blit(pygame.transform.scale(note_img, (700, 600)), (250, 50))
            pygame.draw.rect(screen, (200, 50, 50), back_btn)
            screen.blit(font.render("BACK", True, (255, 255, 255)), (back_btn.x + 10, back_btn.y + 5))

        if application_state["viewing_watch"]:
            screen.blit(pygame.transform.scale(watch_img, (400, 300)), (WIDTH//2 - 150, 300))
            pygame.draw.rect(screen, (200, 50, 50), back_btn)
            screen.blit(font.render("BACK", True, (255, 255, 255)), (back_btn.x + 10, back_btn.y + 5))

        # ---------- INPUT UI ----------
        if application_state["entering_password"] or application_state["entering_siren_code"]:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            label = "Enter Password" if application_state["entering_password"] else "Enter text(app):"
            screen.blit(big_font.render(label, True, (255, 255, 255)), (WIDTH // 2 - 120, HEIGHT // 2 - 120))

            if application_state["entering_siren_code"]:
                for i in range(4):
                    box = pygame.Rect(WIDTH // 2 - 110 + i * 60, HEIGHT // 2, 50, 60)
                    pygame.draw.rect(screen, (255, 255, 255), box, 2)
                    if i < len(application_state["input_text"]):
                        char = font.render(application_state["input_text"][i].upper(), True, (255, 255, 255))
                        screen.blit(char, (box.x + 15, box.y + 15))
            else:
                pygame.draw.rect(screen, (255, 255, 255), input_box, 2)
                txt = font.render(application_state["input_text"], True, (255, 255, 255))
                screen.blit(txt, (input_box.x + 10, input_box.y + 15))

            pygame.draw.rect(screen, (200, 50, 50), back_btn)
            screen.blit(font.render("BACK", True, (255, 255, 255)), (back_btn.x + 10, back_btn.y + 5))

        # ---------- MESSAGES ----------
        if application_state["message"]:
            msg = font.render(application_state["message"], True, (255, 255, 255))
            screen.blit(msg, (WIDTH // 2 - 100, 80))

        # ---------- HUD & UPDATE ----------
        if draw_hud:
            draw_hud(screen)
        inventory.draw(screen)
        pygame.display.update()