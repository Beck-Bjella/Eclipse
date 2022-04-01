import time
import numpy as np
import mss
from lib.Aimbot import Aimbot
import tkinter as tk
from tkinter import ttk
import json
from pynput import keyboard
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


class eclipse_menu(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Eclipse")
        self.geometry("720x360")
        self.resizable(False, False)

        eclipse_string = "___________________  ___     _____________  ___________________ \n" \
                         "\_   _____/_   ___ \|   |   |   |______   \/   _____/_   _____/ \n" \
                         " |    __)_/    \  \/|   |   |   ||     ___/\_____  \ |    __)_  \n" \
                         " |        \     \____   |___|   ||    |    /        \|        \ \n" \
                         "/_______  /\______  /______ \___||____|   /_______  /_______  / \n" \
                         "        \/        \/       \/                     \/        \/  \n"

        eclipse_text = tk.Label(self, text=eclipse_string, font=("Courier", 8))
        eclipse_text.place(x=135, y=0)

        self.xy_sensitivity_input = ttk.Entry(self)
        self.xy_sensitivity_input.place(x=85, y=130)
        xy_sensitivity_label = ttk.Label(self, text="XY Sensitivity")
        xy_sensitivity_label.place(x=85, y=110)

        self.targeting_sensitivity_input = ttk.Entry(self)
        self.targeting_sensitivity_input.place(x=500, y=130)
        targeting_sensitivity_label = ttk.Label(self, text="Targeting Sensitivity")
        targeting_sensitivity_label.place(x=500, y=110)

        self.fps_input = ttk.Entry(self)
        self.fps_input.place(x=320, y=250)
        fps_label = ttk.Label(self, text="FPS")
        fps_label.place(x=320, y=230)

        self.start_button = ttk.Button(text="Start", command=self.start_button_press)
        self.start_button.place(x=320, y=130)

        self.load_gui_data()

    def load_gui_data(self):
        if os.path.isfile("lib/config.json"):
            config_data = get_config_file()

            xy_sensitivity = config_data["xy_sensitivity"]
            targeting_sensitivity = config_data["targeting_sensitivity"]
            fps = config_data["fps"]

            self.xy_sensitivity_input.insert(0, xy_sensitivity)
            self.targeting_sensitivity_input.insert(0, targeting_sensitivity)
            self.fps_input.insert(0, fps)

    def start_button_press(self):
        global run_aimbot
        run_aimbot = True

        if os.path.isfile("lib/config.json"):
            os.remove("lib/config.json")

        xy_sensitivity = float(self.xy_sensitivity_input.get())
        targeting_sensitivity = float(self.targeting_sensitivity_input.get())
        fps = float(self.fps_input.get())

        normal_scale = float(11 / float(xy_sensitivity))
        targeting_scale = float(11 / (float(xy_sensitivity) * ((float(targeting_sensitivity)) / 100)))

        config_data = {"xy_sensitivity": xy_sensitivity,
                       "targeting_sensitivity": targeting_sensitivity,
                       "fps": fps,
                       "normal_scale": normal_scale,
                       "targeting_scale": targeting_scale}

        with open('lib/config.json', 'w', encoding='utf-8') as f:
            json.dump(config_data, f, ensure_ascii=False, indent=4)

        self.destroy()


if __name__ == "__main__":
    run_aimbot = False

    app = eclipse_menu()
    app.mainloop()

    if run_aimbot:

        config_file = get_config_file()
        aimbot = Aimbot(0.3, 0.9, config_file["normal_scale"], config_file["targeting_scale"], config_file["fps"])

        listener = keyboard.Listener(on_release=on_key_release, on_press=on_key_press)
        listener.start()

        while aimbot.running:
            start_time = time.time()
            screenshot = np.array(mss.mss().grab(aimbot.screenshot_region))

            detection = aimbot.inference(screenshot)

            aimbot.update_frame_average(start_time, time.time())

            print(aimbot.is_targeting())

            if aimbot.aiming_status == "ON":
                aimbot.move_crosshair(detection)

            # print(aimbot.running_frame_average)
