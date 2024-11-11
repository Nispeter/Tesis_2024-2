import ollama
import asyncio

def classify_emotion(question):
    """
    Uses Ollama local model to classify the given question into emotions.
    Expected emotions: anticipation, joy, trust, fear, surprise, sadness, disgust, anger, none.
    """
    response = ollama.chat(
        model='llama3.2:3b',
        messages=[
            {
                "role": "user",
                "content": (
                    "classify the emotion of following dialogue and return only the word of the category without any other text, "
                    "categories: anticipation, joy, trust, fear, surprise, sadness, disgust, anger, none. " + question
                )
            }
        ]
    )
    print(response['message']['content'])
    return response['message']['content']
