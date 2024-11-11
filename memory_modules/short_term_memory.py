import numpy as np
import requests
from sentence_transformers import SentenceTransformer, util
import ollama

RAG_SERVER_URL = 'http://localhost:8000'

class ShortTermMemory:
    def __init__(self, memory_size=5, forget_threshold=0.75, retrieval_threshold=3):
        self.memory = []  # List of (text, embedding, retrieval_count) tuples
        self.memory_size = memory_size
        self.forget_threshold = forget_threshold
        self.retrieval_threshold = retrieval_threshold
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def add_memory(self, text):
        embedding = self.model.encode(text, convert_to_tensor=True)
        self.memory.append([text, embedding, 0])
        if len(self.memory) > self.memory_size:
            self.forget()

    def forget(self):
        unique_memory = []
        for i, (text, emb, count) in enumerate(self.memory):
            is_unique = True
            for _, other_emb, _ in unique_memory:
                if util.pytorch_cos_sim(emb, other_emb) > self.forget_threshold:
                    is_unique = False
                    break
            if is_unique:
                unique_memory.append((text, emb, count))

        self.memory = unique_memory[:self.memory_size]

    def summarize(self):
        texts = [text for text, _, _ in self.memory]
        return " ".join(texts) if texts else "No recent memories."

    def retrieve_memories(self, query, top_k=3):
        """
        Retrieves top_k memories most similar to the query and updates retrieval counts.
        """
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        similarities = [
            (i, text, util.pytorch_cos_sim(query_embedding, emb).item())
            for i, (text, emb, _) in enumerate(self.memory)
        ]
        similarities = sorted(similarities, key=lambda x: x[2], reverse=True)[:top_k]
        for i, _, _ in similarities:
            self.memory[i][2] += 1

        self.check_and_store_long_term()
        return [(text, score) for _, text, score in similarities]

    def check_and_store_long_term(self):
        """
        Summarizes and stores memories that exceed the retrieval threshold.
        """
        frequent_memories = [text for text, _, count in self.memory if count >= self.retrieval_threshold]

        if frequent_memories:
            summary = self.summarize_memories(frequent_memories)
            self.long_term_memory_store(summary)
            for memory in self.memory:
                if memory[0] in frequent_memories:
                    memory[2] = 0

    def summarize_memories(self, memories):
        """
        Uses ollama to summarize a list of memories.
        """
        response = ollama.chat(
            model='llama3.2:3b',
            messages=[{
                "role": "user",
                "content": "Summarize the following memories: " + " ".join(memories)
            }]
        )
        return response['message']['content']

    def long_term_memory_store(summary):
        """
        A placeholder function that would send the summarized memories to a long-term storage server.
        """
        url = f"{RAG_SERVER_URL}/add_data"
        payload = {"data":summary}
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Data stored succesfully.")
            print("Answer:", response.json().get("answer"))
        else:
            print("Data storate failed.")
            print("Error:", response.json().get("error", response.text))

# Example usage
memory_system = ShortTermMemory()

# Add some example events
memory_system.add_memory("User entered the room.")
memory_system.add_memory("User asked a question about memory systems.")
memory_system.add_memory("User left the room.")
memory_system.add_memory("User discussed memory retention techniques.")

query = "question about memory"
retrieved_memories = memory_system.retrieve_memories(query, top_k=2)
retrieved_memories = memory_system.retrieve_memories(query, top_k=2)
retrieved_memories = memory_system.retrieve_memories(query, top_k=2)
retrieved_memories = memory_system.retrieve_memories(query, top_k=2)
retrieved_memories = memory_system.retrieve_memories(query, top_k=2)
print("Retrieved memories:", retrieved_memories)
