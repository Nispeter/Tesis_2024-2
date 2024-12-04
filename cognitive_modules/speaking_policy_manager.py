from cognitive_modules.pragmatic_analyst import ConversationContext, PragmaticAnalyst
from cognitive_modules.emotional_module import EmotionalModule

class SpeakingPolicyManager:
    def __init__(self, conversation_context):
        self.emotional_module = EmotionalModule()
        self.pragmatic_analyst = PragmaticAnalyst(conversation_context)
        self.conversation_context = conversation_context
        
        self.speaking_policies = {
            "anticipation-1": "Speak with curiosity and expectation.",
            "joy-1": "Use an enthusiastic and cheerful tone.",
            "trust-1": "Speak confidently and reassuringly.",
            "fear-1": "Speak cautiously and with empathy.",
            "surprise-1": "Express astonishment or curiosity.",
            "sadness-1": "Use a calm and soothing tone.",
            "disgust-1": "Express clear disapproval.",
            "anger-1": "Speak assertively but without aggression.",
            "anger-2": "Speak firmly, but try to de-escalate the tone.",
            "joy-3": "Be jubilant and openly expressive."
        }
        print("Speaking policy manager initialized")

    def classify_and_update_emotions(self, input_text):
        classified_emotion = self.emotional_module.classify_emotion(input_text)
        print(f"Classified Emotion: {classified_emotion}")
        self.pragmatic_analyst.update_context(input_text)

    #TODO: make a function that aligns with SOLID
    def define_speaking_behavior(self):
        context = self.pragmatic_analyst.context_summary()
        behavior = context + "\n" + "Emotional State: " 
        emotional_state = self.emotional_module.emotional_state
        emotions = ""
        for emotion, intensity in emotional_state.items():
            if intensity > 0:  
                search_policy = f"{emotion}-{intensity}"
                if search_policy in self.speaking_policies:
                    emotions += self.speaking_policies[search_policy] + " "
                    
        if emotions == "":
            behavior += "neutral"
        else:
            behavior += emotions
            
        return behavior.strip()

#TODO: Implement a history system so it keeps track of the last 3-5 dialogues and its contexts.
#NOTE: A complete implementation or upgrade could handle the analysis with world rule based system as Cristian mentioned.

# Example Usage
# speaking_policy_manager = SpeakingPolicyManager()

# input_text = "I feel so disappointed with how things are going."
# speaking_policy_manager.classify_and_update_emotions(input_text)
# speaking_behavior = speaking_policy_manager.define_speaking_behavior()
# print("Speaking Behavior:", speaking_behavior)
