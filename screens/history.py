"""History Screen - Chat history browser."""
from kivy.uix.screen import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, RoundedRectangle
from typing import Dict, Any, List
from core.theme_manager import ThemeManager
from core.app_manager import AppManager
from core.storage_manager import StorageManager


class HistoryScreen(Screen):
    """Chat history screen."""

    def __init__(self, **kwargs):
        """Initialize history screen.

        Args:
            **kwargs: Additional arguments
        """
        super().__init__(**kwargs)
        self.theme_manager = ThemeManager.get_instance()
        self.app_manager = AppManager.get_instance()
        self.storage_manager = StorageManager.get_instance()
        self.name = 'history'

        main_layout = BoxLayout(orientation='vertical', spacing=10, padding=(10, 10))

        # Apply theme background
        with main_layout.canvas.before:
            Color(*self.theme_manager.get_color('background'))
            RoundedRectangle(
                size=main_layout.size,
                pos=main_layout.pos,
            )

        # Header
        header = BoxLayout(size_hint_y=None, height=50, spacing=10)
        back_btn = Button(
            text='← Back',
            size_hint_x=0.2,
            background_color=self.theme_manager.get_color('button_bg'),
        )
        back_btn.bind(on_press=self._on_back)
        header.add_widget(back_btn)

        title = Label(
            text='Chat History',
            size_hint_x=0.6,
            color=self.theme_manager.get_color('text_primary'),
        )
        header.add_widget(title)
        main_layout.add_widget(header)

        # Search bar
        search_input = TextInput(
            hint_text='Search chats...',
            size_hint_y=None,
            height=40,
            multiline=False,
        )
        search_input.bind(text=self._on_search)
        main_layout.add_widget(search_input)

        # History list
        history_scroll = ScrollView()
        self.history_layout = GridLayout(
            cols=1,
            spacing=5,
            size_hint_y=None,
            padding=(5, 5),
        )
        self.history_layout.bind(minimum_height=self.history_layout.setter('height'))
        history_scroll.add_widget(self.history_layout)
        main_layout.add_widget(history_scroll)

        self.add_widget(main_layout)

    def on_enter(self) -> None:
        """Called when screen is displayed."""
        self._load_history()

    def _load_history(self) -> None:
        """Load chat history from storage."""
        self.history_layout.clear_widgets()
        chats = self.storage_manager.get_all_chats()

        for chat in chats:
            chat_item = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=60,
                spacing=10,
                padding=(10, 5),
            )

            with chat_item.canvas.before:
                Color(*self.theme_manager.get_color('surface'))
                RoundedRectangle(
                    size=chat_item.size,
                    pos=chat_item.pos,
                    radius=[10, 10, 10, 10]
                )

            # Chat title
            title_label = Label(
                text=chat['title'] or 'Untitled',
                size_hint_x=0.6,
                color=self.theme_manager.get_color('text_primary'),
            )
            chat_item.add_widget(title_label)

            # Open button
            open_btn = Button(
                text='Open',
                size_hint_x=0.15,
                background_color=self.theme_manager.get_color('button_bg'),
            )
            open_btn.bind(on_press=lambda x, c=chat: self._on_open_chat(c))
            chat_item.add_widget(open_btn)

            # Delete button
            delete_btn = Button(
                text='Delete',
                size_hint_x=0.15,
                background_color=(1, 0.3, 0.3, 1),
            )
            delete_btn.bind(on_press=lambda x, c=chat: self._on_delete_chat(c))
            chat_item.add_widget(delete_btn)

            # Pin button
            pin_text = '📌' if chat['pinned'] else '○'
            pin_btn = Button(
                text=pin_text,
                size_hint_x=0.1,
                background_color=self.theme_manager.get_color('button_bg'),
            )
            pin_btn.bind(on_press=lambda x, c=chat: self._on_pin_chat(c))
            chat_item.add_widget(pin_btn)

            self.history_layout.add_widget(chat_item)

    def _on_open_chat(self, chat: Dict[str, Any]) -> None:
        """Open chat.

        Args:
            chat: Chat data
        """
        # TODO: Load chat and switch to chat screen
        pass

    def _on_delete_chat(self, chat: Dict[str, Any]) -> None:
        """Delete chat.

        Args:
            chat: Chat data
        """
        self.storage_manager.delete_chat(chat['id'])
        self._load_history()

    def _on_pin_chat(self, chat: Dict[str, Any]) -> None:
        """Pin/unpin chat.

        Args:
            chat: Chat data
        """
        self.storage_manager.pin_chat(chat['id'], not chat['pinned'])
        self._load_history()

    def _on_search(self, instance, value: str) -> None:
        """Search chats.

        Args:
            instance: TextInput instance
            value: Search query
        """
        if value:
            results = self.storage_manager.search_chats(value)
            self.history_layout.clear_widgets()
            for chat in results:
                # Add chat items (same as _load_history)
                pass
        else:
            self._load_history()

    def _on_back(self, instance) -> None:
        """Go back to chat screen."""
        self.app_manager.switch_screen('chat', direction='right')
