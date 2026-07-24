"""Animation utilities."""
from kivy.animation import Animation
from kivy.uix.widget import Widget
from typing import Callable, Optional


def create_fade_animation(widget: Widget, duration: float = 1.0,
                        start_opacity: float = 1.0,
                        end_opacity: float = 0.0,
                        on_complete: Optional[Callable] = None) -> Animation:
    """Create fade animation.

    Args:
        widget: Widget to animate
        duration: Animation duration in seconds
        start_opacity: Starting opacity
        end_opacity: Ending opacity
        on_complete: Callback when animation completes

    Returns:
        Animation instance
    """
    widget.opacity = start_opacity
    anim = Animation(opacity=end_opacity, duration=duration)
    if on_complete:
        anim.bind(on_complete=lambda x: on_complete())
    return anim


def create_slide_animation(widget: Widget, duration: float = 0.5,
                         x_start: float = 0, y_start: float = 0,
                         x_end: float = 0, y_end: float = 0,
                         on_complete: Optional[Callable] = None) -> Animation:
    """Create slide animation.

    Args:
        widget: Widget to animate
        duration: Animation duration in seconds
        x_start: Starting X position
        y_start: Starting Y position
        x_end: Ending X position
        y_end: Ending Y position
        on_complete: Callback when animation completes

    Returns:
        Animation instance
    """
    widget.x = x_start
    widget.y = y_start
    anim = Animation(x=x_end, y=y_end, duration=duration)
    if on_complete:
        anim.bind(on_complete=lambda x: on_complete())
    return anim


def create_scale_animation(widget: Widget, duration: float = 0.5,
                         start_scale: float = 0.5,
                         end_scale: float = 1.0,
                         on_complete: Optional[Callable] = None) -> Animation:
    """Create scale animation.

    Args:
        widget: Widget to animate
        duration: Animation duration in seconds
        start_scale: Starting scale factor
        end_scale: Ending scale factor
        on_complete: Callback when animation completes

    Returns:
        Animation instance
    """
    widget.scale = start_scale
    anim = Animation(scale=end_scale, duration=duration)
    if on_complete:
        anim.bind(on_complete=lambda x: on_complete())
    return anim
