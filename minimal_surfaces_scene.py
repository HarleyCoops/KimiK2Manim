"""
Minimal Surfaces: Mathematical Soap Films in 3D Space

A comprehensive 3D visualization of minimal surfaces using Manim's ThreeDScene.
Shows catenoid, helicoid, Costa surface, and Enneper surface as translucent
3D objects with dynamic camera movements.

Based on enriched JSON data from the KimiK2Manim pipeline.
"""

from manim import *
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from manim_utils.frame_config import (
    DEFAULT_TITLE_FONT_SIZE,
    DEFAULT_SUBTITLE_FONT_SIZE,
    DEFAULT_BODY_FONT_SIZE,
    DEFAULT_EQUATION_FONT_SIZE
)


class MinimalSurfaces3D(ThreeDScene):
    """
    3D animation demonstrating minimal surfaces as mathematical soap films.
    
    Timeline:
    [0-10s] Introduction and title
    [10-30s] Catenoid surface
    [30-50s] Helicoid surface
    [50-70s] Costa surface
    [70-90s] Enneper surface
    [90-110s] All surfaces together with harmonic property
    [110-120s] Conclusion
    """
    
    def construct(self):
        # Set background
        self.camera.background_color = "#000011"
        
        # Set initial camera orientation
        self.set_camera_orientation(phi=75 * DEGREES, theta=45 * DEGREES)
        
        # Timeline breakdown
        self.intro_sequence()  # 0-10s
        self.catenoid_sequence()  # 10-30s
        self.helicoid_sequence()  # 30-50s
        self.costa_sequence()  # 50-70s
        self.enneper_sequence()  # 70-90s
        self.all_surfaces_sequence()  # 90-110s
        self.conclusion_sequence()  # 110-120s
    
    def intro_sequence(self):
        """[0-10s] Title and introduction."""
        title = Text(
            "Minimal Surfaces",
            font_size=48,
            color=GOLD,
            weight=BOLD
        )
        title.to_edge(UP, buff=0.5)
        
        subtitle = Text(
            "Mathematical Soap Films in 3D Space",
            font_size=32,
            color=WHITE
        ).next_to(title, DOWN, buff=0.3)
        
        # Mathematical context
        context = Text(
            "Surfaces where mean curvature H = 0",
            font_size=28,
            color=BLUE,
            line_spacing=1.2
        ).next_to(subtitle, DOWN, buff=0.5)
        
        eq = MathTex(
            r"H = \frac{1}{2}(\kappa_1 + \kappa_2) = 0",
            font_size=36,
            color=GOLD
        ).next_to(context, DOWN, buff=0.5)
        
        self.play(Write(title), run_time=2)
        self.play(FadeIn(subtitle, shift=UP), run_time=1.5)
        self.play(FadeIn(context, shift=UP), run_time=1.5)
        self.play(Write(eq), run_time=2)
        self.wait(2)
        
        # Transition to 3D
        self.play(
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(context),
            FadeOut(eq),
            run_time=2
        )
        self.wait(1)
    
    def catenoid_sequence(self):
        """[10-30s] Catenoid surface visualization."""
        title = Text(
            "Catenoid: The Classic Minimal Surface",
            font_size=32,
            color=WHITE
        ).to_edge(UP, buff=0.3)
        
        self.play(Write(title), run_time=1)
        
        # Create 3D axes
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-2, 2, 1],
            axis_config={"color": WHITE, "stroke_width": 1}
        )
        
        self.play(Create(axes), run_time=1)
        
        # Catenoid parameterization: X(u,v) = (a cosh(v) cos(u), a cosh(v) sin(u), a v)
        a = 1.0
        u_range = [0, 2 * PI, 0.2]
        v_range = [-1.5, 1.5, 0.15]
        
        def catenoid_func(u, v):
            x = a * np.cosh(v) * np.cos(u)
            y = a * np.cosh(v) * np.sin(u)
            z = a * v
            return np.array([x, y, z])
        
        # Create catenoid surface
        catenoid = Surface(
            lambda u, v: catenoid_func(u, v),
            u_range=[0, 2 * PI],
            v_range=[-1.5, 1.5],
            resolution=(30, 20),
            fill_opacity=0.6,
            fill_color=interpolate_color(BLUE, WHITE, 0.3),
            stroke_width=1,
            stroke_color=BLUE,
            checkerboard_colors=[BLUE_E, BLUE_D],
            stroke_opacity=0.5
        )
        
        self.play(Create(catenoid), run_time=3)
        
        # Show parameterization equation
        param_eq = MathTex(
            r"X(u,v) = \left(a \cosh v \cos u, \; a \cosh v \sin u, \; a v\right)",
            font_size=28,
            color=GOLD
        ).to_edge(DOWN, buff=0.5)
        
        self.play(Write(param_eq), run_time=2)
        
        # Orbital camera movement
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(8)
        self.stop_ambient_camera_rotation()
        
        # Transition
        self.play(
            FadeOut(axes),
            FadeOut(catenoid),
            FadeOut(title),
            FadeOut(param_eq),
            run_time=2
        )
        self.wait(1)
    
    def helicoid_sequence(self):
        """[30-50s] Helicoid surface visualization."""
        title = Text(
            "Helicoid: The Spiral Minimal Surface",
            font_size=32,
            color=WHITE
        ).to_edge(UP, buff=0.3)
        
        self.play(Write(title), run_time=1)
        
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-2, 2, 1],
            axis_config={"color": WHITE, "stroke_width": 1}
        )
        
        self.play(Create(axes), run_time=1)
        
        # Helicoid parameterization: X(u,v) = (u cos(v), u sin(v), v)
        def helicoid_func(u, v):
            x = u * np.cos(v)
            y = u * np.sin(v)
            z = v / PI  # Scale to fit
            return np.array([x, y, z])
        
        helicoid = Surface(
            lambda u, v: helicoid_func(u, v),
            u_range=[-2, 2],
            v_range=[-2 * PI, 2 * PI],
            resolution=(20, 40),
            fill_opacity=0.6,
            fill_color=interpolate_color(GREEN, WHITE, 0.3),
            stroke_width=1,
            stroke_color=GREEN,
            checkerboard_colors=[GREEN_E, GREEN_D],
            stroke_opacity=0.5
        )
        
        self.play(Create(helicoid), run_time=3)
        
        # Rotate camera while helicoid rotates
        self.begin_ambient_camera_rotation(rate=0.15)
        self.play(Rotate(helicoid, PI, axis=UP), run_time=5)
        self.stop_ambient_camera_rotation()
        self.wait(3)
        
        # Transition
        self.play(
            FadeOut(axes),
            FadeOut(helicoid),
            FadeOut(title),
            run_time=2
        )
        self.wait(1)
    
    def costa_sequence(self):
        """[50-70s] Costa surface visualization."""
        title = Text(
            "Costa Surface: Three-Ended Minimal Surface",
            font_size=32,
            color=WHITE
        ).to_edge(UP, buff=0.3)
        
        self.play(Write(title), run_time=1)
        
        axes = ThreeDAxes(
            x_range=[-2, 2, 0.5],
            y_range=[-2, 2, 0.5],
            z_range=[-1, 1, 0.5],
            axis_config={"color": WHITE, "stroke_width": 1}
        )
        
        self.play(Create(axes), run_time=1)
        
        # Costa surface approximation (simplified)
        # Full Costa surface is complex, so we use an approximation
        def costa_func(u, v):
            # Simplified Costa-like surface
            r = np.sqrt(u**2 + v**2)
            x = u * (1 + 0.3 * np.cos(3 * np.arctan2(v, u)))
            y = v * (1 + 0.3 * np.cos(3 * np.arctan2(v, u)))
            z = 0.3 * np.sin(3 * np.arctan2(v, u)) * np.exp(-r**2)
            return np.array([x, y, z])
        
        costa = Surface(
            lambda u, v: costa_func(u, v),
            u_range=[-1.5, 1.5],
            v_range=[-1.5, 1.5],
            resolution=(25, 25),
            fill_opacity=0.7,
            fill_color=interpolate_color(PURPLE, WHITE, 0.3),
            stroke_width=1,
            stroke_color=PURPLE,
            checkerboard_colors=[PURPLE_E, PURPLE_D],
            stroke_opacity=0.5
        )
        
        self.play(Create(costa), run_time=3)
        
        # Show three-fold symmetry
        self.begin_ambient_camera_rotation(rate=0.12)
        self.wait(8)
        self.stop_ambient_camera_rotation()
        
        # Transition
        self.play(
            FadeOut(axes),
            FadeOut(costa),
            FadeOut(title),
            run_time=2
        )
        self.wait(1)
    
    def enneper_sequence(self):
        """[70-90s] Enneper surface visualization."""
        title = Text(
            "Enneper Surface: Self-Intersecting Minimal Surface",
            font_size=32,
            color=WHITE
        ).to_edge(UP, buff=0.3)
        
        self.play(Write(title), run_time=1)
        
        axes = ThreeDAxes(
            x_range=[-2, 2, 0.5],
            y_range=[-2, 2, 0.5],
            z_range=[-2, 2, 0.5],
            axis_config={"color": WHITE, "stroke_width": 1}
        )
        
        self.play(Create(axes), run_time=1)
        
        # Enneper surface: X(u,v) = (u - u³/3 + uv², v - v³/3 + vu², u² - v²)
        def enneper_func(u, v):
            x = u - u**3 / 3 + u * v**2
            y = v - v**3 / 3 + v * u**2
            z = u**2 - v**2
            return np.array([x, y, z])
        
        enneper = Surface(
            lambda u, v: enneper_func(u, v),
            u_range=[-1.5, 1.5],
            v_range=[-1.5, 1.5],
            resolution=(30, 30),
            fill_opacity=0.6,
            fill_color=interpolate_color(RED, WHITE, 0.3),
            stroke_width=1,
            stroke_color=RED,
            checkerboard_colors=[RED_E, RED_D],
            stroke_opacity=0.5
        )
        
        self.play(Create(enneper), run_time=3)
        
        # Show parameterization equation
        param_eq = MathTex(
            r"X(u,v) = \left(u - \frac{u^3}{3} + u v^2, \; v - \frac{v^3}{3} + v u^2, \; u^2 - v^2\right)",
            font_size=24,
            color=GOLD
        ).to_edge(DOWN, buff=0.5)
        
        self.play(Write(param_eq), run_time=2)
        
        # Camera movement to reveal self-intersections
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(8)
        self.stop_ambient_camera_rotation()
        
        # Transition
        self.play(
            FadeOut(axes),
            FadeOut(enneper),
            FadeOut(title),
            FadeOut(param_eq),
            run_time=2
        )
        self.wait(1)
    
    def all_surfaces_sequence(self):
        """[90-110s] All surfaces together showing harmonic property."""
        title = Text(
            "Harmonic Property: Δ_Σ X = 0",
            font_size=32,
            color=WHITE
        ).to_edge(UP, buff=0.3)
        
        self.play(Write(title), run_time=1)
        
        # Create all four surfaces arranged in space
        surfaces_group = VGroup()
        
        # Catenoid (simplified for group view)
        def catenoid_func(u, v):
            a = 0.8
            x = a * np.cosh(v) * np.cos(u) - 2
            y = a * np.cosh(v) * np.sin(u)
            z = a * v
            return np.array([x, y, z])
        
        catenoid = Surface(
            lambda u, v: catenoid_func(u, v),
            u_range=[0, 2 * PI],
            v_range=[-1, 1],
            resolution=(15, 10),
            fill_opacity=0.5,
            fill_color=BLUE,
            stroke_width=0.5,
            stroke_color=BLUE
        )
        
        # Helicoid
        def helicoid_func(u, v):
            x = u * np.cos(v) + 2
            y = u * np.sin(v)
            z = v / PI
            return np.array([x, y, z])
        
        helicoid = Surface(
            lambda u, v: helicoid_func(u, v),
            u_range=[-1, 1],
            v_range=[-PI, PI],
            resolution=(10, 20),
            fill_opacity=0.5,
            fill_color=GREEN,
            stroke_width=0.5,
            stroke_color=GREEN
        )
        
        # Costa (simplified)
        def costa_func(u, v):
            r = np.sqrt(u**2 + v**2)
            x = u * (1 + 0.2 * np.cos(3 * np.arctan2(v, u)))
            y = v * (1 + 0.2 * np.cos(3 * np.arctan2(v, u))) - 2
            z = 0.2 * np.sin(3 * np.arctan2(v, u)) * np.exp(-r**2)
            return np.array([x, y, z])
        
        costa = Surface(
            lambda u, v: costa_func(u, v),
            u_range=[-1, 1],
            v_range=[-1, 1],
            resolution=(12, 12),
            fill_opacity=0.5,
            fill_color=PURPLE,
            stroke_width=0.5,
            stroke_color=PURPLE
        )
        
        # Enneper
        def enneper_func(u, v):
            x = u - u**3 / 3 + u * v**2 + 2
            y = v - v**3 / 3 + v * u**2
            z = u**2 - v**2
            return np.array([x, y, z])
        
        enneper = Surface(
            lambda u, v: enneper_func(u, v),
            u_range=[-1, 1],
            v_range=[-1, 1],
            resolution=(15, 15),
            fill_opacity=0.5,
            fill_color=RED,
            stroke_width=0.5,
            stroke_color=RED
        )
        
        surfaces_group.add(catenoid, helicoid, costa, enneper)
        
        self.play(*[Create(surf) for surf in surfaces_group], run_time=4)
        
        # Show harmonic equation
        harmonic_eq = MathTex(
            r"\Delta_{\Sigma} X = 0",
            font_size=36,
            color=GOLD
        ).to_edge(DOWN, buff=0.5)
        
        self.play(Write(harmonic_eq), run_time=2)
        
        # Grand orbital movement
        self.begin_ambient_camera_rotation(rate=0.08)
        self.wait(10)
        self.stop_ambient_camera_rotation()
        
        # Transition
        self.play(
            FadeOut(surfaces_group),
            FadeOut(title),
            FadeOut(harmonic_eq),
            run_time=2
        )
        self.wait(1)
    
    def conclusion_sequence(self):
        """[110-120s] Conclusion."""
        conclusion = Text(
            "Minimal Surfaces: Where Mathematics Meets Nature",
            font_size=36,
            color=GOLD,
            weight=BOLD
        )
        
        self.play(Write(conclusion), run_time=2)
        self.wait(5)
        self.play(FadeOut(conclusion), run_time=1)

