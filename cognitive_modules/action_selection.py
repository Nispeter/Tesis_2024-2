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
        self.llm_openai_client = LLMCaller("openai", "gpt-4o-mini")
        
    def select_action(self, world_info):
        if world_info is None:
            world_info = "none relevant"
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
            action = self.llm_openai_client.generate_text(prompt)
        except Exception as e:
            print(f"Error in LLM processing: {e}")
            action = "ignore"  

        if action in valid_actions:
            print(f"Selected action: {action}")
            self.do_action(action, world_info)
        else:
            print(f"Invalid action returned by LLM: {action}. Defaulting to 'ignore'.")
            self.do_action("ignore", world_info)
    
    #FIXME: Model never taking talk action
    def do_action(self, action, world_info):
        if action in valid_actions:
            if action == "move":
                print("moving")
            elif action == "talk":
                context_summary = self.conversation_context.summarize_context()
                internal_state_summary = self.internal_state.summarize_states() 

                prompt = (
                    f"The character has the following internal state:\n"
                    f"{internal_state_summary}\n\n"
                    f"The current conversation context is:\n"
                    f"{context_summary}\n\n"
                    f"The world information is:\n"
                    f"{world_info}\n\n"
                    f"Based on this information, generate an appropriate response for the character to say."
                )

                try:
                    # Use one of the LLM clients to generate the response
                    print("generating response from: "+prompt)
                    response = self.llm_openai_client.generate_text(prompt).strip()
                    print(f"Generated response: {response}")
                    # Optionally, you could store this response in the conversation context for continuity
                except Exception as e:
                    print(f"Error generating talk response: {e}")
                    response = "..."  # Default response in case of failure
                    
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