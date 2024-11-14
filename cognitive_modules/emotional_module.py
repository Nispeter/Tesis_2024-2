import ollama
from utils.prompts import emotional_prompts
from utils.LLM_caller import LLMCaller

class EmotionalModule:
    emotional_state = {
        "anticipation": 0,
        "joy": 0,
        "trust": 0,
        "fear": 0,
        "surprise": 0,
        "sadness": 0,
        "disgust": 0,
        "anger": 0
    }
    
    MAX_EMOTION_INTENSITY = 3

    def __init__(self):
        self.llm_client = LLMCaller(service="ollama", model_name="llama3.2:3b")
        
    def classify_emotion(self, question):
        """
        Uses Ollama local model to classify the given question into emotions.
        Expected emotions: anticipation, joy, trust, fear, surprise, sadness, disgust, anger, none.
        """
        prompt = emotional_prompts["classification_query"] + question
        response = self.llm_client.generate_text(prompt)
        self.update_emotional_state(response.strip().lower())
        return response.strip().lower()
    
    def update_emotional_state(self, emotion):
        """Updates the NPC's emotional state based on the classified emotion."""
        if emotion in self.emotional_state:
            self.emotional_state[emotion] = min(self.emotional_state[emotion] + 1, self.MAX_EMOTION_INTENSITY)

    def reset_emotional_state(self):
        """Resets all emotional states to zero if they reach MAX_EMOTION_INTENSITY."""
        for emotion, intensity in self.emotional_state.items():
            if intensity >= self.MAX_EMOTION_INTENSITY:
                self.emotional_state[emotion] = 0

    def speaking_policies(self):
        """Defines how the NPC responds based on emotional state thresholds."""
        if self.emotional_state["anger"] >= self.MAX_EMOTION_INTENSITY:
            response = "The NPC snaps at you angrily and refuses to answer."
        elif self.emotional_state["sadness"] >= self.MAX_EMOTION_INTENSITY:
            response = "The NPC remains silent, looking deeply saddened."
        elif self.emotional_state["joy"] >= 2:
            response = "The NPC responds enthusiastically: 'That's great to hear!'"
        elif self.emotional_state["trust"] >= 2:
            response = "The NPC leans in, confiding softly."
        elif self.emotional_state["fear"] >= 2:
            response = "The NPC looks around nervously and responds quietly."
        else:
            response = "The NPC responds in a neutral tone."
        
        return response

# em = EmotionalModule()
# emotion = em.classify_emotion("I am feeling very happy today.")
# print(emotion)
# print(em.emotional_state)