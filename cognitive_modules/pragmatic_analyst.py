from utils.LLM_caller import LLMCaller


class PragmaticAnalyst:
    def __init__(self, conversation_context):
        self.llm_client = LLMCaller(service="ollama", model_name="llama3.2:3b")
        self.conversation_context = conversation_context

    def analyze_pragmatic_attributes(self, dialogue):
        """
        Analyzes pragmatic attributes of the dialogue, such as intention, tone, and formality.
        :param dialogue: The dialogue input as a string.
        :return: A dictionary of pragmatic attributes.
        """
        prompt = (
            f"Analyze the following dialogue for pragmatic attributes:\n\n{dialogue}\n\n"
            "Provide the following details:\n"
            "- Intention (e.g., question, statement, command, greeting)\n"
            "- Tone (e.g., neutral, friendly, aggressive, sarcastic)\n"
            "- Formality level (e.g., formal, informal)\n"
            "- Subject matter (e.g., personal, technical, casual)\n"
            "Respond in the format:\n"
            "Intention: <value>\n"
            "Tone: <value>\n"
            "Formality: <value>\n"
            "Subject matter: <value>\n"
            "Provide no additional text."
        )
        try:
            response = self.llm_client.generate_text(prompt).strip()
            attributes = self._parse_response(response)
            return attributes
        except Exception as e:
            print(f"Error analyzing pragmatic attributes: {e}")
            return {}

    def _parse_response(self, response):
        """
        Parses the LLM response for key-value pairs.
        :param response: The raw response as a string.
        :return: A dictionary of pragmatic attributes.
        """
        attributes = {}
        for line in response.split("\n"):
            if ": " in line:
                key, value = line.split(": ", 1)
                attributes[key.lower()] = value.strip()
        return attributes

    
    def update_context(self, dialogue):
        """
        Updates the conversation context with the latest dialogue and its pragmatic attributes.
        :param dialogue: The new dialogue to process and add.
        """
        attributes = self.analyze_pragmatic_attributes(dialogue)
        self.conversation_context.update(dialogue, attributes)

    def get_context(self):
        """
        Retrieves the current conversation context.
        :return: A ConversationContext object.
        """
        return self.conversation_context

    def context_summary(self):
        """
        Provides a summary of the conversation context.
        :return: A string summary of the current context.
        """
        return (
            "The following indicates the pragmatic attributes of the conversation:\n"
            + self.conversation_context.summarize_context()
        )


#TODO: Store previous 3 dialogues

class ConversationContext:
    
    MAX_DIALOGUES = 3
    
    def __init__(self):
        self.dialogues = []
        self.state = {
            "intention": None,
            "tone": None,
            "formality": None,
            "subject matter": None,
        }
        print("Conversation context initialized.")

    def update(self, dialogue, attributes):
        """
        Updates the conversation context with a new dialogue and its pragmatic attributes.
        :param dialogue: The dialogue string.
        :param attributes: A dictionary of pragmatic attributes.
        """
        self.dialogues.append(dialogue)
        if len(self.dialogues) > self.MAX_DIALOGUES:
            self.dialogues.pop(0)
            
        self.state.update({
            "intention": attributes.get("intention", self.state["intention"]),
            "tone": attributes.get("tone", self.state["tone"]),
            "formality": attributes.get("formality", self.state["formality"]),
            "subject matter": attributes.get("subject matter", self.state["subject matter"]),
        })

    def summarize_context(self):
        """
        Summarizes the current context state as a string.
        :return: A string summarizing intention, tone, formality, and subject matter.
        """
        summary = "\n".join(
            f"{key.capitalize()}: {value}" for key, value in self.state.items() if value
        )
        return f"Conversation Summary:\n{summary}" if summary else "No context available."
