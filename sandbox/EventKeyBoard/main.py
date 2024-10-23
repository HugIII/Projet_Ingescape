#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  EventKeyBoard
#  Created by Ingenuity i/o on 2024/10/22
#

import sys
import ingescape as igs
'''import pygame

#inputs
def input_callback():
    while True:
        keys = pygame.key.get_pressed()

        # Mouvements
        if keys[pygame.K_z]:  # Avancer
            print("avancer !")
            igs.output_set_impulsion("Z")
        if keys[pygame.K_s]:  # Reculer
            igs.output_set_impulsion("S")
        if keys[pygame.K_q]:  # Gauche
            igs.output_set_impulsion("Q")
        if keys[pygame.K_d]:  # Droite
            igs.output_set_impulsion("D")

        # Rotation
        if keys[pygame.K_e]:  # Tourner à droite
            igs.output_set_impulsion("E")
        if keys[pygame.K_a]:  # Tourner à gauche
            igs.output_set_impulsion("A")
'''

from pynput import keyboard, mouse

# Fonction appelée à chaque pression de touche
def on_press(key):
    try:
        if key.char=='a':
            igs.output_set_impulsion("A")
        if key.char=='e':
            igs.output_set_impulsion("E")
        if key.char=='z':
            igs.output_set_impulsion("Z")
        if key.char=='q':
            igs.output_set_impulsion("Q")
        if key.char=='s':
            igs.output_set_impulsion("S")
        if key.char=='d':
            igs.output_set_impulsion("D")
        if key.char=='m':
            igs.output_set_impulsion("M")
        if key.char=='n':
            igs.output_set_impulsion("N")
    except AttributeError:
        print(f'Touche spéciale appuyée: {key}')

# Fonction appelée à chaque relâchement de touche
def on_release(key):
    if key == keyboard.Key.esc:  # Arrêter le programme quand "Echap" est pressée
        return False

# Fonction appelée lors d'un clic de souris
def on_click(x, y, button, pressed):
    if pressed:
        if button == mouse.Button.left:
            igs.output_set_impulsion("click_left")
        if button == mouse.Button.right:
            igs.output_set_impulsion("click_right")

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

    igs.output_create("A", igs.IMPULSION_T, None)
    igs.output_create("E", igs.IMPULSION_T, None)
    igs.output_create("Z", igs.IMPULSION_T, None)
    igs.output_create("Q", igs.IMPULSION_T, None)
    igs.output_create("S", igs.IMPULSION_T, None)
    igs.output_create("D", igs.IMPULSION_T, None)
    igs.output_create("M", igs.IMPULSION_T, None)
    igs.output_create("N", igs.IMPULSION_T, None)
    igs.output_create("click_left", igs.IMPULSION_T, None)
    igs.output_create("click_right", igs.IMPULSION_T, None)

    igs.start_with_device(sys.argv[2], int(sys.argv[3]))

    # Ecouteur de clavier
    keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    keyboard_listener.start()

    # Ecouteur de souris
    mouse_listener = mouse.Listener(on_click=on_click)
    mouse_listener.start()

    # Attendre la fin des écouteurs
    keyboard_listener.join()
    mouse_listener.join()

    igs.stop()