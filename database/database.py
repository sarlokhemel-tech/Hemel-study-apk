"""Local SQLite Database Handler."""
import sqlite3
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)


class Database:
    """SQLite database for chat history and settings."""

    def __init__(self, db_path: Path):
        """Initialize database.

        Args:
            db_path: Path to database file
        """
        self.db_path = db_path
        self.connection: Optional[sqlite3.Connection] = None

    def initialize(self) -> None:
        """Initialize database tables."""
        try:
            self.connection = sqlite3.connect(str(self.db_path))
            self.connection.row_factory = sqlite3.Row
            self._create_tables()
            logger.info("Database initialized")
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise

    def _create_tables(self) -> None:
        """Create database tables."""
        cursor = self.connection.cursor()

        # Chats table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                theme TEXT DEFAULT 'dark',
                pinned INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER NOT NULL,
                sender TEXT NOT NULL,
                content TEXT NOT NULL,
                message_type TEXT DEFAULT 'text',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (chat_id) REFERENCES chats(id) ON DELETE CASCADE
            )
        ''')

        # Settings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY,
                key TEXT UNIQUE NOT NULL,
                value TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        self.connection.commit()
        logger.info("Database tables created")

    def create_chat(self, title: str = "", theme: str = "dark") -> int:
        """Create new chat.

        Args:
            title: Chat title
            theme: Theme name

        Returns:
            Chat ID
        """
        cursor = self.connection.cursor()
        cursor.execute(
            'INSERT INTO chats (title, theme) VALUES (?, ?)',
            (title, theme)
        )
        self.connection.commit()
        return cursor.lastrowid

    def save_message(self, chat_id: int, sender: str, content: str,
                    message_type: str = "text") -> int:
        """Save message to database.

        Args:
            chat_id: Chat ID
            sender: 'user' or 'ai'
            content: Message content
            message_type: Type of message

        Returns:
            Message ID
        """
        cursor = self.connection.cursor()
        cursor.execute(
            'INSERT INTO messages (chat_id, sender, content, message_type) VALUES (?, ?, ?, ?)',
            (chat_id, sender, content, message_type)
        )
        # Update chat timestamp
        cursor.execute(
            'UPDATE chats SET updated_at = CURRENT_TIMESTAMP WHERE id = ?',
            (chat_id,)
        )
        self.connection.commit()
        return cursor.lastrowid

    def get_chat_messages(self, chat_id: int) -> List[Dict[str, Any]]:
        """Get all messages from a chat.

        Args:
            chat_id: Chat ID

        Returns:
            List of messages
        """
        cursor = self.connection.cursor()
        cursor.execute(
            'SELECT * FROM messages WHERE chat_id = ? ORDER BY created_at ASC',
            (chat_id,)
        )
        messages = [dict(row) for row in cursor.fetchall()]
        return messages

    def get_all_chats(self) -> List[Dict[str, Any]]:
        """Get all chats.

        Returns:
            List of chats
        """
        cursor = self.connection.cursor()
        cursor.execute(
            'SELECT * FROM chats ORDER BY pinned DESC, updated_at DESC'
        )
        chats = [dict(row) for row in cursor.fetchall()]
        return chats

    def get_chat_by_id(self, chat_id: int) -> Optional[Dict[str, Any]]:
        """Get specific chat.

        Args:
            chat_id: Chat ID

        Returns:
            Chat data or None
        """
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM chats WHERE id = ?', (chat_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def update_chat_title(self, chat_id: int, title: str) -> None:
        """Update chat title.

        Args:
            chat_id: Chat ID
            title: New title
        """
        cursor = self.connection.cursor()
        cursor.execute(
            'UPDATE chats SET title = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
            (title, chat_id)
        )
        self.connection.commit()

    def delete_chat(self, chat_id: int) -> None:
        """Delete chat.

        Args:
            chat_id: Chat ID
        """
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM messages WHERE chat_id = ?', (chat_id,))
        cursor.execute('DELETE FROM chats WHERE id = ?', (chat_id,))
        self.connection.commit()

    def pin_chat(self, chat_id: int, pinned: bool) -> None:
        """Pin or unpin chat.

        Args:
            chat_id: Chat ID
            pinned: Pin status
        """
        cursor = self.connection.cursor()
        cursor.execute(
            'UPDATE chats SET pinned = ? WHERE id = ?',
            (1 if pinned else 0, chat_id)
        )
        self.connection.commit()

    def search_chats(self, query: str) -> List[Dict[str, Any]]:
        """Search chats by title.

        Args:
            query: Search query

        Returns:
            List of matching chats
        """
        cursor = self.connection.cursor()
        cursor.execute(
            'SELECT * FROM chats WHERE title LIKE ? ORDER BY updated_at DESC',
            (f'%{query}%',)
        )
        chats = [dict(row) for row in cursor.fetchall()]
        return chats

    def clear_all(self) -> None:
        """Clear all data."""
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM messages')
        cursor.execute('DELETE FROM chats')
        cursor.execute('DELETE FROM settings')
        self.connection.commit()

    def close(self) -> None:
        """Close database connection."""
        if self.connection:
            self.connection.close()
