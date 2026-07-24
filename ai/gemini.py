"""Google Gemini AI Provider."""
import logging
import aiohttp
import asyncio
from typing import Optional, AsyncIterator, List, Dict, Any
from .provider import AIProvider

logger = logging.getLogger(__name__)


class GeminiProvider(AIProvider):
    """Google Gemini AI provider implementation."""

    API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"
    DEFAULT_MODEL = "gemini-pro"

    def __init__(self, api_key: str):
        """Initialize Gemini provider.

        Args:
            api_key: Google Gemini API key
        """
        super().__init__(api_key)
        self.model = self.DEFAULT_MODEL

    async def send_message(self, message: str, system_prompt: str = "",
                          conversation_history: Optional[List[Dict[str, str]]] = None) -> str:
        """Send message to Gemini API.

        Args:
            message: User message
            system_prompt: System instruction
            conversation_history: Previous messages

        Returns:
            AI response
        """
        try:
            contents = []

            # Add conversation history
            if conversation_history:
                for msg in conversation_history:
                    role = "user" if msg["role"] == "user" else "model"
                    contents.append({
                        "role": role,
                        "parts": [{"text": msg["content"]}]
                    })

            # Add current message
            contents.append({
                "role": "user",
                "parts": [{"text": message}]
            })

            payload = {
                "contents": contents,
                "generationConfig": {
                    "temperature": 0.7,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 2048,
                },
            }

            if system_prompt:
                payload["systemInstruction"] = {"parts": [{"text": system_prompt}]}

            url = f"{self.API_BASE}/{self.model}:generateContent?key={self.api_key}"

            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        if 'candidates' in data and len(data['candidates']) > 0:
                            return data['candidates'][0]['content']['parts'][0]['text']
                    else:
                        logger.error(f"Gemini API error: {response.status}")
                        return f"Error: {response.status}"
        except Exception as e:
            logger.error(f"Error sending message to Gemini: {e}")
            return f"Error: {str(e)}"

    async def stream_message(self, message: str, system_prompt: str = "",
                            conversation_history: Optional[List[Dict[str, str]]] = None) -> AsyncIterator[str]:
        """Stream message response from Gemini.

        Args:
            message: User message
            system_prompt: System instruction
            conversation_history: Previous messages

        Yields:
            Response chunks
        """
        try:
            contents = []

            if conversation_history:
                for msg in conversation_history:
                    role = "user" if msg["role"] == "user" else "model"
                    contents.append({
                        "role": role,
                        "parts": [{"text": msg["content"]}]
                    })

            contents.append({
                "role": "user",
                "parts": [{"text": message}]
            })

            payload = {
                "contents": contents,
                "generationConfig": {
                    "temperature": 0.7,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 2048,
                },
            }

            if system_prompt:
                payload["systemInstruction"] = {"parts": [{"text": system_prompt}]}

            url = f"{self.API_BASE}/{self.model}:streamGenerateContent?key={self.api_key}"

            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    if response.status == 200:
                        async for chunk in response.content.iter_chunked(1024):
                            yield chunk.decode('utf-8', errors='ignore')
                    else:
                        yield f"Error: {response.status}"
        except Exception as e:
            logger.error(f"Error streaming from Gemini: {e}")
            yield f"Error: {str(e)}"

    def validate_api_key(self) -> bool:
        """Validate Gemini API key.

        Returns:
            True if key format is valid
        """
        return bool(self.api_key and len(self.api_key) > 20)

    def get_available_models(self) -> List[str]:
        """Get available Gemini models.

        Returns:
            List of model names
        """
        return ["gemini-pro", "gemini-pro-vision"]
