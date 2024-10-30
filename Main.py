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
            if not aimbot.visualize:
                aimbot.visualize_open = True
            aimbot.visualize = not aimbot.visualize
        if key == keyboard.Key.f4:
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

    config_data = {
        "normal_scale": 0.1,
        "targeting_scale": 0.2,
        "resolution": "1920x1080"
    }

    with open('lib/config.json', 'w', encoding='utf-8') as f:
        json.dump(config_data, f, ensure_ascii=False, indent=4)


def validate_config(config_path="lib/config.json"):
    """
    Validates the configuration file.
    """
    # Load the config file
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found at {config_path}.")
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format in config file. Please check for syntax errors.")

    # Expected config format
    expected_config = {
        "normal_scale": (float, 0.0),
        "targeting_scale": (float, 0.0),
        "resolution": (str, ["1920x1080", "1280x720"])
    }

    # Check each value
    for key, (expected_type, valid_values) in expected_config.items():
        if key not in config:
            raise KeyError(f"Missing '{key}' in config file.")
        if not isinstance(config[key], expected_type):
            raise TypeError(f"Invalid type for '{key}' in config file. Expected {expected_type.__name__} not {type(config[key]).__name__}.")
        if isinstance(valid_values, list) and config[key] not in valid_values:
            raise ValueError(f"Invalid value for '{key}' in config file. Expected one of {valid_values}.")


if __name__ == "__main__":
    """
    Starting point of the program. Handles main menu and input logic.
    """
    # Create a configuration file
    if not get_config_file():
        create_config_file()

    # Validate the configuration file
    validate_config()

    print(r" ____________________ .____    ._____________  ____________________")
    print(r"\_   _____/\_   ___ \|    |   |   \______   \/   _____/\_   _____/")
    print(r" |    __)_ /    \  \/|    |   |   ||     ___/\_____  \  |    __)_")
    print(r" |        \\     \___|    |___|   ||    |    /        \ |        \ ")
    print(r"/_______  / \______  /_______ \___||____|   /_______  //_______  /")
    print(r"        \/         \/        \/                     \/         \/")
    print("                     (Neural Network Aimbot)\n")

    # User options
    print("[1] Type 'R' to run the aimbot")
    print("[3] Type 'H' for instructions/help")
    print("[4] Type 'Q' to quit the program\n")

    # User input
    option = None
    valid_input = False
    while not valid_input:
        option = input("Please select an option: ")

        if option in {"Q", "R", "H"}:
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

        case "H":  # Help and instructions
            print("[?] Configuration Guide")
            print("    - To configure the aimbot, edit `lib/config.json` directly with a text editor.")
            print("    - Configuration options:")
            print("        - normal_scale: Controls general aiming sensitivity, corresponding to Fortnite’s X/Y sensitivity.")
            print("        - targeting_scale: Controls sensitivity when aiming down sights (right-click), corresponding to Fortnite’s targeting sensitivity.")
            print("             [TIP]: If in-game targeting sensitivity is set to 50% of X/Y, try setting targeting_scale to about 2x normal_scale.")
            print("        - game_resolution: Set to match your Fortnite resolution (options: '1920x1080', '1280x720').\n")

            print("[?] Calibration Tips")
            print("    - Calibration may take a few attempts for best results.")
            print("    - Adjust in 0.1 increments for both normal_scale and targeting_scale.")
            print("    - If movements are too chaotic, lower sensitivity; if too slow, increase it.\n")

            print("[?] Key Controls")
            print("    - Hold 'F2' to enable the aimbot (hold to keep it active).")
            print("    - Press 'F3' to toggle visualization window.")
            print("    - Press 'F4' to quit the program.\n")

            print("[?] Requirements and Tips")
            print("    - Requires an NVIDIA GPU and a Windows computer.")
            print("    - Closing other programs can improve responsiveness.")
            print("    - Lower Fortnite graphics settings to increase performance.")
            print("    - Close and restart Eclipse after making any changes to `config.json`.\n")

            print("Press any key to quit.")
            input("")  # Pauses to let the user read the help section
            print("----------------------------------------\n")
            print("Quitting...")
            time.sleep(3)
            exit()

        case "R":  # Run aimbot
            # Initialize aimbot
            config_file = get_config_file()
            aimbot = Aimbot(
                0.5,
                0.45,
                config_file["normal_scale"],
                config_file["targeting_scale"],
                config_file["resolution"]
            )
            time.sleep(1)
            print("\n----------------------------------------\n")
            print("[?] Aimbot successfully activated\n")
            print("[1] Hold f2 to enable the aimbot")
            print("[2] Press f3 to toggle visualization window")
            print("[3] Press f4 to quit\n")

            # Setup key listeners
            listener = keyboard.Listener(on_release=on_key_release, on_press=on_key_press)
            listener.start()

            # Main capture loop
            sct = mss.mss()
            visualize_open = False
            while aimbot.running:
                screenshot = np.array(sct.grab(aimbot.screenshot_region))

                # Distance based detection
                detection = aimbot.inference_dist(screenshot)

                # Visualize detection
                if aimbot.visualize:
                    drawn = aimbot.draw_detection(screenshot, detection)
                    cv2.imshow('Aimbot Visualization', drawn)
                    cv2.waitKey(1)
                else:
                    if aimbot.visualize_open:
                        cv2.destroyAllWindows()
                        aimbot.visualize_open = False

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
