import rospy
from std_msgs.msg import String
# import pyttsx3
   
def talker():
    pub = rospy.Publisher('/text_speech', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    pub.publish("Driving to silicon valley")
    rate.sleep()

if __name__ == '__main__':
    
    # converter = pyttsx3.init()

    # voices = converter.getProperty('voices')
  
    # for voice in voices:
    #     # to get the info. about various voices in our PC 
    #     print("Voice:")
    #     print("ID: %s" %voice.id)
    #     print("Name: %s" %voice.name)
    #     print("Age: %s" %voice.age)
    #     print("Gender: %s" %voice.gender)
    #     print("Languages Known: %s" %voice.languages)

    try:
        talker()
    except rospy.ROSInterruptException:
        pass