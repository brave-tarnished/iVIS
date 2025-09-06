import pyautogui
import time
import cv2
import pytesseract
import numpy as np
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
import os

# Initialize Firebase Admin SDK
cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://anpr-bg-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

def add_vehicle_entry(vehicle_number):
    """Adds an outsider vehicle entry with a timestamp"""
    if not vehicle_number:
        print("No valid license plate to upload")
        return
        
    ref = db.reference("outsiders")
    now = datetime.now().strftime("%H:%M:%S")  # Get current time
    vehicle_ref = ref.child(vehicle_number)
    vehicle_ref.set({"entry": now})
    print(f"Entry logged for {vehicle_number} at {now}")

def process_image_and_detect_plate(image_path):
    """Process the image and detect license plate using OCR"""
    # Load the image
    img = cv2.imread(image_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply multiple preprocessing techniques and try OCR on each
    results = []
    
    # 1. Basic thresholding
    _, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    results.append(thresh1)
    
    # 2. Adaptive thresholding
    thresh2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    results.append(thresh2)
    
    # 3. Contrast enhancement
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    _, thresh3 = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    results.append(thresh3)
    
    # 4. Denoising + thresholding
    denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
    _, thresh4 = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    results.append(thresh4)
    
    # OCR configuration
    config = '--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    
    # Try OCR on all preprocessed images
    all_texts = []
    for i, processed_img in enumerate(results):
        # Add border to help Tesseract
        processed_img = cv2.copyMakeBorder(processed_img, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=255)
        
        # Save intermediate results for debugging
        cv2.imwrite(f"processed_{i+1}.jpg", processed_img)
        
        # Perform OCR
        text = pytesseract.image_to_string(processed_img, config=config).strip()
        clean_text = ''.join(e for e in text if e.isalnum())
        
        if clean_text:
            all_texts.append(clean_text)
            print(f"Method {i+1} detected: {clean_text}")
    
    # Choose the most common result or the first non-empty one
    if all_texts:
        from collections import Counter
        most_common = Counter(all_texts).most_common(1)[0][0]
        print(f"\nFinal detected license plate: {most_common}")
        return most_common
    else:
        print("No license plate detected with any method")
        return None

def main():
    # Define the region to capture (left, top, width, height)
    region = (1300, 160, 1200, 570)
    
    # Define the interval in seconds
    interval = 1
    
    # Create a directory for storing screenshots
    os.makedirs("screenshots", exist_ok=True)
    
    # Keep track of the last detected plate to avoid duplicates
    last_detected_plate = None
    
    # Continuous screenshot loop
    try:
        while True:
            # Capture the screenshot
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"screenshots/license_plate_{timestamp}.png"
            screenshot = pyautogui.screenshot(region=region)
            screenshot.save(screenshot_path)
            print(f"Screenshot saved: {screenshot_path}")
            
            # Process the image and detect license plate
            detected_plate = process_image_and_detect_plate(screenshot_path)
            
            # Upload to Firebase if a new plate is detected
            if detected_plate and detected_plate != last_detected_plate:
                add_vehicle_entry(detected_plate)
                last_detected_plate = detected_plate
            
            # Wait for the specified interval
            time.sleep(interval)
    except KeyboardInterrupt:
        print("License plate detection loop stopped.")

if __name__ == "__main__":
    main()