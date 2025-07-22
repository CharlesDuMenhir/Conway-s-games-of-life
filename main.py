# Source : Tech with Tim


import pygame
import random
import button

pygame.init()

GREY = (128, 128, 128)
WHITE = (255, 255, 255)

WIDTH, HEIGHT = 600, 600
TILE_SIZE = 5
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
FPS = 60

MENU_WIDTH = 200
MENU_LEFT = WIDTH + 10
FONT_SIZE = 40

screen = pygame.display.set_mode((WIDTH + MENU_WIDTH, HEIGHT))

clock = pygame.time.Clock()


font = pygame.font.SysFont("arialblack", FONT_SIZE)
TEXT_COLOR = WHITE

def gen(num):
    return set ([(random.randrange(0, GRID_HEIGHT), random.randrange(0, GRID_WIDTH)) for _ in range(num)])

def draw_grid(positions):
    for position in positions:
        col, row = position
        top_left = (col * TILE_SIZE, row * TILE_SIZE)
        pygame.draw.rect(screen, WHITE, (*top_left, TILE_SIZE, TILE_SIZE)) #*top_left unpack top_left

    for row in range(GRID_HEIGHT):
        pygame.draw.line(screen, GREY,(0, row * TILE_SIZE),(WIDTH, row * TILE_SIZE))

    for col in range(GRID_WIDTH+1):
        pygame.draw.line(screen, GREY,(col * TILE_SIZE, 0),(col * TILE_SIZE, HEIGHT))



def adjust_grid(positions):
    all_neighbors = set()
    new_positions = set()

    for position in positions:
        neighbors = get_neighbors(position)
        all_neighbors.update(neighbors)

        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) in [2, 3]:
            new_positions.add(position)

    for position in all_neighbors:
        neighbors = get_neighbors(position)
        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) == 3:
            new_positions.add(position)

    return new_positions

def get_neighbors(pos):
    x, y = pos
    neighbors = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            neighbors.append(((x+dx)%GRID_WIDTH, (y+dy)%GRID_HEIGHT))
    return neighbors

def createplaneur(positions, x, y):
    if x < WIDTH : # Si dans le jeu
        col = x // TILE_SIZE
        row = y // TILE_SIZE
        pos = (col, row)
        planeurAdd = [(-1, -1), (0, 0), (0, 1), (1, -1), (1, 0)]
        for dpos in planeurAdd:
            positions.add((col + dpos[0],  row + dpos[1]))
        planeurRem = [(-1, 0), (-1, 1), (0, -1), (1, 1)]
        #for dpos in planeurRem:
        #   positions.remove((col + dpos[0],  row + dpos[1]))


def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img,(x, y))


def main():
    running = True
    playing = False
    count = 0
    speed = 1
    update_freq = 60
    
    positions = set()

    button_height = 200
    b_play = button.Button(MENU_LEFT, button_height, 'Play', font)
    button_height += 80
    b_planeur = button.Button(MENU_LEFT, button_height, 'Planeur', font)
    button_height += 80
    b_quit = button.Button(MENU_LEFT, button_height, 'Quit', font)

    menu_buttons = [b_play, b_planeur, b_quit]
    
    while running:
        
        clock.tick(FPS) #Unscale time with PC power 

        if playing:
            count += speed

        if count >= update_freq:
            count = 0
            positions = adjust_grid(positions)

        str_playing = "Playing" if playing else "Paused"
        str_speed = 'x' + str(speed)
        pygame.display.set_caption (str_playing + ' (' + str_speed + ')')

        x, y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN: #ajouter retirer
                
                if x < WIDTH : # Si dans le jeu
                    col = x // TILE_SIZE
                    row = y // TILE_SIZE
                    pos = (col, row)

                    if pos in positions:
                        positions.remove(pos)
                    else:
                        positions.add(pos)

                else : # si dans le menu
                    if b_play.checkForInput((x,y)):
                        playing = not playing
                        b_play.setText("Pause" if playing else "Play")
                    if b_quit.checkForInput((x,y)):
                        running = False
                    if b_planeur.checkForInput((x,y)):
                        creating = True
                        while creating:
                            for event in pygame.event.get():
                                if event.type == pygame.MOUSEBUTTONDOWN: #ajouter retirer
                                    x, y = pygame.mouse.get_pos()
                                    createplaneur(positions, x, y)
                                    creating = False
                    

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = not playing
                    b_play.setText("Pause" if playing else "Play")

                if event.key == pygame.K_c:
                    positions = set()
                    playing = False
                    count = 0

                if event.key == pygame.K_g:
                    positions = gen(random.randrange(8, 16) * GRID_WIDTH)
                    playing = False
                    b_play.setText("Play")

                if event.key == pygame.K_KP_PLUS:
                    if speed < 16:
                        speed *= 2

                if event.key == pygame.K_KP_MINUS:
                    if speed > 1:
                        speed //= 2
                        
        screen.fill("black") #background
        draw_grid(positions)
        for m_button in menu_buttons:
            m_button.update(screen)
            m_button.changeColor((x, y),font)
        pygame.display.update()
        
    pygame.quit()

if __name__ == "__main__":
    main()
