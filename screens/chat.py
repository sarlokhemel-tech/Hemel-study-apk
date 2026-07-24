"""Chat Screen - Main conversation interface."""
from kivy.uix.screen import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle
from kivy.clock import Clock
from kivy.core.window import Window
from typing import Optional, Callable, Dict, Any, List
import asyncio
from core.app_manager import AppManager
from core.theme_manager import ThemeManager
from core.settings_manager import SettingsManager
from core.storage_manager import StorageManager
from widgets.input_bar import InputBar
from widgets.message_bubble import MessageBubble
from widgets.sidebar import Sidebar
from ai.gemini import GeminiProvider
from ai.openai import OpenAIProvider


class ChatScreen(Screen):
    """Chat screen with message display and input."""

    def __init__(self, **kwargs):
        """Initialize chat screen.

        Args:
            **kwargs: Additional arguments
        """
        super().__init__(**kwargs)
        self.app_manager = AppManager.get_instance()
        self.theme_manager = ThemeManager.get_instance()
        self.settings_manager = SettingsManager.get_instance()
        self.storage_manager = StorageManager.get_instance()
        self.name = 'chat'
        self.current_chat_id = -1
        self.ai_provider = None
        self.is_loading = False
        self.sidebar_open = False

        # Main layout
        self.main_layout = BoxLayout(orientation='horizontal')

        # Chat content
        chat_layout = BoxLayout(orientation='vertical', size_hint_x=1)

        # Apply theme background
        with chat_layout.canvas.before:
            Color(*self.theme_manager.get_color('background'))
            RoundedRectangle(
                size=chat_layout.size,
                pos=chat_layout.pos,
            )

        # Header with hamburger menu
        header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=56,
            padding=(10, 5),
            spacing=10,
        )
        
        with header.canvas.before:
            Color(*self.theme_manager.get_color('surface'))
            RoundedRectangle(
                size=header.size,
                pos=header.pos,
            )

        menu_btn = Button(
            text='☰',
            size_hint_x=None,
            width=50,
            font_size='24sp',
            background_color=self.theme_manager.get_color('button_bg'),
        )
        menu_btn.bind(on_press=self._toggle_sidebar)
        header.add_widget(menu_btn)

        title_label = Label(
            text='Chat',
            size_hint_x=1,
            color=self.theme_manager.get_color('text_primary'),
        )
        header.add_widget(title_label)

        new_chat_btn = Button(
            text='+',
            size_hint_x=None,
            width=50,
            font_size='24sp',
            background_color=self.theme_manager.get_color('button_bg'),
        )
        new_chat_btn.bind(on_press=self._on_new_chat)
        header.add_widget(new_chat_btn)

        chat_layout.add_widget(header)

        # Messages scroll view
        messages_scroll = ScrollView(size_hint_y=0.85)
        self.messages_layout = GridLayout(
            cols=1,
            spacing=10,
            size_hint_y=None,
            padding=(10, 10),
        )
        self.messages_layout.bind(minimum_height=self.messages_layout.setter('height'))
        messages_scroll.add_widget(self.messages_layout)
        chat_layout.add_widget(messages_scroll)

        # Typing indicator
        self.typing_label = Label(
            text='AI is typing...',
            size_hint_y=None,
            height=30,
            opacity=0,
            color=self.theme_manager.get_color('text_secondary'),
        )
        self.messages_layout.add_widget(self.typing_label)

        # Input bar
        self.input_bar = InputBar(send_callback=self._on_message_sent)
        chat_layout.add_widget(self.input_bar)

        self.main_layout.add_widget(chat_layout)

        # Sidebar (hidden by default)
        self.sidebar = Sidebar(menu_callback=self._on_sidebar_action)
        self.sidebar.size_hint_x = 0

        self.main_layout.add_widget(self.sidebar)

        self.add_widget(self.main_layout)

        # Subscribe to theme changes
        self.theme_manager.subscribe(self._on_theme_change)

    def start_new_chat(self) -> None:
        """Start a new chat session."""
        self.current_chat_id = self.storage_manager.create_chat("New Chat")
        self.messages_layout.clear_widgets()
        self.messages_layout.add_widget(self.typing_label)
        self._initialize_ai_provider()

    def _initialize_ai_provider(self) -> None:
        """Initialize AI provider based on settings."""
        provider_name = self.settings_manager.get_setting('ai_provider', 'gemini')
        api_key = self.settings_manager.get_api_key(provider_name)

        if not api_key:
            self._show_api_error(f"No API key configured for {provider_name}")
            return

        if provider_name == 'gemini':
            self.ai_provider = GeminiProvider(api_key)
        elif provider_name == 'openai':
            self.ai_provider = OpenAIProvider(api_key)
        else:
            self._show_api_error("Unknown AI provider")

    def _on_message_sent(self, message: str) -> None:
        """Handle message sent.

        Args:
            message: Message text
        """
        if not message.strip():
            return

        if self.current_chat_id == -1:
            self.start_new_chat()

        # Add user message to display
        user_bubble = MessageBubble(
            content=message,
            sender='user',
            size_hint_y=None,
            height=80,
        )
        self.messages_layout.add_widget(user_bubble)

        # Save to database
        self.storage_manager.save_message(self.current_chat_id, 'user', message)

        # Show typing indicator
        self.typing_label.opacity = 1
        self.input_bar.set_enabled(False)

        # Request AI response
        Clock.schedule_once(lambda x: self._request_ai_response(message), 0.5)

    def _request_ai_response(self, user_message: str) -> None:
        """Request response from AI.

        Args:
            user_message: User's message
        """
        if not self.ai_provider:
            self._show_api_error("AI provider not initialized")
            return

        try:
            # Get system prompt
            system_prompt = self.settings_manager.get_system_prompt()

            # Get conversation history
            messages = self.storage_manager.get_chat_messages(self.current_chat_id)
            history = [
                {"role": msg['sender'], "content": msg['content']}
                for msg in messages[:-1]  # Exclude current user message
            ]

            # Use asyncio to handle async AI call
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            response = loop.run_until_complete(
                self.ai_provider.send_message(
                    user_message,
                    system_prompt=system_prompt,
                    conversation_history=history
                )
            )
            loop.close()

            # Hide typing indicator
            self.typing_label.opacity = 0
            self.input_bar.set_enabled(True)

            # Add AI response to display
            ai_bubble = MessageBubble(
                content=response,
                sender='ai',
                actions_callback=self._on_message_action,
                size_hint_y=None,
                height=120,
            )
            self.messages_layout.add_widget(ai_bubble)

            # Save to database
            self.storage_manager.save_message(self.current_chat_id, 'ai', response)

            # Auto-scroll to bottom
            self.messages_layout.parent.scroll_y = 0

        except Exception as e:
            self._show_api_error(f"Error: {str(e)}")
            self.typing_label.opacity = 0
            self.input_bar.set_enabled(True)

    def _on_message_action(self, action: str, content: str) -> None:
        """Handle message action.

        Args:
            action: Action type
            content: Message content
        """
        if action == 'copy':
            from kivy.core.clipboard import Clipboard
            Clipboard.copy(content)
        elif action == 'export':
            self._export_message(content)
        elif action == 'listen':
            self._read_message(content)
        elif action == 'regenerate':
            self._regenerate_response()

    def _export_message(self, content: str) -> None:
        """Export message.

        Args:
            content: Message content
        """
        # Placeholder for export functionality
        pass

    def _read_message(self, content: str) -> None:
        """Read message using TTS.

        Args:
            content: Message content
        """
        # Placeholder for TTS functionality
        pass

    def _regenerate_response(self) -> None:
        """Regenerate last AI response."""
        # Get last user message
        messages = self.storage_manager.get_chat_messages(self.current_chat_id)
        if messages and messages[-2]['sender'] == 'user':
            last_user_msg = messages[-2]['content']
            # Remove last AI response
            self.messages_layout.remove_widget(
                self.messages_layout.children[0]
            )
            # Request new response
            self._request_ai_response(last_user_msg)

    def _toggle_sidebar(self, instance) -> None:
        """Toggle sidebar visibility."""
        if self.sidebar_open:
            self.sidebar.size_hint_x = 0
            self.sidebar_open = False
        else:
            self.sidebar.size_hint_x = 0.75
            self.sidebar_open = True

    def _on_sidebar_action(self, action: str) -> None:
        """Handle sidebar action.

        Args:
            action: Action identifier
        """
        self.sidebar_open = False
        self.sidebar.size_hint_x = 0

        if action == 'new_chat':
            self._on_new_chat(None)
        elif action == 'history':
            self.app_manager.switch_screen('history')
        elif action == 'special_settings':
            self.app_manager.switch_screen('special_settings')
        elif action == 'theme':
            self.app_manager.switch_screen('theme')
        elif action == 'settings':
            self.app_manager.switch_screen('settings')

    def _on_new_chat(self, instance) -> None:
        """Start new chat."""
        self.start_new_chat()

    def _show_api_error(self, error: str) -> None:
        """Show API error popup.

        Args:
            error: Error message
        """
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=error))
        
        close_btn = Button(text='Close', size_hint_y=0.2)
        content.add_widget(close_btn)
        
        popup = Popup(title='Error', content=content, size_hint=(0.8, 0.5))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    def _on_theme_change(self, theme) -> None:
        """Handle theme change.

        Args:
            theme: New theme
        """
        pass
