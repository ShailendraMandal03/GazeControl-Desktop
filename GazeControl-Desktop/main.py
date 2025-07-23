import pyautogui, datetime, time, keyboard
import cv2, numpy as np
from config import *
from detection import detect_green_bubble
from click_utils import click_without_moving_cursor, is_on_desktop
from utils import calculate_velocity, plot_scanpath
# from logger import initialize_logs, append_to_csv
from logger import open_csv_with_header
from logger import *
import os


gaze_log = []
fixations = []
saccades = []

last_logged_mouse_pos = None
last_bubble_pos = None
gaze_hold_start = None
gaze_hold_pos = None
last_click_time = 0
clicked = False
last_gaze_time = None
last_gaze_pos = None

print("[INFO] Tracking green bubble (#CC10F61F)")
print("[INFO] Double-click gaze to open folder/file on desktop only")
print("[INFO] Press 'q' to quit")

try:
    while True:
        screenshot = pyautogui.screenshot()
        frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        bubble_pos = detect_green_bubble(frame)

        if bubble_pos:
            dist = 0 if last_bubble_pos is None else ((bubble_pos[0] - last_bubble_pos[0])**2 + (bubble_pos[1] - last_bubble_pos[1])**2)**0.5
            if dist < MAX_BUBBLE_SPEED:
                screen_w, screen_h = pyautogui.size()
                img_h, img_w = frame.shape[:2]
                gaze_x = int(bubble_pos[0] * (screen_w / img_w))
                gaze_y = int(bubble_pos[1] * (screen_h / img_h))
                now = time.time()
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                gaze_log.append((now, gaze_x, gaze_y))
                # append_to_csv(gaze_log_file, [gaze_x, gaze_y, timestamp])
                gaze_csv.writerow([gaze_x, gaze_y, timestamp])


                mouse_x, mouse_y = pyautogui.position()
                if last_logged_mouse_pos != (mouse_x, mouse_y):
                    # append_to_csv(mouse_log_file,[mouse_x, mouse_y, timestamp])
                    mouse_csv.writerow([mouse_x, mouse_y, timestamp])
                    last_logged_mouse_pos = (mouse_x, mouse_y)

                velocity = calculate_velocity(last_gaze_pos, last_gaze_time, (gaze_x, gaze_y), now)
                if velocity > SACCADE_VELOCITY_THRESHOLD:
                    saccade_info = {
                        'from': last_gaze_pos,
                        'to': (gaze_x, gaze_y),
                        'velocity': velocity,
                        'duration': now - last_gaze_time
                    }
                    saccades.append(saccade_info)
                    # append_to_csv(saccade_log_file, [
                        # saccade_info['from'], saccade_info['to'], velocity, timestamp, saccade_info['duration']])
                    
                    saccade_csv.writerow([last_gaze_pos, (gaze_x, gaze_y), velocity,last_gaze_timestamp,timestamp, now - last_gaze_time])

                    print(f"[SACCADE] Velocity={velocity:.1f}px/s From {saccade_info['from']} to {saccade_info['to']}")

                last_gaze_pos = (gaze_x, gaze_y)
                last_gaze_time = now
                last_gaze_timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

                if gaze_hold_pos is None:
                    gaze_hold_start = now
                    gaze_hold_pos = (gaze_x, gaze_y)
                    clicked = False
                else:
                    hold_dist = ((gaze_x - gaze_hold_pos[0])**2 + (gaze_y - gaze_hold_pos[1])**2)**0.5
                    if hold_dist <= GAZE_HOLD_RADIUS:
                        hold_duration = now - gaze_hold_start
                        if not clicked and (now - last_click_time) >= CLICK_COOLDOWN and hold_duration >= GAZE_HOLD_TIME:
                            if hold_duration >= DOUBLE_CLICK_HOLD_TIME:
                                if is_on_desktop(gaze_x, gaze_y):
                                    click_without_moving_cursor(gaze_x, gaze_y, click_type='double')
                                    print(f"\n[DOUBLE CLICK] Desktop item opened at ({gaze_x}, {gaze_y})")
                                else:
                                    click_without_moving_cursor(gaze_x, gaze_y, click_type='left')
                                    print(f"\n[CLICK] Held {hold_duration:.2f}s at ({gaze_x}, {gaze_y}) (Not on desktop)")
                            else:
                                click_without_moving_cursor(gaze_x, gaze_y, click_type='left')
                                print(f"\n[CLICK] Single click at ({gaze_x}, {gaze_y})")
                            clicked = True
                            last_click_time = now

                        if hold_duration >= GAZE_HOLD_TIME and (not fixations or gaze_hold_pos != fixations[-1][1]):
                            fixations.append((now, gaze_hold_pos))
                            # append_to_csv(fixa_log_file, [gaze_hold_pos[0], gaze_hold_pos[1], timestamp])

                            fixa_csv.writerow([gaze_hold_pos[0], gaze_hold_pos[1], timestamp])
                            print(f"\n[FIXATION] {gaze_hold_pos} for {hold_duration:.2f}s")
                    else:
                        gaze_hold_start = now
                        gaze_hold_pos = (gaze_x, gaze_y)
                        clicked = False
                print(f"\r[GAZE] {timestamp} - Gaze at ({gaze_x}, {gaze_y})", end="", flush=True)
            else:
                print(f"\r[GAZE] Skipping fast movement (speed={dist:.1f})", end="", flush=True)
                gaze_hold_start = None
                gaze_hold_pos = None
                clicked = False
            last_bubble_pos = bubble_pos
        else:
            last_bubble_pos = None
            gaze_hold_start = None
            gaze_hold_pos = None
            clicked = False

        if keyboard.is_pressed('q'):
            print("\n[INFO] Exiting...")
            break
        time.sleep(DETECTION_INTERVAL)

except KeyboardInterrupt:
    print("\n[INFO] Stopped by user")
finally:
    cv2.destroyAllWindows()
    plot_scanpath(gaze_log, fixations, saccades)
