import pygame
import math
import random

Warning("Game Version : 0.91")


pygame.init()

font = pygame.font.Font(None, 80)

player_size_dif = 5
# funcs

def PlayLauncher(current_scene):
    current_scene += 1
    print(current_scene)
    return current_scene

def open_save():
    with open("Data/Money.txt", "r") as file:
        saved_value = file.read().strip()
    print("data saved")
    return int(saved_value)


# settings

debug_mode = True
god_mode = False

screen_width, screen_height = 1000, 600
fps = 60
scroll_speed = 1

tile_size = 40
player_speed = 3

enemy_range = tile_size * 9989

# colours
WHITE      = (255, 255, 255)
BLACK      = (0, 0, 0)
BLUE       = (50, 180, 255)
RED        = (255, 60, 60)
GREEN      = (80, 255, 120)
GREY       = (230, 230, 250)
DARK       = (40, 40, 80)
BG_COLOR   = (15, 15, 35)
YELLOW = (255, 255, 0)

colours = [WHITE,BLACK,BLUE,GREEN]


# levels
# # = wall   . = floor   P = player start   E = exit   Y = moving enemy   @ = stationary enemy

# storing levels as arrays and scanning them felt way easier than anything else
levels = [
    [
        "#########################",
        "#########################",
        "-------------------------",
        ".........................",
        ".........................",
        ".........................",
        ".........................",
        ".P......................E",
        ".........................",
        ".........................",
        ".....Y....Y....Y....Y....",
        ".........................",
        "-------------------------",
        "#########################",
        "#########################"
    ],

     [
        "#########################",
        "#########################",
        "-------------------------",
        "-............P..........-.",
        "-.......................-.",
        "-X..........#..@@..@@...-",
        "-...........#...........-",
        "-..X........#.@.@.@.@.@.-",
        "-...........#...........-",
        "-X..........#...........-",
        "-...........#...@@@@@...-",
        "-...........E...........-",
        "-------------------------",
        "#########################",
        "#########################"
    ],

]

# game state

btn_hovered = False
bg_scroll = 0

current_level = 0
scene = "menu"  # menu, name_entry, playing, dead, win, complete
death_count = 0

player_x = 0
player_y = 0
exit_rect = None

# name entry
player_name = ""
name_input = ""

# fading
fade_alpha = 0
fade_speed = 7
fading_out = False
fading_in  = False
fade_next  = None

def start_fade(next_scene):
    global fading_out, fading_in, fade_next, fade_alpha
    fading_out = True
    fading_in  = False
    fade_next  = next_scene
    fade_alpha = 0
    done = True
    return done 



# level functions

def load_level(index):
    global player_x, player_y, enemies, walls, exit_rect

    walls   = []
    enemies = []
    exit_rect = None

    rows = levels[index]
    print(f"loading level {index + 1}")

    for row in range(len(rows)):
        for col in range(len(rows[row])):
            char  = rows[row][col]
            pos_x = col * tile_size
            pos_y = row * tile_size

            if char == "#":
                walls.append(pygame.Rect(pos_x, pos_y, tile_size, tile_size))

            if char == "-":
                walls.append(pygame.Rect(pos_x, pos_y, tile_size, tile_size))

            elif char == "P":
                global spawn_x, spawn_y
                spawn_x  = pos_x
                spawn_y  = pos_y
                player_x = pos_x
                player_y = pos_y

            elif char == "E":
                exit_rect = pygame.Rect(pos_x, pos_y, tile_size, tile_size)

            elif char == "X":
                enemies.append({
                    "speed" : 5,
                    "x"     : pos_x,
                    "y"     : pos_y,
                    "start_x": pos_x,
                    "dir"   : 1,
                    "axis"  : "x",
                    "moves" : True,
                    "colour": RED
                })

            elif char == "Y":
                enemies.append({
                    "speed" : 5,
                    "x"     : pos_x,
                    "y"     : pos_y,
                    "start_x": pos_x,
                    "dir"   : 1,
                    "axis"  : "y",
                    "moves" : True,
                    "colour": RED
                })
            elif char == "S":
                enemies.append({
                    "speed" : 12,
                    "x"     : pos_x,
                    "y"     : pos_y,
                    "start_x": pos_x,
                    "dir"   : 1,
                    "axis"  : "x",
                    "moves" : True,
                    "colour": YELLOW
                })

            elif char == "@":
                enemies.append({
                    "x"     : pos_x,
                    "y"     : pos_y,
                    "start_x": pos_x,
                    "dir"   : 0,
                    "moves" : False,
                    "colour": RED
                })


