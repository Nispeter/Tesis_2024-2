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
        #self.memory_manager = MemoryManager(self.internal_state)
        #self.self_monitor = SelfMonitor(self.internal_state)
        self.conversation_context = ConversationContext()
        self.speaking_policy_manager = SpeakingPolicyManager(self.conversation_context)
        self.action_selection = ActionSelection(self.internal_state, self.speaking_policy_manager, self.conversation_context)
    
    def talk(self, question, world_info):
        #self.memory_manager.recall(question)
        #self.self_monitor.update_summary(self.internal_state)
        self.speaking_policy_manager.classify_and_update_emotions(question)
        self.speaking_policy_manager.define_speaking_behavior()
        self.action_selection.select_action(world_info)
        
        # response = self.generate_response(question)
        # print(response)
    
    def generate_response(self, question):
        return "This is a placeholder response for the question: " + question
    
    def get_emotional_state(self):
        return self.internal_state.self_monitor_summary  # Placeholder logic
    
    def print_state(self):
        self.internal_state.print_internal_state()  # Call the print method
        print(self.speaking_policy_manager.define_speaking_behavior())  # Print the speaking behavior

if __name__ == "__main__":
    # Initialize the Agent with example data
    agent = Agent(
        name="Ebenezer Scrooge",
        description="A cognitive agent designed to interact with the world",
        current_goal="Warn about life events",
        schedule={"8 AM": "Start tasks", "10 AM": "Review progress"}
    )
    
    while True:
        question = input("Ask a question: ")
        if question == "exit":
            break
        agent.talk(question, world_info={"no aditional world info."})
        agent.print_state()
        
    agent.talk("What is your purpose?", world_info={"a person just approached you and asked something"})
    agent.print_state()  # Print the internal state
    # agent.talk("What is your purpose?", world_info={})  # Example conversation
