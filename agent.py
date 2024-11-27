from cognitive_modules.action_selection import ActionSelection
from cognitive_modules.internal_state import InternalState
from cognitive_modules.pragmatic_analyst import ConversationContext
from cognitive_modules.self_monitor import SelfMonitor
from cognitive_modules.speaking_policy_manager import SpeakingPolicyManager
from memory_modules.memory_manager import MemoryManager

class Agent:
    def __init__(self, name, description, current_goal, schedule): 
        self.internal_state = InternalState(
            name=name,
            description=description,
            current_goal=current_goal,
            schedule=schedule,
            retrieved_memories=""
        )
        self.memory_manager = MemoryManager(self.internal_state)
        #self.self_monitor = SelfMonitor(self.internal_state)
        #self.conversation_context = ConversationContext()
        #self.speaking_policy_manager = SpeakingPolicyManager(self.conversation_context)
        #self.action_selection = ActionSelection(self.internal_state, self.speaking_policy_manager, self.conversation_context)
    
    def talk(self, question, world_info):
        self.memory_manager.recall(question)
        #self.self_monitor.update_summary(self.internal_state)
        #self.speaking_policy_manager.classify_and_update_emotions(question)
        #self.speaking_policy_manager.define_speaking_behavior()
        #self.action_selection.select_action(world_info)
        
        # response = self.generate_response(question)
        # print(response)
    
    def generate_response(self, question):
        return "This is a placeholder response for the question: " + question
    
    def add_st_memory(self, memory):
        self.memory_manager.store_st_memory(memory)
    
    def get_emotional_state(self):
        return self.internal_state.self_monitor_summary  # Placeholder logic
    
    def print_state(self):
        if self.internal_state : self.internal_state.print_internal_state()  
        # if self.speaking_policy_manager : print(self.speaking_policy_manager.define_speaking_behavior())  

if __name__ == "__main__":
    # Initialize the Agent with example data
    agent = Agent(
        name="Lautaro",
        description="Lider de los Mapuche, amistoso y valiente",
        current_goal="tu objetivo es guiar a nuevos guerreros mapuche a trascender a la próxima vida",
        schedule={"Monday": "Defender el territorio", "Tuesday": "Cazar", "Wednesday": "Reunión con otros líderes"}
    )
    agent.add_st_memory("Mundo: estas en una carpa mapuche que representa una sala de espera para la próxima vida")
    agent.add_st_memory("Mundo: el lugar esta lleno de poder magico y a la ves parece ser un viejo lugar de almacenamiento, lleno de cajas, barriles y sacos de cuero")
    agent.add_st_memory("Mundo: en el centro de la sala hay un fuego que no quema, pero que emana calor y luz")
    
    while True:
        question = input("Ask a question: ")
        if question == "exit":
            break
        agent.print_state()
        agent.talk(question, world_info={"un guerrero te habla"})
        

    # agent.talk("What is your purpose?", world_info={})  # Example conversation
