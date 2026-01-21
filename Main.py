import pygame
import time
import math
print("jello world")


# font 
pygame.font.init()
font = pygame.font.Font(None, 80)




pygame.init()


#funcs

def replaceVar(var, newval):
    var = newval
    return var

def PlayLauncher(scene):
    scene += 1
    print(scene)
    return scene

def open_save():
    with open("Data/Money.txt", "r") as file:
        value = file.read().strip()

    print("data saved")
    return int(value)




# Vars



Debug = False

play_Hover = False

# multis


# GAME VARS

money = open_save()


WIDTH, HEIGHT = 1000, 600
FPS = 60
SCROLL_SPEED = 1
cur_scene = 0
if Debug == True:
    cur_scene = int(input("Scence name : "))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player_size = 50
player_x = WIDTH // 2 -300
player_y = HEIGHT // 2
player_speed = 5

player2_size = 50
player2_x = WIDTH // 2 +200
player2_y = HEIGHT // 2
player2_speed = 5

# Load image
bg = pygame.image.load("Assets/BG.png").convert()
title = pygame.image.load("Assets/Title.png")
play = pygame.image.load("Assets/Play.png")
play_img = pygame.image.load("Assets/Play.png")
play_hover_img = pygame.image.load("Assets/Play_hover.png")
bg_width = bg.get_width()
bg_height = bg.get_height()

# giving images rect's

play_rect = play.get_rect(topleft = (330, 220))



tiles = math.ceil(WIDTH / bg_width) + 1

scroll = 0
running = True


while running:
    clock.tick(FPS)
    mousepos = pygame.mouse.get_pos()



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if cur_scene == 0 and play_rect.collidepoint(mousepos):
                cur_scene = PlayLauncher(cur_scene)

            elif cur_scene == 1:
                print("")
            
                
        

        

    scroll -= SCROLL_SPEED

    if cur_scene == 0 :

        
        # detecting hover

        if play_rect.collidepoint(mousepos) and play_Hover == False:
            play_Hover = True
            print("[DEBUG] hovered over play")

        if not play_rect.collidepoint(mousepos):
            play_Hover = False

        if abs(scroll) > bg_width:
            scroll = 0

        for tile in range(tiles):
            screen.blit(bg, (tile * bg_width + scroll, 0))
        screen.blit(title, (170,50))
        screen.blit(play , (330, 220))



        # changing based on hovering 
        play = play_hover_img if play_Hover else play_img
        

        #debug prints
    elif cur_scene == 1:
        screen.fill((0,0,0))


        pygame.draw.rect(
        screen,
        (255, 0, 0),
        (player_x, player_y, player_size, player_size)
    )
        pygame.draw.rect(
        screen,
        (0, 0, 255),
        (player2_x, player2_y, player2_size, player2_size)
    )

        # PLAYER CONTROLS 
        keys = pygame.key.get_pressed()

        
        if keys[pygame.K_a]:
            player_x -= player_speed
        if keys[pygame.K_d]:
            player_x += player_speed
        if keys[pygame.K_w]:
            player_y -= player_speed
        if keys[pygame.K_s]:
            player_y += player_speed


        if keys[pygame.K_LEFT]:
            player2_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player2_x += player_speed
        if keys[pygame.K_UP]:
            player2_y -= player_speed
        if keys[pygame.K_DOWN]:
            player2_y += player_speed


        
        
    


        
    pygame.display.update()

pygame.quit()
