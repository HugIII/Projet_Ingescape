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
from PIL import Image, ImageDraw
import http.server
import socketserver

PORT = 8000

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
ennemies_move = []
other_player = []

wall_index = []
player_index = []
other_player_index = []
ennemies_index = []

index = 0

image = Image.new('RGB', (1500,1500),'white')
draw = ImageDraw.Draw(image)

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/download":
            image_path = "./image/map.png"
            self.send_response(200)
            self.send_header('Content-type', 'application/octet-stream')
            self.send_header('Content-Disposition', f'attachment; filename="{image_path}"')
            self.end_headers()
            with open(image_path, 'rb') as file:
                self.wfile.write(file.read())

def start_image_server():
    with socketserver.TCPServer(("",PORT),CustomHandler) as httpd:
        httpd.serve_forever()

def start():
    global image
    global draw
    global index

    while True:
        time.sleep(1)
        image = Image.new('RGB', (1500,1500),'white')
        draw = ImageDraw.Draw(image)
        draw_map_render_2D()
        draw_player_render_2D()
        draw_ennemie_render_2D()
        draw_other_player_render_2D()
        image.save("./image/map.png")
        arguments_list = ("http://localhost:8000/download",50.0,50.0)
        igs.service_call("Whiteboard","addImageFromUrl",arguments_list,"")

#inputs
def send_service_rectangle_whiteboard(x,y,longeur,largeur,color,couleur_contour,contour):
    global draw
    draw.rectangle([(int(x),int(y)),(int(x+longeur),int(y+largeur))],fill=color,outline=couleur_contour,width=int(contour))

def send_service_ellipse_whiteboard(x,y,longeur,largeur,color,couleur_contour,contour):
    global draw
    draw.ellipse([(int(x-longeur/2),int(y-largeur/2)),(int(x+longeur/2),int(y+largeur/2))],fill=color,outline=couleur_contour,width=int(contour))

def clear():
    global image
    global draw
    igs.service_call("Whiteboard","clear",(),"")
    image = Image.new('RGB', (1500,1500),'white')
    draw = ImageDraw.Draw(image)


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
    if len(ennemies_move) == 0:
        for i in ennemies:
            send_service_ellipse_whiteboard(i[0]-10.0,i[1]-10.0,20.0,20.0,"purple","black",1.0)
    else:
        for i in ennemies_move:
            send_service_ellipse_whiteboard(i[0]-10.0,i[1]-10.0,20.0,20.0,"purple","black",1.0)

def draw_other_player_render_2D():   
    for i in other_player:
        send_service_ellipse_whiteboard(i[0]-10.0,i[1]-10.0,20.0,20.0,"yellow","black",1.0)

def input_callback(iop_type, name, value_type, value, my_data):
    global player_x
    global player_y
    global string_map
    global ennemies
    global ennemies_move
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
            ennemies_move = []
            return
        ennemies_move = []
        for i in value.split("("):
            if i != "[" and i != "":
                t = i.strip()[:-2].split(",")
                ennemies_move.append((int(t[0]),int(t[1])))

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

    igs.output_create("score_reprint",igs.IMPULSION_T, None)

    igs.start_with_device(sys.argv[2], int(sys.argv[3]))

    thread = threading.Thread(target=start)
    thread.start()

    thread_server = threading.Thread(target=start_image_server)
    thread_server.start()

    input()

    igs.stop()

