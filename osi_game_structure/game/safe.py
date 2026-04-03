import pygame, sys, math

pygame.init()

# ---------- SCREEN ----------
WIDTH, HEIGHT = 700, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Safe Lock")

clock = pygame.time.Clock()

# ---------- LOAD BACKGROUND ----------
bg = pygame.image.load("safe_bg.png")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

# ---------- COLORS ----------
WHITE = (255,255,255)
BLACK = (0,0,0)
DARK = (60,60,60)

# ---------- CENTER ----------
center = (WIDTH//2 + 5, HEIGHT//2)

# ---------- ANGLES ----------
angle1 = 0
angle2 = 0
angle3 = 0

dragging = None

# ---------- FONT ----------
font = pygame.font.SysFont(None, 50)

# ---------- CONVERT TO CLOCK ANGLE ----------
def get_angle(pos):
    dx = pos[0] - center[0]
    dy = pos[1] - center[1]

    angle = math.degrees(math.atan2(dy, dx))
    angle = (angle + 90) % 360   # 🔥 FIX → makes 0° = top
    return angle

# ---------- DRAW METAL DIAL ----------
def draw_dial(radius, angle):

    # metal fill
    for r in range(radius, radius-15, -1):
        shade = 200 - (radius - r)*6
        pygame.draw.circle(screen, (shade,shade,shade), center, r)

    pygame.draw.circle(screen, DARK, center, radius, 2)

    # ---------- ARROW POINTER ----------
    rad = math.radians(angle - 90)  # 🔥 adjust back for drawing

    tip_x = center[0] + radius * math.cos(rad)
    tip_y = center[1] + radius * math.sin(rad)

    left_x = center[0] + (radius-12) * math.cos(rad - 0.15)
    left_y = center[1] + (radius-12) * math.sin(rad - 0.15)

    right_x = center[0] + (radius-12) * math.cos(rad + 0.15)
    right_y = center[1] + (radius-12) * math.sin(rad + 0.15)

    pygame.draw.polygon(screen, BLACK, [
        (tip_x, tip_y),
        (left_x, left_y),
        (right_x, right_y)
    ])

# ---------- BIG DOTS ----------
def draw_dots(radius):
    for i in range(12):
        ang = (i * 30)

        rad = math.radians(ang - 90)

        x = center[0] + radius * math.cos(rad)
        y = center[1] + radius * math.sin(rad)

        pygame.draw.circle(screen, BLACK, (int(x), int(y)), 9)

# ---------- LOOP ----------
running = True
unlocked = False

while running:

    screen.blit(bg, (0,0))

    mx, my = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            dist = ((mx-center[0])**2 + (my-center[1])**2)**0.5

            if 50 < dist < 75:
                dragging = 3
            elif 95 < dist < 120:
                dragging = 2
            elif 140 < dist < 165:
                dragging = 1

        if event.type == pygame.MOUSEBUTTONUP:
            dragging = None

        if event.type == pygame.MOUSEMOTION:
            if dragging:
                ang = get_angle((mx,my))
                if dragging == 1:
                    angle1 = ang
                elif dragging == 2:
                    angle2 = ang
                elif dragging == 3:
                    angle3 = ang

    # ---------- DRAW ----------
    draw_dial(150, angle1)
    draw_dial(110, angle2)
    draw_dial(70, angle3)

    pygame.draw.circle(screen, (130,130,130), center, 15)
    pygame.draw.circle(screen, BLACK, center, 15, 2)

    draw_dots(180)

    # ---------- UNLOCK CONDITION (CLOCK BASED) ----------
    if (abs(angle1 - 300) < 10 and     # top
        abs(angle2 - 90) < 10 and    # right
        abs(angle3 - 180) < 10):     # bottom
        unlocked = True

    # ---------- MESSAGE ----------
    if unlocked:
        text = font.render("SAFE OPENED", True, BLACK)
        rect = text.get_rect(center=(WIDTH//2, center[1] - 250))
        screen.blit(text, rect)

    pygame.display.update()
    clock.tick(60)