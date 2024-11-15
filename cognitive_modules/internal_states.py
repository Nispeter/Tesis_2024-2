
class InternalState:
    def __init__(self, name, personality, emotions, current_goal, knowledge, schedule):
        self.name = name
        self.personality = personality
        self.emotions = emotions
        self.current_goal = current_goal
        self.knowledge = knowledge
        self.schedule = schedule
        self.self_monitor_summary = "none"
        print("Internal State initialized")