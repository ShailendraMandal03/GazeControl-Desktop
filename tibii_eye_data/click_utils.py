import pyautogui
from pywinauto import mouse

def is_on_desktop(gaze_x, gaze_y):
    screen_width, screen_height = pyautogui.size()
    TASKBAR_HEIGHT = 40
    return gaze_y < (screen_height - TASKBAR_HEIGHT)

def click_without_moving_cursor(x, y, click_type='left'):
    current_pos = pyautogui.position()
    try:
        if click_type == 'left':
            mouse.click(button='left', coords=(x, y))
        elif click_type == 'double':
            mouse.double_click(button='left', coords=(x, y))
        elif click_type == 'right':
            mouse.click(button='right', coords=(x, y))
        print(f"[INFO] {click_type.capitalize()} click at ({x}, {y}) without moving cursor.")
    except Exception as e:
        print(f"[ERROR] Failed click at ({x}, {y}): {e}")
    finally:
        pyautogui.moveTo(current_pos)
