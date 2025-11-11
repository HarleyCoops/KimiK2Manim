"""
Brownian Motion 3D Scene - 2 Minute Animation

A comprehensive 3D visualization of Brownian Motion and its connection to 
Einstein's Heat Equation, using ThreeDScene for immersive 3D rendering.

Based on enriched JSON data from the KimiK2Manim pipeline.
"""

from manim import *
import numpy as np
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from manim_utils.frame_config import (
    DEFAULT_TITLE_FONT_SIZE,
    DEFAULT_SUBTITLE_FONT_SIZE,
    DEFAULT_BODY_FONT_SIZE,
    DEFAULT_EQUATION_FONT_SIZE
)


class BrownianMotion3D(ThreeDScene):
    """
    2-minute (120 second) 3D animation demonstrating Brownian Motion 
    and its connection to Einstein's Heat Equation.
    
    Timeline:
    [0-15s] Title and introduction
    [15-40s] 3D random walk trajectories
    [40-65s] Mean squared displacement and probability spreading
    [65-90s] Diffusion equation visualization
    [90-110s] Einstein's relation and connection to heat equation
    [110-120s] Conclusion
    """
    
    def construct(self):
        # Set background
        self.camera.background_color = "#001122"
        
        # Set initial camera orientation
        self.set_camera_orientation(phi=75 * DEGREES, theta=45 * DEGREES)
        
        # Timeline breakdown for 120 seconds
        self.intro_sequence()  # 0-15s
        self.random_walk_3d()  # 15-40s
        self.probability_spreading()  # 40-65s
        self.diffusion_equation_3d()  # 65-90s
        self.einstein_relation_3d()  # 90-110s
        self.conclusion_3d()  # 110-120s
    
    def intro_sequence(self):
        """[0-15s] Title and introduction."""
        title = Text(
            "Brownian Motion and Einstein's Heat Equation",
            font_size=42,
            color=GOLD,
            weight=BOLD
        )
        title.to_edge(UP, buff=0.5)
        
        subtitle = Text(
            "Connecting microscopic random motion to macroscopic diffusion",
            font_size=28,
            color=WHITE
        ).next_to(title, DOWN, buff=0.3)
        
        # Historical context
        context = Text(
            "Einstein (1905): Random molecular collisions explain\n"
            "the erratic motion of pollen grains in water",
            font_size=24,
            color=BLUE,
            line_spacing=1.2
        ).next_to(subtitle, DOWN, buff=0.5)
        
        self.play(Write(title), run_time=2)
        self.play(FadeIn(subtitle, shift=UP), run_time=1.5)
        self.play(FadeIn(context, shift=UP), run_time=1.5)
        self.wait(2)
        
        # Transition to 3D
        self.play(
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(context),
            run_time=2
        )
        self.wait(1)
    
    def random_walk_3d(self):
        """[15-40s] 3D random walk trajectories."""
        # Create 3D axes
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
            axis_config={"color": WHITE, "stroke_width": 2}
        )
        
        title = Text(
            "3D Random Walk: Brownian Motion",
            font_size=32,
            color=WHITE
        ).to_edge(UP, buff=0.3)
        
        self.play(Create(axes), Write(title), run_time=2)
        
        # Create multiple random walk trajectories
        num_walks = 8
        trajectories = VGroup()
        particles = VGroup()
        colors = [RED, YELLOW, GREEN, BLUE, PURPLE, ORANGE, PINK, TEAL]
        
        for i in range(num_walks):
            # Generate random walk path
            path = [ORIGIN]
            current_pos = np.array([0.0, 0.0, 0.0])
            
            for _ in range(100):
                # Random step in 3D
                step = np.array([
                    random.uniform(-0.15, 0.15),
                    random.uniform(-0.15, 0.15),
                    random.uniform(-0.15, 0.15)
                ])
                current_pos += step
                path.append(current_pos.copy())
            
            # Create trajectory line
            trajectory = VMobject()
            trajectory.set_points_as_corners([axes.c2p(*p) for p in path])
            trajectory.set_stroke(color=colors[i % len(colors)], width=3, opacity=0.8)
            trajectories.add(trajectory)
            
            # Create particle at end
            particle = Sphere(
                radius=0.15,
                color=colors[i % len(colors)],
                fill_opacity=0.9
            ).move_to(axes.c2p(*path[-1]))
            particles.add(particle)
        
        # Animate trajectories
        self.play(*[Create(traj) for traj in trajectories], run_time=5)
        self.play(*[FadeIn(particle) for particle in particles], run_time=2)
        
        # Rotate camera to show 3D nature
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(8)
        self.stop_ambient_camera_rotation()
        
        # Show equation
        eq = MathTex(
            r"\langle x(t) \rangle = 0",
            font_size=36,
            color=GOLD
        ).to_edge(DOWN, buff=0.5)
        
        self.play(Write(eq), run_time=2)
        self.wait(2)
        
        # Transition
        self.play(
            FadeOut(axes),
            FadeOut(trajectories),
            FadeOut(particles),
            FadeOut(title),
            FadeOut(eq),
            run_time=2
        )
        self.wait(1)
    
    def probability_spreading(self):
        """[40-65s] Mean squared displacement and probability spreading."""
        title = Text(
            "Probability Distribution Spreading",
            font_size=32,
            color=WHITE
        ).to_edge(UP, buff=0.3)
        
        self.play(Write(title), run_time=1)
        
        # Create 3D axes for probability visualization
        axes = ThreeDAxes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            z_range=[0, 2, 0.5],
            axis_config={"color": WHITE, "stroke_width": 2}
        )
        
        self.play(Create(axes), run_time=1)
        
        # Animate Gaussian spreading over time
        D = 0.5  # Diffusion coefficient
        times = [0.5, 1.0, 2.0, 4.0]
        colors_gaussian = [RED, YELLOW, GREEN, BLUE]
        gaussians = VGroup()
        
        for t, color in zip(times, colors_gaussian):
            # Create 3D Gaussian surface
            def gaussian_func(x, y):
                return (1 / (4 * np.pi * D * t)) * np.exp(-(x**2 + y**2) / (4 * D * t))
            
            surface = Surface(
                lambda u, v: axes.c2p(
                    u,
                    v,
                    gaussian_func(u, v)
                ),
                u_range=[-3, 3],
                v_range=[-3, 3],
                resolution=(20, 20),
                fill_opacity=0.7,
                fill_color=color,
                stroke_width=1,
                stroke_color=color
            )
            gaussians.add(surface)
        
        # Animate Gaussian spreading
        self.play(Create(gaussians[0]), run_time=2)
        self.begin_ambient_camera_rotation(rate=0.15)
        self.play(Transform(gaussians[0], gaussians[1]), run_time=2)
        self.play(Transform(gaussians[1], gaussians[2]), run_time=2)
        self.play(Transform(gaussians[2], gaussians[3]), run_time=2)
        self.stop_ambient_camera_rotation()
        self.wait(2)
        
        # Show MSD equation
        msd_eq = MathTex(
            r"\langle x^2(t) \rangle = 2Dt",
            font_size=36,
            color=GREEN
        ).to_edge(DOWN, buff=0.5)
        
        self.play(Write(msd_eq), run_time=2)
        self.wait(2)
        
        # Transition
        self.play(
            FadeOut(axes),
            FadeOut(gaussians),
            FadeOut(title),
            FadeOut(msd_eq),
            run_time=2
        )
        self.wait(1)
    
    def diffusion_equation_3d(self):
        """[65-90s] Diffusion equation visualization."""
        title = Text(
            "The Diffusion Equation",
            font_size=32,
            color=WHITE
        ).to_edge(UP, buff=0.3)
        
        self.play(Write(title), run_time=1)
        
        # Show diffusion equation
        diffusion_eq = MathTex(
            r"\frac{\partial P}{\partial t} = D \nabla^2 P",
            font_size=42,
            color=GOLD
        ).shift(UP * 1)
        
        self.play(Write(diffusion_eq), run_time=2)
        
        # Create 3D visualization of diffusion
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[0, 1.5, 0.3],
            axis_config={"color": WHITE, "stroke_width": 2}
        )
        
        # Animate diffusion process
        D = 0.5
        t_vals = np.linspace(0.1, 3.0, 30)
        
        def create_diffusion_surface(t):
            def func(x, y):
                return (1 / (4 * np.pi * D * t)) * np.exp(-(x**2 + y**2) / (4 * D * t))
            return Surface(
                lambda u, v: axes.c2p(u, v, func(u, v)),
                u_range=[-3, 3],
                v_range=[-3, 3],
                resolution=(15, 15),
                fill_opacity=0.6,
                fill_color=BLUE,
                stroke_width=1,
                stroke_color=BLUE
            )
        
        surface = create_diffusion_surface(t_vals[0])
        self.play(Create(axes), Create(surface), run_time=2)
        
        # Animate spreading
        self.begin_ambient_camera_rotation(rate=0.1)
        for i in range(1, len(t_vals), 3):
            new_surface = create_diffusion_surface(t_vals[i])
            self.play(Transform(surface, new_surface), run_time=0.5)
        self.stop_ambient_camera_rotation()
        self.wait(2)
        
        # Show solution equation
        solution_eq = MathTex(
            r"P(x,t) = \frac{1}{\sqrt{4\pi D t}} \exp\left[-\frac{x^2}{4Dt}\right]",
            font_size=36,
            color=BLUE
        ).to_edge(DOWN, buff=0.5)
        
        self.play(Write(solution_eq), run_time=2)
        self.wait(2)
        
        # Transition
        self.play(
            FadeOut(axes),
            FadeOut(surface),
            FadeOut(title),
            FadeOut(diffusion_eq),
            FadeOut(solution_eq),
            run_time=2
        )
        self.wait(1)
    
    def einstein_relation_3d(self):
        """[90-110s] Einstein's relation and connection to heat equation."""
        title = Text(
            "Einstein's Relation",
            font_size=32,
            color=WHITE
        ).to_edge(UP, buff=0.3)
        
        self.play(Write(title), run_time=1)
        
        # Show Einstein's relation
        einstein_eq = MathTex(
            r"D = \frac{k_B T}{6\pi\eta a}",
            font_size=42,
            color=GOLD
        ).shift(UP * 0.5)
        
        self.play(Write(einstein_eq), run_time=2)
        
        # Create 3D visualization: particle in fluid
        # Create fluid molecules (small spheres)
        fluid_molecules = VGroup()
        num_molecules = 50
        
        for _ in range(num_molecules):
            x = random.uniform(-2, 2)
            y = random.uniform(-2, 2)
            z = random.uniform(-2, 2)
            molecule = Sphere(
                radius=0.1,
                color=BLUE,
                fill_opacity=0.6
            ).move_to([x, y, z])
            fluid_molecules.add(molecule)
        
        # Create Brownian particle (larger sphere)
        brownian_particle = Sphere(
            radius=0.3,
            color=GOLD,
            fill_opacity=0.9
        ).move_to(ORIGIN)
        
        self.play(FadeIn(fluid_molecules), FadeIn(brownian_particle), run_time=2)
        
        # Animate molecular collisions
        self.begin_ambient_camera_rotation(rate=0.1)
        
        def update_molecules(mobj, dt):
            for molecule in mobj:
                # Random motion
                shift = np.array([
                    random.uniform(-0.05, 0.05),
                    random.uniform(-0.05, 0.05),
                    random.uniform(-0.05, 0.05)
                ])
                new_pos = molecule.get_center() + shift
                # Keep within bounds
                new_pos = np.clip(new_pos, -2.5, 2.5)
                molecule.move_to(new_pos)
        
        fluid_molecules.add_updater(update_molecules)
        self.add(fluid_molecules)
        self.wait(5)
        fluid_molecules.remove_updater(update_molecules)
        self.stop_ambient_camera_rotation()
        
        # Show connection to heat equation
        heat_eq = MathTex(
            r"\frac{\partial u}{\partial t} = \alpha \nabla^2 u",
            font_size=36,
            color=RED
        ).to_edge(DOWN, buff=0.5)
        
        self.play(Write(heat_eq), run_time=2)
        self.wait(2)
        
        # Transition
        self.play(
            FadeOut(fluid_molecules),
            FadeOut(brownian_particle),
            FadeOut(title),
            FadeOut(einstein_eq),
            FadeOut(heat_eq),
            run_time=2
        )
        self.wait(1)
    
    def conclusion_3d(self):
        """[110-120s] Conclusion."""
        conclusion = Text(
            "Conclusion: Unifying Randomness and Diffusion",
            font_size=36,
            color=GOLD,
            weight=BOLD
        )
        
        self.play(Write(conclusion), run_time=2)
        self.wait(3)
        self.play(FadeOut(conclusion), run_time=1)

