import pygame
import sys

def run_physical_layer(screen, inventory, state):   # ✅ ADDED state

    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()

    # ---------- CLICK AREAS ----------
    switch_rect = pygame.Rect(120,355,135,135)
    wire_rect = pygame.Rect(260,334,188,187)
    hatch_rect = pygame.Rect(390,465,420,150)
    

    # ---------- LOAD IMAGES ----------
    terrace = pygame.image.load("assets/terrace.png")
    terrace = pygame.transform.scale(terrace,(WIDTH,HEIGHT))

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
            "hint": "Maybe that device controls something."
        }

    # ---------- LOAD FROM STATE ----------
    if not state:   # first time
        state.update(reset_room())

    switch_on = state.get("switch_on", False)
    door_open = state.get("door_open", False)
    wire_collected = state.get("wire_collected", False)
    wire_attached = state.get("wire_attached", False)
    hint = state.get("hint", "Maybe that device controls something.")

    font = pygame.font.SysFont("Times New Roman",26)

    running = True

    while running:

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

        inventory.draw(screen)

        
        # HINT BOX
        hint_box = pygame.Rect(WIDTH//2-300,20,600,60)
        pygame.draw.rect(screen,(40,40,40),hint_box)
        pygame.draw.rect(screen,(255,255,255),hint_box,2)

        text = font.render(hint,True,(255,255,255))
        screen.blit(text,text.get_rect(center=hint_box.center))

        pygame.display.update()
        clock.tick(60)

        # ---------- EVENTS ----------
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                inventory.handle_click(event.pos,screen)

                

                # SWITCH
                if switch_rect.collidepoint(event.pos) and not switch_on:

                    switch_on = True
                    door_open = True
                    hint = "The hatch opens. But the ladder is broken."

                # PICK WIRE
                elif wire_rect.collidepoint(event.pos) and not wire_collected:

                    wire_collected = True
                    inventory.add_item("cable")
                    hint = "You picked up a cable."

                # HATCH CLICK
                elif hatch_rect.collidepoint(event.pos):

                    if not door_open:
                        hint = "The hatch won't open."

                    elif door_open and not wire_attached:

                        if inventory.selected_item == "cable":

                            wire_attached = True
                            inventory.remove_item("cable")
                            hint = "You tie the cable and prepare to go down."

                        else:
                            hint = "The ladder is broken. Need something to climb."

                    elif wire_attached:

                        hint = "Climbing down to the next floor..."

                        # ✅ SAVE STATE BEFORE EXIT
                        state["switch_on"] = switch_on
                        state["door_open"] = door_open
                        state["wire_collected"] = wire_collected
                        state["wire_attached"] = wire_attached
                        state["hint"] = hint

                        pygame.time.delay(1000)
                        return "data"

        # ✅ ALSO SAVE CONTINUOUSLY (important for back navigation)
        state["switch_on"] = switch_on
        state["door_open"] = door_open
        state["wire_collected"] = wire_collected
        state["wire_attached"] = wire_attached
        state["hint"] = hint