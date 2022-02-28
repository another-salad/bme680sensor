"""main"""

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

from common.config_reader import get_conf

app_config = get_conf()
app = Flask(__name__)
app.config['SECRET_KEY'] = app_config.SECRET_KEY
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@socketio.on('connect')
def test_connect(auth):
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0")