import numpy as np
import os

output_dir = "data_logs"
os.makedirs(output_dir, exist_ok=True)

gaze_log_file = os.path.join(output_dir, "gaze.csv")
mouse_log_file = os.path.join(output_dir, "mouse.csv")
fixa_log_file = os.path.join(output_dir, "fixation.csv")
saccade_log_file = os.path.join(output_dir, "saccade.csv")

MIN_BUBBLE_AREA = 250
BUBBLE_RADIUS_RANGE = (10, 80)
DETECTION_INTERVAL = 0.05

HSV_LOWER = np.array([55, 180, 180])
HSV_UPPER = np.array([70, 255, 255])


GAZE_HOLD_RADIUS = 25
GAZE_HOLD_TIME = 0.5
DOUBLE_CLICK_HOLD_TIME = 0.6
CLICK_COOLDOWN = 3
MAX_BUBBLE_SPEED = 20
SACCADE_VELOCITY_THRESHOLD = 1200
