import pygame
import sys

def run_physical_layer(screen, inventory, state,draw_hud=None):   # ✅ ADDED state

    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()

    # ---------- CLICK AREAS ----------
    switch_rect = pygame.Rect(120,355,135,135)
    wire_rect = pygame.Rect(260,334,188,187)
    hatch_rect = pygame.Rect(390,465,420,150)
    trap_rect = pygame.Rect(350,50, 600, 200)
    info_button = pygame.Rect(20, 20, 40, 40)

    # ---------- GUIDE CONTENT ----------
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

    # ---------- LOAD IMAGES ----------
    terrace = pygame.image.load("assets/terrace.png")
    terrace = pygame.transform.scale(terrace,(WIDTH,HEIGHT))
    fall_img = pygame.image.load("assets/fall.jpeg")
    dead_img = pygame.image.load("assets/dead.jpeg")
    revive_img = pygame.image.load("assets/revive.jpeg")

    fall_img = pygame.transform.scale(fall_img, (WIDTH, HEIGHT))
    dead_img = pygame.transform.scale(dead_img, (WIDTH, HEIGHT))
    revive_img = pygame.transform.scale(revive_img, (WIDTH, HEIGHT))
    hole = pygame.image.load("assets/hole.png")
    hole = pygame.transform.scale(hole,(hatch_rect.width,hatch_rect.height))

    wired_hole = pygame.image.load("assets/wiredhole.png")
    wired_hole = pygame.transform.scale(wired_hole,(hatch_rect.width,hatch_rect.height))

    hookless = pygame.image.load("assets/hookless.png")
    hookless = pygame.transform.scale(hookless,(wire_rect.width,wire_rect.height))

    switch_img = pygame.image.load("assets/switch.png")
    switch_img = pygame.transform.scale(switch_img,(switch_rect.width,switch_rect.height))

    # ---------- DEFAULT STATE ----------
    def reset_room():
        return {
            "switch_on": False,
            "door_open": False,
            "wire_collected": False,
            "wire_attached": False,
        }

    # ---------- LOAD FROM STATE ----------
    if not state:   # first time
        state.update(reset_room())

    switch_on = state.get("switch_on", False)
    door_open = state.get("door_open", False)
    wire_collected = state.get("wire_collected", False)
    wire_attached = state.get("wire_attached", False)

    font = pygame.font.SysFont("Times New Roman",26)
    title_font = pygame.font.SysFont("Times New Roman",48,bold=True)
    text_font = pygame.font.SysFont("Times New Roman",24)

    WHITE = (255,255,255)
    GOLD = (255,215,0)
    BOX = (40,40,40)
   
    message = ""
    message_timer = 0
    show_guide = False
    guide_scroll_offset = 0

    running = True

    while running:
        if message_timer > 0:
            message_timer -= 1
            if message_timer == 0:
                message = ""
        mouse = pygame.mouse.get_pos()

        # ---------- DRAW ----------
        screen.blit(terrace,(0,0))

        if switch_on:
            screen.blit(switch_img, switch_rect.topleft)

        if door_open and not wire_attached:
            screen.blit(hole, hatch_rect.topleft)

        if wire_attached:
            screen.blit(wired_hole, hatch_rect.topleft)

        if wire_collected:
            screen.blit(hookless, wire_rect.topleft)

        if message:
            msg_surface = font.render(message, True, (0, 0, 0))
            screen.blit(msg_surface, (WIDTH//2 - msg_surface.get_width()//2, 40))
        
        # Draw info button
        pygame.draw.rect(screen, BOX, info_button)
        pygame.draw.rect(screen, WHITE, info_button, 2)
        info_text = font.render("i", True, WHITE)
        screen.blit(info_text, info_text.get_rect(center=info_button.center))

        # ---------- GUIDE POPUP ----------
        if show_guide:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

            # Title
            title = title_font.render("GUIDE",True,GOLD)
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
                if line.startswith("📖") or line.startswith("🏰") or line.startswith("🎯") or line.startswith("🎮") or line.startswith("🎒") or line.startswith("🎓") or line.startswith("⚠️") or line.startswith("🚪"):
                    # Section header with emoji
                    text = title_font.render(line, True, GOLD)
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

            # Back button
            back_button = pygame.Rect(40, 40, 120, 50)
            pygame.draw.rect(screen, BOX, back_button)
            pygame.draw.rect(screen, WHITE, back_button, 2)
            back_text = text_font.render("BACK", True, WHITE)
            screen.blit(back_text, back_text.get_rect(center=back_button.center))
        
        inventory.draw(screen,draw_hud)

        pygame.display.update()
        clock.tick(60)
        
       

        # ---------- EVENTS ----------
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                # Info button click
                if info_button.collidepoint(event.pos) and not show_guide:
                    show_guide = True
                
                # Back button click in guide or other guide interactions
                elif show_guide:
                    back_button = pygame.Rect(40, 40, 120, 50)
                    if back_button.collidepoint(event.pos):
                        show_guide = False
                    # Mouse wheel scroll in guide
                    elif event.button == 4:  # scroll up
                        guide_scroll_offset = max(0, guide_scroll_offset - 50)
                    elif event.button == 5:  # scroll down
                        scroll_area_height = HEIGHT - 250
                        total_content_height = len(guide_content) * 35
                        max_scroll = max(0, total_content_height - scroll_area_height)
                        guide_scroll_offset = min(max_scroll, guide_scroll_offset + 50)
                
                # Regular game events (only if guide not showing)
                elif not show_guide:
                    inventory.handle_click(event.pos,screen)

                    # TRAP AREA (CENTER)
                    if trap_rect.collidepoint(event.pos):

                        # FALL
                        screen.blit(fall_img, (0, 0))
                        pygame.display.update()
                        pygame.time.delay(500)

                        # DEAD
                        screen.blit(dead_img, (0, 0))
                        pygame.display.update()
                        pygame.time.delay(500)

                        # REVIVE SCREEN (wait for click)
                        waiting = True
                        while waiting:
                            screen.blit(revive_img, (0, 0))
                            pygame.display.update()

                            for e in pygame.event.get():
                                if e.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                if e.type == pygame.MOUSEBUTTONDOWN:
                                    waiting = False

                        # Return to same game state (DO NOTHING)
                        continue

                    

                    # SWITCH
                    if switch_rect.collidepoint(event.pos) and not switch_on:

                        switch_on = True
                        door_open = True

                    # PICK WIRE
                    elif wire_rect.collidepoint(event.pos) and not wire_collected:

                        wire_collected = True
                        inventory.add_item("cable")
                       

                    # HATCH CLICK
                    
                    elif hatch_rect.collidepoint(event.pos):

                        if not door_open:
                            message = "The hatch is locked."
                            message_timer = 120

                        elif door_open and not wire_attached:

                            if inventory.selected_item == "cable":
                                wire_attached = True
                                inventory.remove_item("cable")
                            else:
                                message = "The ladder is broken."
                                message_timer = 120

                        elif wire_attached:
                            # ✅ SAVE ONLY HERE (before leaving)
                            state["switch_on"] = switch_on
                            state["door_open"] = door_open
                            state["wire_collected"] = wire_collected
                            state["wire_attached"] = wire_attached

                            pygame.time.delay(1000)
                            return "data"

            # Guide scrolling with arrow keys
            if show_guide and event.type == pygame.KEYDOWN:
                scroll_area_height = HEIGHT - 250
                total_content_height = len(guide_content) * 35
                max_scroll = max(0, total_content_height - scroll_area_height)
                
                if event.key == pygame.K_UP:
                    guide_scroll_offset = max(0, guide_scroll_offset - 50)
                elif event.key == pygame.K_DOWN:
                    guide_scroll_offset = min(max_scroll, guide_scroll_offset + 50)
                elif event.key == pygame.K_ESCAPE:
                    show_guide = False

        # ✅ ALSO SAVE CONTINUOUSLY (important for back navigation)
        state["switch_on"] = switch_on
        state["door_open"] = door_open
        state["wire_collected"] = wire_collected
        state["wire_attached"] = wire_attached
    
        