"""
Updated Brownian Motion Scene using BoundedScene

This demonstrates how to use the BoundedScene base class to ensure
all content stays within frame boundaries.
"""

from manim import *
import numpy as np
import random
import sys
from pathlib import Path

# Add parent directory to path to import bounded_scene
sys.path.insert(0, str(Path(__file__).parent.parent))
from manim_utils.bounded_scene import BoundedScene, SAFE_WIDTH, SAFE_HEIGHT
from manim_utils.frame_config import (
    DEFAULT_TITLE_FONT_SIZE,
    DEFAULT_SUBTITLE_FONT_SIZE,
    DEFAULT_BODY_FONT_SIZE,
    DEFAULT_EQUATION_FONT_SIZE
)


class BrownianMotionBounded(BoundedScene):
    """
    2-minute animation demonstrating Brownian Motion and Einstein's Heat Equation.
    All content is automatically constrained within frame boundaries.
    """
    
    def construct(self):
        # Set background
        self.camera.background_color = "#001122"
        
        # Timeline breakdown for 120 seconds:
        self.intro_sequence()  # 0-15s
        self.microscopic_brownian_motion()  # 15-45s
        self.random_walk_analysis()  # 45-70s
        self.diffusion_equation()  # 70-95s
        self.einstein_relation()  # 95-115s
        self.conclusion()  # 115-120s
    
    def intro_sequence(self):
        """[0-15s] Title and introduction - all bounded."""
        # Use bounded_text to ensure title fits
        title = self.bounded_text(
            "Brownian Motion and Einstein's Heat Equation",
            font_size=DEFAULT_TITLE_FONT_SIZE,
            color=GOLD,
            weight=BOLD
        )
        self.safe_position(title, position='top')
        
        subtitle = self.bounded_text(
            "Connecting microscopic random motion to macroscopic diffusion",
            font_size=DEFAULT_SUBTITLE_FONT_SIZE,
            color=WHITE
        )
        subtitle.next_to(title, DOWN, buff=0.3)
        self.constrain_to_safe_area(subtitle)
        
        # Historical context
        context = self.bounded_text(
            "Einstein (1905): Random molecular collisions explain\n"
            "the erratic motion of pollen grains in water",
            font_size=DEFAULT_BODY_FONT_SIZE,
            color=BLUE,
            line_spacing=1.2
        )
        context.next_to(subtitle, DOWN, buff=0.5)
        self.constrain_to_safe_area(context)
        
        self.play(Write(title), run_time=2)
        self.play(FadeIn(subtitle, shift=UP), run_time=1.5)
        self.play(FadeIn(context, shift=UP), run_time=1.5)
        self.wait(2)
        
        # Transition
        self.play(
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(context),
            run_time=2
        )
        self.wait(1)
    
    def microscopic_brownian_motion(self):
        """[15-45s] Show microscopic view - constrained to safe area."""
        # Create water molecules within safe boundaries
        water_molecules = VGroup()
        num_molecules = 200
        for _ in range(num_molecules):
            x = random.uniform(SAFE_X_MIN, SAFE_X_MAX)
            y = random.uniform(SAFE_Y_MIN, SAFE_Y_MAX)
            molecule = Dot(
                point=[x, y, 0],
                radius=0.05,
                color=BLUE,
                fill_opacity=0.6
            )
            water_molecules.add(molecule)
        
        # Create pollen grains within safe boundaries
        pollen_grains = VGroup()
        num_pollen = 5
        for i in range(num_pollen):
            x = random.uniform(SAFE_X_MIN + 1, SAFE_X_MAX - 1)
            y = random.uniform(SAFE_Y_MIN + 0.5, SAFE_Y_MAX - 0.5)
            pollen = Circle(
                radius=0.3,
                color=GOLD,
                fill_opacity=0.8,
                stroke_width=2
            ).move_to([x, y, 0])
            pollen_grains.add(pollen)
        
        # Label - bounded
        label = self.bounded_text(
            "Microscopic View: Pollen grains in water",
            font_size=DEFAULT_SUBTITLE_FONT_SIZE,
            color=WHITE
        )
        self.safe_position(label, position='top')
        
        self.play(FadeIn(label), run_time=1)
        self.play(
            *[FadeIn(mol) for mol in water_molecules],
            run_time=2
        )
        self.play(
            *[FadeIn(pollen) for pollen in pollen_grains],
            run_time=1.5
        )
        self.wait(1)
        
        # Animate Brownian motion - keep within bounds
        pollen_trajectories = VGroup()
        pollen_colors = [RED, GREEN, YELLOW, PURPLE, ORANGE]
        
        for i, pollen in enumerate(pollen_grains):
            trail = TracedPath(
                pollen.get_center,
                stroke_color=pollen_colors[i % len(pollen_colors)],
                stroke_width=3,
                stroke_opacity=0.7
            )
            pollen_trajectories.add(trail)
        
        self.add(pollen_trajectories)
        
        # Animate motion with boundary checking
        for frame in range(20):
            for mol in water_molecules:
                dx = random.uniform(-0.3, 0.3)
                dy = random.uniform(-0.3, 0.3)
                new_pos = mol.get_center() + np.array([dx, dy, 0])
                new_pos[0] = np.clip(new_pos[0], SAFE_X_MIN, SAFE_X_MAX)
                new_pos[1] = np.clip(new_pos[1], SAFE_Y_MIN, SAFE_Y_MAX)
                mol.move_to(new_pos)
            
            for i, pollen in enumerate(pollen_grains):
                dx = random.uniform(-0.2, 0.2)
                dy = random.uniform(-0.2, 0.2)
                new_pos = pollen.get_center() + np.array([dx, dy, 0])
                new_pos[0] = np.clip(new_pos[0], SAFE_X_MIN + 0.5, SAFE_X_MAX - 0.5)
                new_pos[1] = np.clip(new_pos[1], SAFE_Y_MIN + 0.5, SAFE_Y_MAX - 0.5)
                pollen.move_to(new_pos)
            
            self.wait(0.1)
        
        self.wait(2)
        
        # Store for later
        self.water_molecules = water_molecules
        self.pollen_grains = pollen_grains
        self.pollen_trajectories = pollen_trajectories
        self.label = label
    
    def random_walk_analysis(self):
        """[45-70s] Random walk analysis - bounded axes and equations."""
        # Transition
        self.play(
            FadeOut(self.water_molecules),
            FadeOut(self.pollen_grains),
            FadeOut(self.pollen_trajectories),
            FadeOut(self.label),
            run_time=2
        )
        
        # Title - bounded
        title = self.bounded_text(
            "Random Walk Analysis",
            font_size=DEFAULT_TITLE_FONT_SIZE,
            color=GOLD
        )
        self.safe_position(title, position='top')
        self.play(Write(title), run_time=1)
        
        # Create safe axes
        axes = self.create_safe_axes(
            x_range=[0, 10, 1],
            y_range=[-3, 3, 1],
            width=SAFE_WIDTH * 0.7,  # Use 70% of safe width
            height=SAFE_HEIGHT * 0.5  # Use 50% of safe height
        )
        axes.shift(LEFT * 2 + DOWN * 0.5)
        self.constrain_to_safe_area(axes)
        
        x_label = axes.get_x_axis_label("Time", direction=DOWN)
        y_label = axes.get_y_axis_label("Position", direction=LEFT)
        
        self.play(Create(axes), run_time=1)
        self.play(FadeIn(x_label), FadeIn(y_label), run_time=0.5)
        
        # Simulate random walk trajectory
        num_steps = 50
        positions = [0]
        times = list(range(num_steps + 1))
        
        for i in range(num_steps):
            step = random.uniform(-0.3, 0.3)
            positions.append(positions[-1] + step)
        
        # Plot trajectory
        trajectory_points = [
            axes.coords_to_point(t, pos)
            for t, pos in zip(times, positions)
        ]
        
        trajectory = VMobject()
        trajectory.set_points_as_corners(trajectory_points)
        trajectory.set_stroke(color=YELLOW, width=3)
        
        self.play(Create(trajectory), run_time=3)
        self.wait(1)
        
        # MSD graph - bounded
        msd_title = self.bounded_text(
            "Mean Squared Displacement",
            font_size=DEFAULT_SUBTITLE_FONT_SIZE,
            color=WHITE
        )
        msd_title.next_to(axes, RIGHT, buff=0.5).shift(UP * 1.5)
        self.constrain_to_safe_area(msd_title)
        
        msd_axes = self.create_safe_axes(
            x_range=[0, 10, 2],
            y_range=[0, 2, 0.5],
            width=SAFE_WIDTH * 0.4,
            height=SAFE_HEIGHT * 0.4
        )
        msd_axes.next_to(msd_title, DOWN, buff=0.3)
        self.constrain_to_safe_area(msd_axes)
        
        msd_x_label = msd_axes.get_x_axis_label("t", direction=DOWN)
        msd_y_label = msd_axes.get_y_axis_label("MSD", direction=LEFT)
        
        self.play(
            Write(msd_title),
            Create(msd_axes),
            FadeIn(msd_x_label),
            FadeIn(msd_y_label),
            run_time=2
        )
        
        # Plot MSD = 2Dt
        D = 0.1
        msd_points = [
            msd_axes.coords_to_point(t, 2 * D * t)
            for t in np.linspace(0, 10, 50)
        ]
        
        msd_curve = VMobject()
        msd_curve.set_points_as_corners(msd_points)
        msd_curve.set_stroke(color=GREEN, width=4)
        
        self.play(Create(msd_curve), run_time=2)
        
        # Equation - bounded
        msd_eq = self.bounded_math_tex(
            r"\langle x^2(t) \rangle = 2Dt",
            font_size=DEFAULT_EQUATION_FONT_SIZE,
            color=GREEN
        )
        msd_eq.next_to(msd_axes, DOWN, buff=0.5)
        self.constrain_to_safe_area(msd_eq)
        
        self.play(Write(msd_eq), run_time=1.5)
        self.wait(2)
        
        # Store
        self.title_rw = title
        self.axes = axes
        self.trajectory = trajectory
        self.msd_axes = msd_axes
        self.msd_curve = msd_curve
        self.msd_eq = msd_eq
    
    def diffusion_equation(self):
        """[70-95s] Diffusion equation - bounded."""
        # Transition
        self.play(
            FadeOut(self.title_rw),
            FadeOut(self.axes),
            FadeOut(self.trajectory),
            FadeOut(self.msd_axes),
            FadeOut(self.msd_curve),
            FadeOut(self.msd_eq),
            run_time=2
        )
        
        # Title - bounded
        title = self.bounded_text(
            "The Diffusion Equation",
            font_size=DEFAULT_TITLE_FONT_SIZE,
            color=GOLD
        )
        self.safe_position(title, position='top')
        self.play(Write(title), run_time=1)
        
        # PDE - bounded
        diffusion_eq = self.bounded_math_tex(
            r"\frac{\partial P}{\partial t} = D \nabla^2 P",
            font_size=DEFAULT_EQUATION_FONT_SIZE,
            color=WHITE
        )
        diffusion_eq.shift(UP * 1)
        self.constrain_to_safe_area(diffusion_eq)
        
        self.play(Write(diffusion_eq), run_time=2)
        
        # Explanation - bounded
        explanation = VGroup(
            self.bounded_text("P(x,t): probability density", font_size=DEFAULT_BODY_FONT_SIZE, color=BLUE),
            self.bounded_text("D: diffusion coefficient", font_size=DEFAULT_BODY_FONT_SIZE, color=BLUE),
            self.bounded_text("∇²: Laplacian operator", font_size=DEFAULT_BODY_FONT_SIZE, color=BLUE)
        ).arrange(DOWN, buff=0.3).next_to(diffusion_eq, DOWN, buff=0.8)
        self.constrain_to_safe_area(explanation)
        
        self.play(*[FadeIn(exp) for exp in explanation], run_time=2)
        
        # Solution - bounded
        solution_title = self.bounded_text(
            "Solution: Gaussian spreading",
            font_size=DEFAULT_SUBTITLE_FONT_SIZE,
            color=YELLOW
        )
        solution_title.next_to(explanation, DOWN, buff=0.8)
        self.constrain_to_safe_area(solution_title)
        
        solution_eq = self.bounded_math_tex(
            r"P(x,t|x_0,0) = \frac{1}{\sqrt{4\pi D t}} \exp\left[-\frac{(x-x_0)^2}{4Dt}\right]",
            font_size=DEFAULT_EQUATION_FONT_SIZE - 4,  # Slightly smaller for long equation
            color=WHITE
        )
        solution_eq.next_to(solution_title, DOWN, buff=0.5)
        self.constrain_to_safe_area(solution_eq)
        
        self.play(Write(solution_title), run_time=1)
        self.play(Write(solution_eq), run_time=2)
        
        # Gaussian visualization - bounded
        gaussian_axes = self.create_safe_axes(
            x_range=[-3, 3, 1],
            y_range=[0, 1.5, 0.5],
            width=SAFE_WIDTH * 0.8,
            height=SAFE_HEIGHT * 0.4
        )
        gaussian_axes.next_to(solution_eq, DOWN, buff=0.8)
        self.constrain_to_safe_area(gaussian_axes)
        
        self.play(Create(gaussian_axes), run_time=1)
        
        # Animate Gaussian spreading
        gaussians = VGroup()
        times = [0.5, 1.0, 2.0, 4.0]
        colors = [RED, YELLOW, GREEN, BLUE]
        D = 0.5
        
        for t, color in zip(times, colors):
            x_vals = np.linspace(-3, 3, 100)
            y_vals = (1 / np.sqrt(4 * np.pi * D * t)) * np.exp(-(x_vals**2) / (4 * D * t))
            points = [
                gaussian_axes.coords_to_point(x, y)
                for x, y in zip(x_vals, y_vals)
            ]
            curve = VMobject()
            curve.set_points_as_corners(points)
            curve.set_stroke(color=color, width=3)
            gaussians.add(curve)
        
        self.play(*[Create(g) for g in gaussians], run_time=3)
        self.wait(2)
        
        # Store
        self.title_diff = title
        self.diffusion_eq = diffusion_eq
        self.explanation = explanation
        self.solution_title = solution_title
        self.solution_eq = solution_eq
        self.gaussian_axes = gaussian_axes
        self.gaussians = gaussians
    
    def einstein_relation(self):
        """[95-115s] Einstein's relation - bounded."""
        # Transition
        self.play(
            FadeOut(self.title_diff),
            FadeOut(self.diffusion_eq),
            FadeOut(self.explanation),
            FadeOut(self.solution_title),
            FadeOut(self.solution_eq),
            FadeOut(self.gaussian_axes),
            FadeOut(self.gaussians),
            run_time=2
        )
        
        # Title - bounded
        title = self.bounded_text(
            "Einstein's Relation",
            font_size=DEFAULT_TITLE_FONT_SIZE,
            color=GOLD
        )
        self.safe_position(title, position='top')
        self.play(Write(title), run_time=1)
        
        # Equation - bounded
        einstein_eq = self.bounded_math_tex(
            r"D = \frac{k_B T}{6\pi \eta a}",
            font_size=DEFAULT_EQUATION_FONT_SIZE,
            color=WHITE
        )
        einstein_eq.shift(UP * 1)
        self.constrain_to_safe_area(einstein_eq)
        
        self.play(Write(einstein_eq), run_time=2)
        
        # Definitions - bounded
        definitions = VGroup(
            self.bounded_math_tex(r"k_B: \text{Boltzmann constant}", font_size=DEFAULT_BODY_FONT_SIZE, color=BLUE),
            self.bounded_math_tex(r"T: \text{temperature}", font_size=DEFAULT_BODY_FONT_SIZE, color=BLUE),
            self.bounded_math_tex(r"\eta: \text{viscosity}", font_size=DEFAULT_BODY_FONT_SIZE, color=BLUE),
            self.bounded_math_tex(r"a: \text{particle radius}", font_size=DEFAULT_BODY_FONT_SIZE, color=BLUE)
        ).arrange(DOWN, buff=0.3).next_to(einstein_eq, DOWN, buff=0.8)
        self.constrain_to_safe_area(definitions)
        
        self.play(*[FadeIn(defn) for defn in definitions], run_time=2)
        
        # Connection - bounded
        connection_title = self.bounded_text(
            "Connection to Heat Equation",
            font_size=DEFAULT_SUBTITLE_FONT_SIZE,
            color=YELLOW
        )
        connection_title.next_to(definitions, DOWN, buff=0.8)
        self.constrain_to_safe_area(connection_title)
        
        heat_eq = self.bounded_math_tex(
            r"\frac{\partial u}{\partial t} = \alpha \nabla^2 u",
            font_size=DEFAULT_EQUATION_FONT_SIZE - 2,
            color=WHITE
        )
        heat_eq.next_to(connection_title, DOWN, buff=0.5)
        self.constrain_to_safe_area(heat_eq)
        
        connection_text = self.bounded_text(
            "Same mathematical structure!\n"
            "Probability density ↔ Temperature",
            font_size=DEFAULT_BODY_FONT_SIZE,
            color=GREEN,
            line_spacing=1.2
        )
        connection_text.next_to(heat_eq, DOWN, buff=0.5)
        self.constrain_to_safe_area(connection_text)
        
        self.play(Write(connection_title), run_time=1)
        self.play(Write(heat_eq), run_time=1.5)
        self.play(Write(connection_text), run_time=2)
        self.wait(2)
        
        # Store
        self.title_einstein = title
        self.einstein_eq = einstein_eq
        self.definitions = definitions
        self.connection_title = connection_title
        self.heat_eq = heat_eq
        self.connection_text = connection_text
    
    def conclusion(self):
        """[115-120s] Conclusion - bounded."""
        # Transition
        self.play(
            FadeOut(self.title_einstein),
            FadeOut(self.einstein_eq),
            FadeOut(self.definitions),
            FadeOut(self.connection_title),
            FadeOut(self.heat_eq),
            FadeOut(self.connection_text),
            run_time=2
        )
        
        # Final message - bounded
        conclusion = self.bounded_text(
            "Brownian motion connects\n"
            "microscopic randomness to\n"
            "macroscopic diffusion",
            font_size=DEFAULT_TITLE_FONT_SIZE,
            color=GOLD,
            line_spacing=1.3
        )
        self.safe_position(conclusion, position='center')
        
        self.play(Write(conclusion), run_time=2)
        self.wait(1)

