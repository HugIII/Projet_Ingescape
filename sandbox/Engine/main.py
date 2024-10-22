#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  Engine version 1.0
#  Created by Ingenuity i/o on 2024/09/28
#

import pygame
import sys
import ingescape as igs
import math
import time
import re
import copy
import threading
import moviepy.editor

string_map = [["X","X","X","X","X","X","X","X","X","X"],
              ["X",".",".",".",".",".",".",".",".","X"],
              ["X",".",".",".",".",".",".",".",".","X"],
              ["X",".",".",".",".",".",".",".",".","X"],
              ["X",".",".",".",".",".",".",".",".","X"],
              ["X",".",".",".",".",".",".",".",".","X"],
              ["X",".",".",".",".",".",".",".",".","X"],
              ["X",".",".",".",".",".",".",".",".","X"],
              ["X",".",".",".",".",".",".",".",".","X"],
              ["X","X","X","X","X","X","X","X","X","X"]]


dic_color = {}

WINDOW_HEIGHT = 780.0
WINDOW_WIDTH = 1280.0
WINDOW_HEIGHT_INT = int(WINDOW_HEIGHT)
WINDOW_WIDTH_INT = int(WINDOW_WIDTH)
WINDOW_HEIGHT_DEMI = WINDOW_HEIGHT/2
WINDOW_WIDTH_DEMI = WINDOW_WIDTH/2
MAX_DEPTH = 800

player_x = 430
player_y = 430

angle = 45

fov = math.pi / 3
number_rays = 142
tile_size = 50
middle_rays = number_rays / 2
angle_step = float(fov / number_rays)

wall_width = WINDOW_WIDTH//number_rays

debug_perspective = False
player_click_left = False
player_click_right = False
lock_ennemi_kill = True

ennemies = []
ennemies_move = []
player_enn = []

wall_draw_list = []
ennemy_draw_list = []
player_enn_draw_list = []
ennemy_dict = {}
player_enn_dict = {}

monstre_link = ["./image/monstre1.png","./image/monstre2.png","./image/monstre3.png"]
player_link = "./image/other_player.png"
weapon_link = "./image/weapon.png"
sky_link = "./image/sky.png"
cursor_link = "./image/cursor.png"
scratch_link = ["./image/scratch1.png","./image/scratch2.png","./image/scratch3.png"]

image_monstre = []
for i in monstre_link:
    image_monstre.append(pygame.image.load(i))

image_weapon = pygame.image.load(weapon_link)
image_player = pygame.image.load(player_link)
image_sky = pygame.image.load(sky_link)
image_cursor = pygame.image.load(cursor_link)

image_scratch = []
for i in scratch_link:
    image_scratch.append(pygame.image.load(i))

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

wave = 1
wave_bool = False
cursor_cooldown = 0

arrow_left = 0
vie = 100

#inputs
def send_service_rectangle_whiteboard(x,y,longeur,largeur,color,couleur_contour,contour):
    pygame.draw.rect(screen,color,(x,y,longeur,largeur))

def send_service_ellipse_whiteboard(x,y,longeur,largeur,color,couleur_contour,contour):
    pygame.draw.ellipse(screen,color,(x,y,longeur,largeur))

def send_service_image_whiteboard(image,x,y,height,width):
    if width <= 0 or height <= 0:
        return
    image = pygame.transform.scale(image, (width, height))
    screen.blit(image, (x,y))

def send_service_text(x,y,text):
    text_color = (255, 0, 0)
    font = pygame.font.Font(None, 38)
    text = font.render(text, True, text_color)
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)

def draw_map_render_2D():
    for i in range(len(string_map)):
        for j in range(len(string_map[i])):
            if string_map[i][j] == "X":
                send_service_rectangle_whiteboard(50.0*i,50.0*j,50.0,50.0,"black","grey",1.0)

def cast_rays_2D():
    ray_angle = angle - fov/2
    for i in range(int(fov/angle_step)):
        for depth in range(MAX_DEPTH):
            target_x = player_x + depth * math.cos(ray_angle)
            target_y = player_y + depth * math.sin(ray_angle)

            grid_x = int(target_x / tile_size)
            grid_y = int(target_y / tile_size)

            if 0 <= grid_x < len(string_map[0]) and 0 <= grid_y < len(string_map):
                if string_map[grid_x][grid_y] == "X":
                    send_service_ellipse_whiteboard(target_x-10.0,target_y-10.0,20.0,20.0,"green","black",1.0)
                    break
        ray_angle += angle_step

def draw_player_render_2D():
    send_service_ellipse_whiteboard(player_x-10.0,player_y-10.0,20.0,20.0,"red","black",1.0)

def draw_ennemie_render_2D():
    for i in ennemies:
        send_service_ellipse_whiteboard(i[0]-10.0,i[1]-10.0,20.0,20.0,"purple","black",1.0)
    for i in ennemies_move:
        send_service_ellipse_whiteboard(i[0]-10.0,i[1]-10.0,20.0,20.0,"blue","black",1.0)
    for i in player_enn:
        send_service_ellipse_whiteboard(i[0]-10.0,i[1]-10.0,20.0,20.0,"yellow","black",1.0)


def draw_sky_floor_3D():
    send_service_image_whiteboard(image_sky,0,0,WINDOW_HEIGHT_INT-200,WINDOW_WIDTH_INT)
    send_service_rectangle_whiteboard(0.0,WINDOW_HEIGHT_DEMI,WINDOW_WIDTH,WINDOW_HEIGHT_DEMI,"#655e5c","grey",0.0)

def cast_rays_3D():
    global wall_draw_list
    global ennemy_draw_list
    global player_enn_draw_list
    global string_map
    global ennemies
    global player_enn
    global player_click_left
    global player_click_right
    global lock_ennemi_kill
    global ennemies_move

    start_angle = angle - fov / 2
    wall_height_memory = []
    wall_draw_list = []
    ennemy_draw_list = []
    player_enn_draw_list = []
    degat = 0

    string_map_temp = []
    for i in range(len(string_map)):
        string_map_temp.append([])
        for j in range(len(string_map[i])):
            if string_map[i][j] == ".":
                string_map_temp[i].append([])
            else:
                string_map_temp[i].append(string_map[i][j])

    if len(ennemies_move) == 0:
        for index,i in enumerate(ennemies):
            grid_x = int(i[0]/tile_size)
            grid_y = int(i[1]/tile_size)
            if not isinstance(string_map_temp[grid_x][grid_y],str):
                string_map_temp[grid_x][grid_y].append(str(index))
    else:
        for index,i in enumerate(ennemies_move):
            grid_x = int(i[0]/tile_size)
            grid_y = int(i[1]/tile_size)
            if not isinstance(string_map_temp[grid_x][grid_y],str):
                string_map_temp[grid_x][grid_y].append(str(index))

    for index,i in enumerate(player_enn):
        grid_x = int(i[0]/tile_size)
        grid_y = int(i[1]/tile_size)
        if not isinstance(string_map_temp[grid_x][grid_y],str):
            string_map_temp[grid_x][grid_y].append("P"+str(index))

    for ray in range(-50,number_rays+51):
        touch_enn = False
        touch_player = False
        ray_angle = start_angle + ray * angle_step
        ray_angle_cos = math.cos(ray_angle)
        ray_angle_sin = math.sin(ray_angle)
        for depth in range(0,MAX_DEPTH):
            target_x = player_x + depth * ray_angle_cos
            target_y = player_y + depth * ray_angle_sin
 
            grid_x = int(target_x / tile_size)
            grid_y = int(target_y / tile_size)

            if 0 <= grid_x < len(string_map[0]) and 0 <= grid_y < len(string_map):
                if string_map[grid_x][grid_y] == "X":
                    corrected_depth = depth/10 * math.cos(ray_angle-angle)
                    wall_height = WINDOW_HEIGHT / (corrected_depth + 0.0001)  
                    wall_height = 600 if wall_height > 600 else wall_height            
                    wall_draw_list.append((ray,wall_height))
                    break

                if depth > 300:
                    continue

                if isinstance(string_map_temp[grid_x][grid_y],list):
                    list_case = string_map_temp[grid_x][grid_y]
                    for i in list_case:
                        if i[0] == "P":
                            continue
                        try:
                            if(len(ennemies_move)==0):
                                ennemies_position = ennemies[int(i)]
                            else:
                                ennemies_position = ennemies_move[int(i)]
                        except:
                            continue
                        if touch_enn == False and ennemies_position[0] - 2 < target_x < ennemies_position[0] + 2 and ennemies_position[1] - 2 < target_y < ennemies_position[1] + 2:
                            corrected_depth = depth/5 * math.cos(ray_angle-angle)
                            wall_height = WINDOW_HEIGHT / (corrected_depth + 0.0001)
                            wall_height = 600 if wall_height > 600 else wall_height
                            ennemy_draw_list.append((ray,wall_height,i,ennemies_position[0],ennemies_position[1]))
                            touch_enn = True
                            degat += 0.5 * depth #mettre logarithmique

                            if middle_rays - 3 <= ray <= middle_rays + 3 and (player_click_left == True or (player_click_right == True and depth < 75)) and lock_ennemi_kill == True:
                                if ennemies_position[0] - 2 < target_x < ennemies_position[0] + 2 and ennemies_position[1] - 2 < target_y < ennemies_position[1] + 2:
                                    lock_ennemi_kill = False
                                    igs.output_set_int("kill",int(i))

                if isinstance(string_map_temp[grid_x][grid_y],list):
                    list_case = string_map_temp[grid_x][grid_y]
                    for i in list_case:
                        if i[0] != "P":
                            continue
                        player_enn_position = player_enn[int(i[1:])]
                        if touch_player == False and player_enn_position[0] - 2 < target_x < player_enn_position[0] + 2 and player_enn_position[1] - 2 < target_y < player_enn_position[1] + 2:
                            corrected_depth = depth/5 * math.cos(ray_angle-angle)
                            wall_height = WINDOW_HEIGHT / (corrected_depth + 0.0001)
                            wall_height = 600 if wall_height > 600 else wall_height
                            player_enn_draw_list.append((ray,wall_height,i))
                            touch_player = True

                            if middle_rays - 3 <= ray <= middle_rays + 3 and (player_click_left == True or (player_click_right == True and depth < 75)):
                                if player_enn_position[0] - 2 < target_x < player_enn_position[0] + 2 and player_enn_position[1] - 2 < target_y < player_enn_position[1] + 2:
                                    igs.output_set_int("kill_player",int(i[1:]))

    igs.output_set_double("degat",degat)
    player_click_left = False
    player_click_right = False

def draw_3D_world():
    global cursor_cooldown
    for wall in wall_draw_list:
        send_service_rectangle_whiteboard(wall[0] * wall_width, (WINDOW_HEIGHT-wall[1])//2,wall_width,wall[1],dic_color[int(wall[1])],"black",1.0)

    ennemy_draw_dict = {}
    ennemy_draw_origin_dict = {}
    for enn in ennemy_draw_list:
        if enn[2] not in ennemy_draw_origin_dict.keys():
            ennemy_draw_origin_dict[enn[2]] = enn[0] 
        ennemy_draw_dict[enn[2]] = (ennemy_draw_origin_dict[enn[2]],enn[1],enn[0],enn[3],enn[4],enn[2])

    player_enn_draw_dict = {}
    player_enn_draw_origin_dict = {}
    for pla in player_enn_draw_list:
        if pla[2] not in player_enn_draw_origin_dict.keys():
            player_enn_draw_origin_dict[pla[2]] = pla[0] 
        player_enn_draw_dict[pla[2]] = (player_enn_draw_origin_dict[pla[2]],pla[1],pla[0])

    for enn in ennemy_draw_dict.values():
        try:
            index = (ennemies[int(enn[5])][0]+ennemies[int(enn[5])][1])%len(image_monstre)
            send_service_image_whiteboard(image_monstre[index],enn[0] * wall_width,(WINDOW_HEIGHT-enn[1])//2,int((enn[2]-enn[0])*wall_width),int(enn[1]))
        except:
            pass
    for pla in player_enn_draw_dict.values():
        send_service_image_whiteboard(image_player,pla[0] * wall_width,(WINDOW_HEIGHT-pla[1])//2,int((pla[2]-pla[0])*wall_width),int(pla[1]))

    if cursor_cooldown != 0:
        cursor_cooldown -= 1
        send_service_image_whiteboard(image_cursor,WINDOW_WIDTH_DEMI-15,WINDOW_HEIGHT_DEMI-15,30.0,30.0)
    else:
        send_service_ellipse_whiteboard(WINDOW_WIDTH_DEMI-2,WINDOW_HEIGHT_DEMI-2,5.0,5.0,"red","black",1.0)

    send_service_image_whiteboard(image_weapon,WINDOW_WIDTH-500,0,WINDOW_HEIGHT,500)

    send_service_text(50,50,"  life: "+str(vie))
    send_service_text(50,75,"  arrow: "+str(arrow_left))
    if wave_bool == True:
        send_service_text(50,100,"  wave: "+str(wave))
    
    if vie < 75:
        send_service_image_whiteboard(image_scratch[0],800,0,300,300)
        if vie < 60:
            send_service_image_whiteboard(image_scratch[1],200,400,300,300)
            if vie < 30:
                send_service_image_whiteboard(image_scratch[2],0,0,WINDOW_HEIGHT_INT,WINDOW_WIDTH)

def update():
    global debug_perspective
    if debug_perspective == True:
        draw_map_render_2D()
        draw_player_render_2D()
        cast_rays_2D()
        draw_ennemie_render_2D()
    else:
        draw_sky_floor_3D()
        cast_rays_3D()
        draw_3D_world()
    pygame.display.update()



def input_callback(iop_type, name, value_type, value, my_data):
    global player_x
    global player_y
    global debug_perspective
    global angle
    global player_click_left
    global player_click_right
    global ennemies
    global player_enn
    global string_map
    global player_x
    global player_y
    global lock_ennemi_kill
    global wave
    global wave_bool
    global arrow_left
    global ennemies_move

    if name=="Ennemies":
        if value == "[]":
            ennemies = []
            return
        ennemies = []
        for i in value.split("("):
            if i != "[" and i != "":
                t = i.strip()[:-2].split(",")
                ennemies.append((int(t[0]),int(t[1])))
        lock_ennemi_kill = True
    if name=="other_player":
        if value == "[]":
            player_enn = []
            return
        player_enn = []
        for i in value.split("("):
            if i != "[" and i != "":
                t = i.strip()[:-2].split(",")
                player_enn.append((int(t[0]),int(t[1])))
    elif name=="map":
        temp_list = []
        temp_sub_list = []
        for i in range(len(value)):
            if value[i] == "R":
                temp_list.append(temp_sub_list)
                temp_sub_list = []
            else:
                temp_sub_list.append(value[i])
        temp_list.append(temp_sub_list)
        string_map = temp_list
    elif name=="player_x":
        player_x = value
    elif name=="player_y":
        player_y = value
    elif name=="wave":
        wave_bool = True
        wave = value
    elif name=="arbalete_shot":
        player_click_left = True
        cursor_cooldown = 15
    elif name=="sword_hit":
        player_click_right = True
        cursor_cooldown = 15
    elif name=="arrow_left":
        arrow_left = value
    elif name=="Ennemies_move":
        if value == "[]":
            ennemies_move = []
            return
        ennemies_move = []
        for i in value.split("("):
            if i != "[" and i != "":
                t = i.strip()[:-2].split(",")
                ennemies_move.append((int(t[0]),int(t[1])))
        lock_ennemi_kill = True
    # add code here if needed

def key_pressed_test():
    global player_x
    global player_y
    global debug_perspective
    global angle
    global string_map
    global cursor_cooldown

    keys = pygame.key.get_pressed()  # Récupère l'état des touches

    # Mouvements
    if keys[pygame.K_z]:  # Avancer
        player_x += 1 * math.cos(angle)
        player_y += 1 * math.sin(angle)
    if keys[pygame.K_s]:  # Reculer
        player_x -= 1 * math.cos(angle)
        player_y -= 1 * math.sin(angle)
    if keys[pygame.K_q]:  # Gauche
        player_x += 1 * math.cos(angle - math.pi / 2)
        player_y += 1 * math.sin(angle - math.pi / 2)
    if keys[pygame.K_d]:  # Droite
        player_x += 1 * math.cos(angle + math.pi / 2)
        player_y += 1 * math.sin(angle + math.pi / 2)

    # Changer de perspective de débogage
    if keys[pygame.K_p]:
        debug_perspective = not debug_perspective

    # Rotation
    if keys[pygame.K_e]:  # Tourner à droite
        angle = (angle + 0.1) % (2 * math.pi)  # en radians
    if keys[pygame.K_a]:  # Tourner à gauche
        angle -= 0.1
        if angle < 0:
            angle += 2 * math.pi

if __name__=="__main__":
    if len(sys.argv) < 4:
        print("usage: python3 main.py agent_name network_device port")
        devices = igs.net_devices_list()
        print("Please restart with one of these devices as network_device argument:")
        for device in devices:
            print(f" {device}")
        exit(0)

    igs.agent_set_name(sys.argv[1])
    igs.definition_set_version("1.0")
    igs.log_set_console(True)
    igs.log_set_file(True, None)
    igs.set_command_line(sys.executable + " " + " ".join(sys.argv))

    igs.input_create("Ennemies",igs.STRING_T, None)
    igs.observe_input("Ennemies",input_callback,None)

    igs.input_create("other_player",igs.STRING_T, None)
    igs.observe_input("other_player",input_callback,None)

    igs.input_create("player_blood",igs.IMPULSION_T, None)
    igs.observe_input("player_blood",input_callback,None)

    igs.input_create("map",igs.STRING_T, None)
    igs.observe_input("map",input_callback,None)

    igs.input_create("player_x",igs.INTEGER_T, None)
    igs.observe_input("player_x",input_callback,None)

    igs.input_create("player_y",igs.INTEGER_T, None)
    igs.observe_input("player_y",input_callback,None)

    igs.input_create("wave",igs.INTEGER_T,None)
    igs.observe_input("wave",input_callback,None)

    igs.input_create("arbalete_shot",igs.IMPULSION_T,None)
    igs.observe_input("arbalete_shot",input_callback,None)

    igs.input_create("sword_hit",igs.IMPULSION_T,None)
    igs.observe_input("sword_hit",input_callback,None)

    igs.input_create("arrow_left",igs.INTEGER_T,None)
    igs.observe_input("arrow_left",input_callback,None)

    igs.input_create("vie",igs.INTEGER_T,None)
    igs.observe_input("vie",input_callback,None)

    igs.input_create("Ennemies_move",igs.STRING_T,None)
    igs.observe_input("Ennemies_move",input_callback,None)

    igs.output_create("kill", igs.INTEGER_T, None)
    igs.output_create("kill_player", igs.INTEGER_T, None)
    igs.output_create("degat", igs.DOUBLE_T, None)

    igs.start_with_device(sys.argv[2], int(sys.argv[3]))
    
    pygame.init()
    pygame.display.set_caption("DPPM")

    thread = threading.Thread(target=input)
    thread.start()

    for i in range(int(WINDOW_HEIGHT)+1):
        if len(str(hex(int(i*255/600))[2:])) != 2: 
            dic_color[i] = "#"+("0"+str(hex(int(i*255/600))[2:]))*3
        else: 
            dic_color[i] = "#"+str(hex(int(i*255/600))[2:])*3

    running = True
    clock = pygame.time.Clock()

    video = moviepy.editor.VideoFileClip("./cinematics/intro.mp4")
    #video.preview()

    while running:
        pygame.event.pump()
        key_pressed_test()
        if wave > 15:
            running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        update()
        clock.tick(144)

    if wave > 15:
        video = moviepy.editor.VideoFileClip("./cinematics/Outro.mp4")
        video.preview()

    igs.stop()

    print("test")

    pygame.quit()

    exit()
