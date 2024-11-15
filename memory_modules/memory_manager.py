#from memory_modules.short_term_memory import ShortTermMemory
from memory_modules.long_term_memory import LongTermMemoryService

class MemoryManager():
    def __init__(self):
        #self.ShortTermMemory = ShortTermMemory()
        self.LongTermMemory = LongTermMemoryService()
        print("Memory Manager initialized, missing features")
        
    def recall(prompt):
        pass