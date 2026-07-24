"""Widgets module."""
from .message_bubble import MessageBubble
from .input_bar import InputBar
from .sidebar import Sidebar
from .animations import create_fade_animation, create_slide_animation

__all__ = [
    'MessageBubble',
    'InputBar',
    'Sidebar',
    'create_fade_animation',
    'create_slide_animation',
]
