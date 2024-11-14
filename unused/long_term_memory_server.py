import uuid
import threading
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from queue import Queue
from RAG_module import add_new_data_to_kb, get_session_log_filename, setup_openai_key, load_and_process_local_documents, setup_retriever_and_qa, get_rag_answer
from graphRAG_module import get_graph_answer

# Global task queue and conditions
task_queue = Queue()
task_condition = threading.Condition()
results = {}

def worker():
    while True:
        task = task_queue.get()
        if task is None:  # Exit signal
            break
        task_id, task_type, question = task
        try:
            if task_type == "rag":
                #answer = get_rag_answer(question, retriever, prompt, primary_qa_llm)
                answer = get_rag_answer(question, retriever, primary_qa_llm)
            elif task_type == "graphrag":
                answer = get_graph_answer(question)
            elif task_type == "combined":
                answer = get_combined_answer(question)  
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

def get_combined_answer(question):
    rag_result = [None]
    graphrag_result = [None]

    def fetch_rag():
        rag_result[0] = get_rag_answer(question)

    def fetch_graphrag():
        graphrag_result[0] = get_graph_answer(question)

    rag_thread = threading.Thread(target=fetch_rag)
    graphrag_thread = threading.Thread(target=fetch_graphrag)
    rag_thread.start()
    graphrag_thread.start()

    rag_thread.join()
    graphrag_thread.join()

    return f"RAG Answer: {rag_result[0]}\nGraphRAG Answer: {graphrag_result[0]}"

# Initialize Flask app
app = Flask(__name__)
CORS(app)

@app.route('/rag_query', methods=['POST'])
def rag_query():
    content = request.get_json()
    question = content.get('question')
    if not question:
        return jsonify({"error": "No question provided"}), 400

    task_id = str(uuid.uuid4())
    task_queue.put((task_id, "rag", question))
    
    with task_condition:
        task_condition.wait_for(lambda: task_id in results)
        answer = results.pop(task_id)
        return jsonify({"answer": answer}), 200

@app.route('/graphrag_query', methods=['POST'])
def graphrag_query():
    content = request.get_json()
    question = content.get('question')
    if not question:
        return jsonify({"error": "No question provided"}), 400

    task_id = str(uuid.uuid4())
    task_queue.put((task_id, "graphrag", question))
    
    with task_condition:
        task_condition.wait_for(lambda: task_id in results)
        answer = results.pop(task_id)
        return jsonify({"answer": answer}), 200

@app.route('/combined_query', methods=['POST'])
def combined_query():
    content = request.get_json()
    question = content.get('question')
    if not question:
        return jsonify({"error": "No question provided"}), 400

    task_id = str(uuid.uuid4())
    task_queue.put((task_id, "combined", question))
    
    with task_condition:
        task_condition.wait_for(lambda: task_id in results)
        answer = results.pop(task_id)
        return jsonify({"answer": answer}), 200

@app.route('/shutdown', methods=['POST'])
def shutdown():
    task_queue.put(None)
    worker_thread.join()
    return jsonify({'status': 'Server shutting down...'}), 200

@app.route('/add_data', methods=['POST'])
def add_data():
    content = request.get_json()
    new_data = content.get('data')
    if not new_data or not isinstance(new_data, list):
        return jsonify({"error": "No data provided or data is not a list"}), 400

    try:
        add_new_data_to_kb(new_data)
        return jsonify({"status": "Data added successfully"}), 200
    except Exception as e:
        print(f"Error adding new data: {e}")
        return jsonify({"error": "Failed to add data"}), 500

@app.route('/get_key', methods=['GET'])
def get_api_key():
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        return jsonify({"error": "OpenAI API key is not set"}), 500
    return jsonify({"api_key": api_key})

if __name__ == '__main__':
    setup_openai_key()
    documents = load_and_process_local_documents(r"../ragtest/input/book.txt")
    retriever, prompt, primary_qa_llm = setup_retriever_and_qa(documents)
    app.run(debug=True, port=8000)
