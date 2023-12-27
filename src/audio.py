import rospy
from online_audio_kit import AudioKit

from home_online_audio_kit_pkg.srv import llm, stt

from std_msgs.msg import String

# ===== Configure =======

LANGUAGE = "ja"
VOSK_MODEL_PATH = None
VOSK_MODEL_NAME = None
OPENAI_API_KEY = None

# ======================

class AudioSystem:
    def __init__(self):
        self.audio = AudioKit(language=LANGUAGE, vosk_model_name=VOSK_MODEL_NAME, vosk_model_path=VOSK_MODEL_PATH)
        
        # vosk 
        self.vosk_state = False
        self.vosk_pub = rospy.Publisher("vosk", String, queue_size=1)
        rospy.Subscriber("vosk_toggle", String, self.vosk_callback)
        
        # Speech To Text
        rospy.service("stt", stt, self.stt_callback)

        # Text to Speech
        rospy.Subscriber("tts", String, self.tts_callback)

        # LLM
        rospy.service("llm", llm, self.llm_callback)

    def vosk_callback(self, msg):
        if (msg.mode == "on"):
            self.vosk_state = True
        elif (msg.mode == "off"):
            self.vosk_state = False

        if (self.vosk_state):
            for text in self.audio.vosk():
                self.vosk_pub.publish(text)
    
    def stt_callback(self, msg):
        self.stt_pub(self.audio.stt())
    
    def tts_callback(self, msg):
        self.audio.tts(msg.text)

    def llm_callback(self, msg):
        return self.audio.llm(msg.text, msg.prompt)

if __name__ == "__main__":
    rospy.loginfo("Start Audio node.")
    rospy.init_node("audio")
    audio_system = AudioSystem()
    rospy.spin()
