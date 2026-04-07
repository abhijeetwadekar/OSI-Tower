import pygame
import sys

def run_start_menu(screen):

    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()

    menu_bg = pygame.image.load("assets/tower.png")
    menu_bg = pygame.transform.scale(menu_bg, (WIDTH, HEIGHT))

    WHITE = (255,255,255)
    GOLD = (255,215,0)
    BOX = (40,40,40)

    title_font = pygame.font.SysFont("Times New Roman",72,bold=True)
    button_font = pygame.font.SysFont("Times New Roman",40,bold=True)
    text_font = pygame.font.SysFont("Times New Roman",28)

    start_button = pygame.Rect(WIDTH//2-110,420,220,70)
    guide_button = pygame.Rect(WIDTH//2-110,510,220,70)
    back_button = pygame.Rect(40,40,120,50)

    zoom_scale = 1.0
    zooming = False
    show_guide = False

    # ✅ POPUP STATE
    entering_name = False
    player_name = ""

    running = True

    while running:

        mouse = pygame.mouse.get_pos()

        # ---------------- MENU ----------------
        if not zooming and not show_guide:

            screen.blit(menu_bg,(0,0))

            # START button
            pygame.draw.rect(screen,BOX,start_button)
            if start_button.collidepoint(mouse):
                pygame.draw.rect(screen,(80,80,80),start_button)
            pygame.draw.rect(screen,WHITE,start_button,2)
            start_text = button_font.render("START",True,WHITE)
            screen.blit(start_text,start_text.get_rect(center=start_button.center))

            # GUIDE button
            pygame.draw.rect(screen,BOX,guide_button)
            if guide_button.collidepoint(mouse):
                pygame.draw.rect(screen,(80,80,80),guide_button)
            pygame.draw.rect(screen,WHITE,guide_button,2)
            guide_text = button_font.render("GUIDE",True,WHITE)
            screen.blit(guide_text,guide_text.get_rect(center=guide_button.center))

            # ---------------- POPUP ----------------
            if entering_name:

                # dark overlay
                overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 180))
                screen.blit(overlay, (0, 0))

                # popup box
                popup_rect = pygame.Rect(WIDTH//2 - 250, HEIGHT//2 - 120, 500, 240)
                pygame.draw.rect(screen, BOX, popup_rect)
                pygame.draw.rect(screen, WHITE, popup_rect, 3)

                # title
                prompt = button_font.render("Enter Your Name", True, GOLD)
                screen.blit(prompt, prompt.get_rect(center=(WIDTH//2, HEIGHT//2 - 60)))

                # input box
                input_box = pygame.Rect(WIDTH//2 - 180, HEIGHT//2 - 10, 360, 50)
                pygame.draw.rect(screen, (20,20,20), input_box)
                pygame.draw.rect(screen, WHITE, input_box, 2)

                # typed text
                name_surface = button_font.render(player_name, True, WHITE)
                screen.blit(name_surface, (input_box.x + 10, input_box.y + 10))

                # hint
                hint = text_font.render("Press ENTER to start", True, (200,200,200))
                screen.blit(hint, hint.get_rect(center=(WIDTH//2, HEIGHT//2 + 70)))

        # ---------------- GUIDE SCREEN ----------------
        elif show_guide:

            screen.fill((20,20,30))

            title = title_font.render("GAME GUIDE",True,GOLD)
            screen.blit(title,title.get_rect(center=(WIDTH//2,120)))

            guide_lines = [
                "Escape the OSI Tower by solving puzzles on each layer.",
                "Each floor represents a networking layer.",
                "",
                "Collect items and use them to solve puzzles.",
                "Combine clues to move to the next layer.",
                "",
                "Layers:",
                "Physical → Data Link → Network → Transport → "
                " Session → Presentation → Application"
            ]

            y = 250
            for line in guide_lines:
                text = text_font.render(line,True,WHITE)
                screen.blit(text,(WIDTH//2-350,y))
                y += 40

            pygame.draw.rect(screen,BOX,back_button)
            pygame.draw.rect(screen,WHITE,back_button,2)

            back_text = text_font.render("BACK",True,WHITE)
            screen.blit(back_text,back_text.get_rect(center=back_button.center))

        # ---------------- ZOOM ANIMATION ----------------
        else:

            zoom_scale += 0.02

            new_width = int(WIDTH * zoom_scale)
            new_height = int(HEIGHT * zoom_scale)

            zoomed = pygame.transform.scale(menu_bg,(new_width,new_height))
            rect = zoomed.get_rect(center=(WIDTH//2,HEIGHT//2))

            screen.blit(zoomed,rect)

            if zoom_scale > 2.5:
                running = False

        pygame.display.update()
        clock.tick(60)

        # ---------------- EVENTS ----------------
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # ---------------- MOUSE ----------------
            if event.type == pygame.MOUSEBUTTONDOWN:

                if not zooming and not show_guide:

                    if start_button.collidepoint(event.pos):
                        entering_name = True   # open popup

                    elif guide_button.collidepoint(event.pos):
                        show_guide = True

                elif show_guide:

                    if back_button.collidepoint(event.pos):
                        show_guide = False

            # ---------------- KEYBOARD ----------------
            if entering_name and event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    if player_name.strip() != "":
                        entering_name = False
                        zooming = True

                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]

                else:
                    if len(player_name) < 12:
                        player_name += event.unicode

    return player_name