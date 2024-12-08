import os
from memory_modules.RAG_module import (
    add_new_data_to_kb,
    setup_openai_key,
    load_and_process_local_documents,
    setup_retriever_and_qa,
    get_rag_answer
)

#TODO: use openai from LLMCaller

class LongTermMemory:
    def __init__(self):
        self.retriever, self.prompt, self.primary_qa_llm = self.initialize_system()
        print("Long term memory system initialized")

    def initialize_system(self):
        setup_openai_key()
        documents = load_and_process_local_documents(r"ragtest/input/book_fleeting.txt")        #TODO: make dinamyc reference to a folder
        return setup_retriever_and_qa(documents, "data/embeddings")

    def retrieve_memories(self, question):
        """Process a single RAG question and return the answer."""
        try:
            #print("rag_question: " + question)
            return get_rag_answer(question, self.retriever, self.primary_qa_llm)
        except Exception as e:
            print(f"Error processing question: {e}")
            return "Error processing question."

    def add_data(self, new_data):
        """Add new data to the knowledge base."""
        if not new_data or not isinstance(new_data, list):
            raise ValueError("Data is not provided or not in a list format")
        try:
            add_new_data_to_kb(new_data)
            print("Data successfully added to the knowledge base.")
        except Exception as e:
            print(f"Error adding data: {e}")

    def get_api_key(self):
        """Retrieve the OpenAI API key from the environment."""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise EnvironmentError("OpenAI API key is not set")
        return api_key


# Usage example

# try:
#     service = LongTermMemoryService()

#     # Example questions
#     print(service.retrieve_memories("What is the meaning of life for Scrooge?"))
#     print(service.retrieve_memories("Who was Scrooge?"))

#     # Adding new data to the knowledge base
#     service.add_data(["The meaning of life for Scrooge was the freedom of the Mapuche people"])

#     # Asking the question again with updated knowledge base
#     print(service.ask_question("What is the meaning of life for Scrooge?"))

# except Exception as e:
#     print(f"An error occurred: {e}")
