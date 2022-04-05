import time
import numpy as np
import mss
from lib.Aimbot import Aimbot
import json
from pynput import keyboard
import pyfiglet
import os


def on_key_release(key):
    try:
        if key == keyboard.Key.f1:
            aimbot.update_aimimg_status("OFF")
        if key == keyboard.Key.f3:
            aimbot.running = False
    except NameError:
        pass


def on_key_press(key):
    try:
        if key == keyboard.Key.f1:
            aimbot.update_aimimg_status("ON")
    except NameError:
        pass


def get_config_file():
    with open("lib/config.json") as f:
        config_data = json.load(f)
    return config_data


def create_config_file():
    if os.path.isfile("lib/config.json"):
        os.remove("lib/config.json")

    xy_sensitivity = None
    targeting_sensitivity = None
    fps = None

    valid_input_1 = False
    while not valid_input_1:
        xy_sensitivity = input("Please input your in-game X sensitivity: ")

        try:
            xy_sensitivity = float(xy_sensitivity)
            valid_input_1 = True
        except ValueError:
            print("[ERROR] Invalid input")
        print("")

    valid_input_2 = False
    while not valid_input_2:
        targeting_sensitivity = input("Please input your in-game targeting sensitivity: ")

        try:
            targeting_sensitivity = float(targeting_sensitivity)
            valid_input_2 = True
        except ValueError:
            print("[ERROR] Invalid input")
        print("")

    valid_input_3 = False
    while not valid_input_3:
        fps = input("Please input the average fps of your game: ")

        try:
            fps = float(fps)
            valid_input_3 = True
        except ValueError:
            print("[ERROR] Invalid input")
        print("")

    normal_scale = float(11 / xy_sensitivity)
    targeting_scale = float(11 / (xy_sensitivity * (targeting_sensitivity / 100)))

    config_data = {"xy_sensitivity": xy_sensitivity,
                   "targeting_sensitivity": targeting_sensitivity,
                   "fps": fps,
                   "normal_scale": normal_scale,
                   "targeting_scale": targeting_scale}

    with open('lib/config.json', 'w', encoding='utf-8') as f:
        json.dump(config_data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    eclipse_string = pyfiglet.figlet_format("ECLIPSE", "Graffiti")
    print(eclipse_string, "                   (Neural Network Aimbot)")
    print("")

    print("[1] Type 'R' to run the aimbot")
    print("[2] Type 'E' to edit/create a configuration file")
    print("[3] Type 'Q' to quit the program")
    print("")

    option = None

    valid_input = False
    while not valid_input:
        option = input("Please select a option: ")

        if option == "Q" or option == "E" or option == "R":
            valid_input = True
        else:
            print("[ERROR] Invalid input")
        print("")

    print("----------------------------------------")
    print("")

    if option == "Q" or option is None:
        print("Quitting... ")
        time.sleep(4)
        quit()
    elif option == "E":
        create_config_file()

        print("----------------------------------------")
        print("")
        print("[INFO] Configuration file successfully created.")
        print("")
        print("----------------------------------------")
        print("")
        print("Quitting...")
        time.sleep(4)
        exit()
    elif option == "R":
        if not os.path.isfile("lib/config.json"):
            print("[ERROR] Must have a configuration file to run the aimbot")
            print("")
            create_config_file()

            print("----------------------------------------")
            print("")
            print("[INFO] Configuration file successfully created.")
            print("")
            print("----------------------------------------")
            print("")

        print("[INFO] Loading neural network model")

        config_file = get_config_file()
        aimbot = Aimbot(0.6, 1, config_file["normal_scale"], config_file["targeting_scale"], config_file["fps"])
        print("")

        print("----------------------------------------")
        print("")
        print("[INFO] Aimbot successfully activated")
        print("")
        print("[1] Hold f1 to enable the aimbot")
        print("[2] Press f3 to quit")
        print("")

        listener = keyboard.Listener(on_release=on_key_release, on_press=on_key_press)
        listener.start()

        while aimbot.running:
            start_time = time.time()
            screenshot = np.array(mss.mss().grab(aimbot.screenshot_region))

            detection = aimbot.inference(screenshot)

            aimbot.update_running_frame_time(start_time, time.time())

            if aimbot.aiming_status == "ON":
                aimbot.move_crosshair(detection)

        print("----------------------------------------")
        print("")
        print("Quitting...")
        time.sleep(4)
        exit()
