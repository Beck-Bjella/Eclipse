import ctypes
import cv2
import math
import numpy as np
import time
import torch
import win32api
import win32con
import win32gui
import win32ui

PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


class Aimbot:
    aiming_status = "OFF"
    running = True
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()

    def __init__(self, model_confidence, model_iou, normal_scale, targeting_scale, window_size):
        if not torch.cuda.is_available():
            print("[!] CUDA not available.")
            print("")
            print("Quitting...")
            time.sleep(3)
            exit()

        match window_size:
            case "1920x1080":
                self.screenshot_region = {'left': 752, 'top': 332, 'width': 416, 'height': 416}  # 1920x1080

            case "1280x720":
                self.screenshot_region = {'left': 432, 'top': 152, 'width': 416, 'height': 416}  # 1280x720

            case _:
                self.screenshot_region = {'left': 752, 'top': 332, 'width': 416, 'height': 416}  # 1920x1080

        self.normal_scale = normal_scale
        self.targeting_scale = targeting_scale

        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path='lib/weights.pt/', force_reload=True)
        self.model.conf = model_confidence
        self.model.iou = model_iou

    def update_aimimg_status(self, updated_value):
        self.aiming_status = updated_value

    @staticmethod
    def sleep(duration):
        get_now = time.perf_counter
        now = get_now()
        end = now + duration
        while now < end:
            now = get_now()

    def move_crosshair(self, detection):
        if detection["x1y1"]:
            absolute_head = self.screenshot_region["left"] + detection["head"][0], self.screenshot_region["top"] + detection["head"][1]

            right_state = win32api.GetKeyState(0x02)
            if right_state in (-127, -128):
                scale = self.targeting_scale
            else:
                scale = self.normal_scale

            distance_x = int(absolute_head[0] - 960)
            distance_y = int(absolute_head[1] - 540)

            rel_x = int(distance_x * scale)
            rel_y = int(distance_y * scale)

            self.ii_.mi = MouseInput(rel_x, rel_y, 0, 0x0001, 0, ctypes.pointer(self.extra))
            input_obj = Input(ctypes.c_ulong(0), self.ii_)
            ctypes.windll.user32.SendInput(1, ctypes.byref(input_obj), ctypes.sizeof(input_obj))

    def inference_conf(self, image):
        best_detection = {}

        raw_results = self.model(image)
        results = raw_results.xyxy[0]

        if len(results) > 0:
            highest_confidence = 0

            for x in range(len(results)):
                x1 = int(float(results[x][0]))
                y1 = int(float(results[x][1]))
                x2 = int(float(results[x][2]))
                y2 = int(float(results[x][3]))

                x1y1 = x1, y1
                x2y2 = x2, y2

                head = int(x1 + (abs(x1 - x2) / 2)), int(y1 + (abs(y1 - y2) / 3))

                confidence = results[x][4].item()
                detection_distance = math.dist((208, 208), (head[0], head[1]))

                exclusion_zone = x1 < 40

                if not exclusion_zone and confidence > highest_confidence:
                    highest_confidence = confidence
                    best_detection = {'x1y1': x1y1, 'x2y2': x2y2, 'head': head, 'confidence': confidence, 'distance': detection_distance}

        if not best_detection:
            best_detection.update({'x1y1': False, 'x2y2': False, 'head': False, 'confidence': False, 'distance': False})

        return best_detection

    def inference_dist(self, image):
        best_detection = {}

        raw_results = self.model(image)
        results = raw_results.xyxy[0]

        if len(results) > 0:
            closest_detection = 10000

            for x in range(len(results)):
                x1 = int(float(results[x][0]))
                y1 = int(float(results[x][1]))
                x2 = int(float(results[x][2]))
                y2 = int(float(results[x][3]))

                x1y1 = x1, y1
                x2y2 = x2, y2

                head = int(x1 + (abs(x1 - x2) / 2)), int(y1 + (abs(y1 - y2) / 4.1))

                confidence = results[x][4].item()
                detection_distance = math.dist((208, 208), (head[0], head[1]))

                exclusion_zone = x1 < 40

                if not exclusion_zone and detection_distance < closest_detection:
                    closest_detection = detection_distance
                    best_detection = {'x1y1': x1y1, 'x2y2': x2y2, 'head': head, 'confidence': confidence, 'distance': detection_distance}

        if not best_detection:
            best_detection.update({'x1y1': False, 'x2y2': False, 'head': False, 'confidence': False, 'distance': False})

        return best_detection
