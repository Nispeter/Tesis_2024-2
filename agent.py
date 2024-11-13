
from memory_modules.memory_manager import MemoryManager

class Agent:
    def __init__(self): 
        self.memory_manager = MemoryManager()
        
    def talk(self,quiestion):
        response = self.generate_response(question)
        print(response)
    
    def generate_response(self, question):
        memory_response = self.memory_manager.get_memory_response(question)
        return final_response

if __name__ == "main":
    agent = Agent()
    