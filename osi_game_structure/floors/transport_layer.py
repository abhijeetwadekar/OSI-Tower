import pygame
import sys

from game.colour_game import run_colour_game

def run_transport_layer(screen, inventory, transport_state,draw_hud=None):

    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()

    bg = pygame.image.load("assets/transport.jpeg")
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

    # ---------- CLICK AREAS ----------
    left_box_rect = pygame.Rect(90, 465, 100, 195)
    switch_rect = pygame.Rect(505, 338, 30, 40)
    pc_rect = pygame.Rect(1000, 320, 120, 110)
    game_rect = pygame.Rect(50, 180, 220, 200)
    tick_rect = pygame.Rect(640, 250, 90, 60)   # adjust X slightly if needed
    door_rect = pygame.Rect(555, 177, 251, 415)
    back_door_rect = pygame.Rect(370, 240, 100, 300)

    # ---------- VISUAL AREAS (DEBUG ONLY) ----------
    torch_rect = pygame.Rect(1068, 69, 30, 30)
    matrix_rect = pygame.Rect(500, 590, 260, 130)

    tcp_light_rect = pygame.Rect(582, 150, 68, 30)
    top_light_rect = pygame.Rect(650, 150, 68, 30)
    udp_light_rect = pygame.Rect(720, 150, 66, 30)

    # ---------- IMAGES ----------
    leftdoor_img = pygame.image.load("assets/leftdoor.png")
    blueprint_img = pygame.image.load("assets/blueprint.jpg")

    pc_screen_img = pygame.image.load("assets/screen.jpeg")

    greentorch = pygame.image.load("assets/greentorch.jpg")
    redtorch = pygame.image.load("assets/redtorch.jpg")
    yellowtorch = pygame.image.load("assets/yellowtorch.jpg")

    gmatrix = pygame.image.load("assets/gmatrix.png")
    rmatrix = pygame.image.load("assets/rmatrix.png")
    ymatrix = pygame.image.load("assets/ymatrix.png")

    tcp_light = pygame.image.load("assets/tcplight.png")
    top_light = pygame.image.load("assets/toplight.png")
    udp_light = pygame.image.load("assets/udplight.png")

    tick_img = pygame.image.load("assets/tickmark.png")
    open_door = pygame.image.load("assets/openeddoor4.jpg")

    font = pygame.font.SysFont(None, 30)

    # ---------- STATE ----------
    if not transport_state:
        transport_state.update({
            "left_door_opened": False,
            "blueprint_popup": False,
            "switch_state": 0,
            "pc_popup": False,
            "green_done": False,
            "red_done": False,
            "yellow_done": False,
            "temp_hint": None,
            
            "unlock_popup": False,
            "door_opened": False,
            "final_grid": [[0]*5 for _ in range(5)]
        })

    # unpack
    left_door_opened = transport_state["left_door_opened"]
    blueprint_popup = transport_state["blueprint_popup"]
    switch_state = transport_state["switch_state"]
    pc_popup = transport_state["pc_popup"]

    green_done = transport_state["green_done"]
    red_done = transport_state["red_done"]
    yellow_done = transport_state["yellow_done"]

    unlock_popup = transport_state["unlock_popup"]
    door_opened = transport_state["door_opened"]
    final_grid = transport_state["final_grid"]

    target = [
        [0,0,0,0,0],
        [1,0,0,0,1],
        [1,1,1,0,1],
        [1,0,0,0,1],
        [0,1,0,1,0]
    ]

    def check_final():
        for i in range(5):
            for j in range(5):
                if target[i][j] == 1 and final_grid[i][j] != 1:
                    return False
        return True

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                # ---------- POPUPS ----------
                if blueprint_popup:
                    if pygame.Rect(650,100,300,140).collidepoint(event.pos):

                        blueprint_popup = False
                    continue

                if pc_popup:

                    if pygame.Rect(650,100,100,40).collidepoint(event.pos):
                        pc_popup = False
                    continue

                if unlock_popup:
                    mx, my = event.pos

                    if pygame.Rect(500, 160, 80, 40).collidepoint((mx, my)):
                        unlock_popup = False
                        continue

                    for i in range(5):
                        for j in range(5):
                            rect = pygame.Rect(250+j*60, 200+i*60, 50, 50)
                            if rect.collidepoint(mx, my):
                                final_grid[i][j] = 1 - final_grid[i][j]

                    if check_final():
                        door_opened = True
                        unlock_popup = False
                    continue

                # ---------- NORMAL ----------
                if back_door_rect.collidepoint(event.pos):
                    transport_state.update(locals())
                    return "network"

                if left_box_rect.collidepoint(event.pos):
                    if not left_door_opened:
                        left_door_opened = True
                    else:
                        blueprint_popup = True

                elif switch_rect.collidepoint(event.pos):
                    switch_state = (switch_state + 1) % 4

                elif pc_rect.collidepoint(event.pos):
                    pc_popup = True
                    # transport_state["temp_hint"] = "this looks useless"

                elif game_rect.collidepoint(event.pos):
                    result = run_colour_game(screen,transport_state)   # 🔥 now popup
                    green_done = result["green"]
                    red_done = result["red"]
                    yellow_done = result["yellow"]

                elif door_rect.collidepoint(event.pos):
                    if green_done and red_done and yellow_done and not door_opened:
                        unlock_popup = True
                        # transport_state["temp_hint"] = "Another color puzzle! isn't it look similar?"

                    elif door_opened:
                        transport_state.update(locals())
                        return "session"

        # ---------- DRAW ----------
        screen.blit(bg,(0,0))

        if left_door_opened:
            screen.blit(pygame.transform.scale(leftdoor_img,left_box_rect.size),left_box_rect)

        # SWITCH VISUAL
        if switch_state == 1:
            screen.blit(pygame.transform.scale(greentorch, torch_rect.size), torch_rect)
            screen.blit(pygame.transform.scale(gmatrix, matrix_rect.size), matrix_rect)

        elif switch_state == 2:
            screen.blit(pygame.transform.scale(redtorch, torch_rect.size), torch_rect)
            screen.blit(pygame.transform.scale(rmatrix, matrix_rect.size), matrix_rect)

        elif switch_state == 3:
            screen.blit(pygame.transform.scale(yellowtorch, torch_rect.size), torch_rect)
            screen.blit(pygame.transform.scale(ymatrix, matrix_rect.size), matrix_rect)

        # LIGHTS
        if green_done:

            screen.blit(pygame.transform.scale(tcp_light, tcp_light_rect.size), tcp_light_rect)
        if red_done:
            screen.blit(pygame.transform.scale(top_light, top_light_rect.size), top_light_rect)
        if yellow_done:
            screen.blit(pygame.transform.scale(udp_light, udp_light_rect.size), udp_light_rect)

        if green_done and red_done and yellow_done:
            screen.blit(pygame.transform.scale(tick_img, tick_rect.size), tick_rect)


        if door_opened:
            screen.blit(pygame.transform.scale(open_door,door_rect.size),door_rect)

        # ---------- POPUPS ----------
        if blueprint_popup:
            screen.blit(pygame.transform.scale(blueprint_img,(300,400)),(200,150))
            pygame.draw.rect(screen,(200,50,50),(650,100,100,40))
            screen.blit(font.render("BACK",True,(255,255,255)),(660,110))

        if pc_popup:
            # hint_font = pygame.font.SysFont(None, 30)
            # hint = hint_font.render("this looks useless", True, (255,255,0))
            # screen.blit(hint, (350, 120))
            screen.blit(pygame.transform.scale(pc_screen_img,(600,400)),(200,150))
            pygame.draw.rect(screen,(200,50,50),(650,100,100,40))
            screen.blit(font.render("BACK",True,(255,255,255)),(660,110))

        if unlock_popup:
            # hint_font = pygame.font.SysFont(None, 30)
            # hint = hint_font.render("Another color puzzle! isn't it look similar?", True, (255,255,0))
            # screen.blit(hint, (300, 120))
            pygame.draw.rect(screen,(30,30,30),(200,150,400,400))
            pygame.draw.rect(screen,(200,50,50),(500,160,80,40))
            screen.blit(font.render("BACK",True,(255,255,255)),(510,170))
            for i in range(5):
                for j in range(5):
                    color = (120,120,120) if final_grid[i][j] else (255,255,255)
                    pygame.draw.rect(screen,color,(250+j*60,200+i*60,50,50))
                    pygame.draw.rect(screen,(0,0,0),(250+j*60,200+i*60,50,50),2)

        # ---------- DEBUG ----------
        # pygame.draw.rect(screen,(255,0,0),left_box_rect,2)
        # pygame.draw.rect(screen,(0,255,0),switch_rect,2)
        # pygame.draw.rect(screen,(0,0,255),pc_rect,2)
        # pygame.draw.rect(screen,(255,255,0),game_rect,2)
        # pygame.draw.rect(screen,(255,0,255),door_rect,2)
        # pygame.draw.rect(screen,(0,255,255),back_door_rect,2)
        # pygame.draw.rect(screen,(255,255,255),tick_rect,2)      
        # 🔥 NEW DEBUG
        # pygame.draw.rect(screen,(255,128,0),torch_rect,2)
        # pygame.draw.rect(screen,(128,0,255),matrix_rect,2)
        # pygame.draw.rect(screen,(0,255,128),tcp_light_rect,2)
        # pygame.draw.rect(screen,(255,0,128),top_light_rect,2)
        # pygame.draw.rect(screen,(128,255,0),udp_light_rect,2)

# ---------- DRAW HINT (ONLY FOR POPUPS) ----------
        display_hint = None

        if pc_popup:
            display_hint = "this looks useless"

        elif unlock_popup:
            display_hint = "Another color puzzle! isn't it look similar?"

        if display_hint:
            hint_font = pygame.font.SysFont(None, 32)

            # pygame.draw.rect(screen, (0,0,0), (300, 50, 500, 50))
            # pygame.draw.rect(screen, (255,0,0), (300, 50, 500, 50), 2)

            hint = hint_font.render(display_hint, True, (0,0,0))
            screen.blit(hint, (320, 65))
        # ---------- HUD ----------
        if draw_hud:
            draw_hud(screen, panel_x=WIDTH - 150, start_y=HEIGHT - 60)

        pygame.display.update()
        clock.tick(60)
        