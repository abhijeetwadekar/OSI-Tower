import pygame
import sys
from floors.physical_layer import run_physical_layer
from game.socket_game import run_socket_game

def run_data_layer(screen, inventory, physical_state, data_state):

    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()

    INV_WIDTH = 160
    GAME_WIDTH = WIDTH - INV_WIDTH
    bg = pygame.image.load("assets/data_link.jpeg")
    bg = pygame.transform.scale(bg, (GAME_WIDTH, HEIGHT))

    # ---------- LOAD BASE IMAGE ----------
    red_note_img = pygame.image.load("assets/rednote.png")
    blue_note_img = pygame.image.load("assets/bluenote.png")
    green_note_img = pygame.image.load("assets/greennote.png")
    notice_img = pygame.image.load("assets/note.jpeg")

    # scale all
    red_note_img = pygame.transform.scale(red_note_img, (500, 400))
    blue_note_img = pygame.transform.scale(blue_note_img, (500, 400))
    green_note_img = pygame.transform.scale(green_note_img, (500, 400))
    notice_img = pygame.transform.scale(notice_img, (700, 400))

    # ---------- CLICK AREAS ----------
    box_rect = pygame.Rect(240, 480, 130, 100)
    suitcase_rect = pygame.Rect(645, 185, 130, 110)
    frame_rect = pygame.Rect(300, 260, 80, 115)
    toolbox_rect = pygame.Rect(750, 500, 160, 130)
    notice_rect = pygame.Rect(GAME_WIDTH-160, 250, 140, 120)

    panel_rect = pygame.Rect(603, 350, 33, 70)
    door_rect = pygame.Rect(390, 215, 210, 365)
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

    # 🔥 NOTE IMAGE (used for all notes)
    note_img = pygame.image.load("assets/note.jpeg")
    note_img = pygame.transform.scale(note_img, (400, 400))

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
        "entered_pin": "",
        "temp_hint": None,
        "hint_timer": 0,
        "door_popup": False,
        "note_popup": False,
        "current_note": None   # 🔥 which note is open
    }

    if not data_state:
        data_state.update(default_state)

    # ---------- LOAD STATE ----------
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
    door_popup = data_state["door_popup"]

    note_popup = data_state["note_popup"]
    current_note = data_state["current_note"]

    font = pygame.font.SysFont(None, 40)

    running = True

    while running:

        for event in pygame.event.get():
            # ---------- TEMP HINT TIMER ----------
            if data_state["hint_timer"] > 0:
                data_state["hint_timer"] -= 1
            else:
                data_state["temp_hint"] = None

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                # ---------- NOTE POPUP ----------
                if note_popup:
                    back_btn = pygame.Rect(700, 100, 80, 40)

                    if back_btn.collidepoint(event.pos):
                        note_popup = False
                        current_note = None

                    continue

                # ---------- KEYPAD ----------
                if door_popup:

                    for i in range(10):
                        x = 300 + (i % 3) * 80
                        y = 200 + (i // 3) * 80
                        btn = pygame.Rect(x, y, 60, 60)

                        if btn.collidepoint(event.pos):
                            if puzzle_done and len(entered_pin) < 6:
                                entered_pin += str(i)

                    enter_btn = pygame.Rect(300, 500, 180, 50)
                    if enter_btn.collidepoint(event.pos):
                        if entered_pin == "792685":
                            door_unlocked = True
                            door_popup = False

                            inventory.remove_item("rednote")
                            inventory.remove_item("bluenote")
                            inventory.remove_item("greennote")
                        else:
                            entered_pin = ""

                    close_btn = pygame.Rect(600, 160, 30, 30)
                    if close_btn.collidepoint(event.pos):
                        door_popup = False

                    continue

                # ---------- NORMAL CLICK ----------
                inventory.handle_click(event.pos, screen)

                # 👉 INVENTORY NOTE CLICK
                if inventory.selected_item in ["rednote", "bluenote", "greennote"]:
                    note_popup = True
                    current_note = inventory.selected_item
                    continue

                if hole_rect.collidepoint(event.pos):
                    data_state.update(locals())
                    return "physical"

                elif box_rect.collidepoint(event.pos):
                    if not box_open:
                        box_open = True
                    elif not rednote:
                        rednote = True
                        inventory.add_item("rednote")

                elif suitcase_rect.collidepoint(event.pos):
                    if not suitcase_open:
                        suitcase_open = True
                    elif not bluenote:
                        bluenote = True
                        inventory.add_item("bluenote")

                elif frame_rect.collidepoint(event.pos):
                    if not frame_open:
                        frame_open = True
                    elif not greennote:
                        greennote = True
                        inventory.add_item("greennote")

                elif notice_rect.collidepoint(event.pos):
                    note_popup = True
                    current_note = "notice"

                elif toolbox_rect.collidepoint(event.pos):
                    if not toolbox_open:
                        toolbox_open = True
                    elif not screwdriver:
                        screwdriver = True
                        inventory.add_item("screwdriver")

                elif panel_rect.collidepoint(event.pos):
                    if not panel_open:
                        if inventory.selected_item == "screwdriver":
                            panel_open = True
                            inventory.remove_item("screwdriver")
                        else:
                            data_state["temp_hint"] = "Need something to open"
                            data_state["hint_timer"] = 4
                    elif not puzzle_done:
                        if run_socket_game(screen):
                            puzzle_done = True

                elif door_rect.collidepoint(event.pos):
                    if door_unlocked:
                        data_state.update(locals())
                        return "network"
                    else:
                        door_popup = True

        # ---------- DRAW ----------
        screen.blit(bg, (0, 0))

        # pygame.draw.rect(screen, (255,0,0), door_rect, 2)
        # pygame.draw.rect(screen, (255,255,0), notice_rect, 2)

        if box_open:
            screen.blit(pygame.transform.scale(openbox2 if rednote else openbox1, box_rect.size), box_rect)

        if suitcase_open:
            screen.blit(pygame.transform.scale(suitcase2 if bluenote else suitcase1, suitcase_rect.size), suitcase_rect)

        if frame_open:
            screen.blit(pygame.transform.scale(frame2 if greennote else frame1, frame_rect.size), frame_rect)

        if toolbox_open:
            screen.blit(pygame.transform.scale(toolbox2 if screwdriver else toolbox1, toolbox_rect.size), toolbox_rect)

        if panel_open and not puzzle_done:
            screen.blit(pygame.transform.scale(socket_img, panel_rect.size), panel_rect)

        if door_unlocked:
            screen.blit(pygame.transform.scale(open_door, door_rect.size), door_rect)

        inventory.draw(screen)

        # ---------- NOTE POPUP DRAW ----------
        if note_popup:

            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0,0,0))
            screen.blit(overlay, (0,0))

            note_rect = pygame.Rect(250,100,390,400)
            if current_note == "rednote":
                screen.blit(red_note_img, note_rect)
            elif current_note == "bluenote":
                screen.blit(blue_note_img, note_rect)
            elif current_note == "greennote":
                screen.blit(green_note_img, note_rect)
            elif current_note == "notice":
                screen.blit(notice_img, note_rect)

            back_btn = pygame.Rect(700,100,80,40)
            pygame.draw.rect(screen,(200,0,0),back_btn)
            txt = font.render("BACK", True,(255,255,255))
            screen.blit(txt,(back_btn.x+5,back_btn.y+5))

        # ---------- KEYPAD DRAW ----------
        if door_popup:

            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0,0,0))
            screen.blit(overlay,(0,0))

            pygame.draw.rect(screen,(30,30,30),(250,150,400,450))
            pygame.draw.rect(screen,(255,255,255),(250,150,400,450),2)

            # ---------- DOOR HINT ----------
            if not puzzle_done:
                hint_font = pygame.font.SysFont(None, 26)
                hint_text = hint_font.render("Repair socket to access", True, (255,255,0))
                screen.blit(hint_text, (280, 110))

            pin_text = font.render("PIN: "+entered_pin,True,(255,255,255))
            screen.blit(pin_text,(300,170))


            for i in range(10):
                x = 300 + (i % 3) * 80
                y = 220 + (i // 3) * 80

                btn = pygame.Rect(x,y,60,60)
                color = (100,100,100) if not puzzle_done else (0,150,0)

                pygame.draw.rect(screen,color,btn)
                num = font.render(str(i),True,(255,255,255))
                screen.blit(num,(x+20,y+15))

            pygame.draw.rect(screen,(0,100,200),(300,500,180,50))
            txt = font.render("ENTER",True,(255,255,255))
            screen.blit(txt,(340,510))

            pygame.draw.rect(screen,(200,0,0),(600,160,30,30))
        # ---------- DRAW TEMP HINT ----------
        if data_state.get("temp_hint"):
            hint_font = pygame.font.SysFont(None, 30)
            hint = hint_font.render(data_state["temp_hint"], True, (0,0,0))
            screen.blit(hint, (300, 50))
        pygame.display.update()
        clock.tick(60)