from betsniper_web.app import app, socketio
from flask import render_template
from flask_socketio import emit

@app.route('/', methods=['GET'])
def show_events():
    return render_template("index.html", events=[])

@socketio.on('new_event')
def UpdateEvents(events_flask):
    emit('update_events', {'events_flask': events_flask}, broadcast=True,namespace="/")