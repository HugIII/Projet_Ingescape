#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  Sound_manager
#  Created by Ingenuity i/o on 2024/10/02
#

import sys
import ingescape as igs
import pygame

music_play = True
music_trigger = False
sound_on = True

music_link = "./sounds/music.mp3"
death_link = "./sounds/death.mp3"
monster_death_link = "./sounds/monster_death.mp3"
shoot_link = "./sounds/shoot.mp3"
crossbow_link = "./sounds/crossbow.mp3"
sword_link = "./sounds/sword.mp3"
degat_link = "./sounds/degat.mp3"

vie = 100

# Inputs
def input_callback(iop_type, name, value_type, value, my_data):
    global music_play
    global sound_on
    global music_trigger
    global vie

    if name == "sound_on":
        if music_play:
            pygame.mixer.music.pause()
            music_play = False
        else:
            pygame.mixer.music.unpause()
            music_play = True

    elif name == "music":
        if sound_on:
            sound_on = False
            pygame.mixer.music.pause()
        else:
            sound_on = True
            pygame.mixer.music.unpause()

    elif name == "death" and sound_on:
        death = pygame.mixer.Sound(death_link)
        death.play()
    elif name == "monster_death" and sound_on:
        death_monster = pygame.mixer.Sound(monster_death_link)
        death_monster.set_volume(0.25)
        death_monster.play()
    elif name == "crossbow" and sound_on:
        shoot = pygame.mixer.Sound(crossbow_link)
        shoot.play()
    elif name == "sword" and sound_on:
        shoot = pygame.mixer.Sound(sword_link)
        shoot.set_volume(0.25)
        shoot.play()
    elif name == "degat_recu" and sound_on and vie != value:
        degat = pygame.mixer.Sound(degat_link)
        degat.play()
        vie = value
    elif name == "music_trigger":
        music_trigger = not music_trigger
        if music_trigger == False:
            pygame.mixer.music.pause()
        elif music_trigger == True:
            pygame.mixer.music.set_volume(0.15)
            pygame.mixer.music.play(-1)

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

    igs.input_create("music", igs.IMPULSION_T, None)
    igs.input_create("death", igs.IMPULSION_T, None)
    igs.input_create("monster_death", igs.IMPULSION_T, None)
    igs.input_create("crossbow", igs.IMPULSION_T, None)
    igs.input_create("sword", igs.IMPULSION_T, None)
    igs.input_create("degat_recu", igs.INTEGER_T, None)
    igs.input_create("sound_on", igs.IMPULSION_T, None)
    igs.input_create("music_trigger", igs.IMPULSION_T, None)

    igs.observe_input("music", input_callback, None)
    igs.observe_input("death", input_callback, None)
    igs.observe_input("monster_death", input_callback, None)
    igs.observe_input("crossbow", input_callback, None)
    igs.observe_input("sword", input_callback, None)
    igs.observe_input("degat_recu", input_callback, None)
    igs.observe_input("sound_on", input_callback, None)
    igs.observe_input("music_trigger", input_callback, None)

    igs.start_with_device(sys.argv[2], int(sys.argv[3]))

    pygame.mixer.init()

    pygame.mixer.music.load(music_link)

    input()

    igs.stop()

