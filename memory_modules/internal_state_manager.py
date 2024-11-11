import asyncio
from emotional_module import classify_emotion

if __name__ == "__main__":
    question = "I'm feeling so excited about this new project!"
    emotion = classify_emotion(question)
