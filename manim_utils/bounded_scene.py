"""
Manim Frame Boundary Utilities

This module provides utilities to ensure all Manim content stays within frame boundaries.
Manim's default frame is 14.2 units wide × 8 units tall (16:9 aspect ratio).

The universal problem: Objects often render outside the visible frame because:
1. Font sizes are too large
2. Objects aren't scaled to fit
3. Absolute coordinates exceed ±7.1 (width/2) or ±4 (height/2)
4. No automatic boundary checking

Solution: A base scene class that automatically constrains all content.
"""

from manim import *
import numpy as np
from typing import Union, Tuple


# Manim's default frame dimensions
DEFAULT_FRAME_WIDTH = config.frame_width  # Typically 14.2
DEFAULT_FRAME_HEIGHT = config.frame_height  # Typically 8.0
DEFAULT_FRAME_ASPECT = DEFAULT_FRAME_WIDTH / DEFAULT_FRAME_HEIGHT  # 16:9 = 1.777...

# Safe boundaries (leave margin for edge elements)
SAFE_WIDTH = DEFAULT_FRAME_WIDTH * 0.9  # 12.78 units
SAFE_HEIGHT = DEFAULT_FRAME_HEIGHT * 0.9  # 7.2 units
SAFE_X_MIN = -SAFE_WIDTH / 2  # -6.39
SAFE_X_MAX = SAFE_WIDTH / 2  # 6.39
SAFE_Y_MIN = -SAFE_HEIGHT / 2  # -3.6
SAFE_Y_MAX = SAFE_HEIGHT / 2  # 3.6


class BoundedScene(Scene):
    """
    Base Scene class that automatically constrains all content within frame boundaries.
    
    Usage:
        class MyScene(BoundedScene):
            def construct(self):
                # All content will be automatically constrained
                title = self.bounded_text("My Title", font_size=48)
                ...
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frame_width = DEFAULT_FRAME_WIDTH
        self.frame_height = DEFAULT_FRAME_HEIGHT
        self.safe_width = SAFE_WIDTH
        self.safe_height = SAFE_HEIGHT
    
    def bounded_text(
        self,
        text: str,
        font_size: int = 36,
        max_width: float = None,
        max_height: float = None,
        **kwargs
    ) -> Text:
        """
        Create text that automatically scales to fit within safe boundaries.
        
        Args:
            text: Text content
            font_size: Initial font size (will be scaled down if needed)
            max_width: Maximum width (defaults to safe_width)
            max_height: Maximum height (defaults to safe_height)
            **kwargs: Additional arguments for Text()
        
        Returns:
            Text object constrained within boundaries
        """
        max_width = max_width or self.safe_width
        max_height = max_height or self.safe_height
        
        text_obj = Text(text, font_size=font_size, **kwargs)
        
        # Scale down if too large
        if text_obj.width > max_width:
            text_obj.scale_to_fit_width(max_width)
        if text_obj.height > max_height:
            text_obj.scale_to_fit_height(max_height)
        
        return text_obj
    
    def bounded_math_tex(
        self,
        tex_string: str,
        font_size: int = 36,
        max_width: float = None,
        max_height: float = None,
        **kwargs
    ) -> MathTex:
        """
        Create MathTex that automatically scales to fit within safe boundaries.
        """
        max_width = max_width or self.safe_width
        max_height = max_height or self.safe_height
        
        tex_obj = MathTex(tex_string, font_size=font_size, **kwargs)
        
        if tex_obj.width > max_width:
            tex_obj.scale_to_fit_width(max_width)
        if tex_obj.height > max_height:
            tex_obj.scale_to_fit_height(max_height)
        
        return tex_obj
    
    def bounded_vgroup(
        self,
        *mobjects,
        max_width: float = None,
        max_height: float = None,
        scale_to_fit: bool = True
    ) -> VGroup:
        """
        Create a VGroup that is constrained within boundaries.
        
        Args:
            *mobjects: Mobjects to group
            max_width: Maximum width
            max_height: Maximum height
            scale_to_fit: If True, scale the group to fit
        
        Returns:
            VGroup constrained within boundaries
        """
        max_width = max_width or self.safe_width
        max_height = max_height or self.safe_height
        
        group = VGroup(*mobjects)
        
        if scale_to_fit:
            if group.width > max_width:
                group.scale_to_fit_width(max_width)
            if group.height > max_height:
                group.scale_to_fit_height(max_height)
        
        return group
    
    def constrain_to_safe_area(self, mobject: Mobject) -> Mobject:
        """
        Constrain a mobject to stay within the safe area.
        
        Args:
            mobject: Mobject to constrain
        
        Returns:
            Constrained mobject
        """
        # Get bounding box
        bbox = mobject.get_bounding_box()
        width = bbox[1][0] - bbox[0][0]
        height = bbox[1][1] - bbox[0][1]
        
        # Scale if too large
        if width > self.safe_width:
            mobject.scale_to_fit_width(self.safe_width)
        if height > self.safe_height:
            mobject.scale_to_fit_height(self.safe_height)
        
        # Ensure position is within bounds
        center = mobject.get_center()
        x, y = center[0], center[1]
        
        # Get updated bounding box after scaling
        bbox = mobject.get_bounding_box()
        width = bbox[1][0] - bbox[0][0]
        height = bbox[1][1] - bbox[0][1]
        
        # Adjust position if needed
        if x - width/2 < SAFE_X_MIN:
            mobject.shift(RIGHT * (SAFE_X_MIN - (x - width/2)))
        elif x + width/2 > SAFE_X_MAX:
            mobject.shift(LEFT * ((x + width/2) - SAFE_X_MAX))
        
        if y - height/2 < SAFE_Y_MIN:
            mobject.shift(UP * (SAFE_Y_MIN - (y - height/2)))
        elif y + height/2 > SAFE_Y_MAX:
            mobject.shift(DOWN * ((y + height/2) - SAFE_Y_MAX))
        
        return mobject
    
    def safe_position(
        self,
        mobject: Mobject,
        x: float = None,
        y: float = None,
        position: str = None
    ) -> Mobject:
        """
        Position a mobject safely within boundaries.
        
        Args:
            mobject: Mobject to position
            x: X coordinate (will be clamped to safe range)
            y: Y coordinate (will be clamped to safe range)
            position: Predefined position ('center', 'top', 'bottom', 'left', 'right', etc.)
        
        Returns:
            Positioned mobject
        """
        if position:
            if position == 'center':
                mobject.move_to(ORIGIN)
            elif position == 'top':
                mobject.to_edge(UP, buff=0.3)
            elif position == 'bottom':
                mobject.to_edge(DOWN, buff=0.3)
            elif position == 'left':
                mobject.to_edge(LEFT, buff=0.3)
            elif position == 'right':
                mobject.to_edge(RIGHT, buff=0.3)
            elif position == 'top_left':
                mobject.to_corner(UL, buff=0.3)
            elif position == 'top_right':
                mobject.to_corner(UR, buff=0.3)
            elif position == 'bottom_left':
                mobject.to_corner(DL, buff=0.3)
            elif position == 'bottom_right':
                mobject.to_corner(DR, buff=0.3)
        else:
            if x is not None:
                x = np.clip(x, SAFE_X_MIN, SAFE_X_MAX)
            if y is not None:
                y = np.clip(y, SAFE_Y_MIN, SAFE_Y_MAX)
            
            if x is not None and y is not None:
                mobject.move_to([x, y, 0])
            elif x is not None:
                mobject.shift(RIGHT * (x - mobject.get_center()[0]))
            elif y is not None:
                mobject.shift(UP * (y - mobject.get_center()[1]))
        
        return mobject
    
    def create_safe_axes(
        self,
        x_range: Tuple[float, float, float] = None,
        y_range: Tuple[float, float, float] = None,
        width: float = None,
        height: float = None,
        **kwargs
    ) -> Axes:
        """
        Create axes that fit within safe boundaries.
        
        Args:
            x_range: (x_min, x_max, step)
            y_range: (y_min, y_max, step)
            width: Desired width (will be clamped to safe_width)
            height: Desired height (will be clamped to safe_height)
            **kwargs: Additional arguments for Axes()
        
        Returns:
            Axes object constrained within boundaries
        """
        width = min(width or self.safe_width, self.safe_width)
        height = min(height or self.safe_height, self.safe_height)
        
        x_range = x_range or (-width/2, width/2, width/10)
        y_range = y_range or (-height/2, height/2, height/10)
        
        return Axes(
            x_range=x_range,
            y_range=y_range,
            x_length=width,
            y_length=height,
            **kwargs
        )


def constrain_mobject(mobject: Mobject, max_width: float = None, max_height: float = None) -> Mobject:
    """
    Standalone function to constrain any mobject.
    
    Args:
        mobject: Mobject to constrain
        max_width: Maximum width (defaults to SAFE_WIDTH)
        max_height: Maximum height (defaults to SAFE_HEIGHT)
    
    Returns:
        Constrained mobject
    """
    max_width = max_width or SAFE_WIDTH
    max_height = max_height or SAFE_HEIGHT
    
    if mobject.width > max_width:
        mobject.scale_to_fit_width(max_width)
    if mobject.height > max_height:
        mobject.scale_to_fit_height(max_height)
    
    return mobject


def get_safe_font_size(text: str, max_width: float = SAFE_WIDTH, initial_size: int = 48) -> int:
    """
    Calculate a safe font size for text that will fit within max_width.
    
    Args:
        text: Text content
        max_width: Maximum width constraint
        initial_size: Initial font size to test
    
    Returns:
        Safe font size
    """
    test_text = Text(text, font_size=initial_size)
    
    if test_text.width <= max_width:
        return initial_size
    
    # Scale down proportionally
    scale_factor = max_width / test_text.width
    return int(initial_size * scale_factor * 0.95)  # 5% margin


# Example usage:
if __name__ == "__main__":
    class ExampleScene(BoundedScene):
        def construct(self):
            # Title automatically constrained
            title = self.bounded_text(
                "This is a Very Long Title That Would Normally Overflow",
                font_size=48,
                color=GOLD
            )
            self.safe_position(title, position='top')
            
            # Math equation automatically constrained
            equation = self.bounded_math_tex(
                r"\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}",
                font_size=60,
                color=WHITE
            )
            self.safe_position(equation, position='center')
            
            # Axes automatically fit
            axes = self.create_safe_axes(
                x_range=(-5, 5, 1),
                y_range=(-3, 3, 1)
            )
            self.safe_position(axes, position='bottom')
            
            self.play(Write(title))
            self.play(Write(equation))
            self.play(Create(axes))
            self.wait(2)

