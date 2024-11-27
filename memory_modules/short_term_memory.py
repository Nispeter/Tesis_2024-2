import numpy as np
from sentence_transformers import SentenceTransformer, util
import ollama

from utils.LLM_caller import LLMCaller

class ShortTermMemory:
    def __init__(self, long_term_memory, memory_size=5, forget_threshold=0.75, retrieval_threshold=3):
        self.memory = []  # List of (text, embedding, retrieval_count) tuples
        self.memory_size = memory_size
        self.forget_threshold = forget_threshold
        self.retrieval_threshold = retrieval_threshold
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.long_term_memory = long_term_memory
        self.llm_client = LLMCaller("openai", "gpt-4o-mini")
        print("Short term memory system initialized")

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
        memories_as_string = "\n".join(frequent_memories) 
        if frequent_memories:
            summary = self.summarize_memories(memories_as_string)
            print("storing: " + summary)
            self.long_term_memory.add_data([summary])  
            for memory in self.memory:
                if memory[0] in frequent_memories:
                    memory[2] = 0

    def summarize_memories(self, memories):
        """
        Uses ollama to summarize a list of memories.
        """
        response = self.llm_client.generate_text(memories)
        # response = ollama.chat(
        #     model='llama3.2:3b',
        #     messages=[{
        #         "role": "user",
        #         "content": "Summarize at the best of your abilities the following memories without adding new information: " + " ".join(memories)
        #     }]
        # )
        #return response['message']['content']
        return response

# # Example usage
# long_term_memory = LongTermMemoryService()
# memory_system = ShortTermMemory(long_term_memory)

# # Add some example events
# memory_system.add_memory("User entered the room.")
# memory_system.add_memory("User asked a question about life")
# memory_system.add_memory("User left the room.")
# memory_system.add_memory("User discussed life meaning with a friend.")
# memory_system.add_memory("User said the meaning of life is 42")

# query = "asking about the meaning of life"
# print('asking..')
# retrieved_memories = memory_system.retrieve_memories(query, top_k=2)
# print("Retrieved memories:", retrieved_memories)
# retrieved_memories = memory_system.retrieve_memories(query, top_k=2)
# print("Retrieved memories:", retrieved_memories)
# retrieved_memories = memory_system.retrieve_memories(query, top_k=2)
# print("Retrieved memories:", retrieved_memories)
# retrieved_memories = memory_system.retrieve_memories(query, top_k=2)
# print("Retrieved memories:", retrieved_memories)
# retrieved_memories = memory_system.retrieve_memories(query, top_k=2)
# print("Retrieved memories:", retrieved_memories)
