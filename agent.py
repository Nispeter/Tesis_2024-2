from cognitive_modules.internal_states import InternalState
from cognitive_modules.emotional_module import EmotionalModule
from cognitive_modules.self_monitor import SelfMonitor
from cognitive_modules.speaking_policy_manager import SpeakingPolicyManager
from memory_modules.memory_manager import MemoryManager

class Agent:
    def __init__(self): 
        #self.memory_manager = MemoryManager()
        self.speaking_policy_manager = SpeakingPolicyManager()
        #self.self_monitor = SelfMonitor()
        #self.internal_state = InternalState()
        
    def talk(self,quiestion):
        response = self.generate_response(question)
        print(response)
    
    def generate_response(self, question):
        return 0
    
    def get_emotional_state(self):
        return self.emotional_module.emotional_state

if __name__ == "main":
    agent = Agent()
    # print(agent.get_emotional_state())
    