# SavingImages - By: Akshat - Wed Mar 19 2025

import sensor, time, pyb, os

# Initialize the camera
sensor.reset()
sensor.set_pixformat(sensor.RGB565)  # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.VGA)     # Set frame size to VGA (640x480)
sensor.skip_frames(time=2000)        # Wait for settings to take effect

# Mount the SD card
sd = pyb.SDCard()
try:
    os.mount(sd, '/sd')
    print("SD card mounted successfully!")
except OSError as e:
    print("Error mounting SD card:", e)
    raise

# red LED for visual feedback
red_led = pyb.LED(3)

# Run in an infinite loop
while True:
    try:
        # Create a unique filename based on current time
        filename = "license_plate_image.jpg"

        # Turn on LED to indicate we're taking a photo
        red_led.on()
        time.sleep_ms(200)  # Brief flash before taking photo

        # Take a photo
        print("Taking a photo...")
        img = sensor.snapshot()

        # Save the photo to SD card
        print("Saving", filename)
        img.save(filename)
        print("Image saved successfully!")

        # Flash the LED to indicate completion
        red_led.off()
        time.sleep_ms(300)
        red_led.on()
        time.sleep_ms(300)
        red_led.off()

        # Wait before taking the next photo (adjust as needed)
        time.sleep_ms(100)  # 2-second delay between photos

    except Exception as e:
        print("Error:", e)
        # If an error occurs, wait a bit before trying again
        time.sleep_ms(1000)
