import pygame

class Inventory:

    def __init__(self):

        self.items = []

        self.icons = {
            
            "cable": pygame.image.load("assets/wire.png")
        }

        for key in self.icons:
            self.icons[key] = pygame.transform.scale(self.icons[key], (60,60))


    def add_item(self, item):

        if item not in self.items:
            self.items.append(item)


    def draw(self, screen):

        WIDTH, HEIGHT = screen.get_size()

        panel = pygame.Rect(WIDTH-160, 0, 160, HEIGHT)

        pygame.draw.rect(screen, (40,40,40), panel)
        pygame.draw.rect(screen, (255,255,255), panel, 2)

        font = pygame.font.SysFont("Times New Roman", 26, bold=True)

        title = font.render("Inventory", True, (255,215,0))
        screen.blit(title, (WIDTH-140, 20))

        y = 90

        for item in self.items:

            icon = self.icons[item]

            screen.blit(icon, (WIDTH-120, y))

            y += 80