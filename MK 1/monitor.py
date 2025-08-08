import pyautogui
import time

while True:
    x, y = pyautogui.position()
    print(f"Mouse position: ({x}, {y})")
    time.sleep(0.1)  # Add a 100ms delay