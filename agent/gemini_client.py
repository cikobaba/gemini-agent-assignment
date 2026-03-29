import os
from google import genai


class GeminiClient:
    def __init__(self, model_name: str = "gemini-2.5-flash") -> None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise EnvironmentError("GEMINI_API_KEY environment variable is missing.")

        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name

    def generate(self, prompt: str):
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
        )
        return response