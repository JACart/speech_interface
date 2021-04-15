import rospy
from std_msgs.msg import String
   
def talker():
    pub = rospy.Publisher('/text_speech', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    pub.publish("Hello passenger. This is a voice test. How am I sounding?")
    rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass