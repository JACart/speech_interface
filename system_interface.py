# This module is written to be run using the python2.7 interpreter to 
# connect with ros Melodic
import socket
import rospy
from std_msgs.msg import Int8, String, Bool
host = ''
port = 3010
sock = socket.socket()
sock.bind((host, port))
sock.listen(1)
c, addr = sock.accept()     # Establish connection with client.
print('Got connection from: {}', addr)

port = 3011
whisper_sock = socket.socket()
whisper_sock.bind((host, port))
whisper_sock.listen(1)
whisper_c, whisper_addr = whisper_sock.accept()
print('Got connection from: {}', whisper_addr)

# Sends data 
def whisper(data):
   try:
      print(str(data))
      whisper_c.send(str(data))
      print(whisper_c.fileno())
   except:
      whisper_c.close()
      print("exception occured probably Broken Pipe")


class sys_interface(object):
   def __init__(self):
        rospy.init_node('speech_detector')
        self.speech_text = rospy.Publisher('/speech_text', String, queue_size=10)
        self.text_speech = rospy.Subscriber('/text_speech', String, whisper)
        cart_stopped = False
   
   def anounce(self, text):
      self.speech_text.publish(text)

anouncer = sys_interface()
try:
   while True:
      text = c.recv(2048)
      if(len(text.decode()) > 0):
         fo = open("Log.txt", "w")
         fo.write(text.decode())
         print("Data: %s" %text.decode())
         anouncer.anounce(text.decode())
         if("halt" in text.decode()):
            c.send('garbonzo'.encode())
            c.close()                # Close the connection
            break
      else:
         c.close()
         break
finally:
   c.close()