import pygame
import sys
from game.laptop import run_laptop  # Assuming this is the function name
from game.wall import run_wall    # Assuming this is the function name
from game.server_room import run_server
def run_stairs_transition(screen):
    import pygame
    import sys

    WIDTH, HEIGHT = screen.get_size()

    stairs1 = pygame.image.load("assets/stairs.jpg")
    stairs2 = pygame.image.load("assets/stairs1.jpg")

    stairs1 = pygame.transform.scale(stairs1, (WIDTH, HEIGHT))
    stairs2 = pygame.transform.scale(stairs2, (WIDTH, HEIGHT))

    clock = pygame.time.Clock()

    # show first image
    screen.blit(stairs1, (0, 0))
    pygame.display.update()

    start = pygame.time.get_ticks()

    # 0.5 sec first image
    while pygame.time.get_ticks() - start < 500:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        clock.tick(60)

    # show second image
    screen.blit(stairs2, (0, 0))
    pygame.display.update()

    start = pygame.time.get_ticks()

    # 0.5 sec second image
    while pygame.time.get_ticks() - start < 500:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        clock.tick(60)
def run_session_layer(screen, inventory, session_state):
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 35)

    # ---------- ASSETS & DIMENSIONS ----------
    GAME_WIDTH = WIDTH - 160
    bg = pygame.image.load("assets/session.jpeg")
    bg = pygame.transform.scale(bg, (GAME_WIDTH, HEIGHT))

    # Images
    torch_img = pygame.image.load("assets/torch.png")
    hammer_img = pygame.image.load("assets/hammer.png")
    server_door_img = pygame.image.load("assets/serverdoor.png")
    black_screen_img = pygame.image.load("assets/blackscreen.png")
    server_msg_img = pygame.image.load("assets/servermessage.png")
    wall_dent_img = pygame.image.load("assets/wall_dent.png")
    opened_door_img = pygame.image.load("assets/openeddoor5.png")

    # ---------- RECTS (HITBOXES) ----------
    torch_rect = pygame.Rect(200, 390, 50, 40)        # Extreme left
    hammer_rect = pygame.Rect(250, 200, 40, 60)      # On the wall
    pc_rect = pygame.Rect(0, 220, 105, 150)        # PC above
    laptop_rect = pygame.Rect(70, 360, 90, 80)     # Laptop below
    back_door_rect = pygame.Rect(390, 220, 80, 250)  # Back to network
    destructible_wall = pygame.Rect(500, 200, 120, 300) # Wall for hammer
    exit_door_rect = pygame.Rect(650, 200, 180, 325) # Rightmost door
    server_rect = pygame.Rect(910, 180, 100, 400)    # Area for serverdoor.png
    wall_dent_rect = pygame.Rect(535, 325, 60, 30)

    # ---------- STATE INITIALIZATION ----------
    if not session_state:
        session_state.update({
            "torch_taken": False,
            "hammer_taken": False,
            "server_door_placed": False,
            "laptop_solved": False,
            "wall_solved": False,
            "server_on": False,
            "viewing_msg": False
        })

    while True:
        screen.blit(bg, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # 1. Close Server Message
                if session_state["viewing_msg"]:
                    back_btn = pygame.Rect(WIDTH//2 - 50, HEIGHT - 100, 100, 40)
                    if back_btn.collidepoint(event.pos):
                        session_state["viewing_msg"] = False
                    continue

                inventory.handle_click(event.pos, screen)

                # 2. Torch Pickup
                if torch_rect.collidepoint(event.pos) and not session_state["torch_taken"]:
                    inventory.add_item("torch")
                    session_state["torch_taken"] = True

                # 3. Hammer Pickup
                elif hammer_rect.collidepoint(event.pos) and not session_state["hammer_taken"]:
                    inventory.add_item("wall_hammer")
                    session_state["hammer_taken"] = True

                # 4. Laptop Logic (LOCKED until server is ON)
                elif laptop_rect.collidepoint(event.pos):

                    if session_state["server_on"]:   # ✅ شرط (condition)
                        if run_laptop(screen):
                            session_state["laptop_solved"] = True
                    else:
                        print("we need to connect server first.")

                # 5. PC Logic (Black screen / Server Message)
                elif pc_rect.collidepoint(event.pos):
                    if session_state["server_on"]:
                        session_state["viewing_msg"] = True

                # 6. Back Door (To Network)
                elif back_door_rect.collidepoint(event.pos):
                    return "network"

                # 7. Destructible Wall (Hammer)
                elif destructible_wall.collidepoint(event.pos):
                    if inventory.selected_item == "wall_hammer":
                        if run_wall(screen):
                            session_state["wall_solved"] = True
                            inventory.remove_item("wall_hammer")

                # 8. Server Door & Server Room Entry

                elif server_rect.collidepoint(event.pos):

                    # Step 1: First click → show door
                    if not session_state["server_door_placed"]:
                        session_state["server_door_placed"] = True

                    # Step 2: Door already placed → try entering
                    else:
                        if inventory.selected_item == "torch":
                            if run_server(screen,session_state):
                                session_state["server_on"] = True
                                inventory.remove_item("torch")
                        else:
                            print("Torch not selected")


                # 9️⃣ EXIT DOOR (MIDDLE FINAL DOOR)
                elif exit_door_rect.collidepoint(event.pos):

                    if session_state["laptop_solved"]:
                        if session_state["wall_solved"]:
                            return "presentation"   # ✅ next layer
                        else:
                            run_stairs_transition(screen)
                            

        # ---------- DRAWING LOGIC ----------
        
        # Draw Torch if not taken
        if not session_state["torch_taken"]:
            screen.blit(pygame.transform.scale(torch_img, torch_rect.size), torch_rect)

        # Draw Hammer if not taken
        if not session_state["hammer_taken"]:
            screen.blit(pygame.transform.scale(hammer_img, hammer_rect.size), hammer_rect)

        # Draw Server Door if placed
        if session_state["server_door_placed"]:
            screen.blit(pygame.transform.scale(server_door_img, server_rect.size), server_rect)

        # PC Screen Logic
        if not session_state["server_on"]:
            screen.blit(pygame.transform.scale(black_screen_img, pc_rect.size), pc_rect)

        # Wall Dent
        if session_state["wall_solved"]:
            screen.blit(pygame.transform.scale(wall_dent_img, wall_dent_rect.size), wall_dent_rect)

        # Opened Exit Door
        if session_state["laptop_solved"]:
            screen.blit(pygame.transform.scale(opened_door_img, exit_door_rect.size), exit_door_rect)

        # Server Message Zoom
        if session_state["viewing_msg"]:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            msg_rect = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 - 150, 400, 300)
            screen.blit(pygame.transform.scale(server_msg_img, msg_rect.size), msg_rect)
            
            pygame.draw.rect(screen, (200, 50, 50), (WIDTH//2 - 50, HEIGHT - 100, 100, 40))
            screen.blit(font.render("BACK", True, (255, 255, 255)), (WIDTH//2 - 40, HEIGHT - 95))
        # ---------- DEBUG HITBOXES ----------

        # Torch - YELLOW
        # pygame.draw.rect(screen, (255, 255, 0), torch_rect, 2)

        # Hammer - ORANGE
        # pygame.draw.rect(screen, (255, 165, 0), hammer_rect, 2)

        # PC - BLUE
        # pygame.draw.rect(screen, (0, 100, 255), pc_rect, 2)

        # Laptop - CYAN
        # pygame.draw.rect(screen, (0, 255, 255), laptop_rect, 2)

        # Back Door - GREEN
        # pygame.draw.rect(screen, (0, 255, 0), back_door_rect, 2)

        # Wall - PURPLE
        # pygame.draw.rect(screen, (160, 32, 240), destructible_wall, 2)

        # Exit Door - RED
        # pygame.draw.rect(screen, (255, 0, 0), exit_door_rect, 2)

        # Wall Dent - PINK
        # pygame.draw.rect(screen, (255, 20, 147), wall_dent_rect, 2)
        # Server Door - WHITE
        # pygame.draw.rect(screen, (255, 255, 255), server_rect, 2)
        inventory.draw(screen)

       

        pygame.display.update()
        clock.tick(60)