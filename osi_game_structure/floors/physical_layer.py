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
   
    message = ""
    message_timer = 0

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
        inventory.draw(screen,draw_hud)

        pygame.display.update()
        clock.tick(60)
        
       

        # ---------- EVENTS ----------
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

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

        # ✅ ALSO SAVE CONTINUOUSLY (important for back navigation)
        state["switch_on"] = switch_on
        state["door_open"] = door_open
        state["wire_collected"] = wire_collected
        state["wire_attached"] = wire_attached
    
        