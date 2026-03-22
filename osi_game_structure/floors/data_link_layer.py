import pygame
import sys
from floors.physical_layer import run_physical_layer
from game.socket_game import run_socket_game

def run_data_layer(screen, inventory, physical_state, data_state):   # ✅ UPDATED

    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()

    INV_WIDTH = 160
    GAME_WIDTH = WIDTH - INV_WIDTH

    # ---------- LOAD BASE IMAGE ----------
    bg = pygame.image.load("assets/data_link.jpeg")
    bg = pygame.transform.scale(bg, (GAME_WIDTH, HEIGHT))

    # ---------- CLICK AREAS ----------
    box_rect = pygame.Rect(240, 480, 130, 100)
    suitcase_rect = pygame.Rect(645, 185, 130, 110)
    frame_rect = pygame.Rect(300, 260, 80, 115)
    toolbox_rect = pygame.Rect(750, 500, 160, 130)
    notice_rect = pygame.Rect(GAME_WIDTH-160, 250, 140, 120)

    panel_rect = pygame.Rect(603, 350, 33, 70)
    door_rect = pygame.Rect(400, 220, 180, 330)
    hole_rect = pygame.Rect(360, 40, 250, 80)

    # ---------- LOAD IMAGES ----------
    openbox1 = pygame.image.load("assets/openbox.png")
    openbox2 = pygame.image.load("assets/openbox2.png")

    suitcase1 = pygame.image.load("assets/suitcase.png")
    suitcase2 = pygame.image.load("assets/suitcase2.png")

    frame1 = pygame.image.load("assets/frame.png")
    frame2 = pygame.image.load("assets/frame2.png")

    toolbox1 = pygame.image.load("assets/toolbox.png")
    toolbox2 = pygame.image.load("assets/toolbox2.png")

    socket_img = pygame.image.load("assets/socket.png")
    open_door = pygame.image.load("assets/openeddoor.jpg")
    note_img = pygame.image.load("assets/note.jpeg")

    # ---------- DEFAULT STATE ----------
    default_state = {
        "box_open": False,
        "rednote": False,
        "suitcase_open": False,
        "bluenote": False,
        "frame_open": False,
        "greennote": False,
        "toolbox_open": False,
        "screwdriver": False,
        "panel_open": False,
        "puzzle_done": False,
        "door_unlocked": False,
        "entered_pin": ""
    }

    if not data_state:
        data_state.update(default_state)

    # ---------- LOAD FROM STATE ----------
    box_open = data_state["box_open"]
    rednote = data_state["rednote"]

    suitcase_open = data_state["suitcase_open"]
    bluenote = data_state["bluenote"]

    frame_open = data_state["frame_open"]
    greennote = data_state["greennote"]

    toolbox_open = data_state["toolbox_open"]
    screwdriver = data_state["screwdriver"]

    panel_open = data_state["panel_open"]
    puzzle_done = data_state["puzzle_done"]

    door_unlocked = data_state["door_unlocked"]
    entered_pin = data_state["entered_pin"]

    zoom_note = False
    font = pygame.font.SysFont(None, 40)

    running = True

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                inventory.handle_click(event.pos, screen)

                # 👉 GO TO PHYSICAL LAYER
                if hole_rect.collidepoint(event.pos):
                    
                    # ✅ SAVE STATE BEFORE SWITCH
                    data_state.update({
                        "box_open": box_open,
                        "rednote": rednote,
                        "suitcase_open": suitcase_open,
                        "bluenote": bluenote,
                        "frame_open": frame_open,
                        "greennote": greennote,
                        "toolbox_open": toolbox_open,
                        "screwdriver": screwdriver,
                        "panel_open": panel_open,
                        "puzzle_done": puzzle_done,
                        "door_unlocked": door_unlocked,
                        "entered_pin": entered_pin
                    })

                    return "physical"

                # ---------- BOX ----------
                elif box_rect.collidepoint(event.pos):
                    if not box_open:
                        box_open = True
                    elif not rednote:
                        rednote = True
                        inventory.add_item("rednote")

                # ---------- SUITCASE ----------
                elif suitcase_rect.collidepoint(event.pos):
                    if not suitcase_open:
                        suitcase_open = True
                    elif not bluenote:
                        bluenote = True
                        inventory.add_item("bluenote")

                # ---------- FRAME ----------
                elif frame_rect.collidepoint(event.pos):
                    if not frame_open:
                        frame_open = True
                    elif not greennote:
                        greennote = True
                        inventory.add_item("greennote")

                # ---------- TOOLBOX ----------
                elif toolbox_rect.collidepoint(event.pos):
                    if not toolbox_open:
                        toolbox_open = True
                    elif not screwdriver:
                        screwdriver = True
                        inventory.add_item("screwdriver")

                # ---------- NOTICE ----------
                elif notice_rect.collidepoint(event.pos):
                    zoom_note = True

                # ---------- PANEL ----------
                elif panel_rect.collidepoint(event.pos):

                    if not panel_open:
                        if inventory.selected_item == "screwdriver":
                            panel_open = True
                            inventory.remove_item("screwdriver")

                    elif panel_open and not puzzle_done:
                        result = run_socket_game(screen)
                        if result:
                            puzzle_done = True

                # ---------- DOOR ----------
                elif door_rect.collidepoint(event.pos) and puzzle_done:

                    entered_pin += "1"

                    if len(entered_pin) == 6:
                        if entered_pin == "111111":
                            door_unlocked = True
                            inventory.remove_item("rednote")
                            inventory.remove_item("bluenote")
                            inventory.remove_item("greennote")
                        else:
                            entered_pin = ""

                if door_unlocked and door_rect.collidepoint(event.pos):
                    
                    # ✅ SAVE BEFORE EXIT
                    data_state.update({
                        "box_open": box_open,
                        "rednote": rednote,
                        "suitcase_open": suitcase_open,
                        "bluenote": bluenote,
                        "frame_open": frame_open,
                        "greennote": greennote,
                        "toolbox_open": toolbox_open,
                        "screwdriver": screwdriver,
                        "panel_open": panel_open,
                        "puzzle_done": puzzle_done,
                        "door_unlocked": door_unlocked,
                        "entered_pin": entered_pin
                    })

                    pygame.time.delay(500)
                    return

        # ---------- DRAW ----------
        screen.blit(bg, (0, 0))

        if box_open:
            img = openbox2 if rednote else openbox1
            screen.blit(pygame.transform.scale(img, (box_rect.w, box_rect.h)), box_rect.topleft)

        if suitcase_open:
            img = suitcase2 if bluenote else suitcase1
            screen.blit(pygame.transform.scale(img, (suitcase_rect.w, suitcase_rect.h)), suitcase_rect.topleft)

        if frame_open:
            img = frame2 if greennote else frame1
            screen.blit(pygame.transform.scale(img, (frame_rect.w, frame_rect.h)), frame_rect.topleft)

        if toolbox_open:
            img = toolbox2 if screwdriver else toolbox1
            screen.blit(pygame.transform.scale(img, (toolbox_rect.w, toolbox_rect.h)), toolbox_rect.topleft)

        if panel_open and not puzzle_done:
            screen.blit(pygame.transform.scale(socket_img, (panel_rect.w, panel_rect.h)), panel_rect.topleft)

        if door_unlocked:
            screen.blit(pygame.transform.scale(open_door, (door_rect.w, door_rect.h)), door_rect.topleft)

        inventory.draw(screen)

        if puzzle_done and not door_unlocked:
            pin_text = font.render("PIN: " + entered_pin, True, (255, 255, 255))
            screen.blit(pin_text, (500, 100))

        pygame.display.update()
        clock.tick(60)