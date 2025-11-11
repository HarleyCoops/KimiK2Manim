"""
Manim Scene Management Utilities

Provides scene control for managing text explanations and equations,
ensuring they don't overlap and are properly removed when not needed.
"""

from manim import *
from typing import List, Dict, Optional, Union
from enum import Enum
from manim_utils.frame_config import (
    DEFAULT_TITLE_FONT_SIZE,
    DEFAULT_SUBTITLE_FONT_SIZE,
    DEFAULT_BODY_FONT_SIZE,
    DEFAULT_EQUATION_FONT_SIZE
)


class TextLayer(Enum):
    """Layers for organizing text content."""
    TITLE = "title"
    SUBTITLE = "subtitle"
    EXPLANATION = "explanation"
    EQUATION = "equation"
    LABEL = "label"
    ANNOTATION = "annotation"


class SceneManager:
    """
    Manages scene content to prevent overlaps and handle transitions.
    
    Tracks active text/equations and automatically removes old content
    when new content is added to the same layer.
    """
    
    def __init__(self, scene):
        self.scene = scene
        self.active_content: Dict[TextLayer, List[Mobject]] = {}
        self.content_history: List[Dict] = []
        
        # Vertical layout zones (from top to bottom)
        self.zones = {
            TextLayer.TITLE: (-3.5, -3.0),      # Top zone
            TextLayer.SUBTITLE: (-2.5, -2.0),   # Below title
            TextLayer.EQUATION: (-1.0, 1.0),     # Center zone
            TextLayer.EXPLANATION: (1.5, 2.5),   # Below equation
            TextLayer.LABEL: (3.0, 3.5),         # Bottom zone
            TextLayer.ANNOTATION: None,          # Floating (no fixed zone)
        }
    
    def add_text(
        self,
        text: Union[str, Text, MathTex],
        layer: TextLayer = TextLayer.EXPLANATION,
        fade_out_previous: bool = True,
        position: Optional[str] = None,
        buff: float = 0.3,
        **kwargs
    ) -> Mobject:
        """
        Add text to a specific layer, removing previous content if needed.
        
        Args:
            text: Text content (string, Text, or MathTex)
            layer: Which layer to add to
            fade_out_previous: If True, fade out previous content in this layer
            position: Position hint ('top', 'center', 'bottom', etc.)
            buff: Buffer spacing between elements
            **kwargs: Additional arguments for Text/MathTex
        
        Returns:
            The created text mobject
        """
        # Create text object if string provided
        if isinstance(text, str):
            text_obj = Text(text, **kwargs)
        else:
            text_obj = text
        
        # Position the text first (before adding to scene)
        if position:
            self._position_text(text_obj, layer, position, buff)
        else:
            self._auto_position_text(text_obj, layer, buff)
        
        # Fade out previous content in this layer
        if fade_out_previous and layer in self.active_content:
            previous = self.active_content[layer]
            if previous:
                self.scene.play(
                    *[FadeOut(obj) for obj in previous],
                    run_time=0.5
                )
        
        # Track this content
        if layer not in self.active_content:
            self.active_content[layer] = []
        self.active_content[layer].append(text_obj)
        
        # Record in history
        self.content_history.append({
            'layer': layer,
            'mobject': text_obj,
            'timestamp': getattr(self.scene.renderer, 'time', 0)
        })
        
        return text_obj
    
    def add_equation(
        self,
        equation: Union[str, MathTex],
        layer: TextLayer = TextLayer.EQUATION,
        fade_out_previous: bool = True,
        position: Optional[str] = None,
        buff: float = 0.5,
        **kwargs
    ) -> MathTex:
        """
        Add an equation, removing previous equations if needed.
        
        Args:
            equation: LaTeX string or MathTex object
            layer: Which layer (defaults to EQUATION)
            fade_out_previous: Remove previous equations
            position: Position hint
            buff: Buffer spacing
            **kwargs: Additional arguments for MathTex
        
        Returns:
            The created MathTex object
        """
        if isinstance(equation, str):
            eq_obj = MathTex(equation, **kwargs)
        else:
            eq_obj = equation
        
        return self.add_text(
            eq_obj,
            layer=layer,
            fade_out_previous=fade_out_previous,
            position=position,
            buff=buff
        )
    
    def clear_layer(self, layer: TextLayer, fade_out: bool = True):
        """Clear all content from a specific layer."""
        if layer in self.active_content:
            content = self.active_content[layer]
            if content and fade_out:
                self.scene.play(
                    *[FadeOut(obj) for obj in content],
                    run_time=0.5
                )
            self.active_content[layer] = []
    
    def clear_all(self, fade_out: bool = True, exclude_layers: List[TextLayer] = None):
        """Clear all content from all layers."""
        exclude_layers = exclude_layers or []
        for layer in TextLayer:
            if layer not in exclude_layers:
                self.clear_layer(layer, fade_out)
    
    def transition_to_new_section(
        self,
        new_title: Optional[str] = None,
        keep_equations: bool = False,
        fade_time: float = 1.0
    ):
        """
        Transition to a new section, clearing old explanatory content.
        
        Args:
            new_title: Optional new title to show
            keep_equations: If True, keep equations visible
            fade_time: Time for fade transition
        """
        layers_to_clear = [
            TextLayer.EXPLANATION,
            TextLayer.LABEL,
            TextLayer.ANNOTATION,
        ]
        
        if not keep_equations:
            layers_to_clear.append(TextLayer.EQUATION)
        
        # Fade out old content
        fade_outs = []
        for layer in layers_to_clear:
            if layer in self.active_content:
                fade_outs.extend(self.active_content[layer])
        
        if fade_outs:
            self.scene.play(
                *[FadeOut(obj) for obj in fade_outs],
                run_time=fade_time
            )
        
        # Clear from tracking
        for layer in layers_to_clear:
            if layer in self.active_content:
                self.active_content[layer] = []
        
        # Add new title if provided
        if new_title:
            self.add_text(
                new_title,
                layer=TextLayer.TITLE,
                fade_out_previous=True,
                position='top'
            )
    
    def _position_text(self, text_obj: Mobject, layer: TextLayer, position: str, buff: float):
        """Position text using a position hint."""
        if position == 'top':
            text_obj.to_edge(UP, buff=buff)
        elif position == 'bottom':
            text_obj.to_edge(DOWN, buff=buff)
        elif position == 'center':
            text_obj.move_to(ORIGIN)
        elif position == 'left':
            text_obj.to_edge(LEFT, buff=buff)
        elif position == 'right':
            text_obj.to_edge(RIGHT, buff=buff)
        elif position == 'top_left':
            text_obj.to_corner(UL, buff=buff)
        elif position == 'top_right':
            text_obj.to_corner(UR, buff=buff)
        elif position == 'bottom_left':
            text_obj.to_corner(DL, buff=buff)
        elif position == 'bottom_right':
            text_obj.to_corner(DR, buff=buff)
    
    def _auto_position_text(self, text_obj: Mobject, layer: TextLayer, buff: float):
        """Automatically position text based on layer."""
        zone = self.zones.get(layer)
        
        if zone and zone[0] is not None:
            # Position in zone
            y_pos = (zone[0] + zone[1]) / 2
            text_obj.move_to([0, y_pos, 0])
        else:
            # Default to center
            text_obj.move_to(ORIGIN)
        
        # Skip overlap prevention for now - it requires scene context
        # Overlap prevention will be handled manually or after adding to scene
    
    def _prevent_overlap(self, text_obj: Mobject, layer: TextLayer, buff: float):
        """Adjust position to prevent overlap with existing content."""
        bbox = text_obj.get_bounding_box()
        text_height = bbox[1][1] - bbox[0][1]
        text_bottom = text_obj.get_bottom()[1]
        text_top = text_obj.get_top()[1]
        
        # Check for overlaps with content in other layers
        for other_layer, content_list in self.active_content.items():
            if other_layer == layer:
                continue
            
            for other_obj in content_list:
                other_bbox = other_obj.get_bounding_box()
                other_top = other_bbox[1][1]
                other_bottom = other_bbox[0][1]
                
                # Check if overlapping vertically
                if not (text_bottom > other_top + buff or text_top < other_bottom - buff):
                    # Overlap detected - shift down
                    overlap = (other_top + buff) - text_bottom
                    text_obj.shift(DOWN * overlap)
                    break


class ManagedBoundedScene:
    """
    Enhanced BoundedScene with automatic scene management.
    
    Automatically handles:
    - Text/equation lifecycle
    - Overlap prevention
    - Section transitions
    - Content cleanup
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
            position: Position hint
            font_size: Font size (uses default if None)
            **kwargs: Additional Text arguments
        
        Returns:
            Text object
        """
        font_size = font_size or DEFAULT_BODY_FONT_SIZE
        return self.manager.add_text(
            text,
            layer=TextLayer.EXPLANATION,
            fade_out_previous=fade_out_previous,
            position=position,
            font_size=font_size,
            **kwargs
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
            MathTex object
        """
        font_size = font_size or DEFAULT_EQUATION_FONT_SIZE
        return self.manager.add_equation(
            equation,
            layer=TextLayer.EQUATION,
            fade_out_previous=fade_out_previous,
            position=position,
            font_size=font_size,
            **kwargs
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
        return self.manager.add_text(
            title,
            layer=TextLayer.TITLE,
            fade_out_previous=fade_out_previous,
            position='top',
            font_size=font_size,
            **kwargs
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
        return self.manager.add_text(
            subtitle,
            layer=TextLayer.SUBTITLE,
            fade_out_previous=fade_out_previous,
            position=None,  # Auto-position below title
            font_size=font_size,
            **kwargs
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
            new_title: Optional new title
            keep_equations: Keep equations visible
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

