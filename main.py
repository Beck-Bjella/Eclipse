import time
import numpy as np
import mss
from lib.aimbot import aimbot
import tkinter as tk
from tkinter import ttk
import json
from pynput import keyboard
import cv2 as cv
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
    global slot_1_hotkey
    global slot_2_hotkey
    global slot_3_hotkey
    global slot_4_hotkey
    global slot_5_hotkey
    global shotgun_slot

    try:
        if key == keyboard.Key.f1:
            aimbot.update_aimimg_status("ON")

        if 'char' in dir(key):
            if key.char == slot_1_hotkey:
                aimbot.holding_shotgun = False
            if key.char == slot_2_hotkey:
                aimbot.holding_shotgun = False
            if key.char == slot_3_hotkey:
                aimbot.holding_shotgun = False
            if key.char == slot_4_hotkey:
                aimbot.holding_shotgun = False
            if key.char == slot_5_hotkey:
                aimbot.holding_shotgun = False

            if shotgun_slot == 1:
                if key.char == slot_1_hotkey:
                    aimbot.holding_shotgun = True
            if shotgun_slot == 2:
                if key.char == slot_2_hotkey:
                    aimbot.holding_shotgun = True
            if shotgun_slot == 3:
                if key.char == slot_3_hotkey:
                    aimbot.holding_shotgun = True
            if shotgun_slot == 4:
                if key.char == slot_4_hotkey:
                    aimbot.holding_shotgun = True
            if shotgun_slot == 5:
                if key.char == slot_5_hotkey:
                    aimbot.holding_shotgun = True
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

        self.normal_scale = 0
        self.normal_scale_slider = ttk.Scale(self, from_=0, to=100, length=600, command=self.update_normal_scale_slider, orient='horizontal')
        self.normal_scale_slider.place(x=60, y=200)
        self.normal_scale_label = ttk.Label(self, text="Normal Scale: ")
        self.normal_scale_label.place(x=312, y=180)

        self.targeting_scale = 0
        self.targeting_scale_slider = ttk.Scale(self, from_=0, to=100, length=600, command=self.update_targeting_scale_slider, orient='horizontal')
        self.targeting_scale_slider.place(x=60, y=310)
        self.targeting_scale_label = ttk.Label(self, text="Targeting Scale: ")
        self.targeting_scale_label.place(x=312, y=290)

        self.start_button = ttk.Button(text="Start", command=self.start_button_press)
        self.start_button.place(x=320, y=130)

        self.load_gui_data()

    def update_normal_scale_slider(self, event):
        self.normal_scale = float(round((self.normal_scale_slider.get() / 100), 2))
        self.normal_scale_label.configure(text="Normal Scale: " + str(self.normal_scale))

    def update_targeting_scale_slider(self, event):
        self.targeting_scale = float(round((self.targeting_scale_slider.get() / 100), 2))
        self.targeting_scale_label.configure(text="Targeting Scale: " + str(self.targeting_scale))

    def load_gui_data(self):
        if os.path.isfile("lib/config.json"):
            config_data = get_config_file()

            self.normal_scale_slider.set(int(config_data["normal_scale"] * 100))
            self.targeting_scale_slider.set(int(config_data["targeting_scale"] * 100))
        else:
            self.normal_scale_slider.set(50)
            self.targeting_scale_slider.set(50)

    def start_button_press(self):
        global run_aimbot
        run_aimbot = True

        if os.path.isfile("lib/config.json"):
            os.remove("lib/config.json")

        config_data = {"normal_scale": float(self.normal_scale),
                       "targeting_scale": float(self.targeting_scale)}

        with open('lib/config.json', 'w', encoding='utf-8') as f:
            json.dump(config_data, f, ensure_ascii=False, indent=4)

        self.destroy()


if __name__ == "__main__":
    run_aimbot = False

    app = eclipse_menu()
    app.mainloop()

    if run_aimbot:
        config_file = get_config_file()
        aimbot = aimbot(0.5, 1, config_file["normal_scale"], config_file["targeting_scale"], 0.0001)

        listener = keyboard.Listener(on_release=on_key_release, on_press=on_key_press)
        listener.start()

        while aimbot.running:
            screenshot = np.array(mss.mss().grab(aimbot.screenshot_region))

            results = aimbot.main(screenshot)

            cv.imshow("Eclipse", results)

            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                break
