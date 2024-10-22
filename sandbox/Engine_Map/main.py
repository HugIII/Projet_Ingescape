#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  Engine_Map version 1.0
#  Created by Ingenuity i/o on 2024/10/03
#

import sys
import ingescape as igs

import threading
import time

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

WINDOW_HEIGHT = 600.0
WINDOW_WIDTH = 800.0
WINDOW_HEIGHT_DEMI = WINDOW_HEIGHT/2
WINDOW_WIDTH_DEMI = WINDOW_WIDTH/2

player_x = 430
player_y = 430

ennemies = []
other_player = []

wall_index = []
player_index = []
other_player_index = []
ennemies_index = []

index = 0

def start():
    while True:
        time.sleep(0.1)
        clear()
        draw_map_render_2D()
        time.sleep(0.1)
        draw_player_render_2D()
        time.sleep(0.1)
        draw_ennemie_render_2D()
        time.sleep(0.1)
        draw_other_player_render_2D()

#inputs
def send_service_rectangle_whiteboard(x,y,longeur,largeur,color,couleur_contour,contour):
    arguments_list = ("rectangle",x,y,longeur,largeur,color,couleur_contour,contour)
    igs.service_call("Whiteboard", "addShape", arguments_list, "")

def send_service_ellipse_whiteboard(x,y,longeur,largeur,color,couleur_contour,contour):
    arguments_list = ("ellipse",x,y,longeur,largeur,color,couleur_contour,contour)
    igs.service_call("Whiteboard", "addShape", arguments_list, "")

def clear():
    igs.service_call("Whiteboard","clear",(),"")

def remove_id(index):
    arguments_list = (index)
    igs.service_call("Whiteboard","remove",arguments_list,"")

def draw_map_render_2D():
    for i in range(len(string_map)):
        for j in range(len(string_map[i])):
            if string_map[i][j] == "X":
                send_service_rectangle_whiteboard(50.0*i,50.0*j,50.0,50.0,"black","grey",1.0)

def draw_player_render_2D():
    send_service_ellipse_whiteboard(player_x-10.0,player_y-10.0,20.0,20.0,"red","black",1.0)

def draw_ennemie_render_2D():
    for i in ennemies:
        send_service_ellipse_whiteboard(i[0]-10.0,i[1]-10.0,20.0,20.0,"purple","black",1.0)

def draw_other_player_render_2D():   
    for i in other_player:
        send_service_ellipse_whiteboard(i[0]-10.0,i[1]-10.0,20.0,20.0,"yellow","black",1.0)

def input_callback(iop_type, name, value_type, value, my_data):
    global player_x
    global player_y
    global string_map
    global ennemies
    global other_player

    if name=="player_x":
        player_x = value
    elif name == "player_y":
        player_y = value
    elif name == "map":
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
    elif name == "list_ennemies":
        if value == "[]":
            ennemies = []
            return
        ennemies = []
        for i in value.split("("):
            if i != "[" and i != "":
                t = i.strip()[:-2].split(",")
                ennemies.append((int(t[0]),int(t[1])))
    elif name=="list_other_player":
        if value == "[]":
            other_player = []
            return
        other_player = []
        for i in value.split("("):
            if i != "[" and i != "":
                t = i.strip()[:-2].split(",")
                other_player.append((int(t[0]),int(t[1])))
    elif name=="list_ennemies_move":
        if value == "[]":
            ennemies = []
            return
        ennemies = []
        for i in value.split("("):
            if i != "[" and i != "":
                t = i.strip()[:-2].split(",")
                ennemies.append((int(t[0]),int(t[1])))

if __name__ == "__main__":
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

    igs.input_create("player_x", igs.INTEGER_T, None)
    igs.input_create("player_y", igs.INTEGER_T, None)
    igs.input_create("map", igs.STRING_T, None)
    igs.input_create("list_ennemies", igs.STRING_T, None)
    igs.input_create("list_other_player", igs.STRING_T, None)
    igs.input_create("list_ennemies_move",igs.STRING_T,None)

    igs.observe_input("player_x", input_callback, None)
    igs.observe_input("player_y", input_callback, None)
    igs.observe_input("map", input_callback, None)
    igs.observe_input("list_ennemies", input_callback, None)
    igs.observe_input("list_other_player", input_callback, None)
    igs.observe_input("list_ennemies_move",input_callback,None)

    igs.start_with_device(sys.argv[2], int(sys.argv[3]))

    thread = threading.Thread(target=start)
    thread.start()

    input()

    igs.stop()

