import pygame
import sys

def run_physical_layer(screen, inventory):

    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()

    # ---------- LOAD IMAGES ----------

    terrace_closed = pygame.image.load("assets/terrace.png")
    terrace_closed = pygame.transform.scale(terrace_closed, (WIDTH, HEIGHT))

    terrace_open = pygame.image.load("assets/hole.png")
    terrace_open = pygame.transform.scale(terrace_open, (WIDTH, HEIGHT))

    cable_img = pygame.image.load("assets/wire.png")
    cable_img = pygame.transform.scale(cable_img, (70,70))

    # ---------- COLORS ----------

    WHITE = (255,255,255)
    BOX = (40,40,40)
    HOVER = (255,255,0)

    font = pygame.font.SysFont("Times New Roman", 28)

    # ---------- GAME STATE ----------

    has_cable = False
    hatch_open = False

    hint_text = "Find a cable to go down."

    # ---------- INTERACTION AREAS ----------

    cable_rect = pygame.Rect(350,520,160,120)
    toolbox_rect = pygame.Rect(100,500,160,120)
    hatch_rect = pygame.Rect(520,380,240,180)

    running = True

    while running:

        mouse = pygame.mouse.get_pos()

        # ---------- BACKGROUND ----------

        if hatch_open:
            screen.blit(terrace_open,(0,0))
        else:
            screen.blit(terrace_closed,(0,0))

        # ---------- HINT BOX ----------

        hint_box = pygame.Rect(WIDTH//2-300,20,600,60)

        pygame.draw.rect(screen, BOX, hint_box)
        pygame.draw.rect(screen, WHITE, hint_box, 2)

        text = font.render(hint_text, True, WHITE)
        screen.blit(text, text.get_rect(center=hint_box.center))

        # ---------- INVENTORY ----------

        inventory.draw(screen)

        # ---------- DRAW CABLE IF NOT COLLECTED ----------

        if not has_cable:
            screen.blit(cable_img, (360,540))

        # ---------- HOVER EFFECTS ----------

        if not has_cable and cable_rect.collidepoint(mouse):
            pygame.draw.rect(screen, HOVER, cable_rect, 3)

        if toolbox_rect.collidepoint(mouse):
            pygame.draw.rect(screen, (0,255,255), toolbox_rect, 3)

        if hatch_rect.collidepoint(mouse):
            pygame.draw.rect(screen, (255,100,100), hatch_rect, 3)

        pygame.display.update()
        clock.tick(60)

        # ---------- EVENTS ----------

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                # PICK CABLE
                if cable_rect.collidepoint(event.pos) and not has_cable:

                    has_cable = True
                    inventory.add_item("cable")

                    hint_text = "You picked up a network cable."

                # TOOLBOX HINT
                elif toolbox_rect.collidepoint(event.pos):

                    hint_text = "Hint: Signals require a physical medium."

                # HATCH INTERACTION
                elif hatch_rect.collidepoint(event.pos):

                    if has_cable and not hatch_open:

                        hatch_open = True
                        hint_text = "You attach the cable. The hatch opens."

                    elif hatch_open:

                        hint_text = "You climb down to the next layer."
                        running = False