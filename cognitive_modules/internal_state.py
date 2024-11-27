
class InternalState:
    def __init__(self, name, description, current_goal, retrieved_memories, schedule):
        self.name = name
        self.description = description
        self.current_goal = current_goal
        self.schedule = schedule
        self.retrieved_memories = retrieved_memories
        self.self_monitor_summary = "none"
        print("Internal State initialized")
        
    def print_internal_state(self):
        print("\n--- Internal State ---")
        print(f"Name: {self.name}")
        print(f"Description: {self.description}")
        print(f"Current Goal: {self.current_goal}")
        print(f"Schedule: {self.schedule}")
        print(f"Retrieved Memories: {self.retrieved_memories}")
        print(f"Self-Monitor Summary: {self.self_monitor_summary}")
        print("----------------------\n")
        
    def summarize_states(self):
        return (
            f"--- Internal State ---\n"
            f"Name: {self.name}\n"
            f"Description: {self.description}\n"
            f"Current Goal: {self.current_goal}\n"
            f"Schedule: {self.schedule}\n"
            f"Retrieved Memories: {self.retrieved_memories}\n"
            f"Self-Monitor Summary: {self.self_monitor_summary}\n"
            f"----------------------"
        )