#!/bin/bash
source Jac_speech/bin/activate
python system_interface.py &
sleep 1
echo Server up
python3 speech_interface.py -m deepspeech-0.9.3-models.pbmm -s deepspeech-0.9.3-models.scorer
killall Python