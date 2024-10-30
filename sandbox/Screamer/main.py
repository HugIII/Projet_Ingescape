#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  Screamer
#  Created by Ingenuity i/o on 2024/10/22
#

import sys
import ingescape as igs
import random
import time

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

    igs.output_create("screamer", igs.IMPULSION_T, None)

    igs.start_with_device(sys.argv[2], int(sys.argv[3]))

    while(1):
        r = random.randint(0,1000)
        if r < 2:
            igs.output_set_impulsion("screamer")
        time.sleep(1)

    input()

    igs.stop()

