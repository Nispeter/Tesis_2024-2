import requests
import json

BASE_URL = "http://localhost:8001"

def test_emotion_classification(question):
    url = f"{BASE_URL}/get_emotion_classification"
    
    payload = {"question": question}
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
    
        if response.status_code == 200:
            result = response.json()
            print(f"Question: {question}")
            print(f"Emotion: {result}")
        else:
            print(f"Failed to get a response. Status code: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error while testing server: {e}")

import asyncio
from emotional_module import classify_emotion

async def main():
    question = "I'm feeling so excited about this new project!"
    emotion = await classify_emotion(question)
    print("Detected emotion:", emotion)

# Running the main function if this is the entry point
if __name__ == "__main__":
    asyncio.run(main())


# if __name__ == "__main__":
    
    # test_questions = [
    #     "sup?",
    #     # "I don't really know how to proceed, could you help me?",
    #     "I can’t wait for the concert next week! I’ve been looking forward to it for months.",
    #     "I just got promoted at work! I’m so thrilled and grateful for this opportunity!",
    #     "I know I can rely on you to keep this secret. You've always been there for me.",
    #     "I’m really nervous about this exam. I keep thinking about all the things that could go wrong.",
    #     "I didn’t expect to see you here! What a pleasant surprise!",
    #     "I’ve been feeling down since my friend moved away. It’s hard not having them around.",
    #     "I can’t believe people actually eat that. Just the smell alone makes me feel sick.",
    #     "I’m so frustrated with the way they handled this situation. They completely ignored our concerns!"
    #     ]
    
    # for question in test_questions:
    #     test_emotion_classification(question)





