import pygame, sys

pygame.init()

# ---------- SCREEN ----------
WIDTH, HEIGHT = 900, 600
TASKBAR_HEIGHT = 50

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Computer")

clock = pygame.time.Clock()

# ---------- LOAD WALLPAPER (SAME FOLDER) ----------
try:
    bg = pygame.image.load("wifi_compiler_wallpaper.png")
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
except:
    print("Wallpaper not found, using fallback")
    bg = pygame.Surface((WIDTH, HEIGHT))
    bg.fill((30, 0, 0))

# ---------- FONTS ----------
font = pygame.font.SysFont(None, 26)
big_font = pygame.font.SysFont(None, 36)

# ---------- COLORS ----------
DARK_RED = (60, 0, 0)
RED = (150, 0, 0)
LIGHT_RED = (200, 50, 50)
WHITE = (255,255,255)
GREEN = (0,200,0)

# ---------- STATE ----------
wifi_connected = False
current_app = None
input_text = ""
message = ""
compiled = False

# ---------- ICON BUTTONS ----------
wifi_btn = pygame.Rect(250, 180, 140, 140)
compiler_btn = pygame.Rect(510, 180, 140, 140)

# ---------- UI BUTTONS ----------
back_btn = pygame.Rect(20, 10, 80, 30)
run_btn = pygame.Rect(350, 450, 200, 50)

# ---------- CODE ----------
code_lines = [
    "import socket",
    "",
    "client = socket.socket()",
    "client.connect(('192.168.1.1', 8080))",
    "",
    "def open_door():",
    "    request = 'OPEN_DOOR'",
    "    client.send(request.encode())",
    "    response = client.recv(1024)",
    "    print(response.decode())",
    "",
    "open_door()"
]

# ---------- DRAW ICON ----------
def draw_icon(rect, label, hovered):
    color = LIGHT_RED if hovered else DARK_RED

    pygame.draw.rect(screen, color, rect, border_radius=8)
    pygame.draw.rect(screen, RED, rect, 3, border_radius=8)

    text = font.render(label, True, WHITE)
    screen.blit(text, (
        rect.x + rect.width//2 - text.get_width()//2,
        rect.y + rect.height//2 - text.get_height()//2
    ))

# ---------- LOOP ----------
running = True
while running:

    screen.blit(bg, (0,0))
    mx, my = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            if current_app is None:
                if wifi_btn.collidepoint(event.pos):
                    current_app = "wifi"

                if compiler_btn.collidepoint(event.pos):
                    current_app = "compiler"

            else:
                if back_btn.collidepoint(event.pos):
                    current_app = None
                    message = ""

                if current_app == "compiler":
                    if run_btn.collidepoint(event.pos):
                        if wifi_connected:
                            message = "Compilation Success!"
                            compiled = True
                        else:
                            message = "No WiFi Connected"

        if event.type == pygame.KEYDOWN:
            if current_app == "wifi":
                if event.key == pygame.K_RETURN:
                    if input_text == "modern":
                        wifi_connected = True
                        message = "WiFi Connected"
                    else:
                        message = "Wrong Password"
                    input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

    # ---------- DESKTOP ----------
    if current_app is None:
        draw_icon(wifi_btn, "WiFi", wifi_btn.collidepoint(mx, my))
        draw_icon(compiler_btn, "Compiler", compiler_btn.collidepoint(mx, my))

    # ---------- WIFI APP ----------
    elif current_app == "wifi":
        pygame.draw.rect(screen, (30,0,0), (100,100,700,350), border_radius=10)
        pygame.draw.rect(screen, RED, (100,100,700,350), 3, border_radius=10)

        pygame.draw.rect(screen, RED, back_btn)
        screen.blit(font.render("BACK", True, WHITE), (30,15))

        screen.blit(big_font.render("Enter WiFi Password", True, WHITE), (300,180))
        pygame.draw.rect(screen, WHITE, (300,230,300,40), 2)

        screen.blit(font.render(input_text, True, WHITE), (310,240))
        screen.blit(font.render(message, True, LIGHT_RED), (300,290))

    # ---------- COMPILER ----------
    elif current_app == "compiler":
        pygame.draw.rect(screen, (20,0,0), (50,50,800,450), border_radius=10)
        pygame.draw.rect(screen, RED, (50,50,800,450), 3, border_radius=10)

        pygame.draw.rect(screen, RED, back_btn)
        screen.blit(font.render("BACK", True, WHITE), (30,15))

        # Code box
        pygame.draw.rect(screen, (0,0,0), (100,100,700,300))
        pygame.draw.rect(screen, RED, (100,100,700,300), 2)

        y_offset = 110
        for line in code_lines:
            text = font.render(line, True, (0,255,0))
            screen.blit(text, (120, y_offset))
            y_offset += 20

        # Compile button
        pygame.draw.rect(screen, RED, run_btn, border_radius=6)
        pygame.draw.rect(screen, WHITE, run_btn, 2, border_radius=6)

        screen.blit(font.render("COMPILE", True, WHITE), (420,465))

        screen.blit(font.render(message, True, LIGHT_RED), (350,520))

        if compiled:
            screen.blit(big_font.render("PUZZLE SOLVED", True, GREEN), (330,60))

    # ---------- TASKBAR ----------
    pygame.draw.rect(screen, (20,0,0), (0, HEIGHT - TASKBAR_HEIGHT, WIDTH, TASKBAR_HEIGHT))
    pygame.draw.line(screen, RED, (0, HEIGHT - TASKBAR_HEIGHT), (WIDTH, HEIGHT - TASKBAR_HEIGHT), 2)

    screen.blit(font.render("Mini OS", True, WHITE), (10, HEIGHT - 35))

    if wifi_connected:
        screen.blit(font.render("WiFi: Connected", True, GREEN), (700, HEIGHT - 35))
    else:
        screen.blit(font.render("WiFi: Disconnected", True, LIGHT_RED), (700, HEIGHT - 35))

    pygame.display.update()
    clock.tick(60)