import os
import requests
import json


class AIClient:
    """
    AI Client supporting Google Gemini API
    """

    def __init__(self):
        self.provider = os.getenv("REDSENTINEL_AI_PROVIDER", "gemini").lower()
        self.api_key = os.getenv("REDSENTINEL_AI_KEY")

        if not self.api_key:
            raise EnvironmentError("REDSENTINEL_AI_KEY not set")

        if self.provider != "gemini":
            raise ValueError("Only Gemini provider is supported currently")

        self.api_url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            "gemini-1.5-flash:generateContent"
        )

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """
        Generate AI response using Gemini
        """

        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {
                            "text": f"""
SYSTEM:
{system_prompt}

USER:
{user_prompt}
"""
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": 800
            }
        }

        response = requests.post(
            f"{self.api_url}?key={self.api_key}",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=60
        )

        response.raise_for_status()
        data = response.json()

        return data["candidates"][0]["content"]["parts"][0]["text"].strip()

