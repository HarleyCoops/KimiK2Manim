"""
Combined BoundedScene with Scene Management

This module provides a complete solution combining:
1. Frame boundary constraints (from bounded_scene)
2. Scene management for text/equations (from scene_manager)
"""

from manim import *
from typing import Optional
from manim_utils.bounded_scene import BoundedScene
from manim_utils.scene_manager import (
    SceneManager,
    TextLayer
)
from manim_utils.frame_config import (
    DEFAULT_TITLE_FONT_SIZE,
    DEFAULT_SUBTITLE_FONT_SIZE,
    DEFAULT_BODY_FONT_SIZE,
    DEFAULT_EQUATION_FONT_SIZE
)


class ManagedBoundedScene(BoundedScene):
    """
    Complete scene class with both boundary constraints and scene management.
    
    Features:
    - Automatic boundary checking (from BoundedScene)
    - Automatic text/equation lifecycle management (from ManagedBoundedScene)
    - Overlap prevention
    - Section transitions
    
    Usage:
        class MyScene(ManagedBoundedScene):
            def construct(self):
                # Add title (automatically replaces previous titles)
                self.add_title("My Title")
                
                # Add explanation (automatically replaces previous explanations)
                self.add_explanation("This is an explanation")
                
                # Add equation (automatically replaces previous equations)
                self.add_equation(r"E = mc^2")
                
                # Transition to new section (clears old content)
                self.transition_section("New Section Title")
    """
    
    def __init__(self, *args, **kwargs):
        BoundedScene.__init__(self, *args, **kwargs)
        self.manager = SceneManager(self)
    
    def add_explanation(
        self,
        text: str,
        fade_out_previous: bool = True,
        position: Optional[str] = None,
        font_size: int = None,
        **kwargs
    ) -> Text:
        """
        Add explanatory text that automatically replaces previous explanations.
        
        Args:
            text: Explanation text
            fade_out_previous: Remove previous explanations
            position: Position hint ('top', 'center', 'bottom', etc.)
            font_size: Font size (uses default if None)
            **kwargs: Additional Text arguments
        
        Returns:
            Text object (bounded and constrained)
        """
        font_size = font_size or DEFAULT_BODY_FONT_SIZE
        
        # Create bounded text
        text_obj = self.bounded_text(text, font_size=font_size, **kwargs)
        
        # Add via manager (handles lifecycle and positioning)
        return self.manager.add_text(
            text_obj,
            layer=TextLayer.EXPLANATION,
            fade_out_previous=fade_out_previous,
            position=position
        )
    
    def add_equation(
        self,
        equation: str,
        fade_out_previous: bool = True,
        position: Optional[str] = None,
        font_size: int = None,
        **kwargs
    ) -> MathTex:
        """
        Add an equation that automatically replaces previous equations.
        
        Args:
            equation: LaTeX equation string
            fade_out_previous: Remove previous equations
            position: Position hint
            font_size: Font size (uses default if None)
            **kwargs: Additional MathTex arguments
        
        Returns:
            MathTex object (bounded and constrained)
        """
        font_size = font_size or DEFAULT_EQUATION_FONT_SIZE
        
        # Create bounded equation
        eq_obj = self.bounded_math_tex(equation, font_size=font_size, **kwargs)
        
        # Add via manager
        return self.manager.add_equation(
            eq_obj,
            layer=TextLayer.EQUATION,
            fade_out_previous=fade_out_previous,
            position=position
        )
    
    def add_title(
        self,
        title: str,
        fade_out_previous: bool = True,
        font_size: int = None,
        **kwargs
    ) -> Text:
        """Add a title that replaces previous titles."""
        font_size = font_size or DEFAULT_TITLE_FONT_SIZE
        title_obj = self.bounded_text(title, font_size=font_size, **kwargs)
        return self.manager.add_text(
            title_obj,
            layer=TextLayer.TITLE,
            fade_out_previous=fade_out_previous,
            position='top'
        )
    
    def add_subtitle(
        self,
        subtitle: str,
        fade_out_previous: bool = True,
        font_size: int = None,
        **kwargs
    ) -> Text:
        """Add a subtitle that replaces previous subtitles."""
        font_size = font_size or DEFAULT_SUBTITLE_FONT_SIZE
        subtitle_obj = self.bounded_text(subtitle, font_size=font_size, **kwargs)
        return self.manager.add_text(
            subtitle_obj,
            layer=TextLayer.SUBTITLE,
            fade_out_previous=fade_out_previous,
            position=None  # Auto-position below title
        )
    
    def transition_section(
        self,
        new_title: Optional[str] = None,
        keep_equations: bool = False,
        fade_time: float = 1.0
    ):
        """
        Transition to a new section, clearing old explanatory content.
        
        Args:
            new_title: Optional new title to show
            keep_equations: Keep equations visible during transition
            fade_time: Transition duration
        """
        self.manager.transition_to_new_section(
            new_title=new_title,
            keep_equations=keep_equations,
            fade_time=fade_time
        )
    
    def clear_explanations(self, fade_out: bool = True):
        """Clear all explanatory text."""
        self.manager.clear_layer(TextLayer.EXPLANATION, fade_out)
    
    def clear_equations(self, fade_out: bool = True):
        """Clear all equations."""
        self.manager.clear_layer(TextLayer.EQUATION, fade_out)
    
    def clear_all_text(self, fade_out: bool = True, keep_title: bool = False):
        """Clear all text content."""
        exclude = [TextLayer.TITLE] if keep_title else []
        self.manager.clear_all(fade_out=fade_out, exclude_layers=exclude)

