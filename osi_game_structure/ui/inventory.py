import pygame

class Inventory:

    def __init__(self):
        self.items = []
        self.selected_item = None

        self.icons = {
        "cable": pygame.image.load("assets/wire.png"),
        "rednote": pygame.image.load("assets/rednote.png"),
        "bluenote": pygame.image.load("assets/bluenote.png"),
        "greennote": pygame.image.load("assets/greennote.png"),
        "screwdriver": pygame.image.load("assets/screwdriver.jpg")
    }

    # Resize all icons
        for key in self.icons:
            self.icons[key] = pygame.transform.scale(self.icons[key], (60, 60))

    def add_item(self, item):
        if item not in self.items:
            self.items.append(item)


    def remove_item(self, item):

        if item in self.items:
            self.items.remove(item)

        if self.selected_item == item:
            self.selected_item = None

    def handle_click(self, pos, screen):
        WIDTH, HEIGHT = screen.get_size()
        y = 90

        for item in self.items:
            rect = pygame.Rect(WIDTH-120, y, 60, 60)

            if rect.collidepoint(pos):
                if self.selected_item == item:
                    self.selected_item = None
                else:
                    self.selected_item = item

            y += 80

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

            rect = pygame.Rect(WIDTH-120, y, 60, 60)

            if self.selected_item == item:
                pygame.draw.rect(screen,(255,255,0),rect,3)

            screen.blit(icon, rect.topleft)

            y += 80