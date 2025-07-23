import cv2
from config import HSV_LOWER, HSV_UPPER, MIN_BUBBLE_AREA, BUBBLE_RADIUS_RANGE

def detect_green_bubble(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, HSV_LOWER, HSV_UPPER)
    mask = cv2.erode(mask, None, iterations=1)
    mask = cv2.dilate(mask, None, iterations=1)
    mask = cv2.GaussianBlur(mask, (7, 7), 0)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > MIN_BUBBLE_AREA:
            (x, y), radius = cv2.minEnclosingCircle(cnt)
            if BUBBLE_RADIUS_RANGE[0] < radius < BUBBLE_RADIUS_RANGE[1]:
                return int(x), int(y)
    return None
