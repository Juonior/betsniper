from betsniper_web.app import app, socketio
from threading import Thread
from betsniper.run import main as sniperStart

if __name__ == '__main__':
    Thread(target=sniperStart).start()
    socketio.run(app,host="0.0.0.0", allow_unsafe_werkzeug=True)