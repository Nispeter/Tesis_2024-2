from memory_modules.short_term_memory import ShortTermMemory
from memory_modules.long_term_memory import LongTermMemoryService

class MemoryManager():
    def __init__(self):
        
        self.long_term_memory = LongTermMemoryService()
        self.short_term_memory = ShortTermMemory(self.long_term_memory)
        print("Memory Manager initialized, missing features")
        
    def recall(prompt):
        pass