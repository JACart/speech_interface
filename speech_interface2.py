import socketio
import pyttsx3

sio = socketio.Client()
sio.connect("http://localhost:8021/", namespaces=["/speech"])
print("running here")
sio.emit("test", {"data": "test"}, namespace="/speech")

engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-20)
engine.setProperty('voice', 'english-us') #Voice 16 is us english

def emit():
    print("attemtping to emit")
    sio.emit('spoke', {"data": 'what we hear'}, namespace='/speech')
    print("wth is it doing")

@sio.event(namespace='/speech')
def tts(data):
    engine.say(data)
    engine.runAndWait()
    emit()
