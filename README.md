# IoT Data Visualization System

## Introduction
This project, consisting of `hostserver.py` and `client.py`, was developed as a proof-of-concept to demonstrate the feasibility of viewing real-time location data natively in Google Earth. Originally created as an example for the company I worked at, this application showcases the potential of integrating IoT data with geographic visualization tools.

## Purpose and Scope
This application serves as an introductory example to illustrate that real-time location tracking in Google Earth is achievable. It's important to note that this is a basic implementation, primarily designed for demonstration purposes. As the number of users increases and more sophisticated data management is required, a more complete and robust system would be necessary. This project is intended to inspire and provide a foundation for further development in this domain.

## Features
- **Server-Client Architecture**: Utilizes `hostserver.py` for server-side operations and `client.py` for the client-side interface.
- **Flask Web Server**: `hostserver.py` runs a Flask-based web server for handling data requests.
- **Data Processing and Visualization**: Processes and visualizes geographic data, leveraging `simplekml` for KML file generation.
- **ThingSpeak Integration**: Both scripts interact with ThingSpeak API for IoT data handling.
- **Real-Time Data Handling**: Uses threading for handling real-time data collection and processing.
- **Tkinter GUI**: Client-side graphical interface built with tkinter.
- **Google Earth Real-Time Visualization**: Visualize location data in real-time using Google Earth.

## Requirements
- Python 3.x
- Flask
- Tkinter
- Requests
- SimpleKML
- Additional libraries as needed by the scripts

Install these using pip:
```bash
pip install flask tkinter requests simplekml
```

## Setup
### Configuration
- **ThingSpeak Setup**: Configure both scripts with your ThingSpeak channel ID and API keys.
- **Serial Port Configuration**: For `hostserver.py`, set up the serial port to read data from your IoT device.

### Running the Server
1. Run `hostserver.py` to start the Flask server:
   ```bash
   python hostserver.py
   ```
2. The server will start processing data from the configured serial port and send it to ThingSpeak.

### Running the Client
1. Run `client.py` to start the client interface:
   ```bash
   python client.py
   ```
2. The client will fetch and display data from ThingSpeak, offering real-time visualization.

## Real-Time Location Visualization in Google Earth
To visualize real-time location data in Google Earth:
1. Ensure your system generates KML files with the location data.
2. Open Google Earth.
3. Go to 'File' > 'Open', and select the generated KML file.
4. Google Earth will display the location data, updating in real-time as new data is received.

## Using the GUI for Real-Time Visualization
1. Open the GUI provided by `client.py`.
2. Click the button to copy the KML file link to your clipboard.
3. In Google Earth, go to 'Network Link' and create a new link.
4. Paste the copied URL in the 'Link' field.
5. Google Earth will now fetch the KML file from the URL and update the location visualization in real-time.

## Security Note
Ensure your API keys and sensitive data are secured and not exposed publicly.

## Contributing
Feel free to fork, modify, and submit pull requests to enhance the functionalities.

## License
[Specify the License]

## Contact Information
For queries or feedback, please contact [Your Contact Information].
