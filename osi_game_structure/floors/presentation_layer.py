import pygame
import sys
from game.pattern_game import run_pattern_game  # your popup game


def run_presentation_layer(screen, inventory, presentation_state,draw_hud=None):
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 35)

    # ---------- BACKGROUND ----------
    bg = pygame.image.load("assets/presentation.png")
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

    # ---------- IMAGES ----------
    drawer1_img = pygame.image.load("assets/openeddrawer.png")
    drawer2_img = pygame.image.load("assets/openeddrawer2.png")
    bottle_img = pygame.image.load("assets/bottle.png")

    blank_scroll_img = pygame.image.load("assets/blankscroll.png")
    scroll_img = pygame.image.load("assets/scroll.jpeg")

    book_img = pygame.image.load("assets/encryption_book.png")
    opened_door_img = pygame.image.load("assets/openeddoor6.jpeg")

    # ---------- RECTS ----------
    drawer_rect = pygame.Rect(160, 407, 140, 80)
    scroll_table_rect = pygame.Rect(110, 320, 100, 90)

    stairs_rect = pygame.Rect(330, 200, 110, 250)

    pattern_rect = pygame.Rect(550, 130, 200, 140)

    exit_door_rect = pygame.Rect(WIDTH - 320, 130, 150, 350)

    book_table_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 250, 200, 100)

    # Zoom areas
    back_btn = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 120, 100, 40)

    # ---------- STATE INIT ----------
    if not presentation_state:
        presentation_state.update({
            "drawer_stage": 0,
            "bottle_taken": False,
            "scroll_revealed": False,
            "pattern_solved": False,
            "viewing_scroll": False,
            "viewing_book": False
        })

    while True:
        screen.blit(bg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                # ---------- HANDLE ZOOM STATES ----------
                if presentation_state["viewing_scroll"]:
                    inventory.handle_click(event.pos, screen)
                    if back_btn.collidepoint(event.pos):
                        presentation_state["viewing_scroll"] = False
                    else:
                        # Use bottle on scroll
                        if (inventory.selected_item == "bottle"
                                and not presentation_state["scroll_revealed"]):
                            presentation_state["scroll_revealed"] = True
                            inventory.remove_item("bottle")  # ✅ remove after use
                    continue

                if presentation_state["viewing_book"]:
                    if back_btn.collidepoint(event.pos):
                        presentation_state["viewing_book"] = False
                    continue

                # ---------- INVENTORY ----------
                inventory.handle_click(event.pos, screen)

                # ---------- DRAWER ----------
                if drawer_rect.collidepoint(event.pos):
                    if presentation_state["drawer_stage"] == 0:
                        presentation_state["drawer_stage"] = 1
                    elif presentation_state["drawer_stage"] == 1:
                        presentation_state["drawer_stage"] = 2
                        if not presentation_state["bottle_taken"]:
                            inventory.add_item("bottle")
                            presentation_state["bottle_taken"] = True

                # ---------- SCROLL TABLE ----------
                elif scroll_table_rect.collidepoint(event.pos):
                    presentation_state["viewing_scroll"] = True

                # ---------- STAIRS ----------
                elif stairs_rect.collidepoint(event.pos):
                    return "session"

                # ---------- PATTERN GAME ----------
                elif pattern_rect.collidepoint(event.pos):
                    if run_pattern_game(screen):
                        presentation_state["pattern_solved"] = True

                # ---------- EXIT DOOR ----------
                elif exit_door_rect.collidepoint(event.pos):
                    if presentation_state["pattern_solved"]:
                        return "application"
                    else:
                        print("Door is locked")

                # ---------- BOOK TABLE ----------
                elif book_table_rect.collidepoint(event.pos):
                    presentation_state["viewing_book"] = True

        # ---------- DRAW STATE OBJECTS ----------

        # Drawer visuals
        if presentation_state["drawer_stage"] == 1:
            screen.blit(pygame.transform.scale(drawer1_img, drawer_rect.size), drawer_rect)
        elif presentation_state["drawer_stage"] == 2:
            screen.blit(pygame.transform.scale(drawer2_img, drawer_rect.size), drawer_rect)

        # Exit door open state
        if presentation_state["pattern_solved"]:
            screen.blit(pygame.transform.scale(opened_door_img, exit_door_rect.size), exit_door_rect)

        # ---------- ZOOM SCROLL ----------
        if presentation_state["viewing_scroll"]:
            hint_font = pygame.font.SysFont(None, 30)
            hint = hint_font.render("It can't be empty! think like a spy", True, (255,255,255))

            screen.blit(hint, (600, 120))
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            zoom_rect = pygame.Rect(20, 0, 550, 800)
            

            if presentation_state["scroll_revealed"]:
                screen.blit(pygame.transform.scale(scroll_img, zoom_rect.size), zoom_rect)
            else:
                screen.blit(pygame.transform.scale(blank_scroll_img, zoom_rect.size), zoom_rect)

            pygame.draw.rect(screen, (200, 50, 50), back_btn)
            screen.blit(font.render("BACK", True, (255, 255, 255)),
                        (back_btn.x + 10, back_btn.y + 5))

        # ---------- ZOOM BOOK ----------
        if presentation_state["viewing_book"]:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

            zoom_rect = pygame.Rect(0, 0, WIDTH - 160, HEIGHT)
            screen.blit(pygame.transform.scale(book_img, zoom_rect.size), zoom_rect)

            pygame.draw.rect(screen, (200, 50, 50), back_btn)
            screen.blit(font.render("BACK", True, (255, 255, 255)),
                        (back_btn.x + 10, back_btn.y + 5))

        # ---------- DEBUG RECTS ----------

        # Drawer - YELLOW
        # pygame.draw.rect(screen, (255, 255, 0), drawer_rect, 2)

        # Scroll Table - CYAN
        # pygame.draw.rect(screen, (0, 255, 255), scroll_table_rect, 2)

        # Stairs - GREEN
        # pygame.draw.rect(screen, (0, 255, 0), stairs_rect, 2)

        # Pattern Game - PURPLE
        # pygame.draw.rect(screen, (160, 32, 240), pattern_rect, 2)

        # Exit Door - RED
        # pygame.draw.rect(screen, (255, 0, 0), exit_door_rect, 2)

        # Book Table - ORANGE
        # pygame.draw.rect(screen, (255, 165, 0), book_table_rect, 2)

        # ---------- BOTTLE HINT ----------
        if inventory.selected_item == "bottle":
            hint_font = pygame.font.SysFont(None, 30)
            hint = hint_font.render("sodium hydroxide solution", True, (255,255,255))
            screen.blit(hint, (400, 50))

        inventory.draw(screen,draw_hud)

        pygame.display.update()
        clock.tick(60)