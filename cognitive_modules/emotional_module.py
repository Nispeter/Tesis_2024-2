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
        self.llm_client = LLMCaller("openai", "gpt-4o-mini")        #NOTE: llama3.2:3b is pretty bad at classifying emotions. It's not very accurate.
        print("Emotional Module initialized")
        
    def classify_emotion(self, question):
        """
        Uses Ollama local model to classify the given question into one the 8 following emotions and none other.
        Expected emotions: anticipation, joy, trust, fear, surprise, sadness, disgust, anger, none.
        """
        
        prompt = emotional_prompts["classification_query"] + question
        response = self.llm_client.generate_text(prompt)
        self.update_emotional_state(response.lower())
        return response.lower()
    
    def update_emotional_state(self, emotion):
        """Updates the NPC's emotional state based on the classified emotion."""
        if emotion in self.emotional_state:
            self.emotional_state[emotion] = min(self.emotional_state[emotion] + 1, self.MAX_EMOTION_INTENSITY)

    def reset_emotional_state(self):
        """Resets all emotional states to zero if they reach MAX_EMOTION_INTENSITY."""
        for emotion, intensity in self.emotional_state.items():
            if intensity >= self.MAX_EMOTION_INTENSITY:
                self.emotional_state[emotion] = 0

    
# Example Usage
# em = EmotionalModule()
# emotion = em.classify_emotion("I am feeling very happy today.")
# print(emotion)
# print(em.emotional_state)