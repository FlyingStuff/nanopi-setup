import serial
import threading
import sys
from flask import Flask, Response, redirect
app = Flask(__name__)


def parse_nmea_line(msg):
    def parse_deg(field):
        if len(field.split('.')) != 2:
            return None
        first, second = field.split('.')
        degree = first[:-2]
        minutes = first[-2:] + '.' + second
        return int(degree) + float(minutes)/60

    try:
        msg_fields = msg.split(',')
        if msg_fields[0][-3:] == 'GGA' and len(msg_fields) == 15:
            lat = parse_deg(msg_fields[2])
            if lat is not None and msg_fields[3] == 'S':
                lat = -lat
            lng = parse_deg(msg_fields[4])
            if lng is not None and msg_fields[5] == 'W':
                lng = -lng
            sats = int(msg_fields[7])
            alt = float(msg_fields[9])
            return {'lat': lat, 'lng': lng, 'alt': alt, 'sats': sats}
    except Exception as e:
        print(e)


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
        print(line)
        with last_lines_lock:
            last_lines.append(line)
            while len(last_lines) > 50:
                last_lines.pop(0)
        coordinates_update = parse_nmea_line(line)
        if coordinates_update is not None:
            print(coordinates_update)
            with coordinates_lock:
                coordinates.update(coordinates_update)

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
