import pyautogui
import time

# Define the region to capture (left, top, width, height)
region = (1300, 160, 1200, 570)

# Define the interval in seconds
interval = 1

# Continuous screenshot loop
try:
    while True:
        # Capture the screenshot
        screenshot = pyautogui.screenshot(region=region)
        screenshot.save(f"LM Studio/license_plate_image.jpg")

        # Wait for the specified interval
        time.sleep(interval)
except KeyboardInterrupt:
    print("Screenshot loop stopped.")