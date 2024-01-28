import tkinter as tk
import threading
import requests
import simplekml
import http.server
import socketserver
import time

api_key = "LTMA881ARBZ9ERK4"  # Your Thingspeak Read API Key
channel_id = "2358572"  # Your Thingspeak Channel ID
filename = "default"  # Default filename

def fetch_gps_data(points, url_text):
    while True:
        try:
            response = requests.get(f'https://api.thingspeak.com/channels/{channel_id}/feeds.json?api_key={api_key}&results=1')
            data = response.json()
            if 'feeds' in data and data['feeds']:
                entry = data['feeds'][0]
                coords = entry['field1'].split(',')
                if len(coords) == 2:
                    lat, lon = map(float, coords)
                    points.append((lon, lat))
                    print(f"Latitude: {lat}, Longitude: {lon}")
                    update_kml(points)
                    update_url(url_text)
        except Exception as e:
            print(f"Failed to fetch data from ThingSpeak: {e}")
        time.sleep(1)

def start_server():
    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), Handler)
    print(f"Serving at port {PORT}")
    threading.Thread(target=httpd.serve_forever, daemon=True).start()

def start_fetching(points, url_text):
    threading.Thread(target=fetch_gps_data, args=(points, url_text), daemon=True).start()

def update_url(url_text):
    url = f"http://localhost:8000/{filename}.kml"
    url_text.config(state='normal')
    url_text.delete('1.0', tk.END)
    url_text.insert('1.0', url)
    url_text.config(state='disabled')

def update_kml(points):
    kml = simplekml.Kml()
    for i, point in enumerate(points):
        pnt = kml.newpoint(coords=[point])
        if i == len(points) - 1:
            pnt.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/paddle/blu-circle.png'
            pnt.iconstyle.scale = 1.0
        else:
            pnt.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/paddle/grn-circle.png'
            pnt.iconstyle.scale = 0.5
    kml.save(f"{filename}.kml")

def main():
    root = tk.Tk()
    root.title("GPS Data Fetcher")

    points = []

    # Entry for Filename
    filename_entry = tk.Entry(root)
    filename_entry.pack()

    # Set Filename Button
    set_filename_button = tk.Button(root, text="Set Filename", command=lambda: set_filename(filename_entry))
    set_filename_button.pack()

    # Start Server and Fetching Buttons
    start_button = tk.Button(root, text="Start Server and Fetching", command=lambda: start_server_and_fetching(points, url_text))
    start_button.pack()

    # URL Display
    url_text = tk.Text(root, height=1, width=40)
    url_text.pack()

    root.mainloop()

def set_filename(entry):
    global filename
    filename = entry.get()

def start_server_and_fetching(points, url_text):
    start_server()
    start_fetching(points, url_text)

if __name__ == "__main__":
    main()
