#!/bin/bash
gnome-terminal --tab -- bash -c 'python system_interface.py'
sleep 2
echo "system interface up"
gnome-terminal --tab -- bash -c 'exec -a speech_interface python3 speech_interface.py -m deepspeech-0.9.3-models.pbmm'
sleep 2
echo "speech_interface up"
speech_pid=$(pidof speech_interface)
echo "type 'y' to termintate the speech interface system"
user_input='n'
while [ $user_input = 'n' ]
do
    read -r
    if [ $REPLY = 'y' ]
    then
    pkill -f speech_interface
    user_input='y'
    fi
done
echo "Goodbye"
