"""Base AI Provider Interface."""
from abc import ABC, abstractmethod
from typing import Optional, AsyncIterator, List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class AIProvider(ABC):
    """Abstract base class for AI providers."""

    def __init__(self, api_key: str):
        """Initialize provider.

        Args:
            api_key: API key for the provider
        """
        self.api_key = api_key
        self.model = None

    @abstractmethod
    async def send_message(self, message: str, system_prompt: str = "",
                          conversation_history: Optional[List[Dict[str, str]]] = None) -> str:
        """Send message and get response.

        Args:
            message: User message
            system_prompt: System instruction
            conversation_history: Previous messages

        Returns:
            AI response
        """
        pass

    @abstractmethod
    async def stream_message(self, message: str, system_prompt: str = "",
                            conversation_history: Optional[List[Dict[str, str]]] = None) -> AsyncIterator[str]:
        """Stream message response.

        Args:
            message: User message
            system_prompt: System instruction
            conversation_history: Previous messages

        Yields:
            Response chunks
        """
        pass

    @abstractmethod
    def validate_api_key(self) -> bool:
        """Validate API key.

        Returns:
            True if valid
        """
        pass

    @abstractmethod
    def get_available_models(self) -> List[str]:
        """Get available models.

        Returns:
            List of model names
        """
        pass
