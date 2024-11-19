from utils.LLM_caller import LLMCaller


class PragmaticAnalyst():
    def __init__(self):
        self.llm_client = LLMCaller("ollama", model_name="llama3.2:3b")
    
    def classify_intention(self, question):
        prompt = "What is the intention of the following question?\n" + question
        response = self.llm_client.generate_text(prompt)
        return response.strip().lower()
    
#What to do with this, I need it to be in speaking policies manager
conversation_context = {
    "context": "",
    "dialogues": [],
    "intention":"",
}