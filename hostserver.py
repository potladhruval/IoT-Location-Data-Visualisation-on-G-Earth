from flask import Flask, request
import threading
import serial
import random
import tkinter as tk
from tkinter import ttk
import time
import requests

app = Flask(__name__)

# ThingSpeak API configuration
THINGSPEAK_API_KEY = "YWCP203M9GVHI0E9"
THINGSPEAK_CHANNEL_ID = "2358572"

# Store the server credentials
server_credentials = {}

def parse_gprmc(gprmc_sentence):
    # Parse a GPRMC sentence into latitude, longitude, speed, and direction
    parts = gprmc_sentence.split(",")
    if len(parts) < 8 or not parts[3] or not parts[4] or not parts[5] or not parts[6] or not parts[7]:
        return None, None, None, None

    lat_val = parts[3]
    lat_dir = parts[4]
    lon_val = parts[5]
    lon_dir = parts[6]
    speed = parts[7]
    direction = parts[8]

    if not lat_val.replace(".", "", 1).isdigit() or not lon_val.replace(".", "", 1).isdigit():
        print(f"Invalid latitude or longitude format: {lat_val}, {lon_val}")
        return None, None, None, None

    try:
        lat = float(lat_val)
        lon = float(lon_val)

        if lat_dir == 'S':
            lat = -lat
        if lon_dir == 'W':
            lon = -lon

        return lat, lon, float(speed), float(direction)

    except ValueError:
        print(f"Failed to convert values to float: {lat_val}, {lon_val}, {speed}, {direction}")
        return None, None, None, None

def parse_gpgll(gpgll_sentence):
    # Parse a GPGLL sentence into latitude and longitude
    parts = gpgll_sentence.split(",")
    if len(parts) < 5 or not parts[1] or not parts[3]:
        return None, None

    lat_val = parts[1]
    lat_dir = parts[2]
    lon_val = parts[3]
    lon_dir = parts[4]

    if not lat_val.replace(".", "", 1).isdigit() or not lon_val.replace(".", "", 1).isdigit():
        print(f"Invalid latitude or longitude format: {lat_val}, {lon_val}")
        return None, None

    try:
        lat = float(lat_val)
        lon = float(lon_val)

        if lat_dir == 'S':
            lat = -lat
        if lon_dir == 'W':
            lon = -lon

        return lat, lon

    except ValueError:
        print(f"Failed to convert values to float: {lat_val}, {lon_val}")
        return None, None

@app.route('/api/gps', methods=['POST'])
def receive_gps_data():
    global THINGSPEAK_API_KEY
    gps_data = request.form.get('gps_data')
    print(f"Raw GPS data: {gps_data}")

    # Check if it's a GPRMC sentence
    if gps_data.startswith("$GPRMC"):
        lat, lon, speed, direction = parse_gprmc(gps_data)
    # Check if it's a GPGLL sentence
    elif gps_data.startswith("$GPGLL"):
        lat, lon = parse_gpgll(gps_data)
        # Assume speed and direction are not available in GPGLL
        speed, direction = None, None
    else:
        # Unknown sentence type, ignore
        return {'status': 'success'}

    if lat is not None and lon is not None:
        # Send GPS data to ThingSpeak
        data = {
            'api_key': THINGSPEAK_API_KEY,
            'field1': lat,
            'field2': lon,
            'field3': speed,
            'field4': direction
        }
        response = requests.post(f'https://api.thingspeak.com/update.json', data=data)
        if response.status_code != 200:
            print(f"Failed to send GPS data to ThingSpeak: {response.content}")
        else:
            print(f"Sent GPS data to ThingSpeak: Latitude: {lat}, Longitude: {lon}, Speed: {speed}, Direction: {direction}")
    return {'status': 'success'}

def read_gps_data(port, status_var):
    with serial.Serial(port, 9600, timeout=1) as ser:
        while True:
            line = ser.readline().decode('ascii', errors='replace')
            response = requests.post('http://127.0.0.1:5000/api/gps', data={'gps_data': line})
            if response.status_code != 200:
                print(f"Failed to send data to server: {response.content}")
            status_var.set("Connected to GPS")
            time.sleep(1)

def run_server():
    print("Server is running at http://localhost:5000/api/gps")
    app.run(port=5000)

def start_server(port, status_var):
    server_thread = threading.Thread(target=run_server)
    server_thread.start()

    gps_thread = threading.Thread(target=read_gps_data, args=(port, status_var))
    gps_thread.start()

def generate_credentials(tester_id_var):
    tester_id = ''.join(random.choice('0123456789') for _ in range(4))
    server_credentials[tester_id] = True
    tester_id_var.set(f"Generated tester ID: {tester_id}")

if __name__ == "__main__":
    root = tk.Tk()
    ports = ['COM' + str(i) for i in range(10)]  # replace with your available ports
    cb = ttk.Combobox(root, values=ports)
    cb.pack()
    status_var = tk.StringVar()
    status_label = tk.Label(root, textvariable=status_var)
    status_label.pack()
    connect_button = tk.Button(root, text="Connect", command=lambda: start_server(cb.get(), status_var))
    connect_button.pack()
    tester_id_var = tk.StringVar()
    tester_id_label = tk.Label(root, textvariable=tester_id_var)
    tester_id_label.pack()
    generate_button = tk.Button(root, text="Generate Tester ID", command=lambda: generate_credentials(tester_id_var))
    generate_button.pack()
    root.mainloop()
