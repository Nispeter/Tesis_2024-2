import uuid
import threading
import os
from queue import Queue
from RAG_module import (
    add_new_data_to_kb, 
    get_session_log_filename, 
    setup_openai_key, 
    load_and_process_local_documents, 
    setup_retriever_and_qa, 
    get_rag_answer
)
from graphRAG_module import get_graph_answer

class RAGService:
    def __init__(self):
        self.task_queue = Queue()
        self.task_condition = threading.Condition()
        self.results = {}
        self.worker_thread = threading.Thread(target=self.worker, daemon=True)
        self.worker_thread.start()
        self.retriever, self.prompt, self.primary_qa_llm = self.initialize_system()

    def initialize_system(self):
        setup_openai_key()
        documents = load_and_process_local_documents(r"../ragtest/input/book.txt")
        return setup_retriever_and_qa(documents)

    def worker(self):
        while True:
            task = self.task_queue.get()
            if task is None:  # Exit signal
                break
            task_id, task_type, question = task
            try:
                if task_type == "rag":
                    answer = get_rag_answer(question, self.retriever, self.primary_qa_llm)
                elif task_type == "graphrag":
                    answer = get_graph_answer(question)
                elif task_type == "combined":
                    answer = self.get_combined_answer(question)
                else:
                    answer = "Invalid task type"

                with self.task_condition:
                    self.results[task_id] = answer
                    self.task_condition.notify_all()
            except Exception as e:
                print(f"Error processing task: {e}")
            finally:
                self.task_queue.task_done()

    def get_combined_answer(self, question):
        rag_result = [None]
        graphrag_result = [None]

        def fetch_rag():
            rag_result[0] = get_rag_answer(question, self.retriever, self.primary_qa_llm)

        def fetch_graphrag():
            graphrag_result[0] = get_graph_answer(question)

        rag_thread = threading.Thread(target=fetch_rag)
        graphrag_thread = threading.Thread(target=fetch_graphrag)
        rag_thread.start()
        graphrag_thread.start()

        rag_thread.join()
        graphrag_thread.join()

        return f"RAG Answer: {rag_result[0]}\nGraphRAG Answer: {graphrag_result[0]}"

    def add_task(self, task_type, question):
        task_id = str(uuid.uuid4())
        self.task_queue.put((task_id, task_type, question))
        with self.task_condition:
            self.task_condition.wait_for(lambda: task_id in self.results)
            answer = self.results.pop(task_id)
            return answer

    def add_data(self, new_data):
        if not new_data or not isinstance(new_data, list):
            raise ValueError("Data is not provided or not in a list format")
        add_new_data_to_kb(new_data)

    def get_api_key(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise EnvironmentError("OpenAI API key is not set")
        return api_key

    def shutdown(self):
        self.task_queue.put(None)
        self.worker_thread.join()

# Example usage:
if __name__ == '__main__':
    service = RAGService()
    try:
        # Example of adding a task
        answer = service.add_task("rag", "What is the meaning of life?")
        print(f"Answer: {answer}")

        # Example of adding new data
        service.add_data(["New data point 1", "New data point 2"])
        
        # Example of getting the API key
        api_key = service.get_api_key()
        print(f"API Key: {api_key}")
    finally:
        service.shutdown()