def move_player(move_x, move_y):
    global player_x, player_y

    player_x += move_x
    player_rect = pygame.Rect(player_x, player_y, tile_size- player_size_dif, tile_size - player_size_dif)
    for wall in walls:
        if player_rect.colliderect(wall):
            if move_x > 0: player_x = wall.left - tile_size
            if move_x < 0: player_x = wall.right

    player_y += move_y
    player_rect = pygame.Rect(player_x, player_y, tile_size - player_size_dif, tile_size - player_size_dif)
    for wall in walls:
        if player_rect.colliderect(wall):
            if move_y > 0: player_y = wall.top - tile_size
            if move_y < 0: player_y = wall.bottom


def move_enemies():
    for enemy in enemies:
        if not enemy["moves"]:
            continue

        if enemy["axis"] == "x":
            enemy["x"] += enemy["speed"] * enemy["dir"]
        else:
            enemy["y"] += enemy["speed"] * enemy["dir"]

        enemy_rect = pygame.Rect(enemy["x"], enemy["y"], tile_size, tile_size)
        hit_wall = False
        for wall in walls:
            if enemy_rect.colliderect(wall):
                hit_wall = True

        if hit_wall:
            if enemy["axis"] == "x":
                enemy["dir"] *= -1
                enemy["x"]   += enemy["speed"] * enemy["dir"] * 2
            else:
                enemy["dir"] *= -1
                enemy["y"]   += enemy["speed"] * enemy["dir"] * 2


def touching_enemy():
    player_rect = pygame.Rect(player_x, player_y, tile_size - player_size_dif, tile_size - player_size_dif)
    for enemy in enemies:   
        if player_rect.colliderect(pygame.Rect(enemy["x"], enemy["y"], tile_size, tile_size)):
            print("hit enemy")
            return True
    return False


def touching_exit():
    player_rect = pygame.Rect(player_x, player_y, tile_size - player_size_dif, tile_size - player_size_dif)
    if exit_rect and player_rect.colliderect(exit_rect):
        print("hit exit")
        return True
    return False


def draw_message(screen, big_font, small_font, title, subtitle):
    w, h = screen.get_size()
    title_surf    = big_font.render(title, True, WHITE)
    subtitle_surf = small_font.render(subtitle, True, WHITE)
    screen.blit(title_surf,    title_surf.get_rect(center=(w // 2, h // 2 - 20)))
    screen.blit(subtitle_surf, subtitle_surf.get_rect(center=(w // 2, h // 2 + 30)))


# setup

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("my game")
clock  = pygame.time.Clock()

bg_image    = pygame.image.load("Assets/BG.png").convert()
title_image = pygame.image.load("Assets/Title.png")
play_image  = pygame.image.load("Assets/Play.png")
play_hover  = pygame.image.load("Assets/Play_hover.png")

# name entry screen images
enter_nickname_image    = pygame.image.load("Assets/Enter_Nickname.png")
entering_nickname_image = pygame.image.load("Assets/Entering_Nickname.png")

bg_width    = bg_image.get_width()
bg_tiles    = math.ceil(screen_width / bg_width) + 1

play_rect    = play_image.get_rect(topleft=(330, 220))
play_current = play_image

font_big   = pygame.font.Font(None, 72)
font_mid   = pygame.font.Font(None, 48)
font_small = pygame.font.Font(None, 36)

fade_surface = pygame.Surface((screen_width, screen_height))
fade_surface.fill(BLACK)

if debug_mode:
    player_speed = int(input("[DEBUG] player speed: "))
    god_mode     = str(input("god mode? Y/N: ")).upper()
    level_pick   = int(input("level: "))
    current_level = level_pick - 1
    scene = "playing" if current_level > 0 else "menu"
    load_level(current_level)
    print(current_level)


# main loop

running = True
while running:
    clock.tick(fps)
    mouse_pos = pygame.mouse.get_pos()

    can_input = not (fading_out or fading_in)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and can_input:
            if scene == "menu" and play_rect.collidepoint(mouse_pos):
                start_fade("name_entry")

        elif event.type == pygame.KEYDOWN and can_input:
            if scene == "name_entry":
                if event.key == pygame.K_RETURN:
                    if name_input.strip() != "":
                        player_name = name_input.strip()
                        print(f"name: {player_name}")
                        load_level(current_level)
                        start_fade("playing")
                    
                elif event.key == pygame.K_BACKSPACE:
                    name_input = name_input[:-1]
                elif len(name_input) < 15:
                    name_input += event.unicode

    # draw scenes

    if scene == "menu":

        if play_rect.collidepoint(mouse_pos) and not btn_hovered:
            btn_hovered = True
            print("hovered play")
        if not play_rect.collidepoint(mouse_pos):
            btn_hovered = False

        play_current = play_hover if btn_hovered else play_image

        bg_scroll -= scroll_speed
        if abs(bg_scroll) > bg_width:
            bg_scroll = 0

        for i in range(bg_tiles):
            screen.blit(bg_image, (i * bg_width + bg_scroll, 0))

        screen.blit(title_image, (170, 50))
        screen.blit(play_current, (330, 220))

    elif scene == "name_entry":

        bg_scroll -= scroll_speed
        if abs(bg_scroll) > bg_width:
            bg_scroll = 0
        for i in range(bg_tiles):
            screen.blit(bg_image, (i * bg_width + bg_scroll, 0))

        dim = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        dim.fill((0, 0, 0, 160))
        screen.blit(dim, (0, 0))

        # swap image depending on whether the player has started typing
        if name_input == "":
            nickname_image = enter_nickname_image
        else:
            nickname_image = entering_nickname_image
        screen.blit(nickname_image, nickname_image.get_rect(center=(screen_width // 2, 200)))

        # typed text + blinking cursor, centred where the box was
        
        input_surf = font_mid.render(name_input, True, BLUE)
        screen.blit(input_surf, input_surf.get_rect(center=(screen_width // 2, (screen_height // 2)  - 100 ) ))


    elif scene == "playing":

        keys = pygame.key.get_pressed()

        move_x = 0
        move_y = 0
        if keys[pygame.K_a]: move_x = -player_speed
        if keys[pygame.K_d]: move_x =  player_speed
        if keys[pygame.K_w]: move_y = -player_speed
        if keys[pygame.K_s]: move_y =  player_speed

        move_player(move_x, move_y)
        move_enemies()

        if touching_enemy() and god_mode != "Y":
    
            
            death_count += 1
            scene = "dead"

        if touching_exit():
            current_level += 1
            if current_level >= len(levels):
                scene = "complete"
            else:
                load_level(current_level)
                print("next level")

        screen.fill(BG_COLOR)

        current_level = min(current_level, len(levels) - 1)
        rows = levels[current_level]

        for row in range(len(rows)):
            for col in range(len(rows[row])):
                char  = rows[row][col]
                pos_x = col * tile_size
                pos_y = row * tile_size
                if char == "#":
                    pygame.draw.rect(screen, DARK,     (pos_x, pos_y, tile_size, tile_size))
                elif char == "E":
                    pygame.draw.rect(screen, GREEN,    (pos_x, pos_y, tile_size, tile_size))
                elif char == "-":
                    pygame.draw.rect(screen, BG_COLOR, (pos_x, pos_y, tile_size, tile_size))
                else:
                    pygame.draw.rect(screen, GREY,     (pos_x, pos_y, tile_size, tile_size))

        for enemy in enemies:
            pygame.draw.rect(screen, enemy["colour"], (enemy["x"], enemy["y"], tile_size, tile_size))

        pygame.draw.rect(screen, BLUE, (player_x, player_y, tile_size - player_size_dif, tile_size - player_size_dif))

        if player_name:
            name_surf = font_mid.render(player_name, True, WHITE)
            screen.blit(name_surf, (10, 10))


            death_suff = font_mid.render(f"Deaths:", True, WHITE)
            death_suff_counter = font_mid.render(str(death_count), True, RED)

            screen.blit(death_suff, (800, 10))
            screen.blit(death_suff_counter, (935, 12))

        if scene == "dead":
            fade_speed = 11 
            start_fade("playing")
            print("dead")
            player_x = spawn_x
            player_y = spawn_y

        if scene == "win":
            print("win")
        if scene == "complete":
            print("complete")

    # fade overlay on top of everything
    if fading_out:
        fade_alpha = min(fade_alpha + fade_speed, 255)
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface, (0, 0))
        if fade_alpha >= 255:
            scene      = fade_next
            fading_out = False
            fading_in  = True

    elif fading_in:
        fade_alpha = max(fade_alpha - fade_speed, 0)
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface, (0, 0))
        if fade_alpha <= 0:
            fading_in = False

    pygame.display.update()

pygame.quit()
