"""Custom API Provider for third-party AI services."""
import logging
import aiohttp
import asyncio
from typing import Optional, AsyncIterator, List, Dict, Any
from .provider import AIProvider

logger = logging.getLogger(__name__)


class CustomAPIProvider(AIProvider):
    """Custom API provider for third-party services."""

    def __init__(self, api_key: str, endpoint: str = "", model: str = ""):
        """Initialize Custom API provider.

        Args:
            api_key: API key for custom service
            endpoint: API endpoint URL
            model: Model name
        """
        super().__init__(api_key)
        self.endpoint = endpoint
        self.model = model or "custom"

    async def send_message(self, message: str, system_prompt: str = "",
                          conversation_history: Optional[List[Dict[str, str]]] = None) -> str:
        """Send message to custom API.

        Args:
            message: User message
            system_prompt: System instruction
            conversation_history: Previous messages

        Returns:
            AI response
        """
        if not self.endpoint:
            return "Error: No API endpoint configured"

        try:
            payload = {
                "message": message,
                "system_prompt": system_prompt,
                "history": conversation_history or [],
                "model": self.model,
            }

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(self.endpoint, json=payload, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('response', 'No response')
                    else:
                        logger.error(f"Custom API error: {response.status}")
                        return f"Error: {response.status}"
        except Exception as e:
            logger.error(f"Error sending message to custom API: {e}")
            return f"Error: {str(e)}"

    async def stream_message(self, message: str, system_prompt: str = "",
                            conversation_history: Optional[List[Dict[str, str]]] = None) -> AsyncIterator[str]:
        """Stream message response from custom API.

        Args:
            message: User message
            system_prompt: System instruction
            conversation_history: Previous messages

        Yields:
            Response chunks
        """
        if not self.endpoint:
            yield "Error: No API endpoint configured"
            return

        try:
            payload = {
                "message": message,
                "system_prompt": system_prompt,
                "history": conversation_history or [],
                "model": self.model,
                "stream": True,
            }

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(self.endpoint, json=payload, headers=headers) as response:
                    if response.status == 200:
                        async for chunk in response.content.iter_chunked(1024):
                            yield chunk.decode('utf-8', errors='ignore')
                    else:
                        yield f"Error: {response.status}"
        except Exception as e:
            logger.error(f"Error streaming from custom API: {e}")
            yield f"Error: {str(e)}"

    def validate_api_key(self) -> bool:
        """Validate API key.

        Returns:
            True if key and endpoint are configured
        """
        return bool(self.api_key and self.endpoint)

    def get_available_models(self) -> List[str]:
        """Get available models.

        Returns:
            List of model names
        """
        return [self.model] if self.model else ["custom"]
