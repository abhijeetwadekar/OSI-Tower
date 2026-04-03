import pygame
import sys
import time

def run_wall(screen):

    WIDTH, HEIGHT = 900, 700
    TASKBAR_HEIGHT = 60

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)

    # ---------- BACKGROUND ----------
    bg = pygame.image.load("assets/bg.jpg")
    bg = pygame.transform.rotate(bg, 90)
    bg = pygame.transform.smoothscale(bg, (WIDTH, HEIGHT - TASKBAR_HEIGHT))

    # ---------- HAMMER ----------
    hammer_img = pygame.image.load("assets/wall_hammer.png").convert()
    hammer_img.set_colorkey((0, 0, 0))
    hammer_img = pygame.transform.scale(hammer_img, (60, 60))

    # ---------- DENT ----------
    dent_img = pygame.image.load("assets/wall_dent.png").convert()
    dent_img.set_colorkey((0, 0, 0))
    dent_size = 45
    dent_img = pygame.transform.scale(dent_img, (dent_size, dent_size))

    pygame.mouse.set_visible(False)

    # ---------- GRID ----------
    ROWS, COLS = 15, 15
    CELL_W = WIDTH // COLS
    CELL_H = (HEIGHT - TASKBAR_HEIGHT) // ROWS

    dents = []

    # ---------- CLICK LIMIT ----------
    click_count = 0
    MAX_CLICKS = 4

    # ---------- BUTTON ----------
    back_btn = pygame.Rect(350, HEIGHT - 50, 200, 40)

    # ---------- HITBOXES ----------
    hitbox1 = pygame.Rect(340, 250, 200, 50)
    hitbox2 = pygame.Rect(630, 300, 130, 50)
    hitbox3 = pygame.Rect(300, 550, 320, 50)

    # ---------- PUZZLE STATE ----------
    puzzle_solved = False

    # ---------- TIMER ----------
    timer_active = False
    start_time = 0
    TIME_LIMIT = 420

    # ---------- POPUPS ----------
    popup_active = False
    warning_popup_active = False

    # ---------- TASKBAR ----------
    def draw_taskbar():
        pygame.draw.rect(screen, (20,20,20),
                         (0, HEIGHT - TASKBAR_HEIGHT, WIDTH, TASKBAR_HEIGHT))

        btn_color = (0,150,0) if puzzle_solved else (60,60,60)

        pygame.draw.rect(screen, btn_color, back_btn)
        screen.blit(font.render("BACK", True, (255,255,255)),
                    (back_btn.x+70, back_btn.y+10))

        note_text = font.render("Check effect after 4 hits", True, (200,200,200))
        screen.blit(note_text, (20, HEIGHT - 40))

        if timer_active:
            remaining = max(0, TIME_LIMIT - int(time.time() - start_time))
            minutes = remaining // 60
            seconds = remaining % 60
            timer_text = f"{minutes:02}:{seconds:02}"
            screen.blit(font.render(timer_text, True, (255,50,50)),
                        (750, HEIGHT - 45))

    # ---------- POPUPS ----------
    def draw_popup():
        popup_rect = pygame.Rect(150, 200, 600, 200)
        pygame.draw.rect(screen, (30,30,30), popup_rect)
        pygame.draw.rect(screen, (255,255,255), popup_rect, 2)

        lines = [
            "This seems to be someone's name!!",
            "Are you sure you want to break it?"
        ]

        for i, line in enumerate(lines):
            text = font.render(line, True, (255,255,255))
            screen.blit(text, (popup_rect.x + 20, popup_rect.y + 40 + i*30))

        yes_btn = pygame.Rect(250, 330, 150, 50)
        no_btn = pygame.Rect(500, 330, 150, 50)

        pygame.draw.rect(screen, (100,0,0), yes_btn)
        pygame.draw.rect(screen, (0,100,0), no_btn)

        screen.blit(font.render("YES", True, (255,255,255)),
                    (yes_btn.x + 40, yes_btn.y + 15))
        screen.blit(font.render("NO", True, (255,255,255)),
                    (no_btn.x + 50, no_btn.y + 15))

        return yes_btn, no_btn

    def draw_warning_popup():
        popup_rect = pygame.Rect(120, 200, 660, 220)

        pygame.draw.rect(screen, (40,0,0), popup_rect)
        pygame.draw.rect(screen, (255,0,0), popup_rect, 2)

        lines = [
            "That was the developer's name!!",
            "They are mad and will crash your game in 7 minutes!",
            "Complete the game before time runs out!"
        ]

        for i, line in enumerate(lines):
            text = font.render(line, True, (255,255,255))
            screen.blit(text, (popup_rect.x + 20, popup_rect.y + 40 + i*40))

        ok_btn = pygame.Rect(350, 360, 120, 40)
        pygame.draw.rect(screen, (150,0,0), ok_btn)

        screen.blit(font.render("OK", True, (255,255,255)),
                    (ok_btn.x+40, ok_btn.y+10))

        return ok_btn

    # ---------- LOOP ----------
    while True:
        screen.fill((30,30,30))
        screen.blit(bg, (0, 0))

        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                # POPUP 1
                if popup_active:
                    yes_btn, no_btn = draw_popup()

                    if yes_btn.collidepoint(event.pos):
                        popup_active = False
                        warning_popup_active = True

                    elif no_btn.collidepoint(event.pos):
                        popup_active = False

                    continue

                # POPUP 2
                if warning_popup_active:
                    ok_btn = draw_warning_popup()

                    if ok_btn.collidepoint(event.pos):
                        warning_popup_active = False
                        timer_active = True
                        start_time = time.time()

                    continue

                # BACK BUTTON → EXIT POPUP
                if back_btn.collidepoint(event.pos):
                    pygame.mouse.set_visible(True)
                    return puzzle_solved   # ✅ RETURN RESULT

                # NORMAL CLICK
                if event.pos[1] < HEIGHT - TASKBAR_HEIGHT:

                    if click_count >= MAX_CLICKS:
                        continue

                    if hitbox1.collidepoint(event.pos) or hitbox3.collidepoint(event.pos):
                        popup_active = True
                        continue

                    dents.append(event.pos)
                    click_count += 1

                    if hitbox2.collidepoint(event.pos):
                        if not puzzle_solved:
                            puzzle_solved = True

        # DRAW DENTS
        for d in dents:
            screen.blit(dent_img, (d[0] - dent_size//2, d[1] - dent_size//2))

        if popup_active:
            draw_popup()

        if warning_popup_active:
            draw_warning_popup()

        draw_taskbar()

        screen.blit(hammer_img, (mx - 30, my - 10))

        pygame.display.update()
        clock.tick(60)