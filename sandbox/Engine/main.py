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
import time
import re
import copy

import threading

string_map_og = [["X","X","X","X","X","X","X","X","X","X"],
              ["X",".",".",".",".",".",".",".",".","X"],
              ["X",".",".",".",".",".",".",".",".","X"],
              ["X",".",".",".",".",".",".",".",".","X"],
              ["X",".",".",".",".",".",".",".",".","X"],
              ["X",".",".",".",".",".",".",".",".","X"],
              ["X",".",".",".",".",".",".",".",".","X"],
              ["X",".",".",".",".",".",".",".",".","X"],
              ["X",".",".",".",".",".",".",".",".","X"],
              ["X","X","X","X","X","X","X","X","X","X"]]


string_map = []

dic_color = {}

WINDOW_HEIGHT = 600.0
WINDOW_WIDTH = 800.0
WINDOW_HEIGHT_INT = int(WINDOW_HEIGHT)
WINDOW_WIDTH_INT = int(WINDOW_WIDTH)
WINDOW_HEIGHT_DEMI = WINDOW_HEIGHT/2
WINDOW_WIDTH_DEMI = WINDOW_WIDTH/2
MAX_DEPTH = 800

player_x = 430
player_y = 430

angle = 45

fov = math.pi / 3
tile_size = 50
number_rays = 31
number_rays_total = number_rays * 4
middle_rays = number_rays_total // 2
rays_factor = number_rays_total/number_rays
angle_step = fov / number_rays

modulo_rays_factor = []
divide_rays_factor = []
for i in range(number_rays_total+1):
    modulo_rays_factor.append(i%rays_factor)
    divide_rays_factor.append(i/rays_factor)


wall_width = WINDOW_WIDTH//number_rays

debug_perspective = False
player_doesnt_move = True
player_click = False

ennemies = []

wall_draw_list = []
ennemy_draw_list = []
ennemy_dict = {}

player_blood = 0

monstre_link = "./image/monstre.png"
weapon_link = "./image/weapon.png"
blood_link = "./image/blood.png"
image_monstre = pygame.image.load(monstre_link)
image_weapon = pygame.image.load(weapon_link)
image_blood = pygame.image.load(blood_link)

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

#inputs
def send_service_rectangle_whiteboard(x,y,longeur,largeur,color,couleur_contour,contour):
    pygame.draw.rect(screen,color,(x,y,longeur,largeur))

def send_service_ellipse_whiteboard(x,y,longeur,largeur,color,couleur_contour,contour):
    pygame.draw.ellipse(screen,color,(x,y,longeur,largeur))

def send_service_image_whiteboard(image,x,y,height,width):
    image = pygame.transform.scale(image, (width, height))
    screen.blit(image, (x,y))

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

def draw_sky_floor_3D():
    send_service_rectangle_whiteboard(0.0,0.0,WINDOW_WIDTH,WINDOW_HEIGHT_DEMI,"blue","grey",0.0)
    send_service_rectangle_whiteboard(0.0,WINDOW_HEIGHT_DEMI,WINDOW_WIDTH,WINDOW_HEIGHT_DEMI,"green","grey",0.0)


def cast_rays_3D():
    global wall_draw_list
    global ennemy_draw_list
    global string_map
    global ennemies
    global player_doesnt_move
    global divide_rays_factor
    global modulo_rays_factor
    global player_click
    start_angle = angle - fov / 2
    wall_height_memory = []
    wall_draw_list = []
    ennemy_draw_list = []
    for ray in range(number_rays_total+1):
        touch_enn = False
        ray_angle = start_angle + ray/rays_factor * angle_step
        ray_angle_cos = math.cos(ray_angle)
        ray_angle_sin = math.sin(ray_angle)
        for depth in range(0,MAX_DEPTH):
            target_x = player_x + depth * ray_angle_cos
            target_y = player_y + depth * ray_angle_sin
 
            grid_x = int(target_x / tile_size)
            grid_y = int(target_y / tile_size)

            if 0 <= grid_x < len(string_map[0]) and 0 <= grid_y < len(string_map):
                if touch_enn == False and string_map[grid_x][grid_y][0] == "E":
                    ennemy_position = ennemy_dict[string_map[grid_x][grid_y]]
                    corrected_depth = depth/5 * math.cos(ray_angle-angle)
                    wall_height = WINDOW_HEIGHT / (corrected_depth + 0.0001)
                    wall_height = 600 if wall_height > 600 else wall_height

                    if ennemy_position[0] - 2 < target_x < ennemy_position[0] + 2 and ennemy_position[1] - 2 < target_y < ennemy_position[1] + 2:
                        touch_enn = True
                        ennemy_draw_list.append((divide_rays_factor[ray],wall_height,string_map[grid_x][grid_y]))
                        if ray == middle_rays and player_click == True:
                            for index,i in enumerate(ennemies):
                                if i[0] - 2 < target_x < i[0] + 2 and i[1] - 2 < target_y < i[1] + 2:
                                    igs.output_set_int("kill",index)
                                    player_click = False


                if modulo_rays_factor[ray] == 0 and string_map[grid_x][grid_y] == "X":
                    corrected_depth = depth/10 * math.cos(ray_angle-angle)
                    wall_height = WINDOW_HEIGHT / (corrected_depth + 0.0001)  
                    wall_height = 600 if wall_height > 600 else wall_height            
                    wall_draw_list.append((divide_rays_factor[ray],wall_height))
                    break
    player_click = False

def draw_3D_world():
    global player_blood
    for wall in wall_draw_list:
        send_service_rectangle_whiteboard(wall[0] * wall_width, (WINDOW_HEIGHT-wall[1])//2,wall_width,wall[1],dic_color[int(wall[1])],"black",1.0)

    ennemy_draw_dict = {}
    ennemy_draw_origin_dict = {}
    for enn in ennemy_draw_list:
        if enn[2] not in ennemy_draw_origin_dict.keys():
            ennemy_draw_origin_dict[enn[2]] = enn[0] 
        ennemy_draw_dict[enn[2]] = (ennemy_draw_origin_dict[enn[2]],enn[1],enn[0])

    for enn in ennemy_draw_dict.values():
        send_service_image_whiteboard(image_monstre,enn[0] * wall_width,(WINDOW_HEIGHT-enn[1])//2,int((enn[2]-enn[0])*wall_width),int(enn[1]))

    send_service_ellipse_whiteboard(WINDOW_WIDTH_DEMI-2,WINDOW_HEIGHT_DEMI-2,5.0,5.0,"red","black",1.0)

    send_service_image_whiteboard(image_weapon,700.0,500.0,100,100)

    if player_blood > 0:
        player_blood -= 1
        send_service_image_whiteboard(image_blood,0,0,WINDOW_HEIGHT_INT,WINDOW_WIDTH_INT)

def place_ennemies_on_grid():
    global string_map
    global ennemy_dict
    string_map = copy.deepcopy(string_map_og)
    ennemy_dict = {}
    for i,o in enumerate(ennemies):
        x = int(o[0]/50)
        y = int(o[1]/50)

        ennemy_dict["E"+str(i)] = o
        if string_map[x][y] == "X":
            igs.output_set_int("kill",i)
        else:
            string_map[x][y] = "E"+str(i)

def update():
    global debug_perspective
    global player_doesnt_move
    if player_doesnt_move == True:
        if debug_perspective == True:
            draw_map_render_2D()
            draw_player_render_2D()
            cast_rays_2D()
            draw_ennemie_render_2D()
        else:
            place_ennemies_on_grid()
            draw_sky_floor_3D()
            cast_rays_3D()
            draw_3D_world()
        player_doesnt_move = False
        pygame.display.update()



def input_callback(iop_type, name, value_type, value, my_data):
    global player_x
    global player_y
    global debug_perspective
    global player_doesnt_move
    global angle
    global player_click
    global ennemies
    global player_blood
    global string_map_og
    global string_map
    global player_x
    global player_y
    if name=="Ennemies":
        player_doesnt_move = True
        if value == "[]":
            ennemies = []
            return
        ennemies = []
        for i in value.split("("):
            if i != "[" and i != "":
                t = i.strip()[:-2].split(",")
                ennemies.append((int(t[0]),int(t[1])))
    elif name=="player_blood":
        player_doesnt_move = True
        player_blood = 5
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
        string_map_og = temp_list
        player_doesnt_move = True
    elif name=="player_x":
        player_x = value
        player_doesnt_move = True
    elif name=="player_y":
        player_y = value
        player_doesnt_move = True

    # add code here if needed

def key_pressed_test():
    global player_x
    global player_y
    global debug_perspective
    global player_doesnt_move
    global angle
    global player_click
    global ennemies
    global player_blood
    global string_map_og
    global string_map
    global player_x
    global player_y
    keys = pygame.key.get_pressed()  # Récupère l'état des touches

    # Mouvements
    if keys[pygame.K_z]:  # Avancer
        player_doesnt_move = True
        player_x += 1 * math.cos(angle)
        player_y += 1 * math.sin(angle)
    if keys[pygame.K_s]:  # Reculer
        player_doesnt_move = True
        player_x -= 1 * math.cos(angle)
        player_y -= 1 * math.sin(angle)
    if keys[pygame.K_q]:  # Gauche
        player_doesnt_move = True
        player_x += 1 * math.cos(angle - math.pi / 2)
        player_y += 1 * math.sin(angle - math.pi / 2)
    if keys[pygame.K_d]:  # Droite
        player_doesnt_move = True
        player_x += 1 * math.cos(angle + math.pi / 2)
        player_y += 1 * math.sin(angle + math.pi / 2)

    # Changer de perspective de débogage
    if keys[pygame.K_p]:
        player_doesnt_move = True
        debug_perspective = not debug_perspective

    # Rotation
    if keys[pygame.K_e]:  # Tourner à droite
        player_doesnt_move = True
        angle = (angle + 0.1) % (2 * math.pi)  # en radians
    if keys[pygame.K_a]:  # Tourner à gauche
        player_doesnt_move = True
        angle -= 0.1
        if angle < 0:
            angle += 2 * math.pi

    # Logique du clic du joueur
    if keys[pygame.K_k]:
        player_click = True
        player_doesnt_move = True

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

    igs.input_create("player_blood",igs.IMPULSION_T, None)
    igs.observe_input("player_blood",input_callback,None)

    igs.input_create("map",igs.STRING_T, None)
    igs.observe_input("map",input_callback,None)

    igs.input_create("player_x",igs.INTEGER_T, None)
    igs.observe_input("player_x",input_callback,None)

    igs.input_create("player_y",igs.INTEGER_T, None)
    igs.observe_input("player_y",input_callback,None)

    igs.output_create("kill", igs.INTEGER_T, None)

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
    while running:
        pygame.event.pump()
        key_pressed_test()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        update()
        clock.tick(144)

    igs.stop()

