#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  Ennemies version 1.0
#  Created by Ingenuity i/o on 2024/09/30
#

import sys
import ingescape as igs

ennemies_list = [(440,440),(340,440)]

#inputs
def input_callback(iop_type, name, value_type, value, my_data):
    igs.output_set_string("list_ennemies",str(ennemies_list))
    pass
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

    igs.input_create("in", igs.IMPULSION_T, None)
    igs.input_create("kill", igs.INTEGER_T, None)

    igs.output_create("list_ennemies", igs.STRING_T, None)

    igs.observe_input("in", input_callback, None)
    igs.observe_input("kill", input_callback, None)

    igs.start_with_device(sys.argv[2], int(sys.argv[3]))

    input()

    igs.stop()

