from lib.aimbot import aimbot
import tkinter as tk
from tkinter import ttk
import json
from pynput import keyboard
import numpy as np
import mss
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

        slider_warning_label = ttk.Label(self, text="Before adjusting any of the sliders values, read everything starting and down from the setup section in the README file.")
        slider_warning_label.place(x=45, y=190)

        self.mouse_scale = 0
        self.mouse_scale_slider = ttk.Scale(self, from_=50, to=150, length=600, command=self.update_mouse_scale_slider, orient='horizontal')
        self.mouse_scale_slider.place(x=60, y=260)
        self.mouse_scale_label = ttk.Label(self, text="Mouse Scale: ")
        self.mouse_scale_label.place(x=312, y=240)

        self.start_button = ttk.Button(text="Start", command=self.start_button_press)
        self.start_button.place(x=320, y=130)

        self.load_gui_data()

    def update_mouse_scale_slider(self, event):
        self.mouse_scale = float(round((self.mouse_scale_slider.get() / 100), 2))
        self.mouse_scale_label.configure(text="Mouse Scale: " + str(self.mouse_scale))

    def load_gui_data(self):
        if os.path.isfile("lib/config.json"):
            config_data = get_config_file()

            xy_sensitivity = config_data["xy_sensitivity"]
            targeting_sensitivity = config_data["targeting_sensitivity"]
            mouse_scale = int(config_data["mouse_scale"] * 100)

            self.xy_sensitivity_input.insert(0, xy_sensitivity)
            self.targeting_sensitivity_input.insert(0, targeting_sensitivity)
            self.mouse_scale_slider.set(mouse_scale)
        else:
            self.mouse_scale_slider.set(100)

    def start_button_press(self):
        global run_aimbot
        run_aimbot = True

        if os.path.isfile("lib/config.json"):
            os.remove("lib/config.json")

        xy_sensitivity = float(self.xy_sensitivity_input.get())
        targeting_sensitivity = float(self.targeting_sensitivity_input.get())
        mouse_scale = float(self.mouse_scale)

        normal_scale = (10 / float(xy_sensitivity))
        targeting_scale = (10 / (float(xy_sensitivity) * ((float(targeting_sensitivity)) / 100)))

        config_data = {"xy_sensitivity": xy_sensitivity,
                       "targeting_sensitivity": targeting_sensitivity,
                       "normal_scale": normal_scale,
                       "targeting_scale": targeting_scale,
                       "mouse_scale": mouse_scale}

        with open('lib/config.json', 'w', encoding='utf-8') as f:
            json.dump(config_data, f, ensure_ascii=False, indent=4)

        self.destroy()


if __name__ == "__main__":
    run_aimbot = False

    app = eclipse_menu()
    app.mainloop()

    if run_aimbot:
        config_file = get_config_file()
        normal_scale = config_file["normal_scale"]
        targeting_scale = config_file["targeting_scale"]
        mouse_scale = config_file["mouse_scale"]

        aimbot = aimbot(0.65, 0.45, normal_scale, targeting_scale, 0.001, mouse_scale, 2.3)

        listener = keyboard.Listener(on_release=on_key_release, on_press=on_key_press)
        listener.start()

        while aimbot.running:
            screenshot = np.array(mss.mss().grab(aimbot.screenshot_region))

            detection = aimbot.inference(screenshot)

            aimbot.move_crosshair(detection)

            screenshot = aimbot.draw_on_image(screenshot, detection)

            cv.imshow("Eclipse", screenshot)

            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                break
