import pygame, sys

def run_laptop(screen, laptop_state):
    WIDTH, HEIGHT = 900, 600
    TASKBAR_HEIGHT = 50
    clock = pygame.time.Clock()

    # ---------- INITIALIZE PERSISTENT STATE ----------
    if "wifi_connected" not in laptop_state:
        laptop_state["wifi_connected"] = False
    if "compiled" not in laptop_state:
        laptop_state["compiled"] = False

    # ---------- LOAD WALLPAPER ----------
    try:
        bg = pygame.image.load("assets/wallpaper.png")
        bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    except:
        bg = pygame.Surface((WIDTH, HEIGHT))
        bg.fill((30, 0, 0))

    # ---------- FONTS & COLORS ----------
    font = pygame.font.SysFont("Consolas", 18) # Using Consolas for code feel
    big_font = pygame.font.SysFont(None, 30)
    DARK_RED, RED, LIGHT_RED = (60, 0, 0), (150, 0, 0), (200, 50, 50)
    WHITE, GREEN, GRAY = (255, 255, 255), (0, 255, 0), (100, 100, 100)

    # ---------- LOCAL UI STATE ----------
    current_app = None
    input_text = ""
    message = ""
    scroll_y = 0  # Track scrolling position
    
    # ---------- UI ELEMENTS ----------
    wifi_btn = pygame.Rect(250, 180, 140, 140)
    compiler_btn = pygame.Rect(510, 180, 140, 140)
    back_btn = pygame.Rect(20, 10, 80, 30)
    run_btn = pygame.Rect(350, 450, 200, 50)
    
    # Large Compiler Box
    code_box_rect = pygame.Rect(100, 100, 700, 300)

    # ---------- LARGE CODE CONTENT ----------
    code_lines = [
        "import socket",
        "import time",
        "import sys",
        "",
        "SERVER_IP = '192.168.1.1'",
        "PORT = 8080",
        "",
        "def initialize_handshake():",
        "    print('Initializing encryption...')",
        "    time.sleep(0.5)",
        "    return True",
        "",
        "def connect_to_server():",
        "    try:",
        "        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)",
        "        client.connect((SERVER_IP, PORT))",
        "        if initialize_handshake():",
        "            print('Handshake successful.')",
        "        return client",
        "    except Exception as e:",
        "        print(f'Error: {e}')",
        "        return None",
        "",
        "def open_door():",
        "    conn = connect_to_server()",
        "    if conn:",
        "        request = 'OPEN_SECURE_DOOR_V2'",
        "        conn.send(request.encode())",
        "        response = conn.recv(1024)",
        "        print('Door Status:', response.decode())",
        "        conn.close()",
        "",
        "if __name__ == '__main__':",
        "    print('Starting remote exploit...')",
        "    open_door()",
        "",
        "# --------------------------------------------------",
        "# NOTE: Check underground security logs for fruit-id",
        "# underground password is my favourite fruit and i like pineapple",
    ]

    def draw_icon(rect, label, hovered):
        color = LIGHT_RED if hovered else DARK_RED
        pygame.draw.rect(screen, color, rect, border_radius=8)
        pygame.draw.rect(screen, RED, rect, 3, border_radius=8)
        text = big_font.render(label, True, WHITE)
        screen.blit(text, (rect.x + rect.width//2 - text.get_width()//2,
                          rect.y + rect.height//2 - text.get_height()//2))

    # ---------- MAIN LOOP ----------
    while True:
        screen.blit(bg, (0, 0))
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # SCROLLING LOGIC
            if event.type == pygame.MOUSEWHEEL and current_app == "compiler":
                scroll_y += event.y * 20
                # Clamp scrolling so we don't go too far
                scroll_y = min(0, max(scroll_y, -len(code_lines) * 22 + 250))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if current_app is None and back_btn.collidepoint(event.pos):
                    return laptop_state["compiled"]

                if current_app is None:
                    if wifi_btn.collidepoint(event.pos):
                        current_app = "wifi"
                    elif compiler_btn.collidepoint(event.pos):
                        current_app = "compiler"
                else:
                    if back_btn.collidepoint(event.pos):
                        current_app = None
                        message = ""
                        scroll_y = 0
                    elif current_app == "compiler" and run_btn.collidepoint(event.pos):
                        if laptop_state["wifi_connected"]:
                            message = "Compilation Success!"
                            laptop_state["compiled"] = True
                        else:
                            message = "No WiFi Connected"

            if event.type == pygame.KEYDOWN:
                if current_app == "wifi":
                    if event.key == pygame.K_RETURN:
                        if input_text.lower() == "modern":
                            laptop_state["wifi_connected"] = True
                            message = "WiFi Connected"
                        else:
                            message = "Wrong Password"
                        input_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

        # ---------- RENDERING ----------
        if current_app is None:
            draw_icon(wifi_btn, "WiFi", wifi_btn.collidepoint(mx, my))
            draw_icon(compiler_btn, "Compiler", compiler_btn.collidepoint(mx, my))
            pygame.draw.rect(screen, RED, back_btn)
            screen.blit(big_font.render("EXIT", True, WHITE), (30, 15))

        elif current_app == "wifi":
            pygame.draw.rect(screen, (30, 0, 0), (100, 100, 700, 350), border_radius=10)
            pygame.draw.rect(screen, RED, (100, 100, 700, 350), 3, border_radius=10)
            pygame.draw.rect(screen, RED, back_btn)
            screen.blit(big_font.render("BACK", True, WHITE), (30, 15))
            screen.blit(big_font.render("Enter WiFi Password (modern_vip)", True, WHITE), (250, 180))
            pygame.draw.rect(screen, WHITE, (300, 230, 300, 40), 2)
            screen.blit(big_font.render(input_text, True, WHITE), (310, 240))
            screen.blit(big_font.render(message, True, GREEN if laptop_state["wifi_connected"] else LIGHT_RED), (300, 290))

        elif current_app == "compiler":
            pygame.draw.rect(screen, (20, 0, 0), (50, 50, 800, 450), border_radius=10)
            pygame.draw.rect(screen, RED, (50, 50, 800, 450), 3, border_radius=10)
            pygame.draw.rect(screen, RED, back_btn)
            screen.blit(big_font.render("BACK", True, WHITE), (30, 15))

            # Terminal Window
            pygame.draw.rect(screen, (0, 0, 0), code_box_rect)
            pygame.draw.rect(screen, RED, code_box_rect, 2)

            # SCROLLABLE CODE RENDERING
            # Set clipping region so code doesn't draw outside the black box
            screen.set_clip(code_box_rect)
            y_pos = code_box_rect.y + 10 + scroll_y
            
            for i, line in enumerate(code_lines):
                # Check if it's the last line (the secret hint)
                line_color = GREEN
                if "underground password" in line:
                    line_color = GRAY
                
                text_surf = font.render(line, True, line_color)
                screen.blit(text_surf, (code_box_rect.x + 15, y_pos))
                y_pos += 22
            
            screen.set_clip(None) # Reset clipping

            # UI Buttons
            pygame.draw.rect(screen, RED, run_btn, border_radius=6)
            pygame.draw.rect(screen, WHITE, run_btn, 2, border_radius=6)
            screen.blit(big_font.render("COMPILE", True, WHITE), (run_btn.x+45, run_btn.y+10))
            screen.blit(big_font.render(message, True, GREEN if laptop_state["compiled"] else LIGHT_RED), (350, 520))

            if laptop_state["compiled"]:
                screen.blit(big_font.render("PUZZLE SOLVED", True, GREEN), (330, 60))

        # ---------- TASKBAR ----------
        pygame.draw.rect(screen, (20, 0, 0), (0, HEIGHT - TASKBAR_HEIGHT, WIDTH, TASKBAR_HEIGHT))
        pygame.draw.line(screen, RED, (0, HEIGHT - TASKBAR_HEIGHT), (WIDTH, HEIGHT - TASKBAR_HEIGHT), 2)
        screen.blit(big_font.render("Mini OS", True, WHITE), (10, HEIGHT - 40))

        if laptop_state["wifi_connected"]:
            screen.blit(big_font.render("WiFi: Connected", True, GREEN), (680, HEIGHT - 40))
        else:
            screen.blit(big_font.render("WiFi: Disconnected", True, LIGHT_RED), (680, HEIGHT - 40))

        pygame.display.update()
        clock.tick(60)