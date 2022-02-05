from lib.aimbot import aimbot
import tkinter as tk
from tkinter import ttk
import json
from pynput import keyboard
import numpy as np
import mss
import cv2 as cv
#import os


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
                if shotgun_slot == 1:
                    aimbot.holding_shotgun = True
                else:
                    aimbot.holding_shotgun = False
            elif key.char == slot_2_hotkey:
                if shotgun_slot == 2:
                    aimbot.holding_shotgun = True
                else:
                    aimbot.holding_shotgun = False
            elif key.char == slot_3_hotkey:
                if shotgun_slot == 3:
                    aimbot.holding_shotgun = True
                else:
                    aimbot.holding_shotgun = False
            elif key.char == slot_4_hotkey:
                if shotgun_slot == 4:
                    aimbot.holding_shotgun = True
                else:
                    aimbot.holding_shotgun = False
            elif key.char == slot_5_hotkey:
                if shotgun_slot == 5:
                    aimbot.holding_shotgun = True
                else:
                    aimbot.holding_shotgun = False
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
        self.xy_sensitivity_input.place(x=430, y=135)
        xy_sensitivity_label = ttk.Label(self, text="XY Sensitivity")
        xy_sensitivity_label.place(x=430, y=115)

        self.targeting_sensitivity_input = ttk.Entry(self)
        self.targeting_sensitivity_input.place(x=430, y=190)
        targeting_sensitivity_label = ttk.Label(self, text="Targeting Sensitivity")
        targeting_sensitivity_label.place(x=430, y=170)

        slider_warning_label = ttk.Label(self, text="")
        slider_warning_label.place(x=45, y=190)

        self.mouse_scale = 0
        self.mouse_scale_slider = ttk.Scale(self, from_=50, to=150, length=600, command=self.update_mouse_scale_slider, orient='horizontal')
        self.mouse_scale_slider.place(x=60, y=310)
        self.mouse_scale_label = ttk.Label(self, text="Mouse Scale: ")
        self.mouse_scale_label.place(x=312, y=290)

        self.start_button = ttk.Button(text="Start", command=self.start_button_press)
        self.start_button.place(x=320, y=130)

        self.auto_fire = tk.BooleanVar()
        self.auto_fire_toggle = ttk.Checkbutton(text="Enable shotgun trigger bot", onvalue=True, offvalue=False, variable=self.auto_fire)
        self.auto_fire_toggle.place(x=80, y=115)

        self.slot_1_hotkey_input = ttk.Entry(self)
        self.slot_1_hotkey_input.place(x=80, y=140)

        self.slot_2_hotkey_input = ttk.Entry(self)
        self.slot_2_hotkey_input.place(x=80, y=170)

        self.slot_3_hotkey_input = ttk.Entry(self)
        self.slot_3_hotkey_input.place(x=80, y=200)

        self.slot_4_hotkey_input = ttk.Entry(self)
        self.slot_4_hotkey_input.place(x=80, y=230)

        self.slot_5_hotkey_input = ttk.Entry(self)
        self.slot_5_hotkey_input.place(x=80, y=260)

        self.shotgun_slot = tk.StringVar()
        radio_button_names = {"Item Slot 1": 1,
                              "Item Slot 2": 2,
                              "Item Slot 3": 3,
                              "Item Slot 4": 4,
                              "Item Slot 5": 5}
        position_y = 140
        for (text, value) in radio_button_names.items():
            ttk.Radiobutton(self, text=text, variable=self.shotgun_slot, value=value).place(x=210, y=position_y)
            position_y += 30

        self.load_gui_data()

    def update_mouse_scale_slider(self, event):
        self.mouse_scale = float(round((self.mouse_scale_slider.get() / 100), 2))
        self.mouse_scale_label.configure(text="Mouse Scale: " + str(self.mouse_scale))

    def load_gui_data(self):
        if os.path.isfile("lib/config.json"):
            config_data = get_config_file()

            self.xy_sensitivity_input.insert(0, config_data["xy_sensitivity"])
            self.targeting_sensitivity_input.insert(0, config_data["targeting_sensitivity"])
            self.mouse_scale_slider.set(int(config_data["mouse_scale"] * 100))
            self.auto_fire.set(config_data["auto_fire"])
            self.slot_1_hotkey_input.insert(0, config_data["slot_1_hotkey"])
            self.slot_2_hotkey_input.insert(0, config_data["slot_2_hotkey"])
            self.slot_3_hotkey_input.insert(0, config_data["slot_3_hotkey"])
            self.slot_4_hotkey_input.insert(0, config_data["slot_4_hotkey"])
            self.slot_5_hotkey_input.insert(0, config_data["slot_5_hotkey"])
            self.shotgun_slot.set(str(config_data["shotgun_slot"]))
        else:
            self.mouse_scale_slider.set(100)
            self.auto_fire.set(False)

    def start_button_press(self):
        global run_aimbot
        run_aimbot = True

        if os.path.isfile("lib/config.json"):
            os.remove("lib/config.json")

        xy_sensitivity = float(self.xy_sensitivity_input.get())
        targeting_sensitivity = float(self.targeting_sensitivity_input.get())
        normal_scale = (10 / float(xy_sensitivity))
        targeting_scale = (10 / (float(xy_sensitivity) * ((float(targeting_sensitivity)) / 100)))

        config_data = {"xy_sensitivity": xy_sensitivity,
                       "targeting_sensitivity": targeting_sensitivity,
                       "normal_scale": normal_scale,
                       "targeting_scale": targeting_scale,
                       "mouse_scale": float(self.mouse_scale),
                       "auto_fire": self.auto_fire.get(),
                       "slot_1_hotkey": self.slot_1_hotkey_input.get(),
                       "slot_2_hotkey": self.slot_2_hotkey_input.get(),
                       "slot_3_hotkey": self.slot_3_hotkey_input.get(),
                       "slot_4_hotkey": self.slot_4_hotkey_input.get(),
                       "slot_5_hotkey": self.slot_5_hotkey_input.get(),
                       "shotgun_slot": int(self.shotgun_slot.get())}

        with open('lib/config.json', 'w', encoding='utf-8') as f:
            json.dump(config_data, f, ensure_ascii=False, indent=4)

        self.destroy()


if __name__ == "__main__":
    run_aimbot = False

    app = eclipse_menu()
    app.mainloop()

    if run_aimbot:
        config_file = get_config_file()
        aimbot = aimbot(0.45, 0.01, config_file["normal_scale"], config_file["targeting_scale"], 0.0001, config_file["mouse_scale"], config_file["auto_fire"])

        slot_1_hotkey = config_file["slot_1_hotkey"]
        slot_2_hotkey = config_file["slot_2_hotkey"]
        slot_3_hotkey = config_file["slot_3_hotkey"]
        slot_4_hotkey = config_file["slot_4_hotkey"]
        slot_5_hotkey = config_file["slot_5_hotkey"]
        shotgun_slot = config_file["shotgun_slot"]

        listener = keyboard.Listener(on_release=on_key_release, on_press=on_key_press)
        listener.start()

        while aimbot.running:
            screenshot = np.array(mss.mss().grab(aimbot.screenshot_region))

            detection = aimbot.inference(screenshot)

            aimbot.move_crosshair(detection)

            aimbot.shotgun_auto_fire(detection)

            screenshot = aimbot.draw_on_image(screenshot, detection)

            cv.imshow("Eclipse", screenshot)

            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                break
