import pygame
import sys

def run_underground(screen, inventory):

    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()

    bg = pygame.image.load("assets/godown.png")
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

    # ---------- HITBOXES (ADJUST) ----------
    hitbox1 = pygame.Rect(300, 180, 120, 300) 
    hitbox2 = pygame.Rect(651, 215, 68, 138)  # collect axe

    axe_collected = False
    show_image = False

    # OPTIONAL IMAGE (later replace)
    replace_img = None

    running = True
    while running:

        screen.blit(bg, (0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                # ---------- HITBOX 1 → RETURN ----------
                if hitbox1.collidepoint(event.pos):
                    return "application"

                # ---------- HITBOX 2 → COLLECT AXE ----------
                if hitbox2.collidepoint(event.pos):

                    if not axe_collected:
                        axe_collected = True
                        inventory.add_item("axe")   # 🔥 important

                        # optional image after click
                        try:
                            replace_img = pygame.image.load("assets/empty.png")
                            replace_img = pygame.transform.scale(replace_img, hitbox2.size)
                            show_image = True
                        except:
                            pass

        # ---------- DRAW ----------
        if show_image and replace_img:
            screen.blit(replace_img, (hitbox2.x, hitbox2.y))

        # DEBUG (remove later)
        # pygame.draw.rect(screen, (255,0,0), hitbox1, 2)
        # pygame.draw.rect(screen, (0,255,0), hitbox2, 2)

        inventory.draw(screen)

        pygame.display.update()
        clock.tick(60)