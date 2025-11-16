"""
Torus Eigenfunctions: Standing Wave Modes Animation

A 3D visualization of a torus cycling through its eigenfunctions - the surface's
pure standing-wave modes. Each eigenfunction is indexed by two counts: how many
oscillations wrap the small tube (n) and how many wrap the big ring (m).

Dark regions are nodes (no motion) and bright bands are antinodes.
As the counts rise, nodes crowd together, ridges sharpen, creating a pine-cone look.

Animation duration: 60 seconds
"""

from manim import *
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from manim_utils.frame_config import (
    DEFAULT_TITLE_FONT_SIZE,
    DEFAULT_SUBTITLE_FONT_SIZE,
    DEFAULT_BODY_FONT_SIZE,
    DEFAULT_EQUATION_FONT_SIZE
)


class TorusEigenfunctions(ThreeDScene):
    """
    3D animation demonstrating torus eigenfunctions as standing wave modes.
    
    Timeline:
    [0-5s] Introduction and title
    [5-15s] Mode (1,1) - Simple fundamental mode
    [15-25s] Mode (2,1) - Two oscillations around large circle
    [25-35s] Mode (1,2) - Two oscillations around small circle
    [35-45s] Mode (3,2) - Higher frequency mode
    [45-55s] Mode (4,3) - Pine-cone appearance
    [55-60s] Conclusion
    """
    
    def construct(self):
        # Set background
        self.camera.background_color = "#000000"
        
        # Set initial camera orientation
        self.set_camera_orientation(phi=75 * DEGREES, theta=45 * DEGREES)
        
        # Timeline breakdown
        self.intro_sequence()  # 0-5s
        self.mode_sequence(1, 1, "Fundamental Mode", BLUE)  # 5-15s
        self.mode_sequence(2, 1, "Mode (2,1): Two Large Oscillations", GREEN)  # 15-25s
        self.mode_sequence(1, 2, "Mode (1,2): Two Small Oscillations", YELLOW)  # 25-35s
        self.mode_sequence(3, 2, "Mode (3,2): Higher Frequency", ORANGE)  # 35-45s
        self.mode_sequence(4, 3, "Mode (4,3): Pine-Cone Pattern", RED)  # 45-55s
        self.conclusion_sequence()  # 55-60s
    
    def intro_sequence(self):
        """[0-5s] Brief title and introduction."""
        title = Text(
            "Torus Eigenfunctions",
            font_size=48,
            color=GOLD,
            weight=BOLD
        )
        title.to_edge(UP, buff=0.5)
        
        subtitle = Text(
            "Standing Wave Modes on a Torus",
            font_size=32,
            color=WHITE
        ).next_to(title, DOWN, buff=0.3)
        
        # Mathematical context
        context = Text(
            "Eigenfunctions of the Laplacian",
            font_size=28,
            color=BLUE,
            line_spacing=1.2
        ).next_to(subtitle, DOWN, buff=0.5)
        
        eq = MathTex(
            r"\Delta \psi_{m,n} = \lambda_{m,n} \psi_{m,n}",
            font_size=36,
            color=GOLD
        ).next_to(context, DOWN, buff=0.5)
        
        self.play(Write(title), run_time=1)
        self.play(FadeIn(subtitle, shift=UP), run_time=0.8)
        self.play(FadeIn(context, shift=UP), run_time=0.8)
        self.play(Write(eq), run_time=1)
        self.wait(1.4)
        
        # Transition to 3D
        self.play(
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(context),
            FadeOut(eq),
            run_time=1
        )
        self.wait(0.5)
    
    def torus_eigenfunction(self, u, v, m, n, R=2.0, r=1.0, amplitude=0.5):
        """
        Create torus surface with eigenfunction modulation.
        
        Parameters:
        - u: angle around large circle [0, 2π]
        - v: angle around small circle [0, 2π]
        - m: number of oscillations around large circle
        - n: number of oscillations around small circle
        - R: major radius of torus
        - r: minor radius of torus
        - amplitude: strength of eigenfunction modulation
        
        The eigenfunction creates standing wave patterns:
        - Nodes (dark): where cos(m*u) * cos(n*v) = 0
        - Antinodes (bright): where |cos(m*u) * cos(n*v)| is maximum
        """
        # Eigenfunction: cos(m*u) * cos(n*v)
        # This creates standing wave patterns with m oscillations around
        # the large circle and n oscillations around the small circle
        eigen = amplitude * np.cos(m * u) * np.cos(n * v)
        
        # Apply eigenfunction as radial modulation
        # Positive values (antinodes) expand outward
        # Negative values (nodes) contract inward
        r_modulated = r + eigen
        
        # Standard torus parameterization with modulated radius
        x = (R + r_modulated * np.cos(v)) * np.cos(u)
        y = (R + r_modulated * np.cos(v)) * np.sin(u)
        z = r_modulated * np.sin(v)
        
        return np.array([x, y, z])
    
    def get_color_from_eigenfunction(self, u, v, m, n):
        """
        Map eigenfunction value to color.
        Positive values (antinodes) -> warm colors (orange/yellow)
        Negative values (nodes) -> cool colors (blue/purple)
        """
        eigen_value = np.cos(m * u) * np.cos(n * v)
        # Normalize to [0, 1]
        normalized = (eigen_value + 1) / 2
        
        # Interpolate between blue (nodes) and orange (antinodes)
        if normalized < 0.5:
            # Cool colors for nodes
            t = normalized * 2
            return interpolate_color(BLUE, PURPLE, t)
        else:
            # Warm colors for antinodes
            t = (normalized - 0.5) * 2
            return interpolate_color(PURPLE, ORANGE, t)
    
    def mode_sequence(self, m, n, mode_name, base_color):
        """
        Display a specific eigenfunction mode.
        
        Parameters:
        - m: oscillations around large circle
        - n: oscillations around small circle
        - mode_name: text description
        - base_color: base color for the mode
        """
        # Title showing mode indices
        title = Text(
            mode_name,
            font_size=32,
            color=WHITE
        ).to_edge(UP, buff=0.3)
        
        mode_label = MathTex(
            f"\\psi_{{{m},{n}}}",
            font_size=36,
            color=GOLD
        ).next_to(title, DOWN, buff=0.2)
        
        self.play(Write(title), Write(mode_label), run_time=0.6)
        
        # Create 3D axes
        axes = ThreeDAxes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            z_range=[-3, 3, 1],
            axis_config={"color": GRAY, "stroke_width": 0.5}
        )
        
        self.play(Create(axes), run_time=0.4)
        
        # Determine resolution based on mode complexity
        # Higher modes need more resolution to show detail
        resolution = (max(40, m * 15), max(40, n * 15))
        
        # Create torus with eigenfunction
        def surface_func(u, v):
            return self.torus_eigenfunction(u, v, m, n)
        
        # Create surface with enhanced visualization
        # Use checkerboard pattern to help visualize the eigenfunction structure
        # The pattern will highlight nodes and antinodes
        torus_surface = Surface(
            surface_func,
            u_range=[0, 2 * PI],
            v_range=[0, 2 * PI],
            resolution=resolution,
            fill_opacity=0.9,
            fill_color=base_color,
            stroke_width=0.4,
            stroke_color=WHITE,
            stroke_opacity=0.4,
            # Use checkerboard to create visual contrast
            checkerboard_colors=[interpolate_color(BLUE, base_color, 0.3), 
                               interpolate_color(ORANGE, base_color, 0.3)]
        )
        
        self.play(Create(torus_surface), run_time=1.5)
        
        # Show mode indices
        indices_text = MathTex(
            f"m = {m} \\text{{ (large circle)}}, \\quad n = {n} \\text{{ (small circle)}}",
            font_size=24,
            color=WHITE
        ).to_edge(DOWN, buff=0.5)
        
        self.play(Write(indices_text), run_time=0.5)
        
        # Orbital camera movement to show 3D structure
        self.begin_ambient_camera_rotation(rate=0.12)
        self.wait(4.5)
        self.stop_ambient_camera_rotation()
        
        # Transition
        self.play(
            FadeOut(axes),
            FadeOut(torus_surface),
            FadeOut(title),
            FadeOut(mode_label),
            FadeOut(indices_text),
            run_time=1
        )
        self.wait(0.5)
    
    def conclusion_sequence(self):
        """[55-60s] Conclusion."""
        conclusion = Text(
            "Eigenfunctions reveal the natural",
            font_size=32,
            color=WHITE
        )
        
        conclusion2 = Text(
            "vibrational modes of the torus",
            font_size=32,
            color=WHITE
        ).next_to(conclusion, DOWN, buff=0.3)
        
        eq = MathTex(
            r"\Delta \psi = \lambda \psi",
            font_size=40,
            color=GOLD
        ).next_to(conclusion2, DOWN, buff=0.5)
        
        self.play(Write(conclusion), run_time=1)
        self.play(Write(conclusion2), run_time=1)
        self.play(Write(eq), run_time=1)
        self.wait(2)


if __name__ == "__main__":
    # Render with: python -m manim -pql torus/torus_eigenfunctions.py TorusEigenfunctions
    pass

