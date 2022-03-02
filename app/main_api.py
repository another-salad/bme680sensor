"""main"""

from time import sleep

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

from common.config_reader import get_conf
from common.bme_sensor import BMESensorProperties


# config for socket app and BME680 sensor
CONFIG = get_conf()

# Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = CONFIG.SECRET_KEY
socketio = SocketIO(app)

class Emitter:
    """Emits the sensor properties to a connected client"""

    def __init__(self, watch_obj):
        """init baby"""
        self.watch_obj = watch_obj

    def update(self, attrib):
        """emits updated value for attrib"""
        if hasattr(self.watch_obj, attrib):
            property, value = getattr(self.watch_obj, attrib)
            emit(property, value)

# BME Sensor
bme_sensor = Emitter(BMESensorProperties(CONFIG))

def _set_sensor_values(bme_sensor):
    """Sends the sensor values to the client via the Emitter, then emits query so the
    client asks for an update."""
    for attrib in dir(bme_sensor.watch_obj):
        if attrib.startswith('get'):
            bme_sensor.update(attrib)
    
    emit('query')

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