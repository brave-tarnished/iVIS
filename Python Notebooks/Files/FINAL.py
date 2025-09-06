import pyautogui
import time
import cv2
import pytesseract
import numpy as np
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

# Initialize Firebase Admin SDK
cred = credentials.Certificate("D:/Academics/Semester VI/ES 333 - Microprocessors and Embedded Systems/PROJECT/snippet.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://anpr-bg-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

def get_next_index(ref):
    """Get the next sequential integer key as a string."""
    existing_data = ref.get()
    if not existing_data:
        return "1"
    
    existing_keys = [int(key) for key in existing_data.keys() if key.isdigit()]
    if not existing_keys:
        return "1"
    
    return str(max(existing_keys) + 1)

def add_vehicle_entry(vehicle_number):
    """Adds an outsider vehicle entry with a timestamp and plate number under a sequential key."""
    ref = db.reference("outsiders")
    now = datetime.now().strftime("%H:%M:%S")  # Current time

    next_index = get_next_index(ref)
    
    ref.child(next_index).set({
        "entry": now,
        "plate": vehicle_number
    })

    print(f"Entry logged for {vehicle_number} at {now} under ID {next_index}")

def process_image():
    """Process the captured image with OCR and return the recognized text."""
    # Load and grayscale
    img = cv2.imread("license_plate_image.png")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Enhance contrast with CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    gray = clahe.apply(gray)

    # Resize to improve OCR accuracy
    resized = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # Morph close to connect thin/broken lines
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    closed = cv2.morphologyEx(resized, cv2.MORPH_CLOSE, kernel)

    # Optional: slight blur to suppress tiny noise
    blurred = cv2.GaussianBlur(closed, (3, 3), 0)

    # Optional: invert if text is white
    if np.mean(blurred) < 127:
        blurred = cv2.bitwise_not(blurred)

    # Save for debugging
    cv2.imwrite("ocr_ready.png", blurred)

    # Tesseract config
    config = (
        r'--psm 7 --oem 3 '
        r'-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 '
        r'-c load_system_dawg=0 -c load_freq_dawg=0'
    )

    # OCR
    text = pytesseract.image_to_string(blurred, config=config).strip().replace(" ", "")
    return text

# Define the region to capture (left, top, width, height)
region = (1300, 160, 1200, 570)

# Define the interval in seconds
interval = 5

# Main loop
try:
    print("Starting ANPR system. Press Ctrl+C to stop.")
    while True:
        # 1. Capture the screenshot
        screenshot = pyautogui.screenshot(region=region)
        screenshot.save("license_plate_image.png")
        print("Screenshot captured")
        
        # 2. Process the image with OCR
        plate_text = process_image()
        print("OCR Result:", plate_text)
        
        # 3. Upload to Firebase if text was found
        if plate_text:
            add_vehicle_entry(plate_text)
        else:
            print("No license plate detected or OCR failed")
        
        # Wait for the specified interval
        time.sleep(interval)
        
except KeyboardInterrupt:
    print("ANPR system stopped.")