import pygame
import sys
from game.safe import run_safe_game
from game.underground import run_underground

def run_application_layer(screen, inventory, application_state):

    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 35)

    # ---------- IMAGES ----------
    bg = pygame.image.load("assets/application.png")
    INV_HEIGH = 160   # adjust if your inventory height is different
    bg = pygame.transform.scale(bg, (WIDTH-160, HEIGHT))

    locker_open_img = pygame.image.load("assets/locker.png")  # only overlay after solve
    siren_img = pygame.image.load("assets/siren.png")

    open_door_img = pygame.image.load("assets/openeddoor7.png")

    note_img = pygame.image.load("assets/final_note.jpeg")
    watch_img = pygame.image.load("assets/watch.png")

    # ---------- RECTS ----------
    back_rect = pygame.Rect(20, 150, 100, 400)
    door_rect = pygame.Rect(200, 185, 140, 360)

    locker_rect = pygame.Rect(WIDTH // 2 -88, 323, 170, 110)
    siren_rect = pygame.Rect(WIDTH // 2 + 160, 200, 100, 100)

    table_rect = pygame.Rect(WIDTH // 2 - 140, HEIGHT - 240, 100, 100)

    window_rect = pygame.Rect(WIDTH - 250, 150, 150, 250)

    back_btn = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 120, 100, 40)
    input_box = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 30, 300, 60)

    # ---------- STATE ----------
    if not application_state:
        application_state.update({
            "locker_unlocked": False,
            "siren_active": False,
            "siren_stopped": False,
            "door_unlocked": False,
            "viewing_note": False,
            "viewing_watch": False,
            "entering_password": False,
            "entering_siren_code": False,
            "input_text": "",
            "broken_glass": False
        })

    # ---------- FLICKER ----------
    flicker = False
    flicker_timer = 0

    while True:
        dt = clock.tick(60)
        flicker_timer += dt

        # ---------- EVENTS ----------
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # ---------- KEY INPUT ----------
            if event.type == pygame.KEYDOWN:

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
                        application_state["input_text"] += event.unicode

            # ---------- MOUSE ----------
            if event.type == pygame.MOUSEBUTTONDOWN:

                # PRIORITY STATES
                if application_state["entering_password"] or application_state["entering_siren_code"]:
                    continue

                if application_state["viewing_note"] or application_state["viewing_watch"]:
                    if back_btn.collidepoint(event.pos):
                        application_state["viewing_note"] = False
                        application_state["viewing_watch"] = False
                    continue

                inventory.handle_click(event.pos, screen)

                # ---------- BACK ----------
                if back_rect.collidepoint(event.pos):
                    return "presentation"

                # ---------- DOOR ----------
                elif door_rect.collidepoint(event.pos):

                    if not application_state["door_unlocked"]:
                        application_state["entering_password"] = True
                    else:
                        result = run_underground(screen, inventory)
                        if result == "application":
                            pass

                # ---------- LOCKER ----------
                elif locker_rect.collidepoint(event.pos):

                    if not application_state["locker_unlocked"]:
                        if run_safe_game(screen):
                            application_state["locker_unlocked"] = True
                            application_state["siren_active"] = True

                    elif application_state["locker_unlocked"] and application_state["siren_stopped"]:
                        application_state["viewing_note"] = True

                # ---------- SIREN ----------
                elif siren_rect.collidepoint(event.pos):
                    if application_state["siren_active"] and not application_state["siren_stopped"]:
                        application_state["entering_siren_code"] = True

                # ---------- TABLE ----------
                elif table_rect.collidepoint(event.pos):
                    application_state["viewing_watch"] = True

                # ---------- WINDOW ----------
                elif window_rect.collidepoint(event.pos):
                    if not application_state["broken_glass"]:
                        if inventory.selected_item == "axe":
                            application_state["broken_glass"] = True
                    else:
                        print("GAME OVER")
                        pygame.quit()
                        sys.exit()

        # ---------- DRAW ----------
        screen.blit(bg, (0, 0))

        # 🔥 ONLY DRAW OPEN LOCKER OVERLAY
        if application_state["locker_unlocked"]:
            screen.blit(pygame.transform.scale(locker_open_img, locker_rect.size), locker_rect)

        # 🔥 ONLY DRAW OPEN DOOR OVERLAY
        if application_state["door_unlocked"]:
            screen.blit(pygame.transform.scale(open_door_img, door_rect.size), door_rect)

        # ---------- SIREN FLICKER ----------
        if application_state["siren_active"] and not application_state["siren_stopped"]:
            if flicker_timer > 250:
                flicker = not flicker
                flicker_timer = 0

            if flicker:
                screen.blit(pygame.transform.scale(siren_img, (WIDTH-160, HEIGHT)), (0, 0))

        # ---------- NOTE ----------
        if application_state["viewing_note"]:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            screen.blit(pygame.transform.scale(note_img, (WIDTH - 200, HEIGHT - 100)), (100, 50))

        # ---------- WATCH ----------
        if application_state["viewing_watch"]:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            screen.blit(pygame.transform.scale(watch_img, (WIDTH - 200, HEIGHT - 100)), (100, 50))

        if application_state["viewing_note"] or application_state["viewing_watch"]:
            pygame.draw.rect(screen, (200, 50, 50), back_btn)
            screen.blit(font.render("BACK", True, (255, 255, 255)),
                        (back_btn.x + 10, back_btn.y + 5))

        # ---------- INPUT ----------
        if application_state["entering_password"] or application_state["entering_siren_code"]:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

            pygame.draw.rect(screen, (255, 255, 255), input_box, 2)

            text_surface = font.render(application_state["input_text"], True, (255, 255, 255))
            screen.blit(text_surface, (input_box.x + 10, input_box.y + 15))

            label = "Enter Password" if application_state["entering_password"] else "Enter Code"
            screen.blit(font.render(label, True, (255, 255, 255)),
                        (input_box.x, input_box.y - 40))

        # ---------- DEBUG ----------
        pygame.draw.rect(screen, (255,255,0), back_rect, 2)
        pygame.draw.rect(screen, (255,0,0), door_rect, 2)
        pygame.draw.rect(screen, (0,255,0), locker_rect, 2)
        pygame.draw.rect(screen, (160,32,240), siren_rect, 2)
        pygame.draw.rect(screen, (0,255,255), table_rect, 2)
        pygame.draw.rect(screen, (255,165,0), window_rect, 2)

        inventory.draw(screen)

        pygame.display.update()