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

    dev = sys.argv[2]
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
    Engine.input_create("player_x", igs.DOUBLE_T, None)
    Engine.input_create("player_y", igs.DOUBLE_T, None)
    Engine.input_create("angle", igs.DOUBLE_T, None)
    Engine.input_create("wave",igs.INTEGER_T,None)
    Engine.input_create("arbalete_shot",igs.IMPULSION_T,None)
    Engine.input_create("sword_hit",igs.IMPULSION_T,None)
    Engine.input_create("arrow_left",igs.INTEGER_T,None)
    Engine.input_create("vie",igs.INTEGER_T,None)
    Engine.input_create("screamer",igs.IMPULSION_T,None)
    Engine.output_create("kill", igs.INTEGER_T, None)
    Engine.output_create("kill_player", igs.INTEGER_T, None)
    Engine.output_create("degat", igs.DOUBLE_T, None)

    Weapons = igs.Agent("Weapons_"+str(uuid),False)
    Weapons.input_create("kill",igs.INTEGER_T,None)
    Weapons.input_create("click_left",igs.IMPULSION_T,None)
    Weapons.input_create("click_right",igs.IMPULSION_T,None)
    Weapons.output_create("arbalete_shoot",igs.IMPULSION_T,None)
    Weapons.output_create("sword_shoot",igs.IMPULSION_T,None)
    Weapons.output_create("arrow_left",igs.INTEGER_T,None)

    EventKeyBoard = igs.Agent("EventKeyBoard_"+str(uuid),False)
    EventKeyBoard.output_create("A",igs.IMPULSION_T,None)
    EventKeyBoard.output_create("E",igs.IMPULSION_T,None)
    EventKeyBoard.output_create("Z",igs.IMPULSION_T,None)
    EventKeyBoard.output_create("Q",igs.IMPULSION_T,None)
    EventKeyBoard.output_create("S",igs.IMPULSION_T,None)
    EventKeyBoard.output_create("D",igs.IMPULSION_T,None)
    EventKeyBoard.output_create("M",igs.IMPULSION_T,None)
    EventKeyBoard.output_create("N",igs.IMPULSION_T,None)
    EventKeyBoard.output_create("click_left",igs.IMPULSION_T,None)
    EventKeyBoard.output_create("click_right",igs.IMPULSION_T,None)

    Player = igs.Agent("Player_"+str(uuid),False)
    Player.input_create("A",igs.IMPULSION_T,None)
    Player.input_create("E",igs.IMPULSION_T,None)
    Player.input_create("Z",igs.IMPULSION_T,None)
    Player.input_create("Q",igs.IMPULSION_T,None)
    Player.input_create("S",igs.IMPULSION_T,None)
    Player.input_create("D",igs.IMPULSION_T,None)
    Player.input_create("map",igs.STRING_T,None)
    Player.input_create("degat",igs.DOUBLE_T,None)
    Player.input_create("kill",igs.IMPULSION_T,None)
    Player.output_create("player_x",igs.DOUBLE_T,None)
    Player.output_create("player_y",igs.DOUBLE_T,None)
    Player.output_create("angle",igs.DOUBLE_T,None)
    Player.output_create("vie", igs.DOUBLE_T,None)

    Player_enn = igs.Agent("Player_enn_"+str(uuid),False)
    Player_enn.input_create("kill", igs.INTEGER_T, None)
    Player_enn.input_create("list_player_server", igs.STRING_T, None)
    Player_enn.input_create("multi", igs.BOOL_T, None)
    Player_enn.output_create("list_players", igs.STRING_T, None)
    Player_enn.output_create("score", igs.IMPULSION_T, None)
    Player_enn.output_create("kill", igs.STRING_T, None)

    Client_Server = igs.Agent("Client_Server_"+str(uuid),False)
    Client_Server.input_create("player_x", igs.DOUBLE_T, None)
    Client_Server.input_create("player_y", igs.DOUBLE_T, None)
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
    Ennemies.output_create("wave", igs.INTEGER_T, None)
    Ennemies.output_create("Ennemies_move",igs.STRING_T,None)

    Screamer = igs.Agent("Screamer_"+str(uuid),False)
    Screamer.output_create("screamer",igs.IMPULSION_T,None)
    
    Engine.activate()
    Weapons.activate()
    Player_enn.activate()
    Client_Server.activate()
    Starter.activate()
    Ennemies.activate()
    Scorer.activate()
    Screamer.activate()
    EventKeyBoard.activate()
    Player.activate()

    time.sleep(5)

    Engine.mapping_add("Ennemies","Ennemies_"+str(uuid),"list_ennemies")
    Engine.mapping_add("other_player","Player_enn_"+str(uuid),"list_players")
    Engine.mapping_add("player_x","Player_"+str(uuid),"player_x")
    Engine.mapping_add("player_y","Player_"+str(uuid),"player_y")
    Engine.mapping_add("angle","Player_"+str(uuid),"angle")
    Engine.mapping_add("sword_hit","Weapons_"+str(uuid),"sword_shoot")
    Engine.mapping_add("arbalete_shot","Weapons_"+str(uuid),"arbalete_shoot")
    Engine.mapping_add("arrow_left","Weapons_"+str(uuid),"arrow_left")
    Engine.mapping_add("wave","Ennemies_"+str(uuid),"wave")
    Engine.mapping_add("screamer","Screamer_"+str(uuid),"screamer")
    Engine.mapping_add("vie","Player_"+str(uuid),"vie")
    Engine.mapping_add("Ennemies_move","Ennemies_"+str(uuid),"Ennemies_move")
    Player_enn.mapping_add("kill","Engine_"+str(uuid),"kill_player")
    Player_enn.mapping_add("list_player_server","Client_Server_"+str(uuid),"multi_player")
    Player_enn.mapping_add("multi","Client_Server_"+str(uuid),"multi")
    Client_Server.mapping_add("player_x","Player_"+str(uuid),"player_x")
    Client_Server.mapping_add("player_y","Player_"+str(uuid),"player_y")
    Client_Server.mapping_add("score","Scorer_"+str(uuid),"score")
    Client_Server.mapping_add("kill_ennemies","Engine_"+str(uuid),"kill")
    Client_Server.mapping_add("kill_player","Player_enn_"+str(uuid),"kill")
    Scorer.mapping_add("start","Starter_"+str(uuid),"out")
    Scorer.mapping_add("score","Ennemies_"+str(uuid),"score")
    Scorer.mapping_add("score","Player_enn_"+str(uuid),"score")
    Scorer.mapping_add("score_multi","Client_Server_"+str(uuid),"score_multi")
    Ennemies.mapping_add("kill","Engine_"+str(uuid),"kill")
    Ennemies.mapping_add("multi","Client_Server_"+str(uuid),"multi")
    Ennemies.mapping_add("multi_ennemy","Client_Server_"+str(uuid),"multi_ennemy")
    Weapons.mapping_add("kill","Engine_"+str(uuid),"kill")
    Weapons.mapping_add("kill","Engine_"+str(uuid),"kill_player")
    Weapons.mapping_add("click_left","EventKeyBoard_"+str(uuid),"click_left")
    Weapons.mapping_add("click_right","EventKeyBoard_"+str(uuid),"click_right")
    Player.mapping_add("A","EventKeyBoard_"+str(uuid),"A")
    Player.mapping_add("E","EventKeyBoard_"+str(uuid),"E")
    Player.mapping_add("Z","EventKeyBoard_"+str(uuid),"Z")
    Player.mapping_add("Q","EventKeyBoard_"+str(uuid),"Q")
    Player.mapping_add("D","EventKeyBoard_"+str(uuid),"D")
    Player.mapping_add("S","EventKeyBoard_"+str(uuid),"S")
    Player.mapping_add("degat","Engine_"+str(uuid),"degat")
    Player.mapping_add("kill","Client_Server_"+str(uuid),"kill")

    time.sleep(5)

    Engine.deactivate()
    Player_enn.deactivate()
    Client_Server.deactivate()
    Starter.deactivate()
    Ennemies.deactivate()
    Scorer.deactivate()
    Screamer.deactivate()
    Weapons.deactivate()
    EventKeyBoard.deactivate()
    Player.deactivate()

    time.sleep(4)

    device = dev + " " + str(sys.argv[3])

    os.system("start /B python ./sandbox/Ennemies/main.py Ennemies_"+str(uuid)+" "+device+" False")
    os.system("start /B python ./sandbox/Starter/main.py Starter_"+str(uuid)+" "+device+" "+str(uuid))
    os.system("start /B python ./sandbox/Scorer/main.py Scorer_"+str(uuid)+" "+device+" "+str(uuid))
    os.system("start /B python ./sandbox/Engine/main.py Engine_"+str(uuid)+" "+device+" "+str(uuid))
    os.system("start /B python ./sandbox/Engine_Map/main.py Engine_Map_"+str(uuid)+" "+device+" "+str(uuid))
    os.system("start /B python ./sandbox/Player_enn/main.py Player_enn_"+str(uuid)+" "+device+" "+str(uuid))
    os.system("start /B python ./sandbox/Client_Server/main.py Client_Server_"+str(uuid)+" "+device+" "+str(uuid))
    os.system("start /B python ./sandbox/Weapons/main.py Weapons_"+str(uuid)+" "+device+" "+str(uuid))
    os.system("start /B python ./sandbox/Screamer/main.py Screamer_"+str(uuid)+" "+device+" "+str(uuid))
    os.system("start /B python ./sandbox/Player/main.py Player_"+str(uuid)+"  "+device)
    os.system("start /B python ./sandbox/EventKeyBoard/main.py EventKeyBoard_"+str(uuid)+"  "+device)

    os.system("start /B ./sandbox/whiteboard/Whiteboard.exe --device "+dev+" --port "+str(sys.argv[3]))

    igs.stop()

