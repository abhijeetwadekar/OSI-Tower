import pygame
import sys

def run_physical_layer(screen, inventory):

    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()

    # ---------- CLICK AREAS ----------

    switch_rect = pygame.Rect(120,355,135,135)
    wire_rect = pygame.Rect(260,340,185,185)
    hatch_rect = pygame.Rect(390,465,420,150)

    restart_rect = pygame.Rect(20,20,40,40)

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

    # ---------- GAME RESET FUNCTION ----------

    def reset_room():
        return False, False, False, False, "Maybe that device controls something."

    switch_on, door_open, wire_collected, wire_attached, hint = reset_room()

    font = pygame.font.SysFont("Times New Roman",26)

    running = True

    while running:

        mouse = pygame.mouse.get_pos()

        # ---------- DRAW BACKGROUND ----------

        screen.blit(terrace,(0,0))

        # ---------- DRAW SWITCH ----------

        if switch_on:
            screen.blit(switch_img, switch_rect.topleft)

        # ---------- DRAW HATCH ----------

        if door_open and not wire_attached:
            screen.blit(hole, hatch_rect.topleft)

        if wire_attached:
            screen.blit(wired_hole, hatch_rect.topleft)

        # ---------- DRAW HOOKLESS AREA ----------

        if wire_collected:
            screen.blit(hookless, wire_rect.topleft)

        # ---------- INVENTORY ----------

        inventory.draw(screen)

        # ---------- RESTART BUTTON ----------

        pygame.draw.rect(screen,(200,50,50),restart_rect)
        pygame.draw.rect(screen,(255,255,255),restart_rect,2)

        restart_text = font.render("R",True,(255,255,255))
        screen.blit(restart_text,(restart_rect.x+10,restart_rect.y+5))

        # ---------- DEBUG BORDERS ----------

        # pygame.draw.rect(screen,(255,0,255),switch_rect,3)
        # pygame.draw.rect(screen,(255,255,0),wire_rect,3)
        # pygame.draw.rect(screen,(255,100,100),hatch_rect,3)

        # ---------- HINT BOX ----------

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

                # RESTART
                if restart_rect.collidepoint(event.pos):

                    switch_on, door_open, wire_collected, wire_attached, hint = reset_room()
                    inventory.items.clear()
                    inventory.selected_item = None
                    continue

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
                        pygame.time.delay(1000)
                        running = False