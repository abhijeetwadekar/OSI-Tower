import pygame

def run_cardbord(screen, background, collected_items):

    clock = pygame.time.Clock()

    WIDTH, HEIGHT = screen.get_size()

    # ---------- MINI GAME SIZE ----------
    BOX_W, BOX_H = 700, 500
    BOX_X = (WIDTH - BOX_W) // 2
    BOX_Y = (HEIGHT - BOX_H) // 2

    # ---------- LOAD IMAGE ----------
    bg = pygame.image.load("assets/box.png")
    bg = pygame.transform.scale(bg, (BOX_W, BOX_H))

    font = pygame.font.SysFont(None, 28)

    # ---------- CLICK AREAS ----------
    duct_tape_rect = pygame.Rect(145, 75, 165, 165)
    server1_rect = pygame.Rect(314, 350, 240, 89)
    server2_rect = pygame.Rect(330, 69, 275, 270)
    hdmi_rect = pygame.Rect(150, 260, 155, 170)

    exit_btn = pygame.Rect(BOX_W - 90, 10, 80, 35)

    # ---------- LOAD REPLACEMENT IMAGES ----------
    no_tape_img = pygame.image.load("assets/tapeless.jpg")
    no_server1_img = pygame.image.load("assets/noserver2.jpg")
    no_server2_img = pygame.image.load("assets/noserver1.jpg")
    no_wire_img = pygame.image.load("assets/hdmiless.jpg")

    # scale to rect sizes
    no_tape_img = pygame.transform.scale(no_tape_img, duct_tape_rect.size)
    no_server1_img = pygame.transform.scale(no_server1_img, server1_rect.size)
    no_server2_img = pygame.transform.scale(no_server2_img, server2_rect.size)
    no_wire_img = pygame.transform.scale(no_wire_img, hdmi_rect.size)

    running = True

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEBUTTONDOWN:

                mx, my = event.pos
                local_x = mx - BOX_X
                local_y = my - BOX_Y

                if duct_tape_rect.collidepoint((local_x, local_y)):
                    if "tape" not in collected_items:
                        collected_items.append("tape")

                elif server1_rect.collidepoint((local_x, local_y)):
                    if "server1" not in collected_items:
                        collected_items.append("server1")

                elif server2_rect.collidepoint((local_x, local_y)):
                    if "server2" not in collected_items:
                        collected_items.append("server2")

                elif hdmi_rect.collidepoint((local_x, local_y)):
                    if "pcwire" not in collected_items:
                        collected_items.append("pcwire")

                elif exit_btn.collidepoint((local_x, local_y)):
                    return

        # ---------- DRAW ORIGINAL BACKGROUND ----------
        screen.blit(background, (0, 0))

        # ---------- CARDBOARD HINT ----------
        hint_font = pygame.font.SysFont(None, 32)

        if len(collected_items) == 4:
            text = "i guess that's all"
        else:
            text = "lot of useful things"

        pygame.draw.rect(screen, (0,0,0), (300, 50, 500, 50))
        pygame.draw.rect(screen, (255,0,0), (300, 50, 500, 50), 2)

        hint = hint_font.render(text, True, (255,255,255))
        screen.blit(hint, (320, 65))

        # ---------- DARK OVERLAY ----------
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        screen.blit(overlay, (0, 0))

        # ---------- DRAW BOX ----------
        screen.blit(bg, (BOX_X, BOX_Y))

        # ---------- DRAW COLLECTED (REMOVED ITEMS) ----------
        if "tape" in collected_items:
            screen.blit(no_tape_img, duct_tape_rect.move(BOX_X, BOX_Y))

        if "server1" in collected_items:
            screen.blit(no_server1_img, server1_rect.move(BOX_X, BOX_Y))

        if "server2" in collected_items:
            screen.blit(no_server2_img, server2_rect.move(BOX_X, BOX_Y))

        if "pcwire" in collected_items:
            screen.blit(no_wire_img, hdmi_rect.move(BOX_X, BOX_Y))

        # ---------- EXIT BUTTON ----------
        pygame.draw.rect(screen, (200, 50, 50), exit_btn.move(BOX_X, BOX_Y))
        screen.blit(
            font.render("EXIT", True, (255, 255, 255)),
            (BOX_X + exit_btn.x + 10, BOX_Y + exit_btn.y + 8)
        )

        # ---------- SHOW COLLECTED ITEMS ----------
        y = BOX_Y + BOX_H - 90
        for item in collected_items:
            screen.blit(
                font.render(item, True, (255, 255, 0)),
                (BOX_X + 20, y)
            )
            y += 25

        pygame.display.update()
        clock.tick(60)