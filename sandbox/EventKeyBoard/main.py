#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  EventKeyBoard
#  Created by Ingenuity i/o on 2024/10/22
#

import sys
import ingescape as igs
from pynput import keyboard, mouse

pressed_keys = []

def on_press(key):
    global pressed_keys
    try:
        if key.char not in pressed_keys:
            pressed_keys.append(key.char)
        for k in pressed_keys:
            if k=='a':
                igs.output_set_impulsion("A")
            if k=='e':
                igs.output_set_impulsion("E")
            if k=='z':
                igs.output_set_impulsion("Z")
            if k=='q':
                igs.output_set_impulsion("Q")
            if k=='s':
                igs.output_set_impulsion("S")
            if k=='d':
                igs.output_set_impulsion("D")
            if k=='m':
                igs.output_set_impulsion("M")
            if k=='n':
                igs.output_set_impulsion("N")
    except AttributeError:
        print(f'Touche spéciale appuyée: {key}')

def on_release(key):
    global pressed_keys
    try:
        if key.char in pressed_keys:
            pressed_keys.remove(key.char)
        print("Touches appuyées :", pressed_keys)
    except AttributeError:
        pass
    if key == keyboard.Key.esc:
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