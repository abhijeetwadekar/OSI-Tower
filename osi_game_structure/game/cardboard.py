import pygame

def run_cardbord(screen):

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

    # ---------- CLICK AREAS (RELATIVE TO BOX) ----------
    duct_tape_rect = pygame.Rect(120, 100, 120, 120)
    server_rect = pygame.Rect(120, 280, 200, 120)
    hdmi_rect = pygame.Rect(400, 280, 200, 120)

    exit_btn = pygame.Rect(BOX_W - 90, 10, 80, 35)

    collected_items = []
    running = True

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return collected_items

            if event.type == pygame.MOUSEBUTTONDOWN:

                # adjust click position to box
                mx, my = event.pos
                local_x = mx - BOX_X
                local_y = my - BOX_Y

                if duct_tape_rect.collidepoint((local_x, local_y)):
                    if "tape" not in collected_items:
                        collected_items.append("tape")

                elif server_rect.collidepoint((local_x, local_y)):
                    if "server1" not in collected_items:
                        collected_items.append("server1")

                elif hdmi_rect.collidepoint((local_x, local_y)):
                    if "pcwire" not in collected_items:
                        collected_items.append("pcwire")

                elif exit_btn.collidepoint((local_x, local_y)):
                    return collected_items

        # ---------- DARK BACKGROUND (FOCUS EFFECT) ----------
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0,0,0))
        screen.blit(overlay, (0,0))

        # ---------- DRAW BOX ----------
        screen.blit(bg, (BOX_X, BOX_Y))

        # ---------- DEBUG OUTLINES ----------
        pygame.draw.rect(screen, (255,0,0), duct_tape_rect.move(BOX_X, BOX_Y), 2)
        pygame.draw.rect(screen, (0,255,0), server_rect.move(BOX_X, BOX_Y), 2)
        pygame.draw.rect(screen, (0,0,255), hdmi_rect.move(BOX_X, BOX_Y), 2)

        # exit button
        pygame.draw.rect(screen, (200,50,50), exit_btn.move(BOX_X, BOX_Y))
        screen.blit(font.render("EXIT", True, (255,255,255)),
                    (BOX_X + exit_btn.x + 10, BOX_Y + exit_btn.y + 8))

        # ---------- SHOW COLLECTED ----------
        y = BOX_Y + BOX_H - 90
        for item in collected_items:
            screen.blit(font.render(item, True, (255,255,0)), (BOX_X + 20, y))
            y += 25

        pygame.display.update()
        clock.tick(60)