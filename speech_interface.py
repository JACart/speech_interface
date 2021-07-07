import socket             # Import socket module
from mic_vad_streaming import VADAudio
import os
import logging
import numpy as np
import deepspeech
import threading
import pyttsx3
from halo import Halo
import subprocess
from time import sleep
import socketio

sio = socketio.Client()


def open_socket(port):
    sock = socket.socket()         # Create a socket object
    host = '127.0.0.1' # Get local machine name
    sock.connect((host, port))
    return sock

def recieve(engine):
    sleep(3)
    try:
        socket = open_socket(4343)
    except Exception as e:
        print(e)
        print("connection refused. Most likely busy port.")
        
    text = "Hello World"
    try:
        while(len(text) > 0):
            text = socket.recv(2048)
            if not text:
                break
            if(len(text) > 0):
                if('garbonzo' in text.decode()):
                    print("closing socket")
                    socket.close()
                    break
                else:
                    lines = text.decode()
                    engine.say(lines[5:])
                    engine.runAndWait()
    finally:
        socket.close()

def send_voice():
    socket = open_socket(4445)
    print("setting connected")
    connected = 42

    # Load DeepSpeech model
    if os.path.isdir(ARGS.model):
        model_dir = ARGS.model
        ARGS.model = os.path.join(model_dir, 'output_graph.pb')
        ARGS.scorer = os.path.join(model_dir, ARGS.scorer)

    print('Initializing model...')
    logging.info("ARGS.model: %s", ARGS.model)
    model = deepspeech.Model(ARGS.model)
    if ARGS.scorer:
        logging.info("ARGS.scorer: %s", ARGS.scorer)
        model.enableExternalScorer(ARGS.scorer)

    # Start audio with VAD
    vad_audio = VADAudio(aggressiveness=ARGS.vad_aggressiveness,
                         device=ARGS.device,
                         input_rate=ARGS.rate,
                         file=ARGS.file)
    print("Listening (ctrl-C to exit)...")
    frames = vad_audio.vad_collector()

    # Stream from microphone to DeepSpeech using VAD
    spinner = None
    if not ARGS.nospinner:
        spinner = Halo(spinner='line')
    stream_context = model.createStream()
    wav_data = bytearray()
    for frame in frames:
        if frame is not None:
            if spinner: spinner.start()
            logging.debug("streaming frame")
            stream_context.feedAudioContent(np.frombuffer(frame, np.int16))
            if ARGS.savewav: wav_data.extend(frame)
        else:
            if spinner: spinner.stop()
            logging.debug("end utterence")
            if ARGS.savewav:
                vad_audio.write_wav(os.path.join(ARGS.savewav, datetime.now().strftime("savewav_%Y-%m-%d_%H-%M-%S_%f.wav")), wav_data)
                wav_data = bytearray()
            text = stream_context.finishStream()
            print("Recognized: %s" % text)
            socket.send(text.encode())
            stream_context = model.createStream()
            if("halt" in text):
                socket.close()
                break
    socket.close()


@sio.event(namespace="/speech")
def speech(sid, data):
    emit()
    lines = text.decode()
    engine.say(lines)
    engine.runAndWait()

def emit():
    sio.emit('speech', {"data": 'what we hear'}, namespace='/speech')

def main(ARGS):
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-20)
    engine.setProperty('voice', 'english-us') #Voice 16 is us english

    # reciever = threading.Thread(target=recieve, args=(engine, ))
    # sender = threading.Thread(target=send_voice)

    # sender.start()
    # reciever.start()

    # reciever.join()
    # sender.join()

    sio.connect("http://localhost:8021/")

  

if __name__ == '__main__':
    DEFAULT_SAMPLE_RATE = 16000

    import argparse
    parser = argparse.ArgumentParser(description="Stream from microphone to DeepSpeech using VAD")

    parser.add_argument('-v', '--vad_aggressiveness', type=int, default=3,
                        help="Set aggressiveness of VAD: an integer between 0 and 3, 0 being the least aggressive about filtering out non-speech, 3 the most aggressive. Default: 3")
    parser.add_argument('--nospinner', action='store_true',
                        help="Disable spinner")
    parser.add_argument('-w', '--savewav',
                        help="Save .wav files of utterences to given directory")
    parser.add_argument('-f', '--file',
                        help="Read from .wav file instead of microphone")

    parser.add_argument('-m', '--model', required=True,
                        help="Path to the model (protocol buffer binary file, or entire directory containing all standard-named files for model)")
    parser.add_argument('-s', '--scorer',
                        help="Path to the external scorer file.")
    parser.add_argument('-d', '--device', type=int, default=None,
                        help="Device input index (Int) as listed by pyaudio.PyAudio.get_device_info_by_index(). If not provided, falls back to PyAudio.get_default_device().")
    parser.add_argument('-r', '--rate', type=int, default=DEFAULT_SAMPLE_RATE,
                        help="Input device sample rate. Default: {DEFAULT_SAMPLE_RATE}. Your device may require 44100.")

    ARGS = parser.parse_args()
    main(ARGS)
