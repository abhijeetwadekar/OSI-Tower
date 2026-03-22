import pygame
import sys

def run_socket_game(screen):

    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()

    background = pygame.image.load("assets/background.png")
    background = pygame.transform.scale(background,(WIDTH,HEIGHT))

    # Colors
    BLACK=(0,0,0)
    WHITE=(255,255,255)
    GRAY=(180,180,180)

    ORANGE=(255,165,0)
    YELLOW=(255,255,0)
    BLACK_DOT=(25,25,25)
    BROWN=(139,69,19)
    WHITE_DOT=(240,240,240)
    PURPLE=(160,32,240)

    node_colors=[
        ORANGE,
        BLACK_DOT,
        BROWN,
        YELLOW,
        WHITE_DOT,
        PURPLE
    ]

    nodes=[
        (205,185),
        (205,255),
        (205,325),
        (595,185),
        (595,255),
        (595,325)
    ]

    correct_pairs=[
        {1,2},
        {4,5},
        {0,3}
    ]

    connections=[]
    selected_node=None
    mouse_pos=None

    message="Connect wires to repair"

    font=pygame.font.SysFont("timesnewroman",28,True)
    button_font=pygame.font.SysFont("timesnewroman",26,True)

    check_button=pygame.Rect(245,400,150,55)
    reset_button=pygame.Rect(405,400,150,55)
    back_button=pygame.Rect(20,20,120,50)   # ✅ FIXED POSITION

    message_box=pygame.Rect(250,20,300,45)

    def draw_nodes():
        for i,pos in enumerate(nodes):
            pygame.draw.circle(screen,node_colors[i],pos,14)

    def draw_connections():
        for a,b in connections:
            pygame.draw.line(screen,node_colors[a],nodes[a],nodes[b],6)

    def draw_drag_wire():
        if selected_node is not None and mouse_pos is not None:
            pygame.draw.line(
                screen,
                node_colors[selected_node],
                nodes[selected_node],
                mouse_pos,
                6
            )

    def draw_buttons():

        # CHECK
        pygame.draw.rect(screen,GRAY,check_button)
        pygame.draw.rect(screen,BLACK,check_button,2)

        # RESET
        pygame.draw.rect(screen,GRAY,reset_button)
        pygame.draw.rect(screen,BLACK,reset_button,2)

        # BACK
        pygame.draw.rect(screen,GRAY,back_button)
        pygame.draw.rect(screen,BLACK,back_button,2)

        check_text=button_font.render("CHECK",True,BLACK)
        reset_text=button_font.render("RESET",True,BLACK)
        back_text=button_font.render("BACK",True,BLACK)

        screen.blit(
            check_text,
            (check_button.x+check_button.width//2-check_text.get_width()//2,
             check_button.y+check_button.height//2-check_text.get_height()//2)
        )

        screen.blit(
            reset_text,
            (reset_button.x+reset_button.width//2-reset_text.get_width()//2,
             reset_button.y+reset_button.height//2-reset_text.get_height()//2)
        )

        screen.blit(
            back_text,
            (back_button.x+back_button.width//2-back_text.get_width()//2,
             back_button.y+back_button.height//2-back_text.get_height()//2)
        )

    def draw_message():
        pygame.draw.rect(screen,WHITE,message_box)
        pygame.draw.rect(screen,BLACK,message_box,2)

        text=font.render(message,True,BLACK)

        screen.blit(
            text,
            (message_box.x+message_box.width//2-text.get_width()//2,
             message_box.y+message_box.height//2-text.get_height()//2)
        )

    def check_solution():
        nonlocal message

        if len(connections)!=3:
            message="Connect all wires first"
            return False

        for pair in connections:
            if set(pair) not in correct_pairs:
                message="Wrong connections"
                return False

        message="Repaired"
        return True

    def reset_wires():
        nonlocal connections,message,selected_node
        connections=[]
        selected_node=None
        message="Connect wires to repair"

    running=True

    while running:

        mouse_pos=pygame.mouse.get_pos()
        screen.blit(background,(0,0))

        for event in pygame.event.get():

            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type==pygame.MOUSEBUTTONDOWN:

                x,y=pygame.mouse.get_pos()

                # NODE CLICK
                for i,pos in enumerate(nodes):

                    if (pos[0]-x)**2+(pos[1]-y)**2<20**2:

                        if selected_node is None:
                            selected_node=i
                        else:
                            if selected_node!=i:

                                connections[:]=[
                                    c for c in connections
                                    if selected_node not in c and i not in c
                                ]

                                connections.append((selected_node,i))

                            selected_node=None

                # CHECK
                if check_button.collidepoint(x,y):
                    if check_solution():
                        pygame.time.delay(300)
                        return True   # ✅ solved

                # RESET
                if reset_button.collidepoint(x,y):
                    reset_wires()

                # BACK
                if back_button.collidepoint(x,y):
                    return False   # ✅ go back

        draw_connections()
        draw_drag_wire()
        draw_nodes()
        draw_buttons()
        draw_message()

        pygame.display.flip()
        clock.tick(60)