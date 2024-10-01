#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  Engine version 1.0
#  Created by Ingenuity i/o on 2024/09/28
#

import sys
import ingescape as igs
import math
import time
import keyboard
import time
import re

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
number_rays_total = 310
number_rays = 31
rays_factor = number_rays_total/number_rays
angle_step = fov / number_rays

wall_width = WINDOW_WIDTH//number_rays

debug_perspective = False
player_doesnt_move = True

ennemies = []

wall_draw_list = []
ennemy_draw_list = []
ennemy_dict = {}

player_blood = 0
ennemie_blood = 0

monstre_link = "./image/test.png"
weapon_link = "./image/weapon.png"
blood_link = "./image/blood.png"

#inputs
def send_service_rectangle_whiteboard(x,y,longeur,largeur,color,couleur_contour,contour):
    arguments_list = ("rectangle",x,y,longeur,largeur,color,couleur_contour,contour)
    igs.service_call("Whiteboard", "addShape", arguments_list, "")

def send_service_ellipse_whiteboard(x,y,longeur,largeur,color,couleur_contour,contour):
    arguments_list = ("ellipse",x,y,longeur,largeur,color,couleur_contour,contour)
    igs.service_call("Whiteboard", "addShape", arguments_list, "")

def send_service_image_whiteboard(url,x,y,height,width):
    arguments_list = ("http://localhost:8000/?url="+url+"&width="+str(width)+"&height="+str(height),x,y)
    igs.service_call("Whiteboard","addImageFromUrl",arguments_list,"")

def clear():
    igs.service_call("Whiteboard","clear",(),"")

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
                        ennemy_draw_list.append((ray/rays_factor,wall_height,string_map[grid_x][grid_y]))
 


                if ray % rays_factor == 0 and string_map[grid_x][grid_y] == "X":
                    corrected_depth = depth/10 * math.cos(ray_angle-angle)
                    wall_height = WINDOW_HEIGHT / (corrected_depth + 0.0001)  
                    wall_height = 600 if wall_height > 600 else wall_height            
                    wall_draw_list.append((ray/rays_factor,wall_height))
                    break
    player_click = False

def draw_3D_world():
    global player_blood
    global ennemie_blood
    for wall in wall_draw_list:
        send_service_rectangle_whiteboard(wall[0] * wall_width, (WINDOW_HEIGHT-wall[1])//2,wall_width,wall[1],dic_color[int(wall[1])],"black",1.0)

    ennemy_draw_dict = {}
    ennemy_draw_origin_dict = {}
    for enn in ennemy_draw_list:
        if enn[2] not in ennemy_draw_origin_dict.keys():
            ennemy_draw_origin_dict[enn[2]] = enn[0] 
        ennemy_draw_dict[enn[2]] = (ennemy_draw_origin_dict[enn[2]],enn[1],enn[0])

    for enn in ennemy_draw_dict.values():
        send_service_image_whiteboard(monstre_link,enn[0] * wall_width,(WINDOW_HEIGHT-enn[1])//2,int((enn[2]-enn[0])*wall_width),int(enn[1]))

    send_service_ellipse_whiteboard(WINDOW_WIDTH_DEMI-2,WINDOW_HEIGHT_DEMI-2,5.0,5.0,"black","black",1.0)

    send_service_image_whiteboard(weapon_link,700.0,500.0,100,100)

    if player_blood > 0:
        player_blood -= 1
        send_service_image_whiteboard(blood_link,0,0,WINDOW_HEIGHT_INT,WINDOW_WIDTH_INT)

def place_ennemies_on_grid():
    global string_map
    string_map = string_map_og
    for i,o in enumerate(ennemies):
        x = int(o[0]/50)
        y = int(o[1]/50)

        ennemy_dict["E"+str(i)] = o
        string_map[x][y] = "E"+str(i)

def update():
    global debug_perspective
    global player_doesnt_move
    if player_doesnt_move == True:
        clear()
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



def input_callback(iop_type, name, value_type, value, my_data):
    global player_x
    global player_y
    global debug_perspective
    global player_doesnt_move
    global angle
    global player_click
    global ennemies
    global player_blood
    global ennemie_blood
    if keyboard.is_pressed('z'):
        player_doesnt_move = True
        player_x += 1 * math.cos(angle)
        player_y += 1 * math.sin(angle)
    if keyboard.is_pressed('s'):
        player_doesnt_move = True
        player_x -= 1 * math.cos(angle)
        player_y -= 1 * math.sin(angle)
    if keyboard.is_pressed('q'):
        player_doesnt_move = True
        player_x += 1 * math.cos(angle - math.pi / 2)
        player_y += 1 * math.sin(angle - math.pi / 2)
    if keyboard.is_pressed('d'):
        player_doesnt_move = True
        player_x += 1 * math.cos(angle + math.pi / 2)
        player_y += 1 * math.sin(angle + math.pi / 2)
    if keyboard.is_pressed('p'):
        player_doesnt_move = True
        if debug_perspective:
            debug_perspective = False
        else:
            debug_perspective = True
    if keyboard.is_pressed('e'):
        player_doesnt_move = True
        angle = (angle + 0.1) % 360
    if keyboard.is_pressed('a'):
        player_doesnt_move = True
        angle -= 0.1
        if angle == 0:
            angle = 359
    if name=="Timer":
        update()
    elif name=="Ennemies":
        player_doesnt_move = True
        ennemies = []
        for i in value.split("("):
            if i != "[" and i != "":
                t = i.strip()[:-2].split(",")
                ennemies.append((int(t[0]),int(t[1])))
    elif name=="player_blood":
        player_doesnt_move = True
        player_blood = 40
    elif name=="ennemie_blood":
        player_doesnt_move = True
        ennemie_blood = 20

    # add code here if needed

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

    igs.input_create("Timer", igs.IMPULSION_T, None)
    igs.observe_input("Timer", input_callback, None)

    igs.input_create("Ennemies",igs.STRING_T, None)
    igs.observe_input("Ennemies",input_callback,None)

    igs.input_create("player_blood",igs.IMPULSION_T, None)
    igs.observe_input("player_blood",input_callback,None)


    igs.input_create("ennemies_blood",igs.IMPULSION_T, None)
    igs.observe_input("ennemies_blood",input_callback,None)

    igs.start_with_device(sys.argv[2], int(sys.argv[3]))

    for i in range(int(WINDOW_HEIGHT)+1):
        if len(str(hex(int(i*255/600))[2:])) != 2: 
            dic_color[i] = "#"+("0"+str(hex(int(i*255/600))[2:]))*3
        else: 
            dic_color[i] = "#"+str(hex(int(i*255/600))[2:])*3

    input()

    igs.stop()

