"""Input Bar Widget - Bottom input section for messages."""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.core.window import Window
from typing import Callable, Optional
from core.theme_manager import ThemeManager


class InputBar(BoxLayout):
    """Modern input bar widget with message composition."""

    def __init__(self, send_callback: Optional[Callable] = None, **kwargs):
        """Initialize input bar.

        Args:
            send_callback: Callback when message is sent
            **kwargs: Additional arguments
        """
        super().__init__(**kwargs)
        self.send_callback = send_callback
        self.theme_manager = ThemeManager.get_instance()
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = 80
        self.padding = (10, 10)
        self.spacing = 10

        # Input container
        input_container = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=60,
            spacing=8,
            padding=(5, 5),
        )

        # Apply theme background
        with input_container.canvas.before:
            Color(*self.theme_manager.get_color('input_bg'))
            RoundedRectangle(
                size=input_container.size,
                pos=input_container.pos,
                radius=[20, 20, 20, 20]
            )
            Color(*self.theme_manager.get_color('divider'))
            Line(
                width=1,
                rectangle=(*input_container.pos, *input_container.size),
                radius=[20, 20, 20, 20]
            )

        # Attachment button
        attach_btn = Button(
            text='+',
            size_hint_x=None,
            width=45,
            background_color=self.theme_manager.get_color('button_bg'),
            font_size='24sp',
        )
        attach_btn.bind(on_press=self._on_attach)
        input_container.add_widget(attach_btn)

        # Text input
        self.text_input = TextInput(
            multiline=True,
            hint_text='Type your message...',
            size_hint_y=1,
            background_color=self.theme_manager.get_color('input_bg'),
            foreground_color=self.theme_manager.get_color('text_primary'),
            hint_text_color=self.theme_manager.get_color('text_secondary'),
        )
        self.text_input.bind(text=self._on_text_change)
        input_container.add_widget(self.text_input)

        # Microphone button
        mic_btn = Button(
            text='🎤',
            size_hint_x=None,
            width=45,
            background_color=self.theme_manager.get_color('button_bg'),
            font_size='18sp',
        )
        mic_btn.bind(on_press=self._on_microphone)
        input_container.add_widget(mic_btn)

        # Send button
        self.send_btn = Button(
            text='⬆',
            size_hint_x=None,
            width=45,
            background_color=self.theme_manager.get_color('button_bg'),
            font_size='20sp',
        )
        self.send_btn.bind(on_press=self._on_send)
        input_container.add_widget(self.send_btn)

        # Character counter (optional)
        counter_layout = BoxLayout(size_hint_y=None, height=20)
        self.counter_label = Label(
            text='0/2000',
            size_hint_x=1,
            color=self.theme_manager.get_color('text_secondary'),
            font_size='10sp',
        )
        counter_layout.add_widget(self.counter_label)

        self.add_widget(input_container)
        self.add_widget(counter_layout)

    def _on_text_change(self, instance, value: str) -> None:
        """Handle text change.

        Args:
            instance: TextInput instance
            value: New text value
        """
        # Update character counter
        char_count = len(value)
        self.counter_label.text = f'{char_count}/2000'

        # Limit text length
        if char_count > 2000:
            self.text_input.text = value[:2000]

    def _on_attach(self, instance) -> None:
        """Handle attachment button press."""
        # Placeholder for attachment functionality
        pass

    def _on_microphone(self, instance) -> None:
        """Handle microphone button press."""
        # Placeholder for voice input
        pass

    def _on_send(self, instance) -> None:
        """Handle send button press."""
        message = self.text_input.text.strip()
        if message and self.send_callback:
            self.send_callback(message)
            self.text_input.text = ''

    def get_message(self) -> str:
        """Get current message text.

        Returns:
            Message text
        """
        return self.text_input.text

    def clear_message(self) -> None:
        """Clear message input."""
        self.text_input.text = ''

    def set_enabled(self, enabled: bool) -> None:
        """Enable or disable input.

        Args:
            enabled: True to enable
        """
        self.text_input.disabled = not enabled
        self.send_btn.disabled = not enabled
