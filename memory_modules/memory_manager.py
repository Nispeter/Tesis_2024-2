from memory_modules.short_term_memory import ShortTermMemory
from memory_modules.long_term_memory import LongTermMemory
from utils.prompts import long_term_memory_prompts

class MemoryManager():
    def __init__(self, internal_state):
        self.long_term_memory = LongTermMemory()
        self.short_term_memory = ShortTermMemory(self.long_term_memory)
        self.internal_state = internal_state
        internal_state.description += ' ' + self.get_character(internal_state.name)
        print("Memory Manager initialized, missing features")
        
    def recall(self, prompt):
        distant_memories = self.long_term_memory.retrieve_memories(prompt)
        recent_memories = self.short_term_memory.retrieve_memories(prompt, k=3)
        self.short_term_summary.add_memory("the player says: " + prompt)
        self.internal_state.knowledge = distant_memories + recent_memories
    
    def get_character(self, character_name):
        starter_prompt = f"Using the dataset, write a detailed and cohesive paragraph describing the character {character_name}. "
        return self.long_term_memory.retrieve_memories(starter_prompt + long_term_memory_prompts["get_character"])