"""Message Bubble Widget - Displays chat messages."""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.graphics import RoundedRectangle, Color
from kivy.core.clipboard import Clipboard
from kivy.uix.textinput import TextInput
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import markdown
import re
from typing import Callable, Optional
from core.theme_manager import ThemeManager


class MessageBubble(BoxLayout):
    """Custom message bubble widget."""

    def __init__(self, content: str, sender: str = 'user', actions_callback: Optional[Callable] = None, **kwargs):
        """Initialize message bubble.

        Args:
            content: Message content
            sender: 'user' or 'ai'
            actions_callback: Callback for action buttons
            **kwargs: Additional arguments
        """
        super().__init__(**kwargs)
        self.content = content
        self.sender = sender
        self.actions_callback = actions_callback
        self.theme_manager = ThemeManager.get_instance()
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.padding = (10, 5)
        self.spacing = 5

        # Message container
        bubble_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        bubble_layout.bind(minimum_height=bubble_layout.setter('height'))

        # Message text
        message_label = Label(
            text=self._parse_content(content),
            markup=True,
            size_hint_y=None,
            text_size=(self.width - 40, None),
            padding=(10, 10),
        )
        message_label.bind(texture_size=message_label.setter('size'))

        # Apply theme colors
        bubble_color = self.theme_manager.get_color(
            'user_bubble' if sender == 'user' else 'ai_bubble'
        )
        text_color = self.theme_manager.get_color('text_primary')

        with bubble_layout.canvas.before:
            Color(*bubble_color)
            RoundedRectangle(
                size=bubble_layout.size,
                pos=bubble_layout.pos,
                radius=[15, 15, 15, 15]
            )

        message_label.color = text_color
        bubble_layout.add_widget(message_label)

        # Actions toolbar for AI messages
        if sender == 'ai':
            actions_layout = BoxLayout(size_hint_y=None, height=40, spacing=5, padding=(5, 0))
            
            actions = ['Copy', 'Export', 'Listen', 'Regenerate', 'Edit', 'More']
            for action in actions:
                btn = Button(
                    text=action,
                    size_hint_x=1/len(actions),
                    size_hint_y=1,
                    background_color=self.theme_manager.get_color('button_bg'),
                )
                btn.bind(on_press=lambda x, a=action: self._on_action(a))
                actions_layout.add_widget(btn)

            bubble_layout.add_widget(actions_layout)

        # Alignment
        if sender == 'user':
            self.add_widget(BoxLayout(size_hint_x=0.3))
        
        self.add_widget(bubble_layout)
        
        if sender == 'ai':
            self.add_widget(BoxLayout(size_hint_x=0.3))

        self.bind(size=self._update_size)

    def _parse_content(self, content: str) -> str:
        """Parse content to support basic markdown.

        Args:
            content: Raw content

        Returns:
            Processed content
        """
        # Basic markdown parsing for Kivy markup
        processed = content
        
        # Bold
        processed = re.sub(r'\*\*(.*?)\*\*', r'[b]\1[/b]', processed)
        
        # Italic
        processed = re.sub(r'\*(.*?)\*', r'[i]\1[/i]', processed)
        
        # Code blocks
        processed = re.sub(r'`(.*?)`', r'[font=monospace]\1[/font]', processed)
        
        return processed

    def _on_action(self, action: str) -> None:
        """Handle action button press.

        Args:
            action: Action name
        """
        if action == 'Copy':
            Clipboard.copy(self.content)
        elif action == 'Export':
            if self.actions_callback:
                self.actions_callback('export', self.content)
        elif action == 'Listen':
            if self.actions_callback:
                self.actions_callback('listen', self.content)
        elif action == 'Regenerate':
            if self.actions_callback:
                self.actions_callback('regenerate', self.content)
        elif action == 'Edit':
            if self.actions_callback:
                self.actions_callback('edit', self.content)
        elif action == 'More':
            self._show_more_options()

    def _show_more_options(self) -> None:
        """Show more action options."""
        popup_content = GridLayout(cols=1, spacing=10, size_hint_y=None)
        popup_content.bind(minimum_height=popup_content.setter('height'))
        
        options = ['Fact Check', 'Modify Response', 'Draft Variations']
        for option in options:
            btn = Button(
                text=option,
                size_hint_y=None,
                height=44,
                background_color=self.theme_manager.get_color('button_bg'),
            )
            btn.bind(on_press=lambda x, o=option: self._on_more_option(o))
            popup_content.add_widget(btn)
        
        popup = Popup(
            title='More Options',
            content=popup_content,
            size_hint=(0.8, 0.5),
        )
        popup.open()

    def _on_more_option(self, option: str) -> None:
        """Handle more options.

        Args:
            option: Option name
        """
        if self.actions_callback:
            self.actions_callback(option.lower().replace(' ', '_'), self.content)

    def _update_size(self, instance, value) -> None:
        """Update bubble size."""
        pass
