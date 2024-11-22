from utils.LLM_caller import LLMCaller


valid_actions = {
    "move":"",
    "talk":"",
    "listen":"",
    "ignore":"",
    "observe":"",
}

class ActionSelection:
    def __init__(self, internal_state, speaking_policy_manager):
        self.internal_state = internal_state
        self.speaking_policy_manager = speaking_policy_manager
        self.llm_client = LLMCaller()
        
    def select_action(self, world_info):
        pass
    
    def do_action(self, action, world_info):
        if action in valid_actions:
            if action == "move":
                print("moving")
            elif action == "talk":
                print("talking")
            elif action == "listen":
                print("moving")
            elif action == "ignore":
                print("ignoring")
            elif action == "observe":
                print("observing")
        else:
            print("Invalid action")

    def talk():
        pass