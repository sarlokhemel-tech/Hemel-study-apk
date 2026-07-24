"""Security Manager - Handles encryption and secure storage."""
import logging
import os
from typing import Optional
from cryptography.fernet import Fernet
from pathlib import Path

logger = logging.getLogger(__name__)


class SecurityManager:
    """Manages encryption and secure data handling."""

    _instance: Optional['SecurityManager'] = None
    _config_dir = Path.home() / '.hemel_study_ai'
    _key_file = _config_dir / 'security.key'

    def __init__(self):
        """Initialize SecurityManager singleton."""
        self.cipher = self._initialize_cipher()

    @classmethod
    def get_instance(cls) -> 'SecurityManager':
        """Get singleton instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _initialize_cipher(self) -> Fernet:
        """Initialize or load encryption cipher.

        Returns:
            Fernet cipher instance
        """
        try:
            self._config_dir.mkdir(parents=True, exist_ok=True)

            if self._key_file.exists():
                with open(self._key_file, 'rb') as f:
                    key = f.read()
                logger.info("Encryption key loaded")
            else:
                key = Fernet.generate_key()
                with open(self._key_file, 'wb') as f:
                    f.write(key)
                logger.info("Encryption key generated")

            return Fernet(key)
        except Exception as e:
            logger.error(f"Error initializing cipher: {e}")
            # Fallback: create new key
            key = Fernet.generate_key()
            return Fernet(key)

    def encrypt(self, data: str) -> str:
        """Encrypt string data.

        Args:
            data: String to encrypt

        Returns:
            Encrypted string (base64 encoded)
        """
        try:
            encrypted = self.cipher.encrypt(data.encode())
            return encrypted.decode()
        except Exception as e:
            logger.error(f"Encryption error: {e}")
            return data

    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt string data.

        Args:
            encrypted_data: Encrypted string (base64 encoded)

        Returns:
            Decrypted string
        """
        try:
            decrypted = self.cipher.decrypt(encrypted_data.encode())
            return decrypted.decode()
        except Exception as e:
            logger.error(f"Decryption error: {e}")
            return encrypted_data

    def mask_api_key(self, api_key: str, show_chars: int = 4) -> str:
        """Mask API key for display.

        Args:
            api_key: Full API key
            show_chars: Number of characters to show

        Returns:
            Masked API key
        """
        if len(api_key) <= show_chars:
            return '*' * len(api_key)
        return api_key[:show_chars] + '*' * (len(api_key) - show_chars)

    def validate_api_key(self, api_key: str, provider: str) -> bool:
        """Validate API key format.

        Args:
            api_key: API key to validate
            provider: Provider name

        Returns:
            True if valid
        """
        if not api_key or len(api_key) < 10:
            return False

        if provider.lower() == 'gemini':
            return len(api_key) > 20
        elif provider.lower() == 'openai':
            return api_key.startswith('sk-')

        return len(api_key) > 10

    def secure_clear(self, data: str) -> None:
        """Securely clear sensitive data from memory.

        Args:
            data: Data to clear
        """
        # Note: Python doesn't provide direct memory clearing
        # This is a placeholder for security best practices
        del data
