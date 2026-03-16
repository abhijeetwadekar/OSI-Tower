import pygame
from ui.inventory import Inventory
from ui.start_menu import run_start_menu
from floors.physical_layer import run_physical_layer
from floors.data_link_layer import run_data_layer

pygame.init()

SCREEN_WIDTH = 1152
SCREEN_HEIGHT = 768

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("OSI Mystery Escape")

inventory = Inventory()

# START MENU + ZOOM
run_start_menu(screen)

# PHYSICAL LAYER
run_physical_layer(screen, inventory)

# DATA LINK LAYER
run_data_layer(screen, inventory)

pygame.quit()