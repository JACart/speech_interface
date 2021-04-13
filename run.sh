#!/bin/bash
gnome-terminal --tab -e "python $HOME/catkin_ws/src/speech_interface/system_interface.py"
sleep 3
echo "system interface up"
gnome-terminal --tab -e "python3 $HOME/catkin_ws/src/speech_interface/speech_interface.py -m deepspeech-0.9.3-models.pbmm"
sleep 3
echo "speech_interface up"
gnome-terminal --tab -e "python $HOME/catkin_ws/src/speech_interface/test_publisher.py"
