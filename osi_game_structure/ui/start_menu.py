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
    guide_scroll_offset = 0
    guide_content = [
        "OSI TOWER GUIDE",
        "Welcome to OSI Tower",
        "",
        "You are trapped inside the mysterious OSI Tower, a seven-floor",
        "castle where each floor represents one layer of the OSI",
        "(Open Systems Interconnection) Model.",
        "",
        "Your mission is simple:",
        "",
        "Escape the tower by solving puzzles based on networking concepts",
        "while learning how computer networks communicate.",
        "",
        "=== OBJECTIVE ===",
        "",
        "- Start from the Physical Layer at the top of the tower.",
        "- Solve the puzzle on each floor.",
        "- Find a way out.",
        "",
        "Every puzzle teaches the purpose of an OSI layer.",
        "",
        "=== CONTROLS ===",
        "",
        "Left Click - Interact with objects",
        "Click & Drag - Use collected items when required",
        "",
        "=== INVENTORY ===",
        "",
        "Items collected during the game are stored in the",
        "Inventory Panel.",
        "",
        "Some items can be used immediately, while others may be",
        "useful later in the level.",
        "",
        "Choose the correct item to solve each puzzle.",
        "",
        "Information or clue about certain things may appear",
        "if relevant.",
        "",
        "=== LEARN WHILE YOU PLAY ===",
        "",
        "After completing each floor, you'll receive a",
        "Learning Card explaining:",
        "",
        "- Concept: How the puzzle relates to networking.",
        "- What You Learned: The purpose of that OSI layer.",
        "- Real World Examples: Everyday devices and",
        "  technologies that use it.",
        "",
        "=== REMEMBER ===",
        "",
        "- There is always a logical solution.",
        "- Observe carefully.",
        "- Think like a network engineer.",
        "- Every puzzle represents a real networking concept.",
        "",
        "=== GOOD LUCK! ===",
        "",
        "The tower can only be escaped by understanding how",
        "networks communicate.",
        "",
        "Learn. Solve. Escape.",
    ]

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

            # Title
            title = title_font.render("GAME GUIDE",True,GOLD)
            screen.blit(title,title.get_rect(center=(WIDTH//2,50)))

            # Scroll area dimensions
            scroll_area_top = 150
            scroll_area_height = HEIGHT - 250
            scroll_area_left = 100
            scroll_area_width = WIDTH - 200

            # Draw scrollable content
            guide_surface = pygame.Surface((scroll_area_width, scroll_area_height))
            guide_surface.fill((30,30,40))

            y_pos = 20
            for line in guide_content:
                if line.startswith("==="):
                    # Section header
                    text = text_font.render(line, True, GOLD)
                elif line == "":
                    # Empty line - just space
                    y_pos += 20
                    continue
                else:
                    # Regular text
                    text = text_font.render(line, True, WHITE)
                
                # Apply scroll offset
                render_y = y_pos - guide_scroll_offset
                if -text.get_height() < render_y < scroll_area_height:
                    guide_surface.blit(text, (10, render_y))
                
                y_pos += 35

            # Calculate max scroll
            total_content_height = len(guide_content) * 35
            max_scroll = max(0, total_content_height - scroll_area_height)

            # Draw scroll area border
            pygame.draw.rect(screen, WHITE, (scroll_area_left, scroll_area_top, scroll_area_width, scroll_area_height), 2)
            screen.blit(guide_surface, (scroll_area_left, scroll_area_top))

            # Draw scrollbar
            if max_scroll > 0:
                scrollbar_height = int((scroll_area_height / total_content_height) * scroll_area_height)
                scrollbar_y = scroll_area_top + int((guide_scroll_offset / max_scroll) * (scroll_area_height - scrollbar_height))
                pygame.draw.rect(screen, GOLD, (scroll_area_left + scroll_area_width + 5, scrollbar_y, 8, scrollbar_height))

            # Scroll instructions
            scroll_hint = text_font.render("Scroll: UP/DOWN arrows or Mouse Wheel", True, (150,150,150))
            screen.blit(scroll_hint, scroll_hint.get_rect(center=(WIDTH//2, HEIGHT - 80)))

            # Back button
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
                    
                    # Mouse wheel scroll
                    elif event.button == 4:  # scroll up
                        guide_scroll_offset = max(0, guide_scroll_offset - 50)
                    elif event.button == 5:  # scroll down
                        scroll_area_height = HEIGHT - 250
                        total_content_height = len(guide_content) * 35
                        max_scroll = max(0, total_content_height - scroll_area_height)
                        guide_scroll_offset = min(max_scroll, guide_scroll_offset + 50)

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

            # Guide scrolling with arrow keys
            if show_guide and event.type == pygame.KEYDOWN:
                scroll_area_height = HEIGHT - 250
                total_content_height = len(guide_content) * 35
                max_scroll = max(0, total_content_height - scroll_area_height)
                
                if event.key == pygame.K_UP:
                    guide_scroll_offset = max(0, guide_scroll_offset - 50)
                elif event.key == pygame.K_DOWN:
                    guide_scroll_offset = min(max_scroll, guide_scroll_offset + 50)

    return player_name