"""main"""

import json

from flask import Flask, jsonify, render_template
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

    watch_cache = {}

    def __init__(self, watch_obj):
        """init baby"""
        self.watch_obj = watch_obj

    def update(self, attrib):
        """Checks the cache, updates on value change, else just emits 'query' to keep the cycle going."""
        if hasattr(self.watch_obj, attrib):
            prop, value = getattr(self.watch_obj, attrib)
            if self.watch_cache.get(prop, None) is None or self.watch_cache[prop] != value:
                self.watch_cache[prop] = value
                emit(prop, value)
                return

        emit('query')

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
            return_data[key.strip('get')] = value

    return jsonify(return_data)

@app.route('/')
def index():
    """Main html page"""
    return render_template('index.html', async_mode=socketio.async_mode)

@socketio.on('query')
def query():
    """Updates sensor values"""
    _set_sensor_values(bme_sensor)

@socketio.on('disconnect')
def disconnect():
    """This currently does nothing"""
    pass

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0")