import socket             # Import socket module
from mic_vad_streaming import VADAudio
import os
import logging
import numpy as np
import deepspeech
import threading
import pyttsx3

def open_socket():
    sock = socket.socket()         # Create a socket object
    host = '127.0.0.1' # Get local machine name
    port = 2500             # Reserve a port for your service.
    sock.connect((host, port))
    return sock

def recieve(socket, engine):
    while(socket.fileno() != -1):
        text = socket.recv(2048)
        if(len(text) > 0):
            if(text == 'garbonzo'):
                print("closing socket")
                socket.close()
            else:
                engine.say(text.decode())
                engine.runAndWait()

def main(ARGS):
    engine = pyttsx3.init()
    sock = open_socket()
    reciever = threading.Thread(target=recieve, args=(sock, engine))
    reciever.start()

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
    stream_context = model.createStream()
    wav_data = bytearray()
    for frame in frames:
        if frame is not None:
            logging.debug("streaming frame")
            stream_context.feedAudioContent(np.frombuffer(frame, np.int16))
        else:
            logging.debug("end utterence")
            text = stream_context.finishStream()
            if(sock.fileno() != -1):
                sock.sendall(text.encode())
            else:
                break
            stream_context = model.createStream()
    sock.close()
    recieve.join()

if __name__ == '__main__':
    DEFAULT_SAMPLE_RATE = 16000

    import argparse
    parser = argparse.ArgumentParser(description="Stream from microphone to DeepSpeech using VAD")

    parser.add_argument('-v', '--vad_aggressiveness', type=int, default=3,
                        help="Set aggressiveness of VAD: an integer between 0 and 3, 0 being the least aggressive about filtering out non-speech, 3 the most aggressive. Default: 3")
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
