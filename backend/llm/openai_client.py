import os
from .client_base import LLMClient
# Note: In a real env, you'd import openai. 
# For this skeleton, we'll assume the user installs openai package.
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

class OpenAIClient(LLMClient):
    def __init__(self, model: str = "gpt-4o", api_key: str | None = None):
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if OpenAI and self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None
            print("Warning: OpenAI client not initialized (missing key or package).")

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        if not self.client:
            return "Error: OpenAI client not initialized."
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error calling OpenAI: {str(e)}"
