#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  Weapons
#  Created by Ingenuity i/o on 2024/10/20
#

import sys
import ingescape as igs
import random
import time

arrow_left = 0 #nombre de fleches par defaut

left_time = 0
right_time = 0
left_cooldown = 2 #cooldown avant de pouvoir tirer le prochain coup à l'arbalette
right_cooldown = 0.5 #cooldown avant de pouvoir donner un coup de hache

#inputs
def input_callback(io_type, name, value_type, value, my_data):
    global left_time
    global right_time
    global left_cooldown
    global right_cooldown
    global arrow_left

    if name == "kill": #monstre tué
        arrow_left += random.randint(0,2) #donne un nombre de fleche aleatoire entre 0 et 2
        igs.output_set_int("arrow_left",arrow_left)
    elif name == "click_right": #coup de hache
        timestamp = time.time()
        if timestamp - right_time > right_cooldown: #si cooldown passé
            right_time = timestamp
            igs.output_set_impulsion("sword_shoot")  
    elif name == "click_left": #arbalette
        timestamp = time.time()
        if arrow_left > 0 and timestamp - left_time > left_cooldown: #on a des fleches et si cooldown passé
            arrow_left -= 1
            left_time = timestamp
            igs.output_set_impulsion("arbalete_shoot") 
            igs.output_set_int("arrow_left",arrow_left)

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

    igs.input_create("kill", igs.INTEGER_T, None)
    igs.input_create("click_left", igs.INTEGER_T, None)
    igs.input_create("click_right", igs.INTEGER_T, None)

    igs.output_create("arbalete_shoot", igs.IMPULSION_T, None)
    igs.output_create("sword_shoot", igs.IMPULSION_T, None)
    igs.output_create("arrow_left", igs.INTEGER_T, None)

    igs.observe_input("kill", input_callback, None)
    igs.observe_input("click_left", input_callback, None)
    igs.observe_input("click_right", input_callback, None)

    igs.start_with_device(sys.argv[2], int(sys.argv[3]))

    input()

    igs.stop()

