import pygame
import sys

def run_server(screen,session_state):

    WIDTH, HEIGHT = 1000, 650
    TORCH_RADIUS = 60

    clock = pygame.time.Clock()

    # ---------- LOAD BACKGROUND ----------
    bg = pygame.image.load("assets/server_room.png")
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

    # ---------- SWITCH ----------
    switch_rect = pygame.Rect(175, 260, 50, 70)

    switch_img = pygame.image.load("assets/server_switch.png").convert_alpha()
    switch_img = pygame.transform.scale(
        switch_img,
        (switch_rect.width, switch_rect.height)
    )

    # ---------- CENTER DOOR (BACK TO SESSION) ----------
    door_rect = pygame.Rect(WIDTH//2 , HEIGHT//2 - 120, 120, 240)

    # ---------- STATE ----------
    lights_on = session_state.get("server_on", False)

    pygame.mouse.set_visible(False)

    # ---------- LOOP ----------
    while True:

        screen.blit(bg, (0, 0))
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                # SWITCH
                if not lights_on and switch_rect.collidepoint(event.pos):
                    lights_on = True
                    session_state["server_on"] = True 

                # DOOR → EXIT TO SESSION
                elif door_rect.collidepoint(event.pos):
                    pygame.mouse.set_visible(True)
                    return lights_on   # ✅ return state

        # ---------- TORCH EFFECT ----------
        if not lights_on:
            darkness = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            darkness.fill((0, 0, 0, 255))

            pygame.draw.circle(darkness, (0, 0, 0, 0), (mx, my), TORCH_RADIUS)
            screen.blit(darkness, (0, 0))

        # ---------- SHOW SWITCH AFTER ON ----------
        if lights_on:
            screen.blit(switch_img, (switch_rect.x, switch_rect.y))

        # ---------- OPTIONAL: DEBUG DOOR ----------
        pygame.draw.rect(screen, (255,0,0), door_rect, 2)

        # ---------- CURSOR ----------
        pygame.draw.circle(screen, (255,255,255), (mx, my), 3)

        pygame.display.update()
        clock.tick(60)