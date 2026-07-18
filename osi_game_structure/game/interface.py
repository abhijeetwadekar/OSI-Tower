import pygame
import sys
from datetime import datetime
from PIL import Image

wifi_connected = False

def run_interface(game_screen, wire_fixed, network_state=None):
    global wifi_connected
    wifi_connected = False
    
    # Restore previous interface state if it exists
    restored_state = {}
    if network_state and "interface_state" in network_state:
        restored_state = network_state["interface_state"].copy()
        del network_state["interface_state"]  # Remove so we don't restore again

    # Use the existing game screen (pygame already initialized by main game)
    WIDTH, HEIGHT = game_screen.get_size()
    screen = game_screen
    clock = pygame.time.Clock()

    # Colors
    DARK_BG = (10, 10, 10)
    SCREEN_BG = (15, 24, 39)
    BUTTON_COLOR = (30, 41, 59)
    BUTTON_HOVER = (51, 65, 85)
    TEXT_COLOR = (255, 255, 255)
    TASKBAR_BG = (2, 6, 23)
    
    screen.fill(DARK_BG)
    
    # Load wallpaper
    try:
        wallpaper = Image.open("game/wallpaper.png")
        wallpaper = wallpaper.resize((WIDTH - 100, HEIGHT - 140))
        wallpaper_data = pygame.image.fromstring(wallpaper.tobytes(), wallpaper.size, wallpaper.mode)
    except:
        wallpaper_data = None

    # Fonts
    font_large = pygame.font.SysFont("Times New Roman", 22, bold=True)
    font_normal = pygame.font.SysFont("Times New Roman", 20)
    font_small = pygame.font.SysFont("Times New Roman", 18)
    
    # Camera image
    try:
        camera_img = pygame.image.load("assets/gadha.jpeg")
        camera_img = pygame.transform.scale(camera_img, (400, 150))
    except Exception:
        try:
            camera_img = pygame.image.load("assets/gadga.jpeg")
            camera_img = pygame.transform.scale(camera_img, (400, 150))
        except Exception:
            camera_img = pygame.Surface((400, 150))
            camera_img.fill((40, 40, 40))
            missing_text = font_small.render("Camera image not found", True, TEXT_COLOR)
            camera_img.blit(missing_text, missing_text.get_rect(center=camera_img.get_rect().center))
    
    # Screen area - responsive to window size
    screen_rect = pygame.Rect(50, 40, WIDTH - 100, HEIGHT - 140)
    
    # Button rectangles - larger buttons
    btn_w, btn_h = 220, 120
    btn_start_y = 120
    btn_spacing_x = 300
    
    wifi_btn = pygame.Rect(100, btn_start_y, btn_w, btn_h)
    settings_btn = pygame.Rect(100 + btn_spacing_x, btn_start_y, btn_w, btn_h)
    command_btn = pygame.Rect(100, btn_start_y + 160, btn_w, btn_h)
    camera_btn = pygame.Rect(100 + btn_spacing_x, btn_start_y + 160, btn_w, btn_h)
    
    # Back button
    back_btn_rect = pygame.Rect(50, 40, 80, 40)
    
    # Taskbar at bottom
    taskbar_rect = pygame.Rect(50, HEIGHT - 50, WIDTH - 100, 40)
    
    # Dialog states
    current_dialog = restored_state.get("current_dialog", None)  # "wifi", "settings", "command", "camera"
    wifi_password = restored_state.get("wifi_password", "")
    command_input = restored_state.get("command_input", "")
    command_output = restored_state.get("command_output", [])
    command_output_colors = restored_state.get("command_output_colors", [])
    
    running = True
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        # Draw main screen
        screen.fill(DARK_BG)
        pygame.draw.rect(screen, (40, 40, 40), screen_rect, 5)
        
        if wallpaper_data:
            screen.blit(wallpaper_data, (screen_rect.x, screen_rect.y))
        else:
            pygame.draw.rect(screen, SCREEN_BG, screen_rect)
        
        # Draw buttons if no dialog
        if current_dialog is None:
            # Draw back button
            pygame.draw.rect(screen, BUTTON_COLOR, back_btn_rect)
            pygame.draw.rect(screen, TEXT_COLOR, back_btn_rect, 2)
            back_text = font_normal.render("BACK", True, TEXT_COLOR)
            screen.blit(back_text, back_text.get_rect(center=back_btn_rect.center))
            
            button_list = [
                (wifi_btn, "WiFi"),
                (settings_btn, "Settings"),
                (command_btn, "Command"),
                (camera_btn, "Camera")
            ]
            
            for btn_rect, label in button_list:
                hover = btn_rect.collidepoint(mouse_pos)
                color = BUTTON_HOVER if hover else BUTTON_COLOR
                pygame.draw.rect(screen, color, btn_rect)
                pygame.draw.rect(screen, TEXT_COLOR, btn_rect, 2)
                
                text = font_large.render(label, True, TEXT_COLOR)
                text_rect = text.get_rect(center=btn_rect.center)
                screen.blit(text, text_rect)
        
        # Draw dialogs
        if current_dialog == "wifi":
            dialog_rect = pygame.Rect(WIDTH//2 - 250, HEIGHT//2 - 125, 500, 250)
            pygame.draw.rect(screen, (30, 30, 30), dialog_rect)
            pygame.draw.rect(screen, (100, 100, 100), dialog_rect, 2)
            
            title = font_large.render("WiFi Connection", True, TEXT_COLOR)
            screen.blit(title, (dialog_rect.x + 20, dialog_rect.y + 20))
            
            if not wire_fixed:
                msg = font_normal.render("Error: Wire not connected", True, (255, 0, 0))
                screen.blit(msg, (dialog_rect.x + 20, dialog_rect.y + 80))
                ok_btn = pygame.Rect(dialog_rect.x + 180, dialog_rect.y + 180, 80, 40)
                pygame.draw.rect(screen, BUTTON_COLOR, ok_btn)
                pygame.draw.rect(screen, TEXT_COLOR, ok_btn, 1)
                ok_text = font_normal.render("OK", True, TEXT_COLOR)
                screen.blit(ok_text, ok_text.get_rect(center=ok_btn.center))
            else:
                label = font_normal.render("Password:", True, TEXT_COLOR)
                screen.blit(label, (dialog_rect.x + 20, dialog_rect.y + 80))
                
                input_rect = pygame.Rect(dialog_rect.x + 150, dialog_rect.y + 75, 300, 35)
                pygame.draw.rect(screen, (50, 50, 50), input_rect)
                pygame.draw.rect(screen, (100, 100, 100), input_rect, 1)
                
                pwd_text = font_normal.render("*" * len(wifi_password), True, TEXT_COLOR)
                screen.blit(pwd_text, (input_rect.x + 10, input_rect.y + 7))
                
                connect_btn = pygame.Rect(dialog_rect.x + 150, dialog_rect.y + 140, 100, 40)
                pygame.draw.rect(screen, (0, 150, 0), connect_btn)
                pygame.draw.rect(screen, TEXT_COLOR, connect_btn, 1)
                connect_text = font_normal.render("Connect", True, TEXT_COLOR)
                screen.blit(connect_text, connect_text.get_rect(center=connect_btn.center))
                
                cancel_btn = pygame.Rect(dialog_rect.x + 270, dialog_rect.y + 140, 100, 40)
                pygame.draw.rect(screen, BUTTON_COLOR, cancel_btn)
                pygame.draw.rect(screen, TEXT_COLOR, cancel_btn, 1)
                cancel_text = font_normal.render("Cancel", True, TEXT_COLOR)
                screen.blit(cancel_text, cancel_text.get_rect(center=cancel_btn.center))
        
        elif current_dialog == "settings":
            dialog_rect = pygame.Rect(WIDTH//2 - 250, HEIGHT//2 - 125, 500, 250)
            pygame.draw.rect(screen, (30, 30, 30), dialog_rect)
            pygame.draw.rect(screen, (100, 100, 100), dialog_rect, 2)
            
            title = font_large.render("System Settings", True, TEXT_COLOR)
            screen.blit(title, (dialog_rect.x + 20, dialog_rect.y + 20))
            
            settings_text = [
                "RAM: 8GB",
                "CPU: Intel i5",
                "OS: Custom OS v1.0"
            ]
            
            y_offset = 80
            for setting in settings_text:
                text = font_normal.render(setting, True, TEXT_COLOR)
                screen.blit(text, (dialog_rect.x + 40, dialog_rect.y + y_offset))
                y_offset += 40
            
            close_btn = pygame.Rect(dialog_rect.x + 200, dialog_rect.y + 200, 100, 40)
            pygame.draw.rect(screen, BUTTON_COLOR, close_btn)
            pygame.draw.rect(screen, TEXT_COLOR, close_btn, 1)
            close_text = font_normal.render("Close", True, TEXT_COLOR)
            screen.blit(close_text, close_text.get_rect(center=close_btn.center))
        
        elif current_dialog == "command":
            dialog_rect = pygame.Rect(WIDTH//2 - 300, HEIGHT//2 - 200, 600, 400)
            pygame.draw.rect(screen, (0, 0, 0), dialog_rect)
            pygame.draw.rect(screen, (0, 255, 0), dialog_rect, 2)
            
            title = font_large.render("Command Prompt", True, (0, 255, 0))
            screen.blit(title, (dialog_rect.x + 20, dialog_rect.y + 20))
            
            # Input box
            input_rect = pygame.Rect(dialog_rect.x + 20, dialog_rect.y + 60, 560, 30)
            pygame.draw.rect(screen, (20, 20, 20), input_rect)
            pygame.draw.rect(screen, (0, 255, 0), input_rect, 1)
            
            input_text = font_small.render("> " + command_input, True, (0, 255, 0))
            screen.blit(input_text, (input_rect.x + 5, input_rect.y + 5))
            
            # Output area
            output_rect = pygame.Rect(dialog_rect.x + 20, dialog_rect.y + 110, 560, 220)
            pygame.draw.rect(screen, (10, 10, 10), output_rect)
            pygame.draw.rect(screen, (0, 255, 0), output_rect, 1)
            
            y_pos = output_rect.y + 10
            for i, line in enumerate(command_output[-10:]):
                color_idx = max(0, len(command_output_colors) - 10 + i)
                color = command_output_colors[color_idx] if color_idx < len(command_output_colors) else (255, 255, 255)
                
                # Special coloring for IP address line
                if "192.168.1.10" in line:
                    x_pos = output_rect.x + 10
                    ip_start = line.find("192.168.1.10")
                    for char_idx, char in enumerate(line):
                        if char_idx >= ip_start and char_idx < ip_start + 12:  # Within IP address
                            ip_offset = char_idx - ip_start
                            if char == '9':
                                char_color = (0, 0, 255)  # Blue
                            elif char == '6':
                                char_color = (255, 0, 0)  # Red
                            elif char == '1' and ip_offset == 8:  # The 1 in .1. (7th position = index 8)
                                char_color = (255, 255, 0)  # Yellow
                            elif char == '0':
                                char_color = (0, 255, 0)  # Green
                            else:
                                char_color = color
                        else:
                            char_color = color
                        char_text = font_small.render(char, True, char_color)
                        screen.blit(char_text, (x_pos, y_pos))
                        x_pos += char_text.get_width()
                else:
                    output_text = font_small.render(line, True, color)
                    screen.blit(output_text, (output_rect.x + 10, y_pos))
                y_pos += 20
            
            # Buttons
            run_btn = pygame.Rect(dialog_rect.x + 20, dialog_rect.y + 350, 80, 35)
            pygame.draw.rect(screen, (0, 100, 0), run_btn)
            pygame.draw.rect(screen, (0, 255, 0), run_btn, 1)
            run_text = font_small.render("Run", True, (0, 255, 0))
            screen.blit(run_text, run_text.get_rect(center=run_btn.center))
            
            close_cmd_btn = pygame.Rect(dialog_rect.x + 500, dialog_rect.y + 350, 80, 35)
            pygame.draw.rect(screen, (100, 0, 0), close_cmd_btn)
            pygame.draw.rect(screen, (255, 0, 0), close_cmd_btn, 1)
            close_cmd_text = font_small.render("Close", True, (255, 0, 0))
            screen.blit(close_cmd_text, close_cmd_text.get_rect(center=close_cmd_btn.center))
        
        elif current_dialog == "camera":
            dialog_rect = pygame.Rect(WIDTH//2 - 250, HEIGHT//2 - 125, 500, 250)
            pygame.draw.rect(screen, (30, 30, 30), dialog_rect)
            pygame.draw.rect(screen, (100, 100, 100), dialog_rect, 2)
            
            title = font_large.render("Camera", True, TEXT_COLOR)
            screen.blit(title, (dialog_rect.x + 20, dialog_rect.y + 20))
            
            image_rect = pygame.Rect(dialog_rect.x + 50, dialog_rect.y + 70, 400, 150)
            screen.blit(camera_img, image_rect)
            
            close_camera_btn = pygame.Rect(dialog_rect.x + 200, dialog_rect.y + 180, 100, 40)
            pygame.draw.rect(screen, BUTTON_COLOR, close_camera_btn)
            pygame.draw.rect(screen, TEXT_COLOR, close_camera_btn, 1)
            close_camera_text = font_normal.render("Close", True, TEXT_COLOR)
            screen.blit(close_camera_text, close_camera_text.get_rect(center=close_camera_btn.center))
        
        # Draw taskbar
        pygame.draw.rect(screen, TASKBAR_BG, taskbar_rect)
        pygame.draw.line(screen, (100, 100, 100), (taskbar_rect.x, taskbar_rect.y), (taskbar_rect.right, taskbar_rect.y), 1)
        
        start_text = font_small.render("Start", True, TEXT_COLOR)
        screen.blit(start_text, (taskbar_rect.x + 10, taskbar_rect.y + 12))
        
        now = datetime.now()
        time_str = now.strftime("%H:%M  %d-%m-%Y  %A")
        time_text = font_small.render(time_str, True, TEXT_COLOR)
        screen.blit(time_text, (taskbar_rect.right - time_text.get_width() - 10, taskbar_rect.y + 12))
        
        pygame.display.update()
        clock.tick(60)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if current_dialog is None:
                    if back_btn_rect.collidepoint(event.pos):
                        # Save interface state before exiting
                        if network_state:
                            network_state["interface_state"] = {
                                "current_dialog": current_dialog,
                                "wifi_password": wifi_password,
                                "command_input": command_input,
                                "command_output": command_output,
                                "command_output_colors": command_output_colors
                            }
                        running = False
                    elif wifi_btn.collidepoint(event.pos):
                        current_dialog = "wifi"
                    elif settings_btn.collidepoint(event.pos):
                        current_dialog = "settings"
                    elif command_btn.collidepoint(event.pos):
                        current_dialog = "command"
                    elif camera_btn.collidepoint(event.pos):
                        current_dialog = "camera"
                
                elif current_dialog == "wifi":
                    dialog_rect = pygame.Rect(WIDTH//2 - 250, HEIGHT//2 - 125, 500, 250)
                    if wire_fixed:
                        connect_btn = pygame.Rect(dialog_rect.x + 150, dialog_rect.y + 140, 100, 40)
                        if connect_btn.collidepoint(event.pos):
                            if wifi_password == "i am smart":
                                wifi_connected = True
                                running = False
                            else:
                                wifi_password = ""
                        
                        cancel_btn = pygame.Rect(dialog_rect.x + 270, dialog_rect.y + 140, 100, 40)
                        if cancel_btn.collidepoint(event.pos):
                            current_dialog = None
                    else:
                        ok_btn = pygame.Rect(dialog_rect.x + 180, dialog_rect.y + 180, 80, 40)
                        if ok_btn.collidepoint(event.pos):
                            current_dialog = None
                
                elif current_dialog == "settings":
                    dialog_rect = pygame.Rect(WIDTH//2 - 250, HEIGHT//2 - 125, 500, 250)
                    close_btn = pygame.Rect(dialog_rect.x + 200, dialog_rect.y + 200, 100, 40)
                    if close_btn.collidepoint(event.pos):
                        current_dialog = None
                
                elif current_dialog == "command":
                    dialog_rect = pygame.Rect(WIDTH//2 - 300, HEIGHT//2 - 200, 600, 400)
                    
                    run_btn = pygame.Rect(dialog_rect.x + 20, dialog_rect.y + 350, 80, 35)
                    if run_btn.collidepoint(event.pos):
                        cmd = command_input.lower()
                        command_output = []
                        command_output_colors = []
                        
                        if cmd == "ipconfig":
                            command_output.append("IP Address: 192.168.1.10")
                            command_output_colors.append((255, 255, 255))
                        elif cmd == "wlan_interfaces":
                            if wire_fixed:
                                command_output.append("WiFi Name: Smart WIFI")
                                command_output.append("Password: i am smart")
                                command_output_colors.extend([(255, 255, 255), (255, 255, 255)])
                            else:
                                command_output.append("No WiFi adapters found")
                                command_output_colors.append((255, 0, 0))
                        else:
                            command_output.append("Irrelevant command")
                            command_output_colors.append((255, 255, 255))
                        
                        command_input = ""
                    
                    close_cmd_btn = pygame.Rect(dialog_rect.x + 500, dialog_rect.y + 350, 80, 35)
                    if close_cmd_btn.collidepoint(event.pos):
                        current_dialog = None
                
                elif current_dialog == "camera":
                    dialog_rect = pygame.Rect(WIDTH//2 - 250, HEIGHT//2 - 125, 500, 250)
                    close_camera_btn = pygame.Rect(dialog_rect.x + 200, dialog_rect.y + 180, 100, 40)
                    if close_camera_btn.collidepoint(event.pos):
                        current_dialog = None
            
            if event.type == pygame.KEYDOWN:
                if current_dialog == "wifi" and wire_fixed:
                    if event.key == pygame.K_BACKSPACE:
                        wifi_password = wifi_password[:-1]
                    elif event.key != pygame.K_RETURN:  # Disable Enter key for WiFi
                        if len(wifi_password) < 20:
                            wifi_password += event.unicode
                
                elif current_dialog == "command":
                    if event.key == pygame.K_BACKSPACE:
                        command_input = command_input[:-1]
                    elif event.key == pygame.K_RETURN:
                        cmd = command_input.lower()
                        command_output = []
                        command_output_colors = []
                        
                        if cmd == "ipconfig":
                            command_output.append("IP Address: 192.168.1.10")
                            command_output_colors.append((255, 255, 255))
                        elif cmd == "wlan_interfaces":
                            if wire_fixed:
                                command_output.append("WiFi Name: Smart WIFI")
                                command_output.append("Password: i am smart")
                                command_output_colors.extend([(255, 255, 255), (255, 255, 255)])
                            else:
                                command_output.append("No WiFi adapters found")
                                command_output_colors.append((255, 0, 0))
                        else:
                            command_output.append("Irrelevant command")
                            command_output_colors.append((255, 255, 255))
                        
                        command_input = ""
                    else:
                        if len(command_input) < 50:
                            command_input += event.unicode
    
    return wifi_connected