"""Theme Selection Screen."""
from kivy.uix.screen import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle, Line
from typing import Optional, Callable
from core.theme_manager import ThemeManager, ThemeType
from core.app_manager import AppManager


class ThemeSelectionScreen(Screen):
    """Theme selection screen."""

    def __init__(self, **kwargs):
        """Initialize theme selection screen.

        Args:
            **kwargs: Additional arguments
        """
        super().__init__(**kwargs)
        self.theme_manager = ThemeManager.get_instance()
        self.app_manager = AppManager.get_instance()
        self.name = 'theme'

        main_layout = BoxLayout(orientation='vertical', spacing=15, padding=(10, 10))

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
            text='Select Theme',
            size_hint_x=0.8,
            color=self.theme_manager.get_color('text_primary'),
            bold=True,
        )
        header.add_widget(title)
        main_layout.add_widget(header)

        # Themes grid
        themes_layout = GridLayout(
            cols=1,
            spacing=15,
            size_hint_y=0.9,
            padding=(10, 10),
        )

        current_theme = self.theme_manager.get_theme()

        # Light Theme Card
        light_card = self._create_theme_card(
            'Light Theme',
            'Clean, bright interface perfect for daytime use.',
            ThemeType.LIGHT,
            is_current=(current_theme == ThemeType.LIGHT),
            preview_color=(0.95, 0.95, 0.95, 1)
        )
        themes_layout.add_widget(light_card)

        # Dark Theme Card
        dark_card = self._create_theme_card(
            'Dark Theme',
            'Night-friendly interface, easy on the eyes with OLED optimization.',
            ThemeType.DARK,
            is_current=(current_theme == ThemeType.DARK),
            preview_color=(0.13, 0.13, 0.13, 1)
        )
        themes_layout.add_widget(dark_card)

        # WhatsApp Theme Card
        whatsapp_card = self._create_theme_card(
            'WhatsApp Theme',
            'Green-inspired chat interface with WhatsApp-style design.',
            ThemeType.WHATSAPP,
            is_current=(current_theme == ThemeType.WHATSAPP),
            preview_color=(0.09, 0.12, 0.13, 1)
        )
        themes_layout.add_widget(whatsapp_card)

        main_layout.add_widget(themes_layout)
        self.add_widget(main_layout)

    def _create_theme_card(self, title: str, description: str, theme_type: ThemeType,
                          is_current: bool = False, preview_color=None) -> BoxLayout:
        """Create theme selection card.

        Args:
            title: Theme name
            description: Theme description
            theme_type: Theme type
            is_current: Is this the current theme
            preview_color: Preview color

        Returns:
            Card widget
        """
        card = BoxLayout(orientation='vertical', size_hint_y=None, height=150, spacing=10, padding=(15, 15))

        # Card background
        border_color = self.theme_manager.get_color('primary') if is_current else self.theme_manager.get_color('divider')
        border_width = 3 if is_current else 1

        with card.canvas.before:
            Color(*self.theme_manager.get_color('surface'))
            RoundedRectangle(
                size=card.size,
                pos=card.pos,
                radius=[15, 15, 15, 15]
            )
            Color(*border_color)
            Line(
                width=border_width,
                rectangle=(*card.pos, *card.size),
                radius=[15, 15, 15, 15]
            )

        # Content
        content_layout = BoxLayout(orientation='horizontal', spacing=10)

        # Preview box
        preview_box = BoxLayout(size_hint_x=0.25, size_hint_y=1)
        with preview_box.canvas.before:
            Color(*preview_color)
            RoundedRectangle(
                size=preview_box.size,
                pos=preview_box.pos,
                radius=[10, 10, 10, 10]
            )
        content_layout.add_widget(preview_box)

        # Text and button
        text_button_layout = BoxLayout(orientation='vertical', size_hint_x=0.75, spacing=5)

        # Title
        title_label = Label(
            text=title,
            size_hint_y=0.3,
            color=self.theme_manager.get_color('text_primary'),
            bold=True,
            font_size='16sp',
        )
        text_button_layout.add_widget(title_label)

        # Description
        desc_label = Label(
            text=description,
            size_hint_y=0.5,
            color=self.theme_manager.get_color('text_secondary'),
            font_size='11sp',
        )
        text_button_layout.add_widget(desc_label)

        # Select button
        select_btn = Button(
            text='Current' if is_current else 'Select',
            size_hint_y=0.2,
            background_color=self.theme_manager.get_color('primary') if is_current else self.theme_manager.get_color('button_bg'),
        )
        if not is_current:
            select_btn.bind(on_press=lambda x: self._on_select_theme(theme_type))
        else:
            select_btn.disabled = True
        text_button_layout.add_widget(select_btn)

        content_layout.add_widget(text_button_layout)
        card.add_widget(content_layout)

        return card

    def _on_select_theme(self, theme_type: ThemeType) -> None:
        """Handle theme selection.

        Args:
            theme_type: Selected theme type
        """
        self.theme_manager.set_theme(theme_type)
        # Reload screen
        self.manager.remove_widget(self)
        new_screen = ThemeSelectionScreen()
        self.manager.add_widget(new_screen)
        self.manager.current = 'theme'

    def _on_back(self, instance) -> None:
        """Go back to settings screen."""
        self.app_manager.switch_screen('settings', direction='right')
