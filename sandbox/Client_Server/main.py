#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  Client_Server version 1.0
#  Created by Ingenuity i/o on 2024/10/04
#

import sys
import ingescape as igs
import random
import time

player_x = 0
player_y = 0

not_starting = True

uuid = -1

#inputs
def input_callback(iop_type, name, value_type, value, my_data):
    global player_x
    global player_y
    global uuid 
    if name == "player_x":
        player_x = value
        arguments_list = (uuid,player_x,player_y)
        igs.service_call("Server", "player_position", arguments_list, "")
    elif name == "player_y":
        player_y = value
        arguments_list = (uuid,player_x,player_y)
        igs.service_call("Server", "player_position", arguments_list, "")
    elif name == "score":
        arguments_list = (int(uuid))
        igs.service_call("Server", "score", arguments_list, "")
    elif name == "kill_ennemies":
        arguments_list = (uuid,value)
        igs.service_call("Server", "ennemies_kill", arguments_list, "")
    elif name == "kill_player":
        arguments_list = (uuid,value)
        igs.service_call("Server", "player_kill", arguments_list, "")
    # add code here if needed

def service_callback(sender_agent_name, sender_agent_uuid, service_name, arguments, token, my_data):
    global not_starting
    not_starting = False
    if service_name == "change_liste_player":
        igs.output_set_string("multi_player",arguments[0])
    elif service_name == "change_liste_ennemies":
        igs.output_set_bool("multi",True)
        igs.output_set_string("multi_ennemy",arguments[0])
    elif service_name == "change_score":
        igs.output_set_string("score_multi",arguments[0])
    elif service_name == "chat":
        igs.service_call("Whiteboard", "chat", (arguments[0]+":"+arguments[1]),"")
    elif service_name == "kill_service":
        igs.output_set_impulsion("kill")
    # add code here if needed

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
    igs.input_create("score", igs.INTEGER_T, None)
    igs.input_create("kill_ennemies", igs.INTEGER_T, None)
    igs.input_create("kill_player", igs.STRING_T, None)

    igs.output_create("multi", igs.BOOL_T, None)
    igs.output_create("multi_ennemy", igs.STRING_T, None)
    igs.output_create("multi_player", igs.STRING_T, None)
    igs.output_create("score_multi", igs.STRING_T, None)
    igs.output_create("kill", igs.IMPULSION_T, None)

    igs.observe_input("player_x", input_callback, None)
    igs.observe_input("player_y", input_callback, None)
    igs.observe_input("score", input_callback, None)
    igs.observe_input("kill_ennemies", input_callback, None)
    igs.observe_input("kill_player", input_callback, None)

    igs.service_init("change_liste_player", service_callback, None)
    igs.service_arg_add("change_liste_player", "liste_player", igs.STRING_T)
    igs.service_init("change_liste_ennemies", service_callback, None)
    igs.service_arg_add("change_liste_ennemies", "liste_ennemies", igs.STRING_T)
    igs.service_init("change_score", service_callback, None)
    igs.service_arg_add("change_score", "liste_score", igs.STRING_T)
    igs.service_init("chat", service_callback, None)
    igs.service_arg_add("chat", "uuid", igs.STRING_T)
    igs.service_arg_add("chat", "message", igs.STRING_T)
    #igs.service_init("kill_service", service_callback, None)

    igs.start_with_device(sys.argv[2], int(sys.argv[3]))

    time.sleep(10)

    uuid = sys.argv[4]

    while not_starting:
        arguments_list = (int(sys.argv[4]),player_x,player_y)
        igs.service_call("Server","player_position",arguments_list,"") 
        igs.output_set_bool("multi",True)
        time.sleep(1)

    input()

    igs.stop()

