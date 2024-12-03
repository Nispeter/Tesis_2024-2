import numpy as np
from sentence_transformers import SentenceTransformer, util
import ollama

from utils.LLM_caller import LLMCaller

class ShortTermMemory:
    def __init__(self, long_term_memory=None, memory_size=5, forget_threshold=0.75, retrieval_threshold=3):
        self.memory = []  
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

    def print_memories(self,memories=None):
        if memories == None: memories = self.memory
        """
        Prints a formatted list of memories with their content and metadata.

        Args:
            memories (list): A list of memories, where each memory is a tuple or list
                            with format [text, embedding, count].
        """
        if not memories:
            print("No memories available.")
            return

        print("Current Memories:")
        print("-" * 40)
        for i, (text, _, count) in enumerate(memories):
            print(f"{i + 1}. Text: {text}")
            print(f"   Retrieval Count: {count}")
            print("-" * 40)

    def forget(self):
        """
        Forgets redundant or low-relevance memories based on similarity and usage count.
        """
        unique_memory = []
        for text, emb, count in self.memory:
            is_unique = True
            for _, other_emb, _ in unique_memory:
                if util.pytorch_cos_sim(emb, other_emb) > self.forget_threshold:
                    is_unique = False
                    break
            if is_unique:
                unique_memory.append([text, emb, count])


        #self.print_memories(unique_memory)
        unique_memory = sorted(unique_memory, key=lambda x: x[2], reverse=True)
        self.memory = unique_memory[:self.memory_size]
        #self.print_memories(self.memory)

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
            self.memory[i][2] += 1  # Incrementar contador de uso

        self.check_and_store_long_term()
        return [(text, score) for _, text, score in similarities]

    def check_and_store_long_term(self):
        """
        Summarizes and stores memories exceeding the retrieval threshold.
        Resets counters for stored memories.
        """
        if self.long_term_memory is None:
            return

        frequent_memories = [
            (text, count) for text, _, count in self.memory if count >= self.retrieval_threshold
        ]

        if frequent_memories:
            # Ordenar por relevancia y agrupar para resumen
            frequent_memories = sorted(frequent_memories, key=lambda x: x[1], reverse=True)
            texts = [text for text, _ in frequent_memories]
            summary = self.summarize_memories(" ".join(texts))
            
            print("Storing in long-term memory:", summary)
            self.long_term_memory.add_data([summary])

            # Reiniciar contador para los recuerdos promovidos
            for i, (text, _, count) in enumerate(self.memory):
                if text in texts:
                    self.memory[i][2] = 0

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
