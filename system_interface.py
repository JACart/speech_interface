# This module is written to be run using the python2.7 interpreter to 
# connect with ros Melodic
import socket
import rospy
from std_msgs.msg import Int8, String, Bool

host = ''
port = 2500
sock = socket.socket()
sock.bind((host, port))
sock.listen(1)
c, addr = sock.accept()     # Establish connection with client.
print('Got connection from: {}', addr)

def whisper(data):
   # try:
   #    c.sendall(data)
   # except:
   #    c.close()
   #    print("exception occured probably Broken Pipe")
   c.sendall(data.encode())

class sys_interface(object):
   def __init__(self):
        rospy.init_node('speech_detector')
        self.speech_text = rospy.Publisher('/speech_text', String, queue_size=10)
        self.text_speech = rospy.Subscriber('/text_speech', String, whisper)
        cart_stopped = False
   
   def anounce(self, text):
      print("Publishing")
      self.speech_text.publish(text)

anouncer = sys_interface()

while True:
   text = c.recv(2048)
   fo = open("Log.txt", "w")
   fo.write(text.decode())
   print("Data: %s" %text.decode())
   anouncer.anounce(text.decode())
   if("halt" in text.decode()):
      c.send('the close keyword is intentionally long so no one accidentally says it garbonzo beans'.encode())
      c.close()                # Close the connection
      break