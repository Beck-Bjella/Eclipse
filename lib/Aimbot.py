# Imports
import ctypes
import math
import time
import torch
import win32api
import cv2

PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    """
    Data structure for keyboard input events, used to simulate keyboard actions.
    """
    _fields_ = [("wVk", ctypes.c_ushort),  # Virtual-key code
                ("wScan", ctypes.c_ushort),  # Hardware scan code
                ("dwFlags", ctypes.c_ulong),  # Flags for the event type
                ("time", ctypes.c_ulong),  # Timestamp for the event
                ("dwExtraInfo", PUL)]  # Additional information


class HardwareInput(ctypes.Structure):
    """
    Data structure for hardware input events, used to simulate specific hardware actions.
    """
    _fields_ = [("uMsg", ctypes.c_ulong),  # Message identifier
                ("wParamL", ctypes.c_short),  # Low word parameter
                ("wParamH", ctypes.c_ushort)]  # High word parameter


class MouseInput(ctypes.Structure):
    """
    Data structure for mouse input events, used to simulate mouse movements and clicks.
    """
    _fields_ = [("dx", ctypes.c_long),  # x-coordinate of movement
                ("dy", ctypes.c_long),  # y-coordinate of movement
                ("mouseData", ctypes.c_ulong),  # Additional mouse event data
                ("dwFlags", ctypes.c_ulong),  # Flags for event type
                ("time", ctypes.c_ulong),  # Timestamp for the event
                ("dwExtraInfo", PUL)]  # Additional information


class Input_I(ctypes.Union):
    """
    Union of different input structures, allowing a single input to represent
    keyboard, mouse, or hardware input events.
    """
    _fields_ = [("ki", KeyBdInput),  # Keyboard input
                ("mi", MouseInput),  # Mouse input
                ("hi", HardwareInput)]  # Hardware input


class Input(ctypes.Structure):
    """
    Main input structure, used to send input events via the Windows API.
    """
    _fields_ = [("type", ctypes.c_ulong),  # Input event type
                ("ii", Input_I)]  # Input data


class POINT(ctypes.Structure):
    """
    Structure representing a point on the screen, with x and y coordinates.
    """
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


