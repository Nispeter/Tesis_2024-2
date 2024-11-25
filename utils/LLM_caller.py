import os
from dotenv import load_dotenv
import ollama
import openai
import requests
from groq import Groq

load_dotenv()

class LLMCaller:

    def __init__(self, service="openai", model_name="gpt-4o"):
        self.service = service.lower()
        self.model_name = model_name
        self.verify_service()
        
    def verify_service(self):
        if self.service == "openai":
            self.api_key = os.getenv("OPENAI_API_KEY")
            if not self.api_key:
                raise ValueError("Missing OpenAI API key in .env file.")
            openai.api_key = self.api_key
        elif self.service == "ollama":
            pass
        elif self.service == "groq":
            self.api_key = os.getenv("GROQ_API_KEY")
            if not self.api_key:
                raise ValueError("Missing Groq API key in .env file.")
            self.groq_client = Groq(api_key=self.api_key)
        else:
            raise ValueError(f"Unsupported service name: {self.service}")

    def change_service(self, service):
        self.service = service.lower()
        self.verify_service()

    def set_model(self, model_name):
        self.model_name = model_name
        self.verify_service()

    def generate_text(self, prompt):
        if self.service == "openai":
            return self._generate_openai(prompt)
        elif self.service == "ollama":
            return self._generate_ollama(prompt)
        elif self.service == "groq":
            return self._generate_groq(prompt)
        else:
            raise ValueError(f"Unsupported service: {self.service}")

    def _generate_openai(self, prompt):
        try:
            response = openai.Completion.create(
                engine=self.model_name,
                prompt=prompt,
                max_tokens=150,
                temperature=0.7
            )
            return response.choices[0].text.strip()
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return "Error: Unable to generate text with OpenAI."

    def _generate_ollama(self, prompt):
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            return response['message']['content']
        except Exception as e:
            print(f"Ollama API error: {e}")
            return "Error: Unable to generate text with Ollama."

    def _generate_groq(self, prompt):
        try:
            response = self.groq_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model_name,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Groq API error: {e}")
            return "Error: Unable to generate text with Groq."


# model = LLMCaller(service="groq", model_name="llama-3.1-8b-instant")
# result = model.generate_text("What is the capital of France?")
# print(result)

#TODO
#NOTE
#HACK
#FIXME
#BUG
