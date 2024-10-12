#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  Server version 1.0
#  Created by Ingenuity i/o on 2024/10/04
#

import sys
import ingescape as igs
import random
import time
import threading

list_ennemies = []
index_dict = {}
score = {}

def life_fun():
    while True:
        for i in index_dict.keys():
            arguments_list = (str(list_ennemies))
            igs.service_call("Client_Server_"+str(i),"change_liste_ennemies",arguments_list,"")
        time.sleep(1)

def service_callback(sender_agent_name, sender_agent_uuid, service_name, arguments, token, my_data):
    if service_name == "player_position":
        score[arguments[0]] = 0
        index_dict[arguments[0]] = (arguments[1],arguments[2])
        temp_list = []
        for i in index_dict.keys():
            li = index_dict[i]
            temp_list.append((i,li[0],li[1]))
        arguments_list = (str(temp_list))
        for i in index_dict.keys():
            igs.service_call("Client_Server_"+str(i), "change_liste_player", arguments_list, "") #à changer !!!!!!!!!!!!!!!!!!!!!!!!!!!
    elif service_name == "ennemies_kill":
        print("kill")
        list_ennemies.pop(arguments[1])
        list_ennemies.append((random.randint(60,440),random.randint(60,440)))
        arguments_list = (str(list_ennemies))
        for i in index_dict.keys():
            igs.service_call("Client_Server_"+str(i),"change_liste_ennemies",arguments_list,"") # à changer
    elif service_name == "player_kill":
        for i in index_dict.keys():
            igs.service_call("Client_Server_"+str(i), "kill_service", (), "") # à changer aussi
    elif service_name == "score":
        if arguments[0] in score.keys():
            score[arguments[0]] += 50
        else:
            score[arguments[0]] = 50
        s = "["
        for i in score.keys():
            s+="("+str(i)+","+str(score[i])+")"
        s += "]"
        arguments_list = (s)
        for i in index_dict.keys():
            igs.service_call("Client_Server_"+str(i),"change_score",arguments_list,"") # à changer !!!!!!!!!!!!!!
    elif service_name == "chat":
        arguments_list = (str(arguments[0]),str(arguments[1]))
        for i in index_dict.keys():
            igs.service_call("Client_Server_"+str(i),"chat",arguments_list,"") # à changer !!!!!!!!!!!!!!
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

    igs.service_init("player_position", service_callback, None)
    igs.service_arg_add("player_position", "uuid", igs.INTEGER_T)
    igs.service_arg_add("player_position", "position_x", igs.INTEGER_T)
    igs.service_arg_add("player_position", "position_y", igs.INTEGER_T)
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

    for i in range(4):
        list_ennemies.append((random.randint(50,450),random.randint(50,450)))

    thread = threading.Thread(target=life_fun) 
    thread.start()

    input()

    igs.stop()

