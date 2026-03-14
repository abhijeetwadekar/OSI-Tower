import pygame
import sys

def run_start_menu(screen):

    WIDTH, HEIGHT = screen.get_size()

    # Load background
    bg = pygame.image.load("assets/tower.png")
    bg = pygame.transform.scale(bg,(WIDTH,HEIGHT))

    # Colors
    WHITE = (255,255,255)
    GOLD = (255,215,0)
    BOX = (40,40,40)
    HOVER = (80,80,80)

    # Fonts
    title_font = pygame.font.SysFont("Times New Roman",72,bold=True)
    button_font = pygame.font.SysFont("Times New Roman",40,bold=True)

    # Buttons
    start_button = pygame.Rect(WIDTH//2-110,420,220,70)
    guide_button = pygame.Rect(WIDTH//2-110,510,220,70)

    clock = pygame.time.Clock()

    while True:

        mouse = pygame.mouse.get_pos()

        screen.blit(bg,(0,0))

        # Title
        title = title_font.render("OSI TOWER",True,GOLD)
        screen.blit(title,title.get_rect(center=(WIDTH//2,150)))

        # START button
        if start_button.collidepoint(mouse):
            pygame.draw.rect(screen,HOVER,start_button)
        else:
            pygame.draw.rect(screen,BOX,start_button)

        pygame.draw.rect(screen,WHITE,start_button,2)

        start_text = button_font.render("START",True,WHITE)
        screen.blit(start_text,start_text.get_rect(center=start_button.center))

        # GUIDE button
        if guide_button.collidepoint(mouse):
            pygame.draw.rect(screen,HOVER,guide_button)
        else:
            pygame.draw.rect(screen,BOX,guide_button)

        pygame.draw.rect(screen,WHITE,guide_button,2)

        guide_text = button_font.render("GUIDE",True,WHITE)
        screen.blit(guide_text,guide_text.get_rect(center=guide_button.center))

        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if start_button.collidepoint(event.pos):
                    return "start"

                if guide_button.collidepoint(event.pos):
                    print("Show guide here")