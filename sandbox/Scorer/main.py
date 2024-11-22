#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  Scorer version 1.0
#  Created by Ingenuity i/o on 2024/10/01
#

import sys
import ingescape as igs

score = 0
s = ""

#inputs
def input_callback(iop_type, name, value_type, value, my_data):
    global score
    global s

    if name == "score":
        score += 50
        igs.output_set_string("out","Score: "+str(score)) 
        igs.output_set_int("score",score)
    elif name == "score_multi":
        s = "Tableau des score:\n" 
        if value == "[]":
            return
        for i in value.split("("):
            if i != "[" and i != "":
                t = i.strip()[:-2].split(",")
                s += "player_"+t[0]+" : "+t[1] + "\n"
        s = s[:-1]
        igs.service_call("Whiteboard", "chat",s, "")
    elif name == "print_score_multi":
        igs.service_call("Whiteboard", "chat",s, "")

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

    igs.input_create("start", igs.IMPULSION_T, None)
    igs.input_create("score", igs.IMPULSION_T, None)
    igs.input_create("score_multi", igs.STRING_T, None)

    igs.output_create("out", igs.STRING_T, None)
    igs.output_create("score", igs.INTEGER_T, None)
    igs.output_create("score_chat", igs.STRING_T, None)

    igs.observe_input("start", input_callback, None)
    igs.observe_input("score", input_callback, None)
    igs.observe_input("score_multi", input_callback, None)

    igs.start_with_device(sys.argv[2], int(sys.argv[3]))

    input()

    igs.stop()

