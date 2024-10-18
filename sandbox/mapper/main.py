#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  mapper version 1.0
#  Created by Ingenuity i/o on 2024/10/09
#

import sys
import ingescape as igs
import os
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
    igs.definition_set_version("1.0")
    igs.log_set_console(True)
    igs.log_set_file(True, None)
    igs.set_command_line(sys.executable + " " + " ".join(sys.argv))

    igs.start_with_device(sys.argv[2], int(sys.argv[3]))

    uuid = random.randint(1,9999)

    igs.agent_set_name("mapper_"+str(uuid))

    Scorer = igs.Agent("Scorer_"+str(uuid),False)
    Scorer.input_create("start", igs.IMPULSION_T, None)
    Scorer.input_create("score", igs.IMPULSION_T, None)
    Scorer.input_create("score_multi", igs.STRING_T, None)
    Scorer.output_create("out", igs.STRING_T, None)
    Scorer.output_create("score", igs.INTEGER_T, None)
    Scorer.output_create("score_chat", igs.STRING_T, None)

    Engine = igs.Agent("Engine_"+str(uuid),False)
    Engine.input_create("Ennemies", igs.STRING_T, None)
    Engine.input_create("other_player", igs.STRING_T, None)
    Engine.input_create("player_blood", igs.IMPULSION_T, None)
    Engine.input_create("map", igs.STRING_T, None)
    Engine.input_create("player_x", igs.INTEGER_T, None)
    Engine.input_create("player_y", igs.INTEGER_T, None)
    Engine.output_create("kill", igs.INTEGER_T, None)
    Engine.output_create("kill_player", igs.INTEGER_T, None)
    Engine.output_create("degat", igs.DOUBLE_T, None)

    Engine_map = igs.Agent("Engine_Map_"+str(uuid),False)
    Engine_map.input_create("player_x", igs.INTEGER_T, None)
    Engine_map.input_create("player_y", igs.INTEGER_T, None)
    Engine_map.input_create("map", igs.STRING_T, None)
    Engine_map.input_create("list_ennemies", igs.STRING_T, None)
    Engine_map.input_create("list_other_player", igs.STRING_T, None)

    Player_enn = igs.Agent("Player_enn_"+str(uuid),False)
    Player_enn.input_create("in", igs.IMPULSION_T, None)
    Player_enn.input_create("kill", igs.INTEGER_T, None)
    Player_enn.input_create("list_player_server", igs.STRING_T, None)
    Player_enn.input_create("multi", igs.BOOL_T, None)
    Player_enn.output_create("list_players", igs.STRING_T, None)
    Player_enn.output_create("score", igs.IMPULSION_T, None)
    Player_enn.output_create("kill", igs.STRING_T, None)

    Client_Server = igs.Agent("Client_Server_"+str(uuid),False)
    Client_Server.input_create("player_x", igs.INTEGER_T, None)
    Client_Server.input_create("player_y", igs.INTEGER_T, None)
    Client_Server.input_create("score", igs.INTEGER_T, None)
    Client_Server.input_create("kill_ennemies", igs.INTEGER_T, None)
    Client_Server.input_create("kill_player", igs.STRING_T, None)
    Client_Server.output_create("multi", igs.BOOL_T, None)
    Client_Server.output_create("multi_ennemy", igs.STRING_T, None)
    Client_Server.output_create("multi_player", igs.STRING_T, None)
    Client_Server.output_create("score_multi", igs.STRING_T, None)
    Client_Server.output_create("kill", igs.IMPULSION_T, None)

    Starter = igs.Agent("Starter_"+str(uuid),False)
    Starter.output_create("out", igs.IMPULSION_T, None)
    Starter.output_create("color_background", igs.STRING_T, None)

    Ennemies = igs.Agent("Ennemies_"+str(uuid),False)
    Ennemies.input_create("in", igs.IMPULSION_T, None)
    Ennemies.input_create("kill", igs.INTEGER_T, None)
    Ennemies.input_create("map", igs.STRING_T, None)
    Ennemies.input_create("multi", igs.BOOL_T, None)
    Ennemies.input_create("multi_ennemy", igs.STRING_T, None)
    Ennemies.output_create("list_ennemies", igs.STRING_T, None)
    Ennemies.output_create("score", igs.IMPULSION_T, None)

    Map = igs.Agent("Map_"+str(uuid),False)
    Map.input_create("start",igs.IMPULSION_T,None)
    Map.output_create("map",igs.STRING_T, None)

    Engine.activate()
    Engine_map.activate()
    Player_enn.activate()
    Client_Server.activate()
    Starter.activate()
    Ennemies.activate()
    Scorer.activate()
    Map.activate()

    time.sleep(5)

    Engine.mapping_add("Ennemies","Ennemies_"+str(uuid),"list_ennemies")
    Engine.mapping_add("other_player","Player_enn_"+str(uuid),"list_players")
    # player blood Engine
    Engine.mapping_add("map","Map_"+str(uuid),"map")
    # player_x Engine
    # player_y Engine
    # player_x Engine_Map
    # player_y Engine_Map
    Engine_map.mapping_add("map","Map_"+str(uuid),"map")
    Engine_map.mapping_add("list_ennemies","Ennemies_"+str(uuid),"list_ennemies")
    Engine_map.mapping_add("list_other_player","Player_enn_"+str(uuid),"list_players")
    Player_enn.mapping_add("kill","Engine_"+str(uuid),"kill_player")
    Player_enn.mapping_add("list_player_server","Client_Server_"+str(uuid),"multi_player")
    Player_enn.mapping_add("multi","Client_Server_"+str(uuid),"multi")
    # player x Client_Server
    # player_y Client_Server
    Client_Server.mapping_add("score","Scorer_"+str(uuid),"score")
    Client_Server.mapping_add("kill_ennemies","Engine_"+str(uuid),"kill")
    Client_Server.mapping_add("kill_player","Player_enn_"+str(uuid),"kill")
    Scorer.mapping_add("start","Starter_"+str(uuid),"out")
    Scorer.mapping_add("score","Ennemies_"+str(uuid),"score")
    Scorer.mapping_add("score","Player_enn_"+str(uuid),"score")
    Scorer.mapping_add("score_multi","Client_Server_"+str(uuid),"score_multi")
    Ennemies.mapping_add("kill","Engine_"+str(uuid),"kill")
    # map Ennemies
    Ennemies.mapping_add("multi","Client_Server_"+str(uuid),"multi")
    Ennemies.mapping_add("multi_ennemy","Client_Server_"+str(uuid),"multi_ennemy")
    #Whiteboard
    Map.mapping_add("start","Starter_"+str(uuid),"out")

    time.sleep(4)

    Engine.deactivate()
    Engine_map.deactivate()
    Player_enn.deactivate()
    Client_Server.deactivate()
    Starter.deactivate()
    Ennemies.deactivate()
    Scorer.deactivate()
    Map.deactivate()

    time.sleep(4)
    

    os.system("start /B python ./sandbox/Ennemies/main.py Ennemies_"+str(uuid)+" Wi-Fi 5670 "+str(uuid))
    os.system("start /B python ./sandbox/Starter/main.py Starter_"+str(uuid)+" Wi-Fi 5670 "+str(uuid))
    os.system("start /B python ./sandbox/Scorer/main.py Scorer_"+str(uuid)+" Wi-Fi 5670 "+str(uuid))
    os.system("start /B python ./sandbox/Engine/main.py Engine_"+str(uuid)+" Wi-Fi 5670 "+str(uuid))
    os.system("start /B python ./sandbox/Engine_Map/main.py Engine_Map_"+str(uuid)+" Wi-Fi 5670 "+str(uuid))
    os.system("start /B python ./sandbox/Player_enn/main.py Player_enn_"+str(uuid)+" Wi-Fi 5670 "+str(uuid))
    os.system("start /B python ./sandbox/Client_Server/main.py Client_Server_"+str(uuid)+" Wi-Fi 5670 "+str(uuid))
    os.system("start /B python ./sandbox/Map/main.py Map_"+str(uuid)+" Wi-Fi 5670 "+str(uuid))
    os.system("start /B ./sandbox/whiteboard/Whiteboard.exe --device Wi-Fi --port 5670")

    igs.stop()

