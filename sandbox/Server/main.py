#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  Server
#  Created by BAFFOGNE Clara,BLAYES Hugo on 2024/10/22
#  Created by Ingenuity i/o on 2024/10/22
#  Description:
#   Server du mode multi
#   En multi, le serveur s'occupe d'envoyer les informations au whiteboard
#   De ce fait, cet agent heberge un server image afin que le whiteboard puisse recuperer la map

import sys
import ingescape as igs
import random
import time
import threading
from PIL import Image, ImageDraw
import http.server
import socketserver

# constante ############################################
PORT = 8000

# variable ##############################################
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

list_ennemies = []
index_dict = {}
score = {}

# Classe ################################################

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

# fonction ##############################################
def life_fun():
    # on envoie la liste d'ennemie et la liste player de maniere periodique
    while True:
        temp_list = []
        for i in index_dict.keys():
            li = index_dict[i]
            temp_list.append((i,li[0],li[1]))
        for i in index_dict.keys():
            arguments_list = (str(list_ennemies))
            igs.service_call("Client_Server_"+str(i),"change_liste_ennemies",arguments_list,"")
            igs.service_call("Client_Server_"+str(i), "change_liste_player", (str(temp_list)), "") 
        arguments_list = (str(temp_list))
        time.sleep(0.2)

def start_image_server():
    #permet de lancer le server image
    with socketserver.TCPServer(("",PORT),CustomHandler) as httpd:
        httpd.serve_forever()

def start():
    #permet de dessiner l'image et de la sauvegarder
    global image
    global draw
    global index

    while True:
        time.sleep(1)
        image = Image.new('RGB', (1500,1500),'white')
        draw = ImageDraw.Draw(image)
        draw_map_render_2D()
        draw_ennemie_render_2D()
        draw_other_player_render_2D()
        image.save("./image/map.png")
        arguments_list = ("http://localhost:8000/download",50.0,50.0)
        igs.service_call("Whiteboard","addImageFromUrl",arguments_list,"")

def send_service_rectangle_whiteboard(x,y,longeur,largeur,color,couleur_contour,contour):
    #dessiner un rectangle sur l'image
    global draw
    draw.rectangle([(int(x),int(y)),(int(x+longeur),int(y+largeur))],fill=color,outline=couleur_contour,width=int(contour))

def send_service_ellipse_whiteboard(x,y,longeur,largeur,color,couleur_contour,contour):
    #dessiner une ellipse sur l'image
    global draw
    draw.ellipse([(int(x-longeur/2),int(y-largeur/2)),(int(x+longeur/2),int(y+largeur/2))],fill=color,outline=couleur_contour,width=int(contour))

def clear():
    #clear le white board
    global image
    global draw
    igs.service_call("Whiteboard","clear",(),"")
    image = Image.new('RGB', (1500,1500),'white')
    draw = ImageDraw.Draw(image)


def remove_id(index):
    #enlever un element du whiteboard
    arguments_list = (index)
    igs.service_call("Whiteboard","remove",arguments_list,"")

def draw_map_render_2D():
    #dessiner les murs sur l'image
    for i in range(len(string_map)):
        for j in range(len(string_map[i])):
            if string_map[i][j] == "X":
                send_service_rectangle_whiteboard(50.0*i,50.0*j,50.0,50.0,"black","grey",1.0)

def draw_ennemie_render_2D():
    #dessiner les ennemies sur la carte
    ennemies_move = []
    if len(ennemies_move) == 0:
        for i in list_ennemies:
            send_service_ellipse_whiteboard(i[0]-10.0,i[1]-10.0,20.0,20.0,"purple","black",1.0)
    else:
        for i in ennemies_move:
            send_service_ellipse_whiteboard(i[0]-10.0,i[1]-10.0,20.0,20.0,"purple","black",1.0)

def draw_other_player_render_2D():
    #dessiner les autres players sur la carte
    for key,value in index_dict.items():
        send_service_ellipse_whiteboard(index_dict[key][0]-10.0,index_dict[key][1]-10.0,20.0,20.0,"red","black",1.0)


# service callback #######################################
def service_callback(sender_agent_name, sender_agent_uuid, service_name, arguments, token, my_data):
    # cette fonction permet de mettre a jour les differentes variables
    # sauf pour score, lorsque le score change on fait la mise a jour directement
    if service_name == "player_position":
        index_dict[arguments[0]] = (arguments[1],arguments[2])
    elif service_name == "ennemies_kill":
        list_ennemies.pop(arguments[1])
        list_ennemies.append((random.randint(60,440),random.randint(60,440)))
    elif service_name == "player_kill":
        print("player_kill",arguments[1],arguments[0])
        igs.service_call("Client_Server_"+str(arguments[1]), "kill_service", (), "") 
    elif service_name == "score":
        if arguments[0] in score.keys():
            score[int(arguments[0])] += 50
        else:
            score[int(arguments[0])] = 50
        s = "Tableau des scores :\n" 
        for k,v in score.items():
            s += "player_"+str(k)+" : "+str(v)+ "\n"
        print(s)
        igs.service_call("Whiteboard", "chat",(s), "")
    elif service_name == "chat":
        arguments_list = (str(arguments[0]),str(arguments[1]))
        for i in index_dict.keys():
            igs.service_call("Client_Server_"+str(i),"chat",arguments_list,"")

#code principal ####################################################
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

    igs.service_init("player_position", service_callback, None)
    igs.service_arg_add("player_position", "uuid", igs.INTEGER_T)
    igs.service_arg_add("player_position", "position_x", igs.DOUBLE_T)
    igs.service_arg_add("player_position", "position_y", igs.DOUBLE_T)
    igs.service_init("ennemies_kill", service_callback, None)
    igs.service_arg_add("ennemies_kill", "uuid", igs.INTEGER_T)
    igs.service_arg_add("ennemies_kill", "index", igs.INTEGER_T)
    igs.service_init("player_kill", service_callback, None)
    igs.service_arg_add("player_kill", "uuid", igs.INTEGER_T)
    igs.service_arg_add("player_kill", "uuid_kill", igs.INTEGER_T)
    igs.service_init("score", service_callback, None)
    igs.service_arg_add("score", "uuid", igs.INTEGER_T)
    igs.service_init("chat",service_callback,None)
    igs.service_arg_add("chat", "uuid", igs.INTEGER_T)
    igs.service_arg_add("chat", "message", igs.STRING_T)

    igs.start_with_device(sys.argv[2], int(sys.argv[3]))

    #on fait apparaitre 4 ennemies aleatoirement sur la carte
    for i in range(4):
        list_ennemies.append((random.randint(50,450),random.randint(50,450)))

    #il y a trois thread: un pour ingescape, un pour le server image et un qui creer l'image
    thread = threading.Thread(target=life_fun) 
    thread.start()

    thread2 = threading.Thread(target=start)
    thread2.start()

    thread_server = threading.Thread(target=start_image_server)
    thread_server.start()

    input()

    igs.stop()