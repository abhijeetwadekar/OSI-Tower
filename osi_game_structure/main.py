import pygame
from ui.inventory import Inventory
from floors.physical_layer import run_physical_layer

pygame.init()

SCREEN_WIDTH = 1152
SCREEN_HEIGHT = 768

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("OSI Mystery Escape")

inventory = Inventory()

run_physical_layer(screen, inventory)

pygame.quit()