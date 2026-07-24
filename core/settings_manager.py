"""Settings Manager - Handles user preferences and configuration."""
import logging
import json
from typing import Any, Optional, Dict
from pathlib import Path
from datetime import time
from .security_manager import SecurityManager

logger = logging.getLogger(__name__)


class SettingsManager:
    """Manages application settings and user preferences."""

    _instance: Optional['SettingsManager'] = None
    _config_dir = Path.home() / '.hemel_study_ai'
    _settings_file = _config_dir / 'settings.json'

    DEFAULT_SETTINGS = {
        'language': 'en',
        'ai_provider': 'gemini',
        'system_prompt': 'You are a helpful study assistant.',
        'lock_enabled': False,
        'lock_start_time': '09:00',
        'lock_end_time': '17:00',
        'notifications_enabled': True,
        'auto_save_history': True,
        'text_size': 1.0,
    }

    def __init__(self):
        """Initialize SettingsManager singleton."""
        self.settings: Dict[str, Any] = self.DEFAULT_SETTINGS.copy()
        self.security = SecurityManager.get_instance()
        self.observers = []
        self._load_settings()

    @classmethod
    def get_instance(cls) -> 'SettingsManager':
        """Get singleton instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _load_settings(self) -> None:
        """Load settings from storage."""
        try:
            if self._settings_file.exists():
                with open(self._settings_file, 'r') as f:
                    loaded = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    self.settings = {**self.DEFAULT_SETTINGS, **loaded}
                    logger.info("Settings loaded from file")
            else:
                self._save_settings()
        except Exception as e:
            logger.error(f"Error loading settings: {e}")
            self.settings = self.DEFAULT_SETTINGS.copy()

    def _save_settings(self) -> None:
        """Save settings to storage."""
        try:
            self._config_dir.mkdir(parents=True, exist_ok=True)
            with open(self._settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
            logger.info("Settings saved to file")
        except Exception as e:
            logger.error(f"Error saving settings: {e}")

    def set_setting(self, key: str, value: Any) -> None:
        """Set a setting value.

        Args:
            key: Setting key
            value: Setting value
        """
        self.settings[key] = value
        self._save_settings()
        self._notify_observers(key, value)
        logger.info(f"Setting changed: {key} = {value}")

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a setting value.

        Args:
            key: Setting key
            default: Default value if not found

        Returns:
            Setting value or default
        """
        return self.settings.get(key, default)

    def set_api_key(self, provider: str, api_key: str) -> None:
        """Set encrypted API key for provider.

        Args:
            provider: AI provider name
            api_key: API key to store
        """
        encrypted = self.security.encrypt(api_key)
        key_name = f'api_key_{provider}'
        self.settings[key_name] = encrypted
        self._save_settings()
        logger.info(f"API key set for provider: {provider}")

    def get_api_key(self, provider: str) -> Optional[str]:
        """Get decrypted API key for provider.

        Args:
            provider: AI provider name

        Returns:
            Decrypted API key or None
        """
        key_name = f'api_key_{provider}'
        encrypted = self.settings.get(key_name)
        if encrypted:
            try:
                return self.security.decrypt(encrypted)
            except Exception as e:
                logger.error(f"Error decrypting API key: {e}")
                return None
        return None

    def set_system_prompt(self, prompt: str) -> None:
        """Set system prompt.

        Args:
            prompt: System prompt text
        """
        self.settings['system_prompt'] = prompt
        self._save_settings()
        logger.info("System prompt updated")

    def get_system_prompt(self) -> str:
        """Get system prompt.

        Returns:
            System prompt text
        """
        return self.settings.get('system_prompt', 'You are a helpful study assistant.')

    def set_lock_schedule(self, enabled: bool, start_time: str, end_time: str) -> None:
        """Set lock schedule for settings.

        Args:
            enabled: Whether lock is enabled
            start_time: Start time in HH:MM format
            end_time: End time in HH:MM format
        """
        self.settings['lock_enabled'] = enabled
        self.settings['lock_start_time'] = start_time
        self.settings['lock_end_time'] = end_time
        self._save_settings()
        logger.info(f"Lock schedule set: {start_time} - {end_time}, enabled: {enabled}")

    def is_settings_locked(self) -> bool:
        """Check if settings are currently locked.

        Returns:
            True if settings are locked
        """
        if not self.settings.get('lock_enabled', False):
            return False

        try:
            from datetime import datetime
            now = datetime.now().time()
            start = datetime.strptime(self.settings['lock_start_time'], '%H:%M').time()
            end = datetime.strptime(self.settings['lock_end_time'], '%H:%M').time()

            if start <= end:
                return start <= now <= end
            else:
                return now >= start or now <= end
        except Exception as e:
            logger.error(f"Error checking lock schedule: {e}")
            return False

    def get_lock_info(self) -> Dict[str, Any]:
        """Get lock schedule information.

        Returns:
            Dictionary with lock info
        """
        return {
            'enabled': self.settings.get('lock_enabled', False),
            'start_time': self.settings.get('lock_start_time', '09:00'),
            'end_time': self.settings.get('lock_end_time', '17:00'),
            'is_locked': self.is_settings_locked(),
        }

    def subscribe(self, callback) -> None:
        """Subscribe to settings changes.

        Args:
            callback: Function to call on change
        """
        self.observers.append(callback)

    def _notify_observers(self, key: str, value: Any) -> None:
        """Notify observers of setting change.

        Args:
            key: Setting key
            value: New value
        """
        for callback in self.observers:
            try:
                callback(key, value)
            except Exception as e:
                logger.error(f"Observer callback error: {e}")

    def reset_to_defaults(self) -> None:
        """Reset all settings to defaults."""
        self.settings = self.DEFAULT_SETTINGS.copy()
        self._save_settings()
        logger.info("Settings reset to defaults")
