import pygame

def run_colour_game(screen, transport_state):

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)

    WIDTH, HEIGHT = screen.get_size()

    # ---------- POPUP ----------
    popup_rect = pygame.Rect(WIDTH//2 - 350, HEIGHT//2 - 300, 700, 600)

    # ---------- GRID ----------
    ROWS, COLS = 5, 5
    SIZE = 60
    MARGIN = 8

    grid_start_x = popup_rect.x + 60
    grid_start_y = popup_rect.y + 60

    # ---------- COLORS ----------
    WHITE = (255,255,255)
    GRAY = (100,100,100)
    GREEN = (0,200,0)
    RED = (200,0,0)
    YELLOW = (230,200,0)

    color_cycle = [GRAY, GREEN, RED, YELLOW]

    # ---------- ✅ STATE GRID ----------
    if "color_grid" not in transport_state:
        transport_state["color_grid"] = [[0 for _ in range(COLS)] for _ in range(ROWS)]

    grid = transport_state["color_grid"]

    # ---------- MATRICES ----------
    green_matrix = [
        [1,0,1,0,0],
        [0,1,0,0,0],
        [0,0,0,0,0],
        [0,0,0,1,0],
        [0,0,0,0,1]
    ]

    red_matrix = [
        [0,1,0,0,1],
        [0,0,0,1,0],
        [0,0,0,0,0],
        [0,1,0,0,0],
        [1,0,0,0,0]
    ]

    yellow_matrix = [
        [0,0,0,1,0],
        [0,0,1,0,0],
        [0,0,0,1,0],
        [0,0,1,0,0],
        [0,0,1,0,0]
    ]

    # ---------- FUNCTIONS ----------
    def evaluate_color(matrix, color_code):
        correct = 0
        total_selected = 0

        for i in range(ROWS):
            for j in range(COLS):
                if grid[i][j] == color_code:
                    total_selected += 1
                    if matrix[i][j] == 1:
                        correct += 1

        return correct, total_selected

    def get_cell(pos):
        mx, my = pos
        for i in range(ROWS):
            for j in range(COLS):
                x = grid_start_x + j * (SIZE + MARGIN)
                y = grid_start_y + i * (SIZE + MARGIN)
                rect = pygame.Rect(x,y,SIZE,SIZE)
                if rect.collidepoint(mx,my):
                    return i,j
        return None

    # ---------- LIGHT SYSTEM ----------
    blink_timer = 0
    blink_state = True

    def draw_lights(g_data, r_data, y_data):
        nonlocal blink_state

        base_y = popup_rect.bottom - 40

        def get_color_light(data, base_color):
            correct, selected = data

            if selected > 5:
                return (40,40,40)

            if correct == 5 and selected == 5:
                return base_color if blink_state else tuple(c//2 for c in base_color)

            return (40,40,40)

        pygame.draw.circle(screen, get_color_light(g_data,(0,255,0)), (popup_rect.centerx - 100, base_y), 12)
        pygame.draw.circle(screen, get_color_light(r_data,(255,0,0)), (popup_rect.centerx, base_y), 12)
        pygame.draw.circle(screen, get_color_light(y_data,(255,255,0)), (popup_rect.centerx + 100, base_y), 12)

    # ---------- LOOP ----------
    while True:

        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                return {"green": False, "red": False, "yellow": False}

            if event.type == pygame.MOUSEBUTTONDOWN:

                # BACK BUTTON
                back_btn = pygame.Rect(popup_rect.right - 100, popup_rect.y + 10, 80, 35)
                if back_btn.collidepoint(event.pos):

                    green_ok = (evaluate_color(green_matrix,1) == (5,5))
                    red_ok = (evaluate_color(red_matrix,2) == (5,5))
                    yellow_ok = (evaluate_color(yellow_matrix,3) == (5,5))

                    return {
                        "green": green_ok,
                        "red": red_ok,
                        "yellow": yellow_ok
                    }

                # GRID CLICK
                cell = get_cell(event.pos)
                if cell:
                    i, j = cell
                    grid[i][j] = (grid[i][j] + 1) % len(color_cycle)

        # ---------- EVALUATE ----------
        green_data = evaluate_color(green_matrix, 1)
        red_data = evaluate_color(red_matrix, 2)
        yellow_data = evaluate_color(yellow_matrix, 3)

        green_ok = (green_data == (5,5))
        red_ok = (red_data == (5,5))
        yellow_ok = (yellow_data == (5,5))

        # ---------- BLINK ----------
        blink_timer += 1
        if blink_timer > 30:
            blink_state = not blink_state
            blink_timer = 0

        # ---------- DRAW ----------
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(160)
        overlay.fill((0,0,0))
        screen.blit(overlay,(0,0))

        pygame.draw.rect(screen,(30,30,30),popup_rect)
        pygame.draw.rect(screen,(200,200,200),popup_rect,2)

        # BACK BUTTON
        pygame.draw.rect(screen,(200,50,50),(popup_rect.right - 100, popup_rect.y + 10, 80, 35))
        screen.blit(font.render("BACK",True,(255,255,255)),(popup_rect.right - 90, popup_rect.y + 15))

        # GRID
        for i in range(ROWS):
            for j in range(COLS):
                x = grid_start_x + j * (SIZE + MARGIN)
                y = grid_start_y + i * (SIZE + MARGIN)

                color = color_cycle[grid[i][j]]
                pygame.draw.rect(screen, color, (x,y,SIZE,SIZE))
                pygame.draw.rect(screen, WHITE, (x,y,SIZE,SIZE), 2)

        draw_lights(green_data, red_data, yellow_data)

        txt = font.render(
            "PUZZLE SOLVED ✔" if (green_ok and red_ok and yellow_ok)
            else "Match the matrix pattern",
            True,
            (0,255,0) if (green_ok and red_ok and yellow_ok) else WHITE
        )

        screen.blit(txt, (popup_rect.centerx - 150, popup_rect.bottom - 70))

        pygame.display.update()
        clock.tick(60)