class Aimbot:
    """
    Aimbot class to perform object detection on screen regions and simulate
    mouse movements for aiming at detected objects.
    """
    aiming_status = "OFF"
    running = True
    visualize = False
    visualize_open = False
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()

    def __init__(self, model_confidence, model_iou, normal_scale, targeting_scale, window_size):
        """
        Initializes the Aimbot with configuration for object detection and screen regions.
        """
        # Check for CUDA
        if not torch.cuda.is_available():
            print("[!] CUDA not available.")
            print("Quitting...")
            time.sleep(3)
            exit()

        # Screen region based on window size
        match window_size:
            case "1920x1080":
                self.screenshot_region = {'left': 752, 'top': 332, 'width': 416, 'height': 416}
            case "1280x720":
                self.screenshot_region = {'left': 432, 'top': 152, 'width': 416, 'height': 416}
            case _:
                self.screenshot_region = {'left': 752, 'top': 332, 'width': 416, 'height': 416}

        self.normal_scale = normal_scale
        self.targeting_scale = targeting_scale

        # Load the YOLOv5 model
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path='lib/weights.pt/', force_reload=True)
        self.model.conf = model_confidence
        self.model.iou = model_iou

    def update_aimimg_status(self, updated_value):
        """
        Updates the aiming status.
        """
        self.aiming_status = updated_value

    @staticmethod
    def sleep(duration):
        """
        Sleep function for very precise time intervals.
        """
        get_now = time.perf_counter
        now = get_now()
        end = now + duration
        while now < end:
            now = get_now()

    def move_crosshair(self, detection):
        """
        Moves the crosshair based on the detected object's location.
        """
        if detection["x1y1"]:
            absolute_head = self.screenshot_region["left"] + detection["head"][0], self.screenshot_region["top"] + detection["head"][1]

            # Adjust scale based on held right mouse button
            right_state = win32api.GetKeyState(0x02)
            scale = self.targeting_scale if right_state in (-127, -128) else self.normal_scale

            # Calculate relative movements
            distance_x = int(absolute_head[0] - 960)
            distance_y = int(absolute_head[1] - 540)
            rel_x = int(distance_x * scale)
            rel_y = int(distance_y * scale)

            # Move mouse
            self.ii_.mi = MouseInput(rel_x, rel_y, 0, 0x0001, 0, ctypes.pointer(self.extra))
            input_obj = Input(ctypes.c_ulong(0), self.ii_)
            ctypes.windll.user32.SendInput(1, ctypes.byref(input_obj), ctypes.sizeof(input_obj))

    def inference_conf(self, image):
        """
        Performs object detection and returns the best detection based on confidence.
        """
        best_detection = {}
        raw_results = self.model(image)
        results = raw_results.xyxy[0]

        if len(results) > 0:
            highest_confidence = 0
            for x in range(len(results)):
                # Extract bounding box coordinates and calculate head position
                x1, y1 = int(float(results[x][0])), int(float(results[x][1]))
                x2, y2 = int(float(results[x][2])), int(float(results[x][3]))
                head = int(x1 + (abs(x1 - x2) / 2)), int(y1 + (abs(y1 - y2) / 3))
                confidence = results[x][4].item()
                detection_distance = math.dist((208, 208), head)

                exclusion_zone = x1 < 40
                if not exclusion_zone and confidence > highest_confidence:
                    highest_confidence = confidence
                    best_detection = {'x1y1': (x1, y1), 'x2y2': (x2, y2), 'head': head, 'confidence': confidence, 'distance': detection_distance}

        if not best_detection:
            best_detection.update({'x1y1': False, 'x2y2': False, 'head': False, 'confidence': False, 'distance': False})

        return best_detection

    def inference_dist(self, image):
        """
        Performs object detection and returns the closest detection based on distance.
        """
        best_detection = {}
        raw_results = self.model(image)
        results = raw_results.xyxy[0]

        if len(results) > 0:
            closest_detection = 10000
            for x in range(len(results)):
                # Extract bounding box coordinates and calculate head position
                x1, y1 = int(float(results[x][0])), int(float(results[x][1]))
                x2, y2 = int(float(results[x][2])), int(float(results[x][3]))
                head = int(x1 + (abs(x1 - x2) / 2)), int(y1 + (abs(y1 - y2) / 3.9))
                confidence = results[x][4].item()
                detection_distance = math.dist((208, 208), head)

                exclusion_zone = x1 < 40
                if not exclusion_zone and detection_distance < closest_detection:
                    closest_detection = detection_distance
                    best_detection = {'x1y1': (x1, y1), 'x2y2': (x2, y2), 'head': head, 'confidence': confidence, 'distance': detection_distance}

        if not best_detection:
            best_detection.update({'x1y1': False, 'x2y2': False, 'head': False, 'confidence': False, 'distance': False})

        return best_detection

    @staticmethod
    def draw_detection(image, detection):
        """
        Draws bounding boxes and detection information on an image.
        """
        if detection["x1y1"]:
            x1y1, x2y2, head, confidence = detection["x1y1"], detection["x2y2"], detection["head"], detection["confidence"]

            # Draw bounding box
            cv2.rectangle(image, x1y1, x2y2, (255, 0, 0), 2)
            cv2.line(image, (208, 208), head, (255, 0, 0), 2)
            cv2.circle(image, head, 5, (255, 0, 0), -1)

            # Draw confidence text
            confidence_text = str(int(confidence * 100)) + "%"
            cv2.putText(image, text=confidence_text, org=(x1y1[0], x1y1[1] - 7), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.65, color=(255, 0, 0), thickness=2, lineType=cv2.LINE_AA)

        return image
