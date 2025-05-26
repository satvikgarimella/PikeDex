import RPi.GPIO as GPIO
import time
import requests
import json
import atexit
import signal

# Joystick GPIO pin mapping
PIN_RIGHT = 22  # Move right
PIN_LEFT = 17   # Move left
PIN_SW = 27     # Press down (SW)

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_LEFT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)

BASE_URL = "http://localhost:5050"
last_prediction = None

def cleanup():
    print("\nCleaning up GPIO...")
    GPIO.cleanup()
    print("Goodbye!")

# Register cleanup function
atexit.register(cleanup)

# Handle SIGINT (Ctrl+C)
def signal_handler(sig, frame):
    cleanup()
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

def capture_and_predict():
    global last_prediction
    try:
        requests.post(f"{BASE_URL}/capture")
        time.sleep(2)
        response = requests.get(f"{BASE_URL}/predict")
        if response.status_code == 200:
            last_prediction = response.json()
            print(f"Detected: {last_prediction['name']} ({last_prediction['confidence']:.2%})")
        else:
            print("Failed to get prediction")
    except Exception as e:
        print(f"Error: {str(e)}")

def favorite_pokemon():
    if last_prediction:
        try:
            response = requests.post(
                f"{BASE_URL}/favorite",
                json={"name": last_prediction["name"]}
            )
            if response.status_code == 200:
                print(f"Added {last_prediction['name']} to favorites!")
            else:
                print("Failed to add to favorites")
        except Exception as e:
            print(f"Error: {str(e)}")
    else:
        print("No Pokémon detected yet!")

def show_collection():
    try:
        response = requests.get(f"{BASE_URL}/collection")
        if response.status_code == 200:
            collection = response.json()["collection"]
            print("\nYour Pokémon Collection:")
            for pokemon in collection:
                print(f"- {pokemon}")
        else:
            print("Failed to get collection")
    except Exception as e:
        print(f"Error: {str(e)}")

def right_callback(channel):
    if GPIO.input(channel) == GPIO.LOW:
        show_collection()
        time.sleep(0.3)

def left_callback(channel):
    if GPIO.input(channel) == GPIO.LOW:
        favorite_pokemon()
        time.sleep(0.3)

def sw_callback(channel):
    if GPIO.input(channel) == GPIO.LOW:
        capture_and_predict()
        time.sleep(0.3)

# Set up event detection
GPIO.add_event_detect(PIN_RIGHT, GPIO.FALLING, callback=right_callback, bouncetime=300)
GPIO.add_event_detect(PIN_LEFT, GPIO.FALLING, callback=left_callback, bouncetime=300)
GPIO.add_event_detect(PIN_SW, GPIO.FALLING, callback=sw_callback, bouncetime=300)

print("Pokédex Joystick Controller Ready!")
print("➡️ Move right: Show collection")
print("⬅️ Move left: Favorite current Pokémon")
print("⬇️ Press down (SW): Capture + predict")

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    cleanup()
    print("\nGoodbye!") 