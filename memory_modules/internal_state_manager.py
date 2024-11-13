import asyncio
from cognitive_modules.emotional_module import classify_emotion

class InternatState:
    metadata = [
        "name",
        "personality",
        "emotions",
        "current_goal"
        "knowledge",
        "schedule" 
    ]

    def __init__(self, name, personality, emotions, current_goal, knowledge, schedule):
        self.name = name
        self.personality = personality
        self.emotions = emotions
        self.current_goal = current_goal
        self.knowledge = knowledge
        self.schedule = schedule

if __name__ == "__main__":
    question = "I'm feeling so excited about this new project!"
    emotion = classify_emotion(question)
