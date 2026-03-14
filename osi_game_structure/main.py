import pygame
import sys

from floors.physical_layer import run_physical_layer
from ui.inventory import Inventory

pygame.init()

screen = pygame.display.set_mode((1280,720))

inventory = Inventory()

while True:

    run_physical_layer(screen, inventory)