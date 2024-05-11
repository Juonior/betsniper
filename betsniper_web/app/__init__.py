from flask import Flask
from flask_socketio import SocketIO
import os,sys


base_dir = '..'
if hasattr(sys, '_MEIPASS'):
    base_dir = os.path.join(sys._MEIPASS)

app = Flask(__name__,static_folder=os.path.join(base_dir, 'static'), template_folder=os.path.join(base_dir, 'templates'))
socketio = SocketIO(app,async_mode='gevent')


from betsniper_web.app import views
