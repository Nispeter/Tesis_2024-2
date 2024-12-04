from cognitive_modules.internal_state import InternalState
from utils.LLM_caller import LLMCaller
from utils.prompts import self_monitor_prompts

class SelfMonitor:
    def __init__(self, internal_state):
        #self.previous_summary = ""
        self.internal_state = internal_state
        self.llm_client = LLMCaller(service="groq", model_name="llama-3.1-8b-instant")
        print("Self Monitor initialized")
        
    def update_summary(self):
        """Updates the summary using the provided InternalState object."""
        self.previous_summary = self.generate_new_summary()
        self.internal_state.self_monitor_summary = self.previous_summary
        
    def generate_new_summary(self):
        prompt = (
            f"Previous Summary:\n{self.internal_state.self_monitor_summary}\n\n"
            "Current State:\n"
            f"- Name: {self.internal_state.name}\n"
            f"- Personality: {self.internal_state.description}\n"
            f"- Current Goal: {self.internal_state.current_goal}\n"
            f"- Knowledge: {self.internal_state.retrieved_memories}\n"
            f"- Schedule: {self.internal_state.schedule}\n\n" + self_monitor_prompts["generate_summary"]
        )

        new_summary = self.generate_text(prompt)
        return new_summary

    def generate_text(self, prompt):
        generated_summary = self.llm_client.generate_text(prompt)
        print("Generated Summary: " + generated_summary)
        return generated_summary
    

# Example Usage

# internal_state = InternalState(
#     name="AI",
#     personality="Friendly and curious",
#     emotions="Calm and focused",
#     current_goal="Assist with research",
#     knowledge="Extensive knowledge about various topics",
#     schedule="Meeting at 3 PM, complete report by 5 PM"
# )
  
# self_monitor = SelfMonitor(previous_summary="Initial summary", internal_state=internal_state)
# self_monitor.update_summary(internal_state)

# print(self_monitor.previous_summary)