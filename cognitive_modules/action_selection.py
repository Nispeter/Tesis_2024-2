from utils.LLM_caller import LLMCaller


valid_actions = {
    "move":"",
    "talk":"",
    "listen":"",
    "ignore":"",
    "observe":"",
}

class ActionSelection:
    def __init__(self, internal_state, speaking_policy_manager,conversation_context):
        self.internal_state = internal_state
        self.speaking_policy_manager = speaking_policy_manager
        self.conversation_context = conversation_context
        self.llm_ollama_client = LLMCaller("ollama", "llama3.2:3b")
        self.llm_openai_client = LLMCaller()
        
    def select_action(self, world_info):
        context_summary = self.conversation_context.summarize_context()
        prompt = (
            f"The following is the current conversation context:\n"
            f"{context_summary}\n\n"
            f"The world information is:\n"
            f"{world_info}\n\n"
            f"Based on the context and world information, select one of these actions: "
            f"{', '.join(valid_actions.keys())}.\n"
            f"Respond with only the action name."
        )
        try:
            action = self.llm_ollama_client.generate_text(prompt).strip()
        except Exception as e:
            print(f"Error in LLM processing: {e}")
            action = "ignore"  

        if action in valid_actions:
            print(f"Selected action: {action}")
            self.do_action(action, world_info)
        else:
            print(f"Invalid action returned by LLM: {action}. Defaulting to 'ignore'.")
            self.do_action("ignore", world_info)
    
    def do_action(self, action, world_info):
        if action in valid_actions:
            if action == "move":
                print("moving")
            elif action == "talk":
                print("talking")
            elif action == "listen":
                print("listening")
            elif action == "ignore":
                print("ignoring")
            elif action == "observe":
                print("observing")
        else:
            print("Invalid action")

    def talk():
        pass