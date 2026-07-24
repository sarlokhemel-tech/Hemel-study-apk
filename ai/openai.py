"""OpenAI API Provider."""
import logging
import aiohttp
import asyncio
from typing import Optional, AsyncIterator, List, Dict, Any
from .provider import AIProvider

logger = logging.getLogger(__name__)


class OpenAIProvider(AIProvider):
    """OpenAI API provider implementation."""

    API_BASE = "https://api.openai.com/v1"
    DEFAULT_MODEL = "gpt-3.5-turbo"

    def __init__(self, api_key: str):
        """Initialize OpenAI provider.

        Args:
            api_key: OpenAI API key
        """
        super().__init__(api_key)
        self.model = self.DEFAULT_MODEL

    async def send_message(self, message: str, system_prompt: str = "",
                          conversation_history: Optional[List[Dict[str, str]]] = None) -> str:
        """Send message to OpenAI API.

        Args:
            message: User message
            system_prompt: System instruction
            conversation_history: Previous messages

        Returns:
            AI response
        """
        try:
            messages = []

            # Add system prompt
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })

            # Add conversation history
            if conversation_history:
                messages.extend(conversation_history)

            # Add current message
            messages.append({
                "role": "user",
                "content": message
            })

            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 2048,
            }

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            url = f"{self.API_BASE}/chat/completions"

            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        if 'choices' in data and len(data['choices']) > 0:
                            return data['choices'][0]['message']['content']
                    else:
                        logger.error(f"OpenAI API error: {response.status}")
                        return f"Error: {response.status}"
        except Exception as e:
            logger.error(f"Error sending message to OpenAI: {e}")
            return f"Error: {str(e)}"

    async def stream_message(self, message: str, system_prompt: str = "",
                            conversation_history: Optional[List[Dict[str, str]]] = None) -> AsyncIterator[str]:
        """Stream message response from OpenAI.

        Args:
            message: User message
            system_prompt: System instruction
            conversation_history: Previous messages

        Yields:
            Response chunks
        """
        try:
            messages = []

            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })

            if conversation_history:
                messages.extend(conversation_history)

            messages.append({
                "role": "user",
                "content": message
            })

            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 2048,
                "stream": True,
            }

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            url = f"{self.API_BASE}/chat/completions"

            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, headers=headers) as response:
                    if response.status == 200:
                        async for chunk in response.content.iter_chunked(1024):
                            yield chunk.decode('utf-8', errors='ignore')
                    else:
                        yield f"Error: {response.status}"
        except Exception as e:
            logger.error(f"Error streaming from OpenAI: {e}")
            yield f"Error: {str(e)}"

    def validate_api_key(self) -> bool:
        """Validate OpenAI API key.

        Returns:
            True if key format is valid
        """
        return bool(self.api_key and self.api_key.startswith('sk-'))

    def get_available_models(self) -> List[str]:
        """Get available OpenAI models.

        Returns:
            List of model names
        """
        return ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview"]
