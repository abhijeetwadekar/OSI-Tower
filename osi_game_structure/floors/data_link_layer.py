import pygame
import sys

def run_data_layer(screen, inventory):

    font = pygame.font.SysFont(None,50)

    running = True

    while running:

        screen.fill((20,20,40))

        text = font.render("DATA LINK LAYER",True,(255,255,255))
        screen.blit(text,(400,300))

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()