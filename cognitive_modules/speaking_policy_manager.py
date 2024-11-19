from cognitive_modules.emotional_module import EmotionalModule
from cognitive_modules.pragmatic_analyst import PragmaticAnalyst

class SpeakingPolicyManager():
    def __init__(self):
        self.emotional_module = EmotionalModule()
        self.pragmatic_analyst = PragmaticAnalyst()
        
speaking_policies = {
    "anticipation-1": "",
    "joy-1": "",
    "trust-1": "",
    "fear-1": "",
    "surprise-1": "",
    "sadness-1": "",
    "disgust-1": "",
    "anger-1": ""
}