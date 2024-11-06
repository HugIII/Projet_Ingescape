#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  Map
#  Created by Ingenuity i/o on 2024/10/18
#

import sys
import ingescape as igs
import random
import numpy

string_map = []


#inputs
def input_callback(io_type, name, value_type, value, my_data):
    if (name == "start"):
        s = ""
        for m in string_map:
            for l in m:
                s += l
            s += "R"
        igs.output_set_string("map", s)

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

    igs.input_create("start", igs.IMPULSION_T, None)

    igs.output_create("map", igs.STRING_T, None)

    igs.observe_input("start", input_callback, None)

    igs.start_with_device(sys.argv[2], int(sys.argv[3]))

    map_size = 10
    room_number = 10
    room_size = 5

    room_centers = []
    index_to_visit = set()

    for i in range(map_size):
        l = []
        for j in range(map_size):
            l.append("X")
        string_map.append(l)

    for i in range(random.randint(2,room_number)):
        room_ok = False
        while not room_ok:
            room_size = random.randint(2,room_size)
            room_x = random.randint(1,map_size-room_size-1)
            room_y = random.randint(1,map_size-room_size-1)
            room_ok = True
            for p in range(room_size):
                for j in range(room_size):
                    if string_map[room_x+p][room_y+j] == ".":
                        room_ok = False

        room_centers.append((int(room_x+room_size/2),int(room_y+room_size/2),room_size))
        index_to_visit.add(i)

        for k in range(room_size):
            for j in range(room_size):
                string_map[room_x+k][room_y+j] = "."

    index = -1
    while len(index_to_visit) != 0 and index < len(room_centers):
        index += 1
        if index in index_to_visit:
            index_candidate = -1
            dist_candidate = 1000000000000
            for j in index_to_visit:
                if index != j:
                    dist = (abs(room_centers[index][0]-room_centers[j][0])+abs(room_centers[index][1]-room_centers[j][1]))/room_centers[j][2]
                    if dist < dist_candidate:
                        index_candidate = j
                        dist_candidate = dist
            t_x = room_centers[index][0]
            t_y = room_centers[index][1]
            goal_x = room_centers[index_candidate][0]
            goal_y = room_centers[index_candidate][1]
            while t_x != goal_x or t_y != goal_y:
                if t_y < goal_y:
                    t_y += 1
                elif t_y > goal_y:
                    t_y -= 1
                elif t_x < goal_x:
                    t_x += 1
                elif t_x > goal_x:
                    t_x -= 1
                string_map[t_x][t_y] = "."
            index_to_visit.remove(index)

    s = ""
    for m in string_map:
        for l in m:
            s += l
        s += "R"
    print(s)
    igs.output_set_string("map", s)

    input()

    igs.stop()

