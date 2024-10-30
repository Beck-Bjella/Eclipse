import time
import numpy as np
import mss
import json
from lib.Aimbot import Aimbot
from pynput import keyboard
import os
import cv2


def on_key_release(key):
    """
    Handles key release events.
    """
    try:
        if key == keyboard.Key.f2:
            aimbot.update_aimimg_status("OFF")
        if key == keyboard.Key.f3:
            aimbot.running = False
    except NameError:
        pass


def on_key_press(key):
    """
    Handles key press events.
    """
    try:
        if key == keyboard.Key.f2:
            aimbot.update_aimimg_status("ON")

    except NameError:
        pass


def get_config_file():
    """
    Loads an existing configuration file.
    """
    if not os.path.isfile("lib/config.json"):
        return False
    else:
        with open("lib/config.json") as f:
            config_data = json.load(f)

        return config_data


def create_config_file():
    """
    Creates a configuration file with temporary settings.
    """
    if os.path.isfile("lib/config.json"):
        os.remove("lib/config.json")

    config_data = {"normal_scale": 0.1, "targeting_scale": 0.2}

    with open('lib/config.json', 'w', encoding='utf-8') as f:
        json.dump(config_data, f, ensure_ascii=False, indent=4)


def update_config_file():
    """
    Updates the configuration file with inputted values.
    """
    print("[?] Updating file\n")

    config_data = get_config_file()
    normal_scale = config_data["normal_scale"]
    targeting_scale = config_data["targeting_scale"]
    print(f"Current Normal Scale: {normal_scale}")
    print(f"Current Targeting Scale: {normal_scale}\n")

    # Update normal scale with user input
    valid_input = False
    while not valid_input:
        new_normal_scale = input("Enter a new normal scale: ")
        try:
            normal_scale = float(new_normal_scale)
            valid_input = True
        except ValueError:
            print("[!] Invalid input\n")

    # Update targeting scale with user input
    valid_input = False
    while not valid_input:
        new_targeting_scale = input("Enter a new targeting scale: ")
        try:
            targeting_scale = float(new_targeting_scale)
            valid_input = True
        except ValueError:
            print("[!] Invalid input\n")

    config_data = {"normal_scale": normal_scale, "targeting_scale": targeting_scale}

    # Save new configuration
    with open('lib/config.json', 'w', encoding='utf-8') as f:
        json.dump(config_data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    """
    Starting point of the program. Handles main menu and input logic.
    """
    print(r" ____________________ .____    ._____________  ____________________")
    print(r"\_   _____/\_   ___ \|    |   |   \______   \/   _____/\_   _____/")
    print(r" |    __)_ /    \  \/|    |   |   ||     ___/\_____  \  |    __)_")
    print(r" |        \\     \___|    |___|   ||    |    /        \ |        \ ")
    print(r"/_______  / \______  /_______ \___||____|   /_______  //_______  /")
    print(r"        \/         \/        \/                     \/         \/")
    print("                     (Neural Network Aimbot)\n")

    # User options
    print("[1] Type 'R' to run the aimbot")
    print("[2] Type 'E' to edit/create a configuration file")
    print("[3] Type 'H' for instructions/help")
    print("[4] Type 'Q' to quit the program\n")

    # User input
    option = None
    valid_input = False
    while not valid_input:
        option = input("Please select an option: ")

        if option in {"Q", "E", "R", "H"}:
            valid_input = True
        else:
            print("[!] Invalid input\n")

    print("----------------------------------------\n")

    # Handle user input
    match option:
        case "Q":  # Quit program
            print("Quitting... ")
            time.sleep(3)
            quit()

        case "E":  # Edit or create configuration file
            if not get_config_file():
                create_config_file()
                print("[!] No Configuration file found\n")
                print("[?] Creating file...\n")
                time.sleep(3)
                print("----------------------------------------\n")
                print("[?] New configuration file created\n")
                print("----------------------------------------\n")
                print("Quitting...")
                time.sleep(3)
                exit()
            else:
                update_config_file()
                print("[?] Configuration file successfully updated\n")
                print("----------------------------------------\n")
                print("Quitting...")
                time.sleep(3)
                exit()

        case "H":  # Help and instructions
            print("[?] Aimbot Calibration")
            print("    - Adjust sensitivity to improve aim accuracy")
            print("    - General rules: Quick/snappy movements = too high sensitivity")
            print("                      Slow/no movements = too low sensitivity")
            print("    - Recommended sensitivity adjustment in increments of 0.1\n")
            print("    - Optimal sensitivity depends on factors like Mouse DPI and Game Sensitivity\n")
            print("[?] Hardware Requirements")
            print("    - Requires an NVIDIA GPU on a Windows Computer\n")
            print("[?] Optimizations")
            print("    - Close unnecessary tabs for improved performance\n")
            print("    - Lower in-game graphics settings for faster aimbot performance\n")
            print("[?] Press any key to continue")
            input("")  # Pause for user to review instructions
            print("----------------------------------------\n")
            print("Quitting...")
            time.sleep(3)
            exit()

        case "R":  # Run aimbot
            # Load configuration file
            if not get_config_file():
                print("[!] Must have a configuration file to run the aimbot\n")
                print("----------------------------------------\n")
                print("Quitting...")
                time.sleep(3)
                exit()

            # Initialize aimbot
            config_file = get_config_file()
            aimbot = Aimbot(0.5, 0.45, config_file["normal_scale"], config_file["targeting_scale"], "1920x1080")
            time.sleep(1)
            print("\n----------------------------------------\n")
            print("[?] Aimbot successfully activated\n")
            print("[1] Hold f2 to enable the aimbot")
            print("[2] Press f3 to quit\n")

            # Setup key listeners
            listener = keyboard.Listener(on_release=on_key_release, on_press=on_key_press)
            listener.start()

            # Main capture loop
            sct = mss.mss()
            while aimbot.running:
                screenshot = np.array(sct.grab(aimbot.screenshot_region))

                # Distance based detection
                detection = aimbot.inference_dist(screenshot)
                if aimbot.visualize:
                    drawn = aimbot.draw_detection(screenshot, detection)
                    cv2.imshow('Aimbot Visualization', drawn)
                    cv2.waitKey(1)

                # Move crosshair
                if aimbot.aiming_status == "ON":
                    aimbot.move_crosshair(detection)

            # Close Open CV windows
            if aimbot.visualize:
                cv2.destroyAllWindows()

            print("----------------------------------------\n")
            print("Quitting...")
            time.sleep(3)
            exit()
