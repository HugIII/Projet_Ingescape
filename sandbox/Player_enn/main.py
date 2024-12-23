#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  Player_enn
#  Created by BAFFOGNE Clara,BLAYES Hugo on 2024/10/22
#  Created by Ingenuity i/o on 2024/10/22
#  Description:
#   Cet agent permet de faire le lien entre le client server et l'engine


import sys
import ingescape as igs

#variables#################################################################
player_enn = []
player_enn_uuid = []
multi = True

#inputs callback ###########################################################
def input_callback(iop_type, name, value_type, value, my_data):
    global player_enn
    global multi
    # permet de passer switch entre solo et multi
    if name=="multi":
        if value == False:
            multi = False
            player_enn = []
            igs.output_set_string("list_players",str(player_enn))
        else:
            multi = True
    # recuperation et mise en forme de la liste player server
    elif name=="list_player_server":
        player_enn = []
        for i in value.split("("):
            if i != "[" and i != "":
                t = i.strip()[:-2].split(",")
                try:
                    player_enn_uuid.append((int(t[0])))
                except:
                    return
                player_enn.append((float(t[1]),float(t[2])))
        igs.output_set_string("list_players",str(player_enn))
    # lorsqu'on tue un adversaire on envoie l'uuid du player mort au client server
    elif name=="kill":
        igs.output_set_impulsion("score")
        igs.output_set_string("kill",str(player_enn_uuid[value]))

# code principal ######################################################
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
    igs.input_create("list_player_server", igs.STRING_T, None)
    igs.input_create("multi", igs.BOOL_T, None)

    igs.output_create("list_players", igs.STRING_T, None)
    igs.output_create("score", igs.IMPULSION_T, None)
    igs.output_create("kill", igs.STRING_T, None)

    igs.observe_input("kill", input_callback, None)
    igs.observe_input("list_player_server", input_callback, None)
    igs.observe_input("multi", input_callback, None)

    igs.start_with_device(sys.argv[2], int(sys.argv[3]))

    input()

    igs.stop()

