#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  Ennemies
#  Created by BLAYES Hugo, BAFFOGNE Clara on 2024/10/04
#  Created by Ingenuity i/o on 2024/10/04
#  Description:
#   Ce programme s'occupe de la gestion des ennemies dans notre jeu video
#   en solo, cela comprend leurs mouvements, leurs apparitions, le format vague, les collisions des ennemies avec les murs
#   en multi, cet agent fait le tampon entre l'engine et le client server
#

import sys
import ingescape as igs
import random
import threading
import time
import math

#variables########################################################
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

ennemies_list = []
ennemies_list_move = []

multi_ennemies = []
multi = False

wave = 0
into_spawn = False

player_x = 350
player_y = 350

#fonction #######################################################
def move_ennemies():
    #cette fonction gere le deplacement des ennemies sur la carte
    global ennemies_list_move

    #si la variable multi est fause, l'agent se met en mode fonctionnement solo
    while multi==False:
        #pour chaque ennemies
        for i in range(len(ennemies_list_move)):
            x = ennemies_list_move[i][0]
            y = ennemies_list_move[i][1]
            x_temp = ennemies_list_move[i][0]
            y_temp = ennemies_list_move[i][1]
            x_temp_mur = ennemies_list_move[i][0]
            y_temp_mur = ennemies_list_move[i][1]

            #on calcule le potentiel deplacement de l'ennemie
            if x > player_x + 20:
                x_temp -= 1
                x_temp_mur -= 10
            elif x < player_x - 20:
                x_temp += 1
                x_temp_mur += 10

            if y > player_y + 20:
                y_temp -= 1
                y_temp_mur -= 10
            elif y < player_y - 20:
                y_temp += 1
                y_temp_mur += 10

            #si l'ennemie est dans le mur on le teleporte au hasard sur la carte
            if string_map[int(x/50)][int(y/50)] == "X":
                random_x = random.randint(0,499)
                random_y = random.randint(0,499)
                ennemies_list_move[i] = (random_x,random_y)
            #si le deplacement en x et y est pas dans le mur alors l'ennemie bouge
            elif string_map[int(x_temp_mur / 50)][int(y_temp_mur / 50)] != "X":
                ennemies_list_move[i] = (x_temp,y_temp)
            #idem avec seulement x
            elif string_map[int(x_temp_mur / 50)][int(y / 50)] != "X":
                ennemies_list_move[i] = (x_temp,y)
            #idem seulement avec y
            elif string_map[int(x / 50)][int(y_temp_mur / 50)] != "X":
                ennemies_list_move[i] = (x,y_temp)

        #on recalcule toutes les 0.2 secondes le positionnement de l'ennemie
        igs.output_set_string("Ennemies_move",str(ennemies_list_move))    
        time.sleep(0.2)

    #si on est en mode multi on laisse vide la liste ennemies move
    igs.output_set_string("Ennemies_move","[]")

#input callback ##########################################################
def input_callback(iop_type, name, value_type, value, my_data):
    global ennemies_list
    global string_map
    global multi
    global multi_ennemies
    global wave
    global into_spawn
    global player_x
    global player_y

    #permet de definir que nous sommes en mode multi
    if name == "multi":
        multi = value
        if value == True:
            igs.output_set_string("list_ennemies",str(multi_ennemies))
    #maj positionnement player
    elif name == "player_x":
        player_x = value
    elif name == "player_y":
        player_y = value
    #recupere et traite les positions servers des ennemies
    elif name == "multi_ennemy":
        multi_ennemies = []
        for i in value.split("("):
            if i != "[" and i != "":
                t = i.strip()[:-2].split(",")
                multi_ennemies.append((int(t[0]),int(t[1])))
        igs.output_set_string("list_ennemies",str(multi_ennemies))

    #si on a un kill on mode multi juste on augmente le score
    if name == "kill":
        igs.output_set_impulsion("score")
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

    #si on est en multi on a finit le traitement
    if multi == True:
        return

    #si on est en solo et qu'on a un kill, on enleve l'ennemies de la liste
    if name == "kill":
        ennemies_list.pop(value)
        ennemies_list_move.pop(value)

    #lorsque la liste des ennemies est vide on cherche a les refaire spawns
    if len(ennemies_list) == 0 and into_spawn == False:
        into_spawn = True
        wave += 1
        igs.output_set_int("wave",wave)
        spawn_ennemies()
        into_spawn = False
    
    igs.output_set_string("Ennemies_move",str(ennemies_list_move))
    igs.output_set_string("list_ennemies",str(ennemies_list))

def spawn_ennemies():
    #fonction qui permet de faire spawner les ennemies
    global ennemies_list

    #on considere que plus le nombre de wave augmente plus le nombre d'ennemies est grand
    coeff = int(3 + wave * 1.5)

    #on fait spawn les ennemies avec des positions aleatoire
    while(len(ennemies_list)<coeff):
        random_x = random.randint(0,499)
        random_y = random.randint(0,499)
        if string_map[int(random_x/50)][int(random_y/50)] != "X":
            coord_not_wall = True
            ennemies_list.append((random_x,random_y))
            ennemies_list_move.append((random_x,random_y))

#code principal ###########################################################
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

    igs.input_create("kill", igs.INTEGER_T, None)
    igs.observe_input("kill", input_callback, None)

    igs.input_create("in", igs.IMPULSION_T, None)
    igs.observe_input("in", input_callback, None)

    igs.output_create("list_ennemies", igs.STRING_T, None)
    igs.output_create("score", igs.IMPULSION_T, None)
    igs.output_create("wave", igs.INTEGER_T, None)
    igs.output_create("Ennemies_move",igs.STRING_T,None)

    igs.input_create("map",igs.STRING_T, None)
    igs.observe_input("map",input_callback,None)

    igs.input_create("multi", igs.BOOL_T, None)
    igs.observe_input("multi", input_callback, None)

    igs.input_create("multi_ennemy",igs.STRING_T, None)
    igs.observe_input("multi_ennemy", input_callback, None)

    igs.input_create("player_x",igs.DOUBLE_T,None)
    igs.observe_input("player_x",input_callback,None)

    igs.input_create("player_y",igs.DOUBLE_T,None)
    igs.observe_input("player_y",input_callback,None)

    igs.start_with_device(sys.argv[2], int(sys.argv[3]))

    #nous avons deux threads:
    #un periodique qui calcule le deplacement des ennemies
    #un qui permet de gerer les entrees ingescape
    t = threading.Thread(target=move_ennemies)
    t.start()

    input()

    igs.stop()

