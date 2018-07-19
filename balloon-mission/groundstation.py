import serial
import threading
import sys
from flask import Flask, Response, redirect
app = Flask(__name__)


port = '/dev/ttyUSB0'
if len(sys.argv) > 1:
    port = sys.argv[1]

modem = serial.Serial(port, baudrate=57600)
log = open('gps_log.txt', 'a+')
last_lines_lock = threading.Lock()
last_lines = []
coordinates_lock = threading.Lock()
coordinates = {'lat': 0, 'lng': 0, 'alt': 0}

def read_serial():
    while True:
        line = modem.readline().decode(encoding="ascii", errors="ignore")
        log.write(line)
        with last_lines_lock:
            last_lines.append(line)
            while len(last_lines) > 50:
                last_lines.pop(0)
        with coordinates_lock:
            coordinates['lat'] = 1
            coordinates['lng'] = 2
            coordinates['alt'] = 3

serial_thread = threading.Thread(target=read_serial)
serial_thread.start()


@app.route("/")
def links():
    text = '''<!doctype html>
    <html><body>
        <h1><p><a href="map">map</a></p></h1>
        <h1><p><a href="raw">raw</a></p></h1>
        <h1><p><a href="gps">gps</a></p></h1>
    </body></html>'''
    return Response(text, mimetype='text/html')

@app.route("/raw")
def raw_output():
    with last_lines_lock:
        content = last_lines.copy()
    text = ''.join(content)
    return Response(text, mimetype='text/plain')

@app.route("/gps")
def gps_output():
    with coordinates_lock:
        text = str(coordinates)
    return Response(text, mimetype='text/plain')

@app.route("/map")
def google_maps_app_link():
    with coordinates_lock:
        link = 'comgooglemaps://?center={lat},{lng}&zoom=14&q={lat},{lng}'.format(**coordinates)
    return redirect(link)

@app.route("/web")
def google_maps_web_link():
    with coordinates_lock:
        link = "http://www.google.com/maps/place/{lat},{lng}".format(**coordinates)
    return redirect(link, code=302)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
