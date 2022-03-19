import math
import torch
import win32api
import ctypes
import cv2 as cv
import time

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


class aimbot:
    screenshot_region = {'left': 752, 'top': 332, 'width': 416, 'height': 416}
    aiming_status = "OFF"
    running = True
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()

    def __init__(self, model_confidence, model_iou, normal_scale, targeting_scale, movement_size, movement_steps):
        if not torch.cuda.is_available():
            print("")
            print("[ERROR] CUDA not available.")
            print("")
            print("Quitting...")
            time.sleep(2)
            exit()

        self.normal_scale = normal_scale
        self.targeting_scale = targeting_scale
        self.movement_size = movement_size

        self.model = torch.hub.load('lib/yolov5-master/', 'custom', path='lib/weights.pt/', source='local')
        self.model.conf = model_confidence
        self.model.iou = model_iou
        self.model.classes = [0]

    @staticmethod
    def update_aimimg_status(updated_value):
        if updated_value == "toggle":
            if aimbot.aiming_status == "ON":
                aimbot.aiming_status = "OFF"
            else:
                aimbot.aiming_status = "ON"
        else:
            aimbot.aiming_status = updated_value

    @staticmethod
    def sleep(duration):
        get_now = time.perf_counter
        if duration == 0:
            return
        now = get_now()
        end = now + duration
        while now < end:
            now = get_now()

    @staticmethod
    def draw_on_image(image, detection):
        if detection["x1y1"]:
            x1y1 = detection["x1y1"]
            x2y2 = detection["x2y2"]
            x1, y1 = detection["x1y1"]
            head = detection["head"]
            confidence = detection["confidence"]

            cv.rectangle(image, x1y1, x2y2, (255, 255, 255), 2)

            cv.circle(image, head, 6, (255, 255, 255), -1)

            cv.line(image, (208, 208), head, (255, 255, 255), 2)

            confidence_text = str(int(confidence * 100)) + "%"
            cv.putText(image, text=confidence_text, org=(x1, y1 - 7), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=0.65, color=(255, 255, 255), thickness=2, lineType=cv.LINE_AA)

        return image

    def move_crosshair(self, detection):
        if detection["x1y1"]:
            absolute_head = aimbot.screenshot_region["left"] + detection["head"][0], aimbot.screenshot_region["top"] + detection["head"][1]

            right_state = win32api.GetKeyState(0x02)
            if right_state in (-127, -128):
                scale = self.targeting_scale
            else:
                scale = self.normal_scale

            diff_x = (absolute_head[0] - 960)
            diff_y = (absolute_head[1] - 540)
            length = int(math.dist((0, 0), (diff_x, diff_y)))

            if length == 0:
                return False

            temp_movement_size = self.movement_size
            if length < temp_movement_size:
                temp_movement_size = length

            rel_x = int(((diff_x / length) * temp_movement_size) * scale)
            rel_y = int(((diff_y / length) * temp_movement_size) * scale)

            aimbot.ii_.mi = MouseInput(rel_x, rel_y, 0, 0x0001, 0, ctypes.pointer(aimbot.extra))
            input_obj = Input(ctypes.c_ulong(0), aimbot.ii_)
            ctypes.windll.user32.SendInput(1, ctypes.byref(input_obj), ctypes.sizeof(input_obj))

    def inference(self, image):
        best_detection = {}

        raw_results = self.model(image, 140)
        results = raw_results.xyxy[0]

        if len(results) > 0:
            closest_detection = 50

            for x in range(len(results)):
                x1 = int(float(results[x][0]))
                y1 = int(float(results[x][1]))
                x2 = int(float(results[x][2]))
                y2 = int(float(results[x][3]))

                x1y1 = x1, y1
                x2y2 = x2, y2

                head = int(x1 + (abs(x1 - x2) / 2)), int(y1 + (abs(y1 - y2) / 4.3))

                confidence = results[x][4].item()

                exclusion_zone = x1 < 15

                detection_distance = ((y2 - y1) * 2) + ((x2 - x1) * 2)

                if not exclusion_zone and detection_distance > closest_detection:
                    closest_detection = detection_distance
                    best_detection = {'x1y1': x1y1, 'x2y2': x2y2, 'head': head, 'confidence': confidence}

        if best_detection:
            pass
        else:
            best_detection.update({'x1y1': False, 'x2y2': False, 'head': False, 'confidence': False})

        return best_detection
