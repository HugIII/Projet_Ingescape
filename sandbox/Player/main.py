#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  Player
#  Created by BLAYES Hugo, BAFFOGNE Clara on 2024/09/28
#  Created by Ingenuity i/o on 2024/10/23
#  Description:
#   Cet agent gere toutes les actions liees au player :
#   les deplacements, sa vie

import sys
import ingescape as igs
import math
import random


angle = 45 #valeur par defaut

vie = 100 #vie par defaut

#Map de secours, "X" represente les murs
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

#Position du player aleatoire
player_x = random.randint(0,499)
player_y = random.randint(0,499)

#inputs
def input_callback(io_type, name, value_type, value, my_data):
    global player_x
    global player_y
    global angle
    global string_map
    global vie

    #tant que le player se trouve dans un mur, on retire une position aléatoire
    while string_map[int(player_x/50)][int(player_y/50)] == "X":
        player_x = random.randint(0,499)
        player_y = random.randint(0,499)

    #sauvegarde de la pos du player avant mouvements
    tmp_x = player_x
    tmp_y = player_y

    # Mouvements
    if name=="Z":  # Avancer
        player_x += 1 * math.cos(angle)
        player_y += 1 * math.sin(angle)
    if name=="S":  # Reculer
        player_x -= 1 * math.cos(angle)
        player_y -= 1 * math.sin(angle)
    if name=="Q":  # Gauche
        player_x += 1 * math.cos(angle - math.pi / 2)
        player_y += 1 * math.sin(angle - math.pi / 2)
    if name=="D":  # Droite
        player_x += 1 * math.cos(angle + math.pi / 2)
        player_y += 1 * math.sin(angle + math.pi / 2)


    # Rotation
    if name=="E":  # Tourner à droite
        angle = (angle + 0.1) % (2 * math.pi)  # en radians
    elif name=="A":  # Tourner à gauche
        angle -= 0.1
        if angle < 0:
            angle += 2 * math.pi

    #mise en forme de la map dans le string
    elif name=="map":
        temp_list = []
        temp_sub_list = []
        for i in range(len(value)):
            if value[i] == "R": #retour à la ligne
                temp_list.append(temp_sub_list)
                temp_sub_list = []
            else:
                temp_sub_list.append(value[i])
        temp_list.append(temp_sub_list)
        string_map = temp_list

    #gestion degat et de la vie
    elif name=="degat":
        vie -= value
        igs.output_set_double("vie",vie)
        if vie < 1: #mort
            igs.output_set_impulsion("death")
            mur = 1
            while mur!=0 : #respawn aleatoire sur la map
                random_x = random.randint(0,499)
                random_y = random.randint(0,499)
                if string_map[int(random_x/50)][int(random_y/50)] != "X":
                    player_x = random_x
                    player_y = random_y
                    mur = 0
            vie = 100

    #le player se fait tuer par un autre player
    elif name=="kill":
        mur = 1;
        while mur :
            random_x = random.randint(0,499)
            random_y = random.randint(0,499)
            if string_map[int(random_x/50)][int(random_y/50)] != "X":
                player_x = random_x
                player_y = random_y
                mur = 0
    
    #cas si le deplacement du joueur est dans le mur
    if string_map[int(player_x/50)][int(player_y/50)] == "X":
        player_x = tmp_x
        player_y = tmp_y

    igs.output_set_double("player_x",player_x)
    igs.output_set_double("player_y",player_y)
    igs.output_set_double("angle",angle)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage: python3 main.py agent_name network_device port")
        devices = igs.net_devices_list()
        print("Please restart with one of these devices as network_device argument:")
        for device in devices:
            print(f" {device}")
        exit(0)

    igs.agent_set_name(sys.argv[1])
    igs.log_set_console(True)
    igs.log_set_file(True, None)
    igs.set_command_line(sys.executable + " " + " ".join(sys.argv))

    igs.debug(f"Ingescape version: {igs.version()} (protocol v{igs.protocol()})")

    igs.input_create("A", igs.IMPULSION_T, None)
    igs.input_create("E", igs.IMPULSION_T, None)
    igs.input_create("Z", igs.IMPULSION_T, None)
    igs.input_create("Q", igs.IMPULSION_T, None)
    igs.input_create("S", igs.IMPULSION_T, None)
    igs.input_create("D", igs.IMPULSION_T, None)
    igs.input_create("map", igs.STRING_T, None)
    igs.input_create("degat", igs.DOUBLE_T, None)
    igs.input_create("kill", igs.IMPULSION_T, None)

    igs.output_create("player_x", igs.DOUBLE_T, None)
    igs.output_create("player_y", igs.DOUBLE_T, None)
    igs.output_create("angle", igs.DOUBLE_T, None)
    igs.output_create("vie", igs.INTEGER_T, None)
    igs.output_create("death", igs.IMPULSION_T, None)

    igs.observe_input("A", input_callback, None)
    igs.observe_input("E", input_callback, None)
    igs.observe_input("Z", input_callback, None)
    igs.observe_input("Q", input_callback, None)
    igs.observe_input("S", input_callback, None)
    igs.observe_input("D", input_callback, None)
    igs.observe_input("map", input_callback, None)
    igs.observe_input("degat", input_callback, None)
    igs.observe_input("kill", input_callback, None)

    igs.start_with_device(sys.argv[2], int(sys.argv[3]))

    input()

    igs.stop()

