import uuid
import threading
import os
import ollama
from flask import Flask, request, jsonify
from flask_cors import CORS
from queue import Queue

task_queue = Queue()
task_condition = threading.Condition()
results = {}

def classify_emotion(question):
    """
    Uses Ollama local model to classify the given question into emotions.
    Expected emotions: anticipation, joy, trust, fear, surprise, sadness, disgust, anger.
    """
    response = ollama.chat( model='llama3.2:3b', messages= [
        {
            "role": "user",
            "content": "classify the emotion of following dialogue and return only the word of the category without any other text, categoies: anticipation, joy, trust, fear, surprise, sadness, disgust, anger, none. " + question
        }
    ])
    print(response['message']['content'])
    return response['message']['content']

def worker():
    while True:
        task = task_queue.get()
        if task is None: 
            break
        task_id, task_type, question = task
        try:
            if task_type == "emotion_classification":
                answer = classify_emotion(question)
            else:
                answer = "Invalid task type"
            
            with task_condition:
                results[task_id] = answer
                task_condition.notify_all()  
        except Exception as e:
            print(f"Error processing task: {e}")
        finally:
            task_queue.task_done()

worker_thread = threading.Thread(target=worker, daemon=True)
worker_thread.start()

app = Flask(__name__)
CORS(app)

@app.route('/get_emotion_classification', methods=['POST'])
def get_emotion_classification():
    content = request.get_json()
    question = content.get('question')
    if not question:
        return jsonify({"error": "No question provided"}), 400

    task_id = str(uuid.uuid4())
    task_queue.put((task_id, "emotion_classification", question))
    
    with task_condition:
        task_condition.wait_for(lambda: task_id in results)
        answer = results.pop(task_id)
        return jsonify({"emotion": answer}), 200

@app.route('/shutdown', methods=['POST'])
def shutdown():
    task_queue.put(None)
    worker_thread.join()
    return jsonify({'status': 'Server shutting down...'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=8001)
