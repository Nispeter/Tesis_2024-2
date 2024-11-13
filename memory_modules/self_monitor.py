class SelfMonitor:
    def __init__(self, name, previous_summary, internal_state):
        self.name = name
        self.previous_summary = previous_summary
        self.internal_state = internal_state

    def generate_new_summary(self):
        prompt = (
            f"Previous Summary:\n{self.previous_summary}\n\n"
            "Current State:\n"
            f"- Name: {self.internal_state.name}\n"
            f"- Personality: {self.internal_state.personality}\n"
            f"- Emotions: {self.internal_state.emotions}\n"
            f"- Current Goal: {self.internal_state.current_goal}\n"
            f"- Knowledge: {self.internal_state.knowledge}\n"
            f"- Schedule: {self.internal_state.schedule}\n\n"
            "Generate a new summary based on this information, maintaining continuity with previous summary."
        )

        new_summary = self.generate_text(prompt)
        return new_summary