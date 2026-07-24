"""Sidebar Widget - Navigation drawer."""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from typing import Callable, Optional, Dict, Any
from core.theme_manager import ThemeManager


class Sidebar(BoxLayout):
    """Navigation sidebar widget."""

    def __init__(self, menu_callback: Optional[Callable] = None, **kwargs):
        """Initialize sidebar.

        Args:
            menu_callback: Callback for menu item selection
            **kwargs: Additional arguments
        """
        super().__init__(**kwargs)
        self.menu_callback = menu_callback
        self.theme_manager = ThemeManager.get_instance()
        self.orientation = 'vertical'
        self.size_hint_x = 0.75
        self.spacing = 0
        self.padding = 0

        # Apply theme background
        with self.canvas.before:
            Color(*self.theme_manager.get_color('surface'))
            RoundedRectangle(
                size=self.size,
                pos=self.pos,
            )

        # Header
        header = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=100,
            padding=(15, 15),
            spacing=5,
        )
        
        with header.canvas.before:
            Color(*self.theme_manager.get_color('primary'))
            RoundedRectangle(
                size=header.size,
                pos=header.pos,
                radius=[0, 0, 20, 0]
            )

        title = Label(
            text='Hemel Study AI',
            size_hint_y=None,
            height=30,
            font_size='20sp',
            bold=True,
            color=self.theme_manager.get_color('button_text'),
        )
        subtitle = Label(
            text='Made by Hemel',
            size_hint_y=None,
            height=20,
            font_size='12sp',
            color=self.theme_manager.get_color('button_text'),
        )
        header.add_widget(title)
        header.add_widget(subtitle)

        self.add_widget(header)

        # Menu items
        menu_scroll = ScrollView(size_hint_y=1)
        menu_layout = GridLayout(
            cols=1,
            spacing=2,
            size_hint_y=None,
            padding=(0, 10),
        )
        menu_layout.bind(minimum_height=menu_layout.setter('height'))

        menu_items = [
            ('New Chat', 'new_chat'),
            ('Chat History', 'history'),
            ('Pinned Chats', 'pinned'),
            ('Extensions (@)', 'extensions'),
            ('Special Feature & Settings', 'special_settings'),
            ('Theme', 'theme'),
            ('Help', 'help'),
            ('About', 'about'),
        ]

        for label, action in menu_items:
            btn = Button(
                text=label,
                size_hint_y=None,
                height=50,
                background_color=self.theme_manager.get_color('surface'),
                color=self.theme_manager.get_color('text_primary'),
            )
            btn.bind(on_press=lambda x, a=action: self._on_menu_item(a))
            menu_layout.add_widget(btn)

        menu_scroll.add_widget(menu_layout)
        self.add_widget(menu_scroll)

    def _on_menu_item(self, action: str) -> None:
        """Handle menu item selection.

        Args:
            action: Action identifier
        """
        if self.menu_callback:
            self.menu_callback(action)
