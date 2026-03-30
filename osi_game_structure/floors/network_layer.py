import pygame
import sys
from game.interface import run_interface
from game.cardboard import run_cardbord   # 🔥 NEW

def run_network_layer(screen, inventory, data_state, network_state):

    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()

    INV_WIDTH = 160
    GAME_WIDTH = WIDTH - INV_WIDTH

    bg = pygame.image.load("assets/network.png")
    bg = pygame.transform.scale(bg, (GAME_WIDTH, HEIGHT))

    # ---------- CLICK AREAS ----------
    box_rect = pygame.Rect(740, 500, 120, 100)
    notice_rect = pygame.Rect(300, 100, 120, 80)  # 🔥 NOTICE BOARD

    tape_area = pygame.Rect(685, 385, 30, 70)

    server1_rect = pygame.Rect(855, 420, 58, 80)
    server2_rect = pygame.Rect(853, 320, 58, 100)

    pc_screen_rect = pygame.Rect(52, 352, 144, 95)
    pc_cable_rect = pygame.Rect(80, 434, 130, 224)

    door_rect = pygame.Rect(450, 200, 200, 350)
    back_door = pygame.Rect(280, 200, 100, 300)

    # lights
    red_light_rect = pygame.Rect(474, 179, 33, 20)
    yellow_light_rect = pygame.Rect(522, 179, 32, 20)
    green_light_rect = pygame.Rect(570, 179, 32, 20)
    blue_light_rect = pygame.Rect(616, 179, 32, 20)

    # ---------- IMAGES ----------
    command_img = pygame.image.load("assets/commandlist.png")
    command_img = pygame.transform.scale(command_img, (500, 300))

    taped_img = pygame.image.load("assets/taped.png")
    taped_img = pygame.transform.scale(taped_img, tape_area.size)

    add_server1_img = pygame.image.load("assets/addserver1.png")
    add_server2_img = pygame.image.load("assets/addserver2.png")

    pccable_img = pygame.image.load("assets/pccable.png")
    pcon_img = pygame.image.load("assets/pcon.png")

    open_door = pygame.image.load("assets/openeddoor3.png")
    open_door = pygame.transform.scale(open_door, door_rect.size)

    red_light = pygame.image.load("assets/redlight.png")
    yellow_light = pygame.image.load("assets/yellowlight.png")
    green_light = pygame.image.load("assets/greenlight.png")
    blue_light = pygame.image.load("assets/bluelight.png")

    font = pygame.font.SysFont(None, 35)

    # ---------- STATE ----------
    if not network_state:
        network_state.update({
            "items_collected": False,
            "wire_fixed": False,
            "server1_done": False,
            "server2_done": False,
            "pc_connected": False,
            "pc_on": False,
            "wifi_done": False,
            "door_popup": False,
            "entered_ip": "",
            "door_unlocked": False,
            "notice_open": False   # 🔥 NEW
        })

    items_collected = network_state["items_collected"]
    wire_fixed = network_state["wire_fixed"]
    server1_done = network_state["server1_done"]
    server2_done = network_state["server2_done"]
    pc_connected = network_state["pc_connected"]
    pc_on = network_state["pc_on"]
    wifi_done = network_state["wifi_done"]
    door_popup = network_state["door_popup"]
    entered_ip = network_state["entered_ip"]
    door_unlocked = network_state["door_unlocked"]
    notice_open = network_state["notice_open"]

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                # ---------- NOTICE VIEW ----------
                if notice_open:
                    back_btn = pygame.Rect(650, 120, 80, 40)
                    if back_btn.collidepoint(event.pos):
                        notice_open = False
                    continue

                # ---------- KEYPAD ----------
                if door_popup:

                    keys = [
                        ("1",0,0),("2",1,0),("3",2,0),
                        ("4",0,1),("5",1,1),("6",2,1),
                        ("7",0,2),("8",1,2),("9",2,2),
                        ("0",1,3)
                    ]

                    for key,col,row in keys:
                        x = 350 + col*70
                        y = 250 + row*70
                        btn = pygame.Rect(x,y,50,50)

                        if btn.collidepoint(event.pos):
                            if len(entered_ip) < 4:
                                entered_ip += key

                    enter_btn = pygame.Rect(500,460,80,50)
                    if enter_btn.collidepoint(event.pos):
                        if entered_ip == "1234":
                            door_unlocked = True
                            door_popup = False
                        else:
                            entered_ip = ""

                    close_btn = pygame.Rect(650,210,30,30)
                    if close_btn.collidepoint(event.pos):
                        door_popup = False

                    continue

                # ---------- NORMAL ----------
                inventory.handle_click(event.pos, screen)

                if notice_rect.collidepoint(event.pos):
                    notice_open = True

                elif box_rect.collidepoint(event.pos):
                    if not items_collected:
                        collected_items = run_cardbord(screen)
                        for item in collected_items:
                            inventory.add_item(item)

                        if collected_items:
                            items_collected = True

                elif tape_area.collidepoint(event.pos):
                    if inventory.selected_item == "tape":
                        wire_fixed = True
                        inventory.remove_item("tape")

                elif server1_rect.collidepoint(event.pos):
                    if inventory.selected_item == "server1":
                        server1_done = True
                        inventory.remove_item("server1")

                elif server2_rect.collidepoint(event.pos):
                    if inventory.selected_item == "server2":
                        server2_done = True
                        inventory.remove_item("server2")

                elif pc_cable_rect.collidepoint(event.pos):
                    if inventory.selected_item == "pcwire":
                        pc_connected = True
                        inventory.remove_item("pcwire")

                elif pc_screen_rect.collidepoint(event.pos):
                    if pc_connected and not pc_on:
                        pc_on = True
                    elif pc_on:
                        if run_interface():
                            wifi_done = True

                elif door_rect.collidepoint(event.pos):
                    if door_unlocked:
                        return "transport"
                    elif wire_fixed and pc_connected and server1_done and server2_done and wifi_done:
                        door_popup = True

        # ---------- DRAW ----------
        screen.blit(bg,(0,0))

        if wire_fixed:
            screen.blit(taped_img,tape_area)

        if pc_connected:
            screen.blit(pygame.transform.scale(pccable_img, pc_cable_rect.size), pc_cable_rect)

        if pc_on:
            screen.blit(pygame.transform.scale(pcon_img, pc_screen_rect.size), pc_screen_rect)

        if wifi_done:
            screen.blit(pygame.transform.scale(blue_light, blue_light_rect.size), blue_light_rect)

        if door_unlocked:
            screen.blit(open_door, door_rect)

        inventory.draw(screen)

        # ---------- NOTICE ----------
        if notice_open:
            screen.blit(command_img,(250,150))
            pygame.draw.rect(screen,(200,50,50),(650,120,80,40))
            screen.blit(font.render("BACK",True,(255,255,255)),(655,125))

        # ---------- KEYPAD ----------
        if door_popup:

            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0,0,0))
            screen.blit(overlay,(0,0))

            pygame.draw.rect(screen,(30,30,30),(300,200,400,350))

            screen.blit(font.render("CODE: "+entered_ip,True,(255,255,255)),(320,220))

            keys = [
                ("1",0,0),("2",1,0),("3",2,0),
                ("4",0,1),("5",1,1),("6",2,1),
                ("7",0,2),("8",1,2),("9",2,2),
                ("0",1,3)
            ]

            for key,col,row in keys:
                x = 350 + col*70
                y = 250 + row*70
                pygame.draw.rect(screen,(100,100,100),(x,y,50,50))
                screen.blit(font.render(key,True,(255,255,255)),(x+15,y+10))

            pygame.draw.rect(screen,(0,150,0),(500,460,80,50))
            screen.blit(font.render("GO",True,(255,255,255)),(515,470))

            pygame.draw.rect(screen,(200,50,50),(650,210,30,30))
            screen.blit(font.render("X",True,(255,255,255)),(655,210))

        pygame.display.update()
        clock.tick(60)