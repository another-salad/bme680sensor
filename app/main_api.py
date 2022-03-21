"""main"""

import json
from hashlib import sha1

from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit

from common.config_reader import get_conf
from common.bme_sensor import BMESensorProperties


# config for socket app and BME680 sensor
CONFIG = get_conf()

# Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = CONFIG.SECRET_KEY
socketio = SocketIO(app)

class Watcher:
    """Watches the sensor properties, emits on change to a connected client"""

    watch_cache = dict()
    active_connections = set()

    def __init__(self, watch_obj):
        """init baby"""
        self.watch_obj = watch_obj

    def update(self, attrib: str):
        """Checks the cache, updates on value change, else just emits 'query' to keep the cycle going."""
        for active_conn in self.active_connections:
            active_conn_sha = sha1(repr(active_conn).encode('utf-8'), usedforsecurity=False).hexdigest()
            if hasattr(self.watch_obj, attrib):
                prop, value = getattr(self.watch_obj, attrib)
                if (self.watch_cache.get(active_conn_sha, None) is None):
                    # creates the initial dict
                    self.watch_cache[active_conn_sha] = dict()

                if (self.watch_cache[active_conn_sha].get(prop, None) is None):
                    self.watch_cache[active_conn_sha].update({prop: value})
                elif (self.watch_cache[active_conn_sha][prop] != value):
                    self.watch_cache[active_conn_sha][prop] = value

                emit(prop, value, room=active_conn)

# BME Sensor
bme_sensor = Watcher(BMESensorProperties(CONFIG))

def _set_sensor_values(bme_sensor):
    """Sends the sensor values to the client via the Watcher, then emits query so the
    client asks for an update."""
    for attrib in dir(bme_sensor.watch_obj):
        if attrib.startswith('get'):
            bme_sensor.update(attrib)
    
    emit('query')

@app.route('/api')
def api() -> json:
    """api call, returns all sensor data as json"""
    return_data = {}
    for attrib in dir(bme_sensor.watch_obj):
        if attrib.startswith('get'):
            key, value = getattr(bme_sensor.watch_obj, attrib)
            return_data[key.replace('get', '')] = value

    return jsonify(return_data)

@socketio.on('connect')
def connected():
    bme_sensor.active_connections.add(request.sid)
    emit('connect')


@socketio.on('disconnected')
def disconnected():
    bme_sensor.active_connections.remove(request.sid)


@app.route('/')
def index():
    """Main html page"""
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('query')
def query():
    """Updates sensor values"""
    _set_sensor_values(bme_sensor)


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0")