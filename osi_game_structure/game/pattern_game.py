import pygame, sys

pygame.init()

# ---------- SCREEN ----------
WIDTH, HEIGHT = 900, 600
TASKBAR_HEIGHT = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pattern Game")

clock = pygame.time.Clock()

# ---------- LOAD BACKGROUND ----------
bg = pygame.image.load("assets/bg2.png")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

# ---------- FONT ----------
font = pygame.font.SysFont("algerian", 48)
btn_font = pygame.font.SysFont(None, 28)

# ---------- COLORS ----------
MAROON = (128, 0, 0)
BROWN = (101, 67, 33)
WHITE = (255,255,255)

# ---------- GRID ----------
GRID_SIZE = 4
CELL_SIZE = 110

OFFSET_X = WIDTH//2 - (GRID_SIZE * CELL_SIZE)//2
OFFSET_Y = HEIGHT//2 - (GRID_SIZE * CELL_SIZE)//2 - 20

# ---------- FIXED LETTERS ----------
letters = [
    ["L","R","T","K"],
    ["A","G","H","M"],
    ["I","W","O","P"],
    ["Z","X","Y","S"]
]

# ---------- TARGET ----------
TARGET = "ALGORITHM"

# ---------- STATE ----------
selected = []
input_string = ""
show_popup = False

# ---------- BUTTONS ----------
back_btn = pygame.Rect(WIDTH//2 - 180, HEIGHT - 50, 140, 40)
reset_btn = pygame.Rect(WIDTH//2 + 40, HEIGHT - 50, 140, 40)

# ---------- GET CELL ----------
def get_cell(pos):
    mx, my = pos
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            x = OFFSET_X + j * CELL_SIZE
            y = OFFSET_Y + i * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            if rect.collidepoint(mx, my):
                return (i, j, x, y)
    return None

# ---------- POPUP ----------
def draw_popup():
    popup = pygame.Rect(250, 200, 400, 150)
    pygame.draw.rect(screen, (30,30,30), popup)
    pygame.draw.rect(screen, (255,255,255), popup, 2)

    text = font.render("DOOR OPENED", True, WHITE)
    screen.blit(text, (popup.x + 60, popup.y + 50))

# ---------- GAME LOOP ----------
running = True
while running:

    screen.blit(bg, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            if not show_popup:

                # ---------- GRID CLICK ----------
                cell = get_cell(event.pos)
                if cell:
                    i,j,x,y = cell

                    if (i,j) not in [(c[0],c[1]) for c in selected]:
                        selected.append((i,j,x,y))
                        input_string += letters[i][j]

                        # ---------- CHECK ONLY AFTER FULL LENGTH ----------
                        if len(input_string) == len(TARGET):
                            if input_string == TARGET:
                                show_popup = True
                            else:
                                # wrong pattern → reset after short delay
                                pygame.time.delay(400)
                                selected.clear()
                                input_string = ""

                # ---------- RESET ----------
                if reset_btn.collidepoint(event.pos):
                    selected.clear()
                    input_string = ""

                # ---------- BACK ----------
                if back_btn.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

    # ---------- DRAW LETTERS ----------
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            x = OFFSET_X + j * CELL_SIZE
            y = OFFSET_Y + i * CELL_SIZE

            text = font.render(letters[i][j], True, MAROON)
            screen.blit(text, (x + 35, y + 25))

    # ---------- DRAW CONNECTIONS ----------
    for k in range(len(selected) - 1):
        x1 = selected[k][2] + CELL_SIZE // 2
        y1 = selected[k][3] + CELL_SIZE // 2
        x2 = selected[k+1][2] + CELL_SIZE // 2
        y2 = selected[k+1][3] + CELL_SIZE // 2

        pygame.draw.line(screen, BROWN, (x1,y1), (x2,y2), 5)

    # ---------- TASKBAR ----------
    pygame.draw.rect(screen, (30,30,30), (0, HEIGHT - TASKBAR_HEIGHT, WIDTH, TASKBAR_HEIGHT))

    # BACK BUTTON
    pygame.draw.rect(screen, (80,80,80), back_btn)
    screen.blit(btn_font.render("BACK", True, WHITE),
                (back_btn.x + 40, back_btn.y + 10))

    # RESET BUTTON
    pygame.draw.rect(screen, (120,40,40), reset_btn)
    screen.blit(btn_font.render("RESET", True, WHITE),
                (reset_btn.x + 40, reset_btn.y + 10))

    # ---------- POPUP ----------
    if show_popup:
        draw_popup()

    pygame.display.update()
    clock.tick(60)