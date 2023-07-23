import time
import numpy as np
import mss
from lib.Aimbot import Aimbot
import json
from pynput import keyboard
import os


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


def update_config_file(new_normal_scale, new_targeting_scale):
    config_file = get_config_file()

    normal_scale = config_file["normal_scale"]
    if new_normal_scale:
        normal_scale = new_normal_scale

    targeting_scale = config_file["targeting_scale"]
    if new_targeting_scale:
        targeting_scale = new_targeting_scale

    config_data = {"normal_scale": normal_scale,
                   "targeting_scale": targeting_scale}

    with open('lib/config.json', 'w', encoding='utf-8') as f:
        json.dump(config_data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    print(" ____________________ .____    ._____________  ____________________\n",
          "\_   _____/\_   ___ \|    |   |   \______   \/   _____/\_   _____/\n",
          " |    __)_ /    \  \/|    |   |   ||     ___/\_____  \  |    __)_\n",
          " |        \\\\     \___|    |___|   ||    |    /        \ |        \\\n",
          "/_______  / \______  /_______ \___||____|   /_______  //_______  /\n",
          "        \/         \/        \/                     \/         \/")
    print("                     (Neural Network Aimbot)")
    print("")

    print("[1] Type 'R' to run the aimbot")
    print("[2] Type 'E' to edit a configuration file")
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

                print("[INFO] New configuration file created.")
                print("")
                print("----------------------------------------")
                print("")
                print("Quitting...")
                time.sleep(3)
                exit()

            else:
                create_default_config_file()

                print("[INFO] New configuration file successfully created.")
                print("")
                print("----------------------------------------")
                print("")
                print("Quitting...")
                time.sleep(3)
                exit()

        case "H":
            print("[INFO] Aimbot Calibration!")
            print("    * ")
            print("    * ")
            print("    * ")
            print("")
            print("[INFO] TIPS")
            print("    * ")
            print("    * ")
            print("    * ")
            print("")
            print("[INFO] Press any key to continue")

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
            print("[INFO] Aimbot successfully activated")
            print("")
            print("[1] Hold f2 to enable the aimbot")
            print("[2] Press f3 to quit")
            print("")

            listener = keyboard.Listener(on_release=on_key_release, on_press=on_key_press)
            listener.start()

            while aimbot.running:
                screenshot = np.array(mss.mss().grab(aimbot.screenshot_region))

                detection = aimbot.inference_dist(screenshot)

                if aimbot.aiming_status == "ON":
                    aimbot.move_crosshair(detection)

            print("----------------------------------------")
            print("")
            print("Quitting...")
            time.sleep(3)
            exit()
