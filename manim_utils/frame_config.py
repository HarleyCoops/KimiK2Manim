"""
Manim Configuration Module

Centralized configuration for Manim frame sizes and rendering settings.
This ensures consistent frame boundaries across all scenes.
"""

from manim import config

# Frame dimensions (Manim defaults)
FRAME_WIDTH = config.frame_width  # Default: 14.2
FRAME_HEIGHT = config.frame_height  # Default: 8.0
FRAME_ASPECT_RATIO = FRAME_WIDTH / FRAME_HEIGHT  # Default: 1.777... (16:9)

# Safe rendering area (90% of frame to leave margins)
SAFE_FRAME_WIDTH = FRAME_WIDTH * 0.9
SAFE_FRAME_HEIGHT = FRAME_HEIGHT * 0.9

# Coordinate boundaries
FRAME_X_MIN = -FRAME_WIDTH / 2  # -7.1
FRAME_X_MAX = FRAME_WIDTH / 2   # 7.1
FRAME_Y_MIN = -FRAME_HEIGHT / 2 # -4.0
FRAME_Y_MAX = FRAME_HEIGHT / 2  # 4.0

SAFE_X_MIN = -SAFE_FRAME_WIDTH / 2  # -6.39
SAFE_X_MAX = SAFE_FRAME_WIDTH / 2   # 6.39
SAFE_Y_MIN = -SAFE_FRAME_HEIGHT / 2  # -3.6
SAFE_Y_MAX = SAFE_FRAME_HEIGHT / 2  # 3.6

# Default font sizes (scaled to fit safe area)
DEFAULT_TITLE_FONT_SIZE = 42  # Fits comfortably in safe width
DEFAULT_SUBTITLE_FONT_SIZE = 32
DEFAULT_BODY_FONT_SIZE = 24
DEFAULT_EQUATION_FONT_SIZE = 36

# Export constants
__all__ = [
    'FRAME_WIDTH',
    'FRAME_HEIGHT',
    'FRAME_ASPECT_RATIO',
    'SAFE_FRAME_WIDTH',
    'SAFE_FRAME_HEIGHT',
    'FRAME_X_MIN',
    'FRAME_X_MAX',
    'FRAME_Y_MIN',
    'FRAME_Y_MAX',
    'SAFE_X_MIN',
    'SAFE_X_MAX',
    'SAFE_Y_MIN',
    'SAFE_Y_MAX',
    'DEFAULT_TITLE_FONT_SIZE',
    'DEFAULT_SUBTITLE_FONT_SIZE',
    'DEFAULT_BODY_FONT_SIZE',
    'DEFAULT_EQUATION_FONT_SIZE',
]

