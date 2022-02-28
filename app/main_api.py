"""main"""

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

from common.config_reader import get_conf
from common.bme_sensor import BMESensor

# config for socket app and BME680 sensor
config = get_conf()

# BME680 Sensor variable in waiting...
bme_sensor = None

# Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@socketio.on('connect')
def connect(auth):
    emit('connect', {'data': 'Connected'})

@socketio.on('initialConnect')
def populate_all():
    emit('setTemp', bme_sensor.temperature)

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    bme_sensor = BMESensor(sea_level_pressure=config)
    socketio.run(app, host="0.0.0.0")