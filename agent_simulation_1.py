

#IMPLEMENTATION THAT CAN BE PUT ON THE GAME CLIENT (AS A NPC)

import requests
import time

MEMORY_URL = 'http://localhost:8000'
EMOTIONAL_URL = 'http://localhost:8001'

self_state = {
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

def call_rag_server(question):
    """Calls the RAG server to retrieve a memory response."""
    try: 
        response = requests.post(f"{MEMORY_URL}/rag_query", json={"question": question})
        if response.status_code == 200:
            result = response.json()
            return result.get("answer", "")
        else:
            print(f"Failed to get a RAG response. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error calling RAG server: {e}")
    return ""

def call_emotion_server(question):
    """Calls the emotion server to classify the emotion of the input question."""
    try:
        response = requests.post(f"{EMOTIONAL_URL}/get_emotion_classification", json={"question": question})
        if response.status_code == 200:
            result = response.json()
            return result.get("emotion", "")
        else:
            print(f"Failed to get an emotion classification. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error calling emotion server: {e}")
    return ""

def update_emotional_state(emotion):
    """Updates the NPC's emotional state based on the classified emotion."""
    if emotion in self_state:
        self_state[emotion] = min(self_state[emotion] + 1, MAX_EMOTION_INTENSITY)

def reset_emotional_state():
    """Resets all emotional states to zero if they reach MAX_EMOTION_INTENSITY."""
    for emotion, intensity in self_state.items():
        if intensity >= MAX_EMOTION_INTENSITY:
            self_state[emotion] = 0

def generate_final_response(memory_response):
    """Generates a response based on emotional intensity."""
    response = ""

    if self_state["anger"] >= MAX_EMOTION_INTENSITY:
        response = "The NPC snaps at you angrily and refuses to answer."
    elif self_state["sadness"] >= MAX_EMOTION_INTENSITY:
        response = "The NPC remains silent, looking deeply saddened."
    elif self_state["joy"] >= 2:
        response = "The NPC responds enthusiastically: 'That's great to hear!'"
    elif self_state["trust"] >= 2:
        response = "The NPC leans in, confiding softly."
    elif self_state["fear"] >= 2:
        response = "The NPC looks around nervously and responds quietly."

    if not response:
        response = memory_response if memory_response else "The NPC is unsure how to respond."

    print(self_state)
    # reset_emotional_state() 
    return response

def npc_interaction_loop():
    """Main interaction loop for the NPC simulation."""
    print("NPC is ready. Type 'exit' to quit.")
    
    while True:
        question = input("You: ")
        if question.lower() == "exit":
            print("Ending NPC interaction.")
            break

        memory_response = call_rag_server(question)
        emotion = call_emotion_server(question)
        
        update_emotional_state(emotion)
        final_response = generate_final_response(memory_response)
        
        print(f"NPC: {final_response}")

if __name__ == "__main__":
    npc_interaction_loop()
