import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 600, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Matrix Color Puzzle")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

ROWS, COLS = 5, 5
SIZE = 80
MARGIN = 10

# ---------- COLORS ----------
WHITE = (255,255,255)
GRAY = (100,100,100)
GREEN = (0,200,0)
RED = (200,0,0)
YELLOW = (230,200,0)

color_cycle = [GRAY, GREEN, RED, YELLOW]

# ---------- PLAYER GRID ----------
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

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

# ---------- CHECK COLOR ----------
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

# ---------- DRAW GRID ----------
def draw_grid():
    for i in range(ROWS):
        for j in range(COLS):
            x = j * (SIZE + MARGIN) + 50
            y = i * (SIZE + MARGIN) + 50

            color = color_cycle[grid[i][j]]
            pygame.draw.rect(screen, color, (x,y,SIZE,SIZE))
            pygame.draw.rect(screen, WHITE, (x,y,SIZE,SIZE), 2)

# ---------- GET CLICK ----------
def get_cell(pos):
    mx, my = pos
    for i in range(ROWS):
        for j in range(COLS):
            x = j * (SIZE + MARGIN) + 50
            y = i * (SIZE + MARGIN) + 50
            rect = pygame.Rect(x,y,SIZE,SIZE)
            if rect.collidepoint(mx,my):
                return i,j
    return None

# ---------- LIGHT SYSTEM ----------
blink_timer = 0
blink_state = True

def draw_lights(g_data, r_data, y_data):

    global blink_state

    base_y = 600

    def get_color_light(data, base_color):
        correct, selected = data

        # ❌ if more than 5 selected → OFF
        if selected > 5:
            return (40,40,40)

        # 🔥 exact match → BLINK
        if correct == 5 and selected == 5:
            if blink_state:
                return base_color
            else:
                return tuple(c//2 for c in base_color)

        # ❌ otherwise OFF
        return (40,40,40)

    # GREEN
    pygame.draw.circle(screen,
        get_color_light(g_data, (0,255,0)),
        (180, base_y), 15)

    # RED
    pygame.draw.circle(screen,
        get_color_light(r_data, (255,0,0)),
        (300, base_y), 15)

    # YELLOW
    pygame.draw.circle(screen,
        get_color_light(y_data, (255,255,0)),
        (420, base_y), 15)


# ---------- GAME LOOP ----------
running = True

while running:
    screen.fill((30,30,30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            cell = get_cell(event.pos)
            if cell:
                i, j = cell
                grid[i][j] = (grid[i][j] + 1) % len(color_cycle)

    # ---------- EVALUATE ----------
    green_data = evaluate_color(green_matrix, 1)
    red_data = evaluate_color(red_matrix, 2)
    yellow_data = evaluate_color(yellow_matrix, 3)

    # ---------- BLINK TIMER ----------
    blink_timer += 1
    if blink_timer > 30:
        blink_state = not blink_state
        blink_timer = 0

    # ---------- DRAW ----------
    draw_grid()
    draw_lights(green_data, red_data, yellow_data)

    # ---------- WIN ----------
    if (green_data == (5,5) and
        red_data == (5,5) and
        yellow_data == (5,5)):

        txt = font.render("PUZZLE SOLVED!", True, (0,255,0))
    else:
        txt = font.render("Match the matrix pattern", True, WHITE)

    screen.blit(txt, (140, 620))

    pygame.display.update()
    clock.tick(60)