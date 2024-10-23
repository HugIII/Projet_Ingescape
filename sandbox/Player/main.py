#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  Player
#  Created by Ingenuity i/o on 2024/10/23
#

import sys
import ingescape as igs
import math

player_x = 430
player_y = 430
angle = 45

#inputs
def input_callback(io_type, name, value_type, value, my_data):
    global player_x
    global player_y
    global angle

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
    if name=="A":  # Tourner à gauche
        angle -= 0.1
        if angle < 0:
            angle += 2 * math.pi

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

    igs.output_create("player_x", igs.DOUBLE_T, None)
    igs.output_create("player_y", igs.DOUBLE_T, None)
    igs.output_create("angle", igs.DOUBLE_T, None)

    igs.observe_input("A", input_callback, None)
    igs.observe_input("E", input_callback, None)
    igs.observe_input("Z", input_callback, None)
    igs.observe_input("Q", input_callback, None)
    igs.observe_input("S", input_callback, None)
    igs.observe_input("D", input_callback, None)

    igs.start_with_device(sys.argv[2], int(sys.argv[3]))

    input()

    igs.stop()

