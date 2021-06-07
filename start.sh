#!/bin/bash
gnome-terminal --tab -- /bin/sh -c 'python system_interface.py; exec bash'
sleep 3
echo "system interface up"
gnome-terminal --tab -- /bin/sh -c 'python3 speech_interface.py -m deepspeech-0.9.3-models.pbmm; exec bash'
sleep 3
echo "speech_interface up"
