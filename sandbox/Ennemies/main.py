#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  Ennemies version 1.0
#  Created by Ingenuity i/o on 2024/09/30
#

import sys
import ingescape as igs
import random
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

ennemies_list = []
ennemies_list_move = []

multi_ennemies = []
multi = False

wave = 0
into_spawn = False

player_x = 350
player_y = 350

def move_ennemies():
    global ennemies_list_move

    while multi==False:
        for i in range(len(ennemies_list_move)):
            x = ennemies_list_move[i][0]
            y = ennemies_list_move[i][1]
            x_temp = ennemies_list_move[i][0]
            y_temp = ennemies_list_move[i][1]
            x_temp_mur = ennemies_list_move[i][0]
            y_temp_mur = ennemies_list_move[i][1]
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

            if string_map[int(x/50)][int(y/50)] == "X":
                random_x = random.randint(0,499)
                random_y = random.randint(0,499)
                ennemies_list_move[i] = (random_x,random_y)
            elif string_map[int(x_temp_mur / 50)][int(y_temp_mur / 50)] != "X":
                ennemies_list_move[i] = (x_temp,y_temp)
            elif string_map[int(x_temp_mur / 50)][int(y / 50)] != "X":
                ennemies_list_move[i] = (x_temp,y)
            elif string_map[int(x / 50)][int(y_temp_mur / 50)] != "X":
                ennemies_list_move[i] = (x,y_temp)

        igs.output_set_string("Ennemies_move",str(ennemies_list_move))    
        time.sleep(0.2)

    igs.output_set_string("Ennemies_move","[]")

#inputs
def input_callback(iop_type, name, value_type, value, my_data):
    global ennemies_list
    global string_map
    global multi
    global multi_ennemies
    global wave
    global into_spawn
    global player_x
    global player_y

    if name == "multi":
        multi = value
        if value == True:
            igs.output_set_string("list_ennemies",str(multi_ennemies))
    elif name == "player_x":
        player_x = value
    elif name == "player_y":
        player_y = value
    elif name == "multi_ennemy":
        multi_ennemies = []
        for i in value.split("("):
            if i != "[" and i != "":
                t = i.strip()[:-2].split(",")
                multi_ennemies.append((int(t[0]),int(t[1])))
        igs.output_set_string("list_ennemies",str(multi_ennemies))

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

    if multi == True:
        return

    if name == "kill":
        ennemies_list.pop(value)
        ennemies_list_move.pop(value)

    if len(ennemies_list) == 0 and into_spawn == False:
        into_spawn = True
        wave += 1
        igs.output_set_int("wave",wave)
        spawn_ennemies()
        into_spawn = False
    
    igs.output_set_string("Ennemies_move",str(ennemies_list_move))
    igs.output_set_string("list_ennemies",str(ennemies_list))

def spawn_ennemies():
    global ennemies_list
    coeff = int(3 + wave * 1.5)

    while(len(ennemies_list)<coeff):
        random_x = random.randint(0,499)
        random_y = random.randint(0,499)
        if string_map[int(random_x/50)][int(random_y/50)] != "X":
            coord_not_wall = True
            ennemies_list.append((random_x,random_y))
            ennemies_list_move.append((random_x,random_y))

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

    t = threading.Thread(target=move_ennemies)
    t.start()

    input()

    igs.stop()

