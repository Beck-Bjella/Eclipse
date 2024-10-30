import time
import numpy as np
import mss
import json
from lib.Aimbot import Aimbot
from pynput import keyboard
import os
import cv2


def on_key_release(key):
    try:
        if key == keyboard.Key.f2:
            aimbot.update_aimimg_status("OFF")
        if key == keyboard.Key.f3:
            aimbot.running = False
    except NameError:
        pass


def on_key_press(key):
    try:
        if key == keyboard.Key.f2:
            aimbot.update_aimimg_status("ON")

    except NameError:
        pass


def get_config_file():
    if not os.path.isfile("lib/config.json"):
        return False
    else:
        with open("lib/config.json") as f:
            config_data = json.load(f)

        return config_data


def create_default_config_file():
    if os.path.isfile("lib/config.json"):
        os.remove("lib/config.json")

    config_data = {"normal_scale": 0.1,
                   "targeting_scale": 0.2}

    with open('lib/config.json', 'w', encoding='utf-8') as f:
        json.dump(config_data, f, ensure_ascii=False, indent=4)


def update_config_file():
    print("[?] Updating file")
    print("")

    config_data = get_config_file()

    normal_scale = config_data["normal_scale"]
    targeting_scale = config_data["targeting_scale"]
    print(f"Current Normal Scale: {normal_scale}")
    print(f"Current Targeting Scale: {normal_scale}")
    print()

    valid_input = False
    while not valid_input:
        new_normal_scale = input("Enter a new normal scale: ")

        try:
            normal_scale = float(new_normal_scale)
            valid_input = True

        except ValueError:
            print("[!] Invalid input")

        print("")

    valid_input = False
    while not valid_input:
        new_targeting_scale = input("Enter a new targeting scale: ")

        try:
            targeting_scale = float(new_targeting_scale)
            valid_input = True

        except ValueError:
            print("[!] Invalid input")

        print("")

    print("----------------------------------------")
    print("")

    config_data = {"normal_scale": normal_scale,
                   "targeting_scale": targeting_scale}

    with open('lib/config.json', 'w', encoding='utf-8') as f:
        json.dump(config_data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    print(r" ____________________ .____    ._____________  ____________________")
    print(r"\_   _____/\_   ___ \|    |   |   \______   \/   _____/\_   _____/")
    print(r" |    __)_ /    \  \/|    |   |   ||     ___/\_____  \  |    __)_")
    print(r" |        \\     \___|    |___|   ||    |    /        \ |        \ ")
    print(r"/_______  / \______  /_______ \___||____|   /_______  //_______  /")
    print(r"        \/         \/        \/                     \/         \/")
    print("                     (Neural Network Aimbot)")
    print("")

    print("[1] Type 'R' to run the aimbot")
    print("[2] Type 'E' to edit/create a configuration file")
    print("[3] Type 'H' for instructions/help")
    print("[4] Type 'Q' to quit the program")
    print("")

    option = None

    valid_input = False
    while not valid_input:
        option = input("Please select a option: ")

        if option == "Q" or option == "E" or option == "R" or option == "H":
            valid_input = True
        else:
            print("[!] Invalid input")
        print("")

    print("----------------------------------------")
    print("")

    match option:
        case "Q":
            print("Quitting... ")
            time.sleep(3)
            quit()

        case "E":
            if not get_config_file():
                create_default_config_file()

                print("[!] No Configuration file found")
                print("")
                print("[?] Creating file...")
                print("")
                time.sleep(3)
                print("----------------------------------------")
                print("")
                print("[?] New configuration file created")
                print("")
                print("----------------------------------------")
                print("")
                print("Quitting...")
                time.sleep(3)
                exit()

            else:
                update_config_file()

                print("[?] New configuration file successfully created")
                print("")
                print("----------------------------------------")
                print("")
                print("Quitting...")
                time.sleep(3)
                exit()

        case "H":
            print("[?] Aimbot Calibration")
            print("    - If the aimbot is barely moving then you need to increase the sensitivity")
            print("    - If the aimbot is oscillating around a target then you need to lower the sensitivity")
            print("")
            print("    - General rules")
            print("        - Quick/snappy movements = too high sensitivity")
            print("        - Slow/no movements = too low sensitivity")
            print("")
            print("    - Sensitivity scales from (0.0 - 1.0)")
            print("    - It's recommended to change sensitivity in chucks of 0.1")
            print("")
            print("    - The value that works best for you is based on your")
            print("        - Mouse DPI")
            print("        - Game Sensitivity")
            print("")
            print("[?] Hardware Requirements")
            print("    - You must have a NVIDIA GPU")
            print("    - You must be on a Windows Computer")
            print("")
            print("[?] Optimisations")
            print("    - Close other tabs on your computer")
            print("")
            print("    - The faster your GPU the better the aimbot will work")
            print("")
            print("    - The lower your graphics in the game are the faster the aimbot will run")
            print("        - This can make a huge difference")
            print("")
            print("[?] Press any key to continue")

            wait = input("")

            print("----------------------------------------")
            print("")
            print("Quitting...")
            time.sleep(3)
            exit()

        case "R":
            if not get_config_file():
                print("[!] Must have a configuration file to run the aimbot")
                print("")
                print("----------------------------------------")
                print("")
                print("Quitting...")
                time.sleep(3)
                exit()

            config_file = get_config_file()
            aimbot = Aimbot(0.5, 0.45, config_file["normal_scale"], config_file["targeting_scale"], "1920x1080")
            time.sleep(1)
            print("")

            print("----------------------------------------")
            print("")
            print("[?] Aimbot successfully activated")
            print("")
            print("[1] Hold f2 to enable the aimbot")
            print("[2] Press f3 to quit")
            print("")

            listener = keyboard.Listener(on_release=on_key_release, on_press=on_key_press)
            listener.start()

            sct = mss.mss()
            last = None
            while aimbot.running:
                screenshot = np.array(sct.grab(aimbot.screenshot_region))

                detection = aimbot.inference_dist(screenshot)

                if aimbot.visualize:
                    drawn = aimbot.draw_detection(screenshot, detection)

                    cv2.imshow('Eclipse', drawn)
                    cv2.waitKey(1)

                if aimbot.aiming_status == "ON":
                    aimbot.move_crosshair(detection)

            if aimbot.visualize:
                cv2.destroyAllWindows()

            print("----------------------------------------")
            print("")
            print("Quitting...")
            time.sleep(3)
            exit()
