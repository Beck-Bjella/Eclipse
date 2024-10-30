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

    config_data = {
        "normal_scale": 0.1,
        "targeting_scale": 0.2,
        "visualize": True,
        "resolution": "1920x1080"
    }

    with open('lib/config.json', 'w', encoding='utf-8') as f:
        json.dump(config_data, f, ensure_ascii=False, indent=4)


def update_config_file():
    """
    Updates the configuration file with inputted values.
    """
    print("[?] Updating file\n")

    config_data = get_config_file()
    print(f"Current Configuration:")
    print(f" - Normal Scale: {config_data["normal_scale"]}")
    print(f" - Targeting Scale: {config_data["targeting_scale"]}")
    print(f" - Visualize: {config_data["visualize"]}")
    print(f" - Resolution: {config_data["resolution"]}\n")

    # Update normal scale with user input
    valid_input = False
    while not valid_input:
        new_normal_scale = input("Enter a new normal scale: ")
        try:
            normal_scale = float(new_normal_scale)
            valid_input = True
        except ValueError:
            print("[!] Invalid input\n")
    print()

    # Update targeting scale with user input
    valid_input = False
    while not valid_input:
        new_targeting_scale = input("Enter a new targeting scale: ")
        try:
            targeting_scale = float(new_targeting_scale)
            valid_input = True
        except ValueError:
            print("[!] Invalid input\n")
    print()

    # Update visualization with user input
    valid_input = False
    while not valid_input:
        new_visualize = input("Enable visualization? (Y/N): ")
        if new_visualize in {"Y", "N"}:
            visualize = True if new_visualize == "Y" else False
            valid_input = True
        else:
            print("[!] Invalid input\n")
    print()

    # Update resolution with user input
    valid_input = False
    while not valid_input:
        print("[?] Valid Resolutions:")
        print("    - 1920x1080")
        print("    - 1280x720")
        new_resolution = input("Enter a new resolution: ")
        if new_resolution in {"1920x1080", "1280x720"}:
            resolution = new_resolution
            valid_input = True
        else:
            print("[!] Invalid input\n")
    print()

    # Save new configuration
    config_data = {
        "normal_scale": normal_scale,
        "targeting_scale": targeting_scale,
        "visualize": visualize,
        "resolution": resolution
    }
    with open('lib/config.json', 'w', encoding='utf-8') as f:
        json.dump(config_data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    """
    Starting point of the program. Handles main menu and input logic.
    """
    # Create a configuration file
    if not get_config_file():
        create_config_file()

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
            print("        - visualize: Set to `true` to open a separate window for displaying bounding boxes around detected targets, useful for calibration.")
            print("        - game_resolution: Set to match your Fortnite resolution for best accuracy (options: '1920x1080', '1280x720').\n")

            print("[?] Calibration Tips")
            print("    - Calibration may take a few attempts for best results.")
            print("    - Adjust in 0.1 increments for both normal_scale and targeting_scale.")
            print("    - If movements are too fast, lower sensitivity; if too slow, increase it.\n")

            print("[?] Key Controls")
            print("    - Press 'F2' to enable/disable the aimbot (hold to keep it active).")
            print("    - Press 'F3' to quit the program.\n")

            print("[?] Requirements and Tips")
            print("    - Requires an NVIDIA GPU and a Windows computer.")
            print("    - Closing other programs can improve responsiveness.")
            print("    - Lower Fortnite graphics settings to increase performance.")
            print("    - Close and restart Eclipse after making any changes to `config.json`.\n")

            print("Press any key to return to the main menu.")
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
                config_file["visualize"],
                config_file["resolution"]
            )
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

                # Visualize detection
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
