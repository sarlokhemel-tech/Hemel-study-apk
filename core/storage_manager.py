"""Storage Manager - Handles local data persistence and database operations."""
import logging
from typing import Optional, List, Dict, Any
from pathlib import Path
from .settings_manager import SettingsManager
from database.database import Database

logger = logging.getLogger(__name__)


class StorageManager:
    """Manages local storage and database operations."""

    _instance: Optional['StorageManager'] = None
    _config_dir = Path.home() / '.hemel_study_ai'

    def __init__(self):
        """Initialize StorageManager singleton."""
        self.db = Database(self._config_dir / 'hemel_study.db')
        self.settings = SettingsManager.get_instance()

    @classmethod
    def get_instance(cls) -> 'StorageManager':
        """Get singleton instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def initialize(self) -> None:
        """Initialize storage system."""
        try:
            self._config_dir.mkdir(parents=True, exist_ok=True)
            self.db.initialize()
            logger.info("Storage system initialized")
        except Exception as e:
            logger.error(f"Error initializing storage: {e}")

    def create_chat(self, title: str = "", theme: str = "dark") -> int:
        """Create new chat.

        Args:
            title: Chat title
            theme: Theme name

        Returns:
            Chat ID
        """
        try:
            chat_id = self.db.create_chat(title, theme)
            logger.info(f"Chat created with ID: {chat_id}")
            return chat_id
        except Exception as e:
            logger.error(f"Error creating chat: {e}")
            return -1

    def save_message(self, chat_id: int, sender: str, content: str, 
                    message_type: str = "text") -> int:
        """Save message to chat.

        Args:
            chat_id: Chat ID
            sender: Message sender ('user' or 'ai')
            content: Message content
            message_type: Type of message

        Returns:
            Message ID
        """
        try:
            msg_id = self.db.save_message(chat_id, sender, content, message_type)
            logger.debug(f"Message saved with ID: {msg_id}")
            return msg_id
        except Exception as e:
            logger.error(f"Error saving message: {e}")
            return -1

    def get_chat_messages(self, chat_id: int) -> List[Dict[str, Any]]:
        """Get all messages from a chat.

        Args:
            chat_id: Chat ID

        Returns:
            List of messages
        """
        try:
            messages = self.db.get_chat_messages(chat_id)
            return messages
        except Exception as e:
            logger.error(f"Error retrieving messages: {e}")
            return []

    def get_all_chats(self) -> List[Dict[str, Any]]:
        """Get all chat histories.

        Returns:
            List of chats
        """
        try:
            chats = self.db.get_all_chats()
            return chats
        except Exception as e:
            logger.error(f"Error retrieving chats: {e}")
            return []

    def update_chat_title(self, chat_id: int, title: str) -> bool:
        """Update chat title.

        Args:
            chat_id: Chat ID
            title: New title

        Returns:
            True if successful
        """
        try:
            self.db.update_chat_title(chat_id, title)
            logger.info(f"Chat {chat_id} title updated: {title}")
            return True
        except Exception as e:
            logger.error(f"Error updating chat title: {e}")
            return False

    def delete_chat(self, chat_id: int) -> bool:
        """Delete chat and all messages.

        Args:
            chat_id: Chat ID

        Returns:
            True if successful
        """
        try:
            self.db.delete_chat(chat_id)
            logger.info(f"Chat {chat_id} deleted")
            return True
        except Exception as e:
            logger.error(f"Error deleting chat: {e}")
            return False

    def pin_chat(self, chat_id: int, pinned: bool) -> bool:
        """Pin or unpin chat.

        Args:
            chat_id: Chat ID
            pinned: Pin status

        Returns:
            True if successful
        """
        try:
            self.db.pin_chat(chat_id, pinned)
            logger.info(f"Chat {chat_id} pinned: {pinned}")
            return True
        except Exception as e:
            logger.error(f"Error pinning chat: {e}")
            return False

    def get_chat_by_id(self, chat_id: int) -> Optional[Dict[str, Any]]:
        """Get specific chat.

        Args:
            chat_id: Chat ID

        Returns:
            Chat data or None
        """
        try:
            chat = self.db.get_chat_by_id(chat_id)
            return chat
        except Exception as e:
            logger.error(f"Error retrieving chat: {e}")
            return None

    def search_chats(self, query: str) -> List[Dict[str, Any]]:
        """Search chats by title.

        Args:
            query: Search query

        Returns:
            List of matching chats
        """
        try:
            results = self.db.search_chats(query)
            return results
        except Exception as e:
            logger.error(f"Error searching chats: {e}")
            return []

    def clear_all_data(self) -> bool:
        """Clear all stored data.

        Returns:
            True if successful
        """
        try:
            self.db.clear_all()
            logger.info("All data cleared")
            return True
        except Exception as e:
            logger.error(f"Error clearing data: {e}")
            return False

    def shutdown(self) -> None:
        """Shutdown storage system."""
        try:
            self.db.close()
            logger.info("Storage system shutdown")
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
