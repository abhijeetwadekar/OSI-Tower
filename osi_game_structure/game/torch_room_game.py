import pygame
import sys

pygame.init()

# ---------- SCREEN ----------
WIDTH, HEIGHT = 1000, 650
TORCH_RADIUS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Torch Room")

clock = pygame.time.Clock()

# ---------- LOAD BACKGROUND ----------
bg = pygame.image.load("assets/server_room.png")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

# ---------- SWITCH HITBOX ----------
switch_rect = pygame.Rect(175, 260, 50, 70)  # adjust this

# ---------- LOAD SWITCH IMAGE ----------
switch_img = pygame.image.load("assets/server_switch.png").convert_alpha()
switch_img = pygame.transform.scale(
    switch_img,
    (switch_rect.width, switch_rect.height)
)

# ---------- STATE ----------
lights_on = False

pygame.mouse.set_visible(False)

# ---------- GAME LOOP ----------
running = True
while running:

    screen.blit(bg, (0, 0))
    mx, my = pygame.mouse.get_pos()

    # ---------- EVENTS ----------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not lights_on and switch_rect.collidepoint(event.pos):
                lights_on = True
                print("Switch clicked!")  # debug

    # ---------- TORCH EFFECT ----------
    if not lights_on:
        darkness = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        darkness.fill((0, 0, 0, 255))

        pygame.draw.circle(darkness, (0, 0, 0, 0), (mx, my), TORCH_RADIUS)
        screen.blit(darkness, (0, 0))

    # ---------- DRAW HITBOX (REFERENCE) ----------
    #pygame.draw.rect(screen, (255, 0, 0), switch_rect, 2)

    # ---------- SHOW SWITCH IMAGE AFTER CLICK ----------
    if lights_on:
        screen.blit(switch_img, (switch_rect.x, switch_rect.y))

    # ---------- CURSOR DOT ----------
    pygame.draw.circle(screen, (255,255,255), (mx, my), 3)

    pygame.display.update()
    clock.tick(60)