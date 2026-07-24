"""Special Feature & Settings Screen."""
from kivy.uix.screen import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.switch import Switch
from kivy.uix.popup import Popup
from kivy.uix.timepicker import TimePicker
from kivy.graphics import Color, RoundedRectangle
from kivy.core.clipboard import Clipboard
from typing import Optional, Callable
from core.theme_manager import ThemeManager
from core.app_manager import AppManager
from core.settings_manager import SettingsManager
from core.security_manager import SecurityManager
import logging

logger = logging.getLogger(__name__)


class SpecialSettingsScreen(Screen):
    """Special Feature & Settings screen."""

    def __init__(self, **kwargs):
        """Initialize special settings screen.

        Args:
            **kwargs: Additional arguments
        """
        super().__init__(**kwargs)
        self.theme_manager = ThemeManager.get_instance()
        self.app_manager = AppManager.get_instance()
        self.settings_manager = SettingsManager.get_instance()
        self.security_manager = SecurityManager.get_instance()
        self.name = 'special_settings'
        self.api_key_visible = False

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
            text='Special Feature & Settings',
            size_hint_x=0.8,
            color=self.theme_manager.get_color('text_primary'),
            bold=True,
        )
        header.add_widget(title)
        main_layout.add_widget(header)

        # Settings scroll
        settings_scroll = ScrollView()
        settings_layout = GridLayout(
            cols=1,
            spacing=15,
            size_hint_y=None,
            padding=(10, 10),
        )
        settings_layout.bind(minimum_height=settings_layout.setter('height'))

        # ============ SECTION 1: INPUT API ============
        settings_layout.add_widget(self._create_section_title('Input API'))

        # Provider selection
        provider_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        provider_layout.add_widget(Label(
            text='Provider:',
            size_hint_x=0.3,
            color=self.theme_manager.get_color('text_primary'),
        ))
        
        current_provider = self.settings_manager.get_setting('ai_provider', 'gemini')
        self.provider_spinner = Spinner(
            text=current_provider.capitalize(),
            values=['Gemini', 'OpenAI', 'Custom'],
            size_hint_x=0.7,
        )
        self.provider_spinner.bind(text=self._on_provider_change)
        provider_layout.add_widget(self.provider_spinner)
        settings_layout.add_widget(provider_layout)

        # API Key input
        api_key_label = Label(
            text='API Key:',
            size_hint_y=None,
            height=30,
            color=self.theme_manager.get_color('text_primary'),
        )
        settings_layout.add_widget(api_key_label)

        api_key_container = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=5)
        self.api_key_input = TextInput(
            hint_text='Paste your API key here',
            multiline=False,
            password=True,
            size_hint_x=0.8,
        )
        
        stored_key = self.settings_manager.get_api_key(current_provider)
        if stored_key:
            self.api_key_input.text = self.security_manager.mask_api_key(stored_key)
        
        api_key_container.add_widget(self.api_key_input)

        # Show/Hide button
        toggle_visibility_btn = Button(
            text='👁',
            size_hint_x=0.1,
            background_color=self.theme_manager.get_color('button_bg'),
        )
        toggle_visibility_btn.bind(on_press=self._on_toggle_api_visibility)
        api_key_container.add_widget(toggle_visibility_btn)

        # Copy button
        copy_btn = Button(
            text='📋',
            size_hint_x=0.1,
            background_color=self.theme_manager.get_color('button_bg'),
        )
        copy_btn.bind(on_press=self._on_copy_api_key)
        api_key_container.add_widget(copy_btn)

        settings_layout.add_widget(api_key_container)

        # Connection status
        self.api_status_label = Label(
            text='Status: Not connected',
            size_hint_y=None,
            height=30,
            color=(1, 1, 0, 1),
        )
        settings_layout.add_widget(self.api_status_label)

        # Save API button
        save_api_btn = Button(
            text='Save API Configuration',
            size_hint_y=None,
            height=50,
            background_color=self.theme_manager.get_color('primary'),
        )
        save_api_btn.bind(on_press=self._on_save_api)
        settings_layout.add_widget(save_api_btn)

        # ============ SECTION 2: SYSTEM PROMPT ============
        settings_layout.add_widget(self._create_section_title('System Prompt'))

        prompt_label = Label(
            text='Custom instructions for AI behavior:',
            size_hint_y=None,
            height=30,
            color=self.theme_manager.get_color('text_secondary'),
        )
        settings_layout.add_widget(prompt_label)

        # System prompt text area
        current_prompt = self.settings_manager.get_system_prompt()
        self.prompt_input = TextInput(
            text=current_prompt,
            multiline=True,
            size_hint_y=None,
            height=120,
            background_color=self.theme_manager.get_color('input_bg'),
            foreground_color=self.theme_manager.get_color('text_primary'),
        )
        settings_layout.add_widget(self.prompt_input)

        # Character counter
        self.prompt_counter = Label(
            text=f'{len(current_prompt)}/1000',
            size_hint_y=None,
            height=20,
            color=self.theme_manager.get_color('text_secondary'),
        )
        self.prompt_input.bind(text=self._on_prompt_text_change)
        settings_layout.add_widget(self.prompt_counter)

        # Prompt buttons
        prompt_buttons = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=50,
            spacing=10,
        )

        save_prompt_btn = Button(
            text='Save',
            size_hint_x=0.5,
            background_color=self.theme_manager.get_color('primary'),
        )
        save_prompt_btn.bind(on_press=self._on_save_prompt)
        prompt_buttons.add_widget(save_prompt_btn)

        reset_prompt_btn = Button(
            text='Reset',
            size_hint_x=0.5,
            background_color=(1, 0.5, 0.3, 1),
        )
        reset_prompt_btn.bind(on_press=self._on_reset_prompt)
        prompt_buttons.add_widget(reset_prompt_btn)

        settings_layout.add_widget(prompt_buttons)

        # ============ SECTION 3: LOCK ALL SETTINGS ============
        settings_layout.add_widget(self._create_section_title('Lock All Settings'))

        lock_info = self.settings_manager.get_lock_info()

        # Enable/Disable toggle
        lock_toggle_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=50,
            spacing=10,
        )
        lock_toggle_layout.add_widget(Label(
            text='Enable Lock:',
            size_hint_x=0.7,
            color=self.theme_manager.get_color('text_primary'),
        ))
        
        self.lock_switch = Switch(
            active=lock_info['enabled'],
            size_hint_x=0.3,
        )
        self.lock_switch.bind(active=self._on_lock_toggle)
        lock_toggle_layout.add_widget(self.lock_switch)
        settings_layout.add_widget(lock_toggle_layout)

        # Start time
        start_time_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=50,
            spacing=10,
        )
        start_time_layout.add_widget(Label(
            text='Start Time:',
            size_hint_x=0.5,
            color=self.theme_manager.get_color('text_primary'),
        ))
        
        self.start_time_input = TextInput(
            text=lock_info['start_time'],
            hint_text='HH:MM',
            multiline=False,
            size_hint_x=0.3,
        )
        start_time_layout.add_widget(self.start_time_input)
        
        start_time_btn = Button(
            text='⏰',
            size_hint_x=0.2,
            background_color=self.theme_manager.get_color('button_bg'),
        )
        start_time_btn.bind(on_press=self._on_select_start_time)
        start_time_layout.add_widget(start_time_btn)
        settings_layout.add_widget(start_time_layout)

        # End time
        end_time_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=50,
            spacing=10,
        )
        end_time_layout.add_widget(Label(
            text='End Time:',
            size_hint_x=0.5,
            color=self.theme_manager.get_color('text_primary'),
        ))
        
        self.end_time_input = TextInput(
            text=lock_info['end_time'],
            hint_text='HH:MM',
            multiline=False,
            size_hint_x=0.3,
        )
        end_time_layout.add_widget(self.end_time_input)
        
        end_time_btn = Button(
            text='⏰',
            size_hint_x=0.2,
            background_color=self.theme_manager.get_color('button_bg'),
        )
        end_time_btn.bind(on_press=self._on_select_end_time)
        end_time_layout.add_widget(end_time_btn)
        settings_layout.add_widget(end_time_layout)

        # Lock status
        self.lock_status_label = Label(
            text=self._get_lock_status_text(),
            size_hint_y=None,
            height=40,
            color=(0, 1, 0, 1) if not lock_info['is_locked'] else (1, 0.3, 0.3, 1),
        )
        settings_layout.add_widget(self.lock_status_label)

        # Save lock schedule button
        save_lock_btn = Button(
            text='Save Lock Schedule',
            size_hint_y=None,
            height=50,
            background_color=self.theme_manager.get_color('primary'),
        )
        save_lock_btn.bind(on_press=self._on_save_lock_schedule)
        settings_layout.add_widget(save_lock_btn)

        settings_scroll.add_widget(settings_layout)
        main_layout.add_widget(settings_scroll)

        self.add_widget(main_layout)
        self.theme_manager.subscribe(self._on_theme_change)

    def _create_section_title(self, title: str) -> Label:
        """Create section title widget.

        Args:
            title: Section title

        Returns:
            Label widget
        """
        return Label(
            text=title,
            size_hint_y=None,
            height=35,
            color=self.theme_manager.get_color('primary'),
            bold=True,
            font_size='18sp',
        )

    def _on_provider_change(self, spinner, text: str) -> None:
        """Handle provider change.

        Args:
            spinner: Spinner instance
            text: Selected provider
        """
        provider = text.lower()
        stored_key = self.settings_manager.get_api_key(provider)
        if stored_key:
            self.api_key_input.text = self.security_manager.mask_api_key(stored_key)
        else:
            self.api_key_input.text = ''
        self.api_key_visible = False
        self.api_key_input.password = True

    def _on_toggle_api_visibility(self, instance) -> None:
        """Toggle API key visibility."""
        self.api_key_visible = not self.api_key_visible
        self.api_key_input.password = not self.api_key_visible

    def _on_copy_api_key(self, instance) -> None:
        """Copy API key to clipboard."""
        if self.api_key_input.text:
            Clipboard.copy(self.api_key_input.text)
            self.api_status_label.text = 'Copied to clipboard!'

    def _on_save_api(self, instance) -> None:
        """Save API configuration."""
        provider = self.provider_spinner.text.lower()
        api_key = self.api_key_input.text.strip()

        if not api_key:
            self._show_error('Please enter an API key')
            return

        if not self.security_manager.validate_api_key(api_key, provider):
            self._show_error(f'Invalid API key format for {provider}')
            return

        try:
            self.settings_manager.set_api_key(provider, api_key)
            self.settings_manager.set_setting('ai_provider', provider)
            self.api_status_label.text = f'✓ {provider.capitalize()} API configured'
            self.api_status_label.color = (0, 1, 0, 1)
            logger.info(f'API key saved for provider: {provider}')
        except Exception as e:
            self._show_error(f'Error saving API key: {str(e)}')

    def _on_prompt_text_change(self, instance, value: str) -> None:
        """Handle system prompt text change.

        Args:
            instance: TextInput instance
            value: New text
        """
        char_count = len(value)
        self.prompt_counter.text = f'{char_count}/1000'

        if char_count > 1000:
            self.prompt_input.text = value[:1000]

    def _on_save_prompt(self, instance) -> None:
        """Save system prompt."""
        prompt = self.prompt_input.text.strip()
        if not prompt:
            self._show_error('System prompt cannot be empty')
            return

        try:
            self.settings_manager.set_system_prompt(prompt)
            self._show_success('System prompt saved successfully')
            logger.info('System prompt saved')
        except Exception as e:
            self._show_error(f'Error saving system prompt: {str(e)}')

    def _on_reset_prompt(self, instance) -> None:
        """Reset system prompt to default."""
        default_prompt = 'You are a helpful study assistant.'
        self.prompt_input.text = default_prompt
        self.settings_manager.set_system_prompt(default_prompt)
        self._show_success('System prompt reset to default')

    def _on_lock_toggle(self, instance, value: bool) -> None:
        """Handle lock toggle.

        Args:
            instance: Switch instance
            value: New value
        """
        pass

    def _on_select_start_time(self, instance) -> None:
        """Open start time picker."""
        content = BoxLayout(orientation='vertical', spacing=10, padding=(10, 10))
        
        # Time input fields
        time_input_layout = BoxLayout(orientation='horizontal', size_hint_y=0.3, spacing=5)
        
        hour_input = TextInput(
            text=self.start_time_input.text.split(':')[0] if ':' in self.start_time_input.text else '09',
            hint_text='Hour',
            multiline=False,
            input_filter='int',
        )
        time_input_layout.add_widget(hour_input)
        
        colon = Label(text=':')
        time_input_layout.add_widget(colon)
        
        minute_input = TextInput(
            text=self.start_time_input.text.split(':')[1] if ':' in self.start_time_input.text else '00',
            hint_text='Min',
            multiline=False,
            input_filter='int',
        )
        time_input_layout.add_widget(minute_input)
        
        content.add_widget(time_input_layout)
        
        # Buttons
        button_layout = BoxLayout(size_hint_y=0.3, spacing=10)
        
        def on_confirm():
            try:
                hour = int(hour_input.text)
                minute = int(minute_input.text)
                if 0 <= hour <= 23 and 0 <= minute <= 59:
                    self.start_time_input.text = f'{hour:02d}:{minute:02d}'
                    popup.dismiss()
                else:
                    self._show_error('Invalid time')
            except ValueError:
                self._show_error('Please enter valid numbers')
        
        confirm_btn = Button(text='Confirm', size_hint_x=0.5)
        confirm_btn.bind(on_press=lambda x: on_confirm())
        button_layout.add_widget(confirm_btn)
        
        cancel_btn = Button(text='Cancel', size_hint_x=0.5)
        button_layout.add_widget(cancel_btn)
        
        content.add_widget(button_layout)
        
        popup = Popup(title='Select Start Time', content=content, size_hint=(0.8, 0.4))
        cancel_btn.bind(on_press=popup.dismiss)
        popup.open()

    def _on_select_end_time(self, instance) -> None:
        """Open end time picker."""
        content = BoxLayout(orientation='vertical', spacing=10, padding=(10, 10))
        
        time_input_layout = BoxLayout(orientation='horizontal', size_hint_y=0.3, spacing=5)
        
        hour_input = TextInput(
            text=self.end_time_input.text.split(':')[0] if ':' in self.end_time_input.text else '17',
            hint_text='Hour',
            multiline=False,
            input_filter='int',
        )
        time_input_layout.add_widget(hour_input)
        
        colon = Label(text=':')
        time_input_layout.add_widget(colon)
        
        minute_input = TextInput(
            text=self.end_time_input.text.split(':')[1] if ':' in self.end_time_input.text else '00',
            hint_text='Min',
            multiline=False,
            input_filter='int',
        )
        time_input_layout.add_widget(minute_input)
        
        content.add_widget(time_input_layout)
        
        button_layout = BoxLayout(size_hint_y=0.3, spacing=10)
        
        def on_confirm():
            try:
                hour = int(hour_input.text)
                minute = int(minute_input.text)
                if 0 <= hour <= 23 and 0 <= minute <= 59:
                    self.end_time_input.text = f'{hour:02d}:{minute:02d}'
                    popup.dismiss()
                else:
                    self._show_error('Invalid time')
            except ValueError:
                self._show_error('Please enter valid numbers')
        
        confirm_btn = Button(text='Confirm', size_hint_x=0.5)
        confirm_btn.bind(on_press=lambda x: on_confirm())
        button_layout.add_widget(confirm_btn)
        
        cancel_btn = Button(text='Cancel', size_hint_x=0.5)
        button_layout.add_widget(cancel_btn)
        
        content.add_widget(button_layout)
        
        popup = Popup(title='Select End Time', content=content, size_hint=(0.8, 0.4))
        cancel_btn.bind(on_press=popup.dismiss)
        popup.open()

    def _on_save_lock_schedule(self, instance) -> None:
        """Save lock schedule."""
        try:
            start_time = self.start_time_input.text.strip()
            end_time = self.end_time_input.text.strip()
            enabled = self.lock_switch.active

            # Validate time format
            if not all(c in '0123456789:' for c in start_time) or not all(c in '0123456789:' for c in end_time):
                self._show_error('Invalid time format. Use HH:MM')
                return

            self.settings_manager.set_lock_schedule(enabled, start_time, end_time)
            self.lock_status_label.text = self._get_lock_status_text()
            self._show_success('Lock schedule saved successfully')
            logger.info(f'Lock schedule saved: {start_time} - {end_time}, enabled: {enabled}')
        except Exception as e:
            self._show_error(f'Error saving lock schedule: {str(e)}')

    def _get_lock_status_text(self) -> str:
        """Get lock status text.

        Returns:
            Status text
        """
        lock_info = self.settings_manager.get_lock_info()
        if lock_info['enabled']:
            if lock_info['is_locked']:
                return f"🔒 Settings are LOCKED until {lock_info['end_time']}"
            else:
                return f"🔓 Settings are unlocked. Lock starts at {lock_info['start_time']}"
        else:
            return "🔓 Lock is disabled"

    def _show_error(self, message: str) -> None:
        """Show error popup.

        Args:
            message: Error message
        """
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message))
        
        close_btn = Button(text='Close', size_hint_y=0.3)
        content.add_widget(close_btn)
        
        popup = Popup(title='Error', content=content, size_hint=(0.8, 0.4))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    def _show_success(self, message: str) -> None:
        """Show success popup.

        Args:
            message: Success message
        """
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message))
        
        close_btn = Button(text='OK', size_hint_y=0.3)
        content.add_widget(close_btn)
        
        popup = Popup(title='Success', content=content, size_hint=(0.8, 0.4))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    def _on_theme_change(self, theme) -> None:
        """Handle theme change.

        Args:
            theme: New theme
        """
        # Reload screen colors (simplified)
        pass

    def _on_back(self, instance) -> None:
        """Go back to settings screen."""
        self.app_manager.switch_screen('settings', direction='right')
