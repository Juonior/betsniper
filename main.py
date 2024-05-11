from betsniper_web.app import app, socketio
from threading import Thread
from betsniper_web.app.views import UpdateEvents
import time
def gg():
    pass

    # events_flask = []
    # event_flask = {
    #     'site1': "Fonbet",
    #     'type1': overlapping_bid[0],
    #     'link1': f[event]["url"],
    #     'coefficient1': f1,
    #     'matchName1': event,
    #     'site2': "Olimp",
    #     'type2': overlapping_bid[1],
    #     'link2': o[event2]["url"],
    #     'coefficient2': o2,
    #     'matchName2': event2,
    #     'profit': round(percent2,2),
    #     'time': first_appearance_times[ "".join([event,str(percent1),str(percent2)])].isoformat()
    # }
    # events_flask.append(event_flask)
    # with app.app_context():   
    #     UpdateEvents(events_flask)
if __name__ == '__main__':
    Thread(target=gg).start()
    socketio.run(app,host="0.0.0.0", allow_unsafe_werkzeug=True)