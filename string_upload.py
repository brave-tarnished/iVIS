import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

# Initialize Firebase Admin SDK
cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://anpr-bg-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

def add_vehicle_entry(vehicle_number):
    """Adds an outsider vehicle entry with a timestamp"""
    ref = db.reference("outsiders")
    now = datetime.now().strftime("%H:%M:%S")  # Get current time
    vehicle_ref = ref.child(vehicle_number)
    vehicle_ref.set({"entry": now})
    print(f"Entry logged for {vehicle_number} at {now}")

# Get user input and log entry
vehicle_number = "GJ12AB5678"  # Example vehicle number
add_vehicle_entry(vehicle_number)