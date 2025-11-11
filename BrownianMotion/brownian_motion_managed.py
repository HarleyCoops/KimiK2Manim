"""
Example: Brownian Motion Scene with Scene Management

Demonstrates how to use ManagedBoundedScene to prevent text/equation overlaps
and automatically manage content lifecycle.
"""

from manim import *
import numpy as np
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from manim_utils.managed_scene import ManagedBoundedScene


class BrownianMotionManaged(ManagedBoundedScene):
    """
    2-minute animation with automatic scene management.
    Text and equations are automatically managed to prevent overlaps.
    """
    
    def construct(self):
        self.camera.background_color = "#001122"
        
        self.intro_sequence()  # 0-15s
        self.microscopic_brownian_motion()  # 15-45s
        self.random_walk_analysis()  # 45-70s
        self.diffusion_equation()  # 70-95s
        self.einstein_relation()  # 95-115s
        self.conclusion()  # 115-120s
    
    def intro_sequence(self):
        """[0-15s] Title and introduction."""
        # Title automatically replaces any previous titles
        title = self.add_title(
            "Brownian Motion and Einstein's Heat Equation",
            color=GOLD
        )
        self.play(Write(title), run_time=2)
        
        # Subtitle automatically positioned below title
        subtitle = self.add_subtitle(
            "Connecting microscopic random motion to macroscopic diffusion",
            color=WHITE
        )
        self.play(FadeIn(subtitle, shift=UP), run_time=1.5)
        
        # Explanation automatically replaces previous explanations
        context = self.add_explanation(
            "Einstein (1905): Random molecular collisions explain\n"
            "the erratic motion of pollen grains in water",
            color=BLUE,
            position='center'
        )
        self.play(FadeIn(context, shift=UP), run_time=1.5)
        self.wait(2)
        
        # Transition clears all explanatory text
        self.transition_section(fade_time=2)
        self.wait(1)
    
    def microscopic_brownian_motion(self):
        """[15-45s] Microscopic view."""
        # New section title (automatically clears old explanations)
        title = self.add_title(
            "Microscopic View: Pollen grains in water",
            color=GOLD
        )
        self.play(Write(title), run_time=1)
        
        # Create particles (same as before)
        water_molecules = VGroup()
        num_molecules = 200
        for _ in range(num_molecules):
            x = random.uniform(-6, 6)
            y = random.uniform(-3, 3)
            molecule = Dot(
                point=[x, y, 0],
                radius=0.05,
                color=BLUE,
                fill_opacity=0.6
            )
            water_molecules.add(molecule)
        
        pollen_grains = VGroup()
        num_pollen = 5
        for i in range(num_pollen):
            x = random.uniform(-4, 4)
            y = random.uniform(-2, 2)
            pollen = Circle(
                radius=0.3,
                color=GOLD,
                fill_opacity=0.8,
                stroke_width=2
            ).move_to([x, y, 0])
            pollen_grains.add(pollen)
        
        self.play(
            *[FadeIn(mol) for mol in water_molecules],
            run_time=2
        )
        self.play(
            *[FadeIn(pollen) for pollen in pollen_grains],
            run_time=1.5
        )
        
        # Add explanation (automatically positioned, no overlap)
        explanation = self.add_explanation(
            "Water molecules collide randomly with pollen grains,\n"
            "causing erratic Brownian motion",
            color=WHITE,
            position='bottom'
        )
        self.play(FadeIn(explanation), run_time=1)
        
        # Animate motion
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
        
        for frame in range(20):
            for mol in water_molecules:
                dx = random.uniform(-0.3, 0.3)
                dy = random.uniform(-0.3, 0.3)
                new_pos = mol.get_center() + np.array([dx, dy, 0])
                new_pos[0] = np.clip(new_pos[0], -6, 6)
                new_pos[1] = np.clip(new_pos[1], -3, 3)
                mol.move_to(new_pos)
            
            for i, pollen in enumerate(pollen_grains):
                dx = random.uniform(-0.2, 0.2)
                dy = random.uniform(-0.2, 0.2)
                new_pos = pollen.get_center() + np.array([dx, dy, 0])
                new_pos[0] = np.clip(new_pos[0], -5, 5)
                new_pos[1] = np.clip(new_pos[1], -2.5, 2.5)
                pollen.move_to(new_pos)
            
            self.wait(0.1)
        
        self.wait(2)
        
        # Store
        self.water_molecules = water_molecules
        self.pollen_grains = pollen_grains
        self.pollen_trajectories = pollen_trajectories
    
    def random_walk_analysis(self):
        """[45-70s] Random walk analysis."""
        # Transition clears old explanations, keeps title if desired
        self.transition_section(
            new_title="Random Walk Analysis",
            keep_equations=False,
            fade_time=2
        )
        
        # Create axes
        axes = self.create_safe_axes(
            x_range=[0, 10, 1],
            y_range=[-3, 3, 1],
            width=6,
            height=4
        )
        axes.shift(LEFT * 2 + DOWN * 0.5)
        
        x_label = axes.get_x_axis_label("Time", direction=DOWN)
        y_label = axes.get_y_axis_label("Position", direction=LEFT)
        
        self.play(Create(axes), run_time=1)
        self.play(FadeIn(x_label), FadeIn(y_label), run_time=0.5)
        
        # Simulate trajectory
        num_steps = 50
        positions = [0]
        times = list(range(num_steps + 1))
        
        for i in range(num_steps):
            step = random.uniform(-0.3, 0.3)
            positions.append(positions[-1] + step)
        
        trajectory_points = [
            axes.coords_to_point(t, pos)
            for t, pos in zip(times, positions)
        ]
        
        trajectory = VMobject()
        trajectory.set_points_as_corners(trajectory_points)
        trajectory.set_stroke(color=YELLOW, width=3)
        
        self.play(Create(trajectory), run_time=3)
        
        # Add explanation (automatically positioned, no overlap with title)
        explanation = self.add_explanation(
            "Random walk trajectory shows unpredictable motion",
            color=WHITE,
            position='bottom'
        )
        self.play(FadeIn(explanation), run_time=1)
        self.wait(1)
        
        # Add equation (automatically replaces previous equations)
        msd_eq = self.add_equation(
            r"\langle x^2(t) \rangle = 2Dt",
            color=GREEN,
            position='center'
        )
        self.play(Write(msd_eq), run_time=1.5)
        
        # Add explanation for equation (positioned below equation)
        eq_explanation = self.add_explanation(
            "Mean squared displacement grows linearly with time",
            color=GREEN,
            position='bottom'
        )
        self.play(FadeIn(eq_explanation), run_time=1)
        self.wait(2)
        
        # Store
        self.axes = axes
        self.trajectory = trajectory
        self.msd_eq = msd_eq
    
    def diffusion_equation(self):
        """[70-95s] Diffusion equation."""
        # Transition clears old explanations
        self.transition_section(
            new_title="The Diffusion Equation",
            keep_equations=False,
            fade_time=2
        )
        
        # Add main equation
        diffusion_eq = self.add_equation(
            r"\frac{\partial P}{\partial t} = D \nabla^2 P",
            color=WHITE,
            position='center'
        )
        self.play(Write(diffusion_eq), run_time=2)
        
        # Add explanation (automatically positioned below equation)
        explanation = self.add_explanation(
            "P(x,t): probability density\n"
            "D: diffusion coefficient\n"
            "∇²: Laplacian operator",
            color=BLUE,
            position='bottom'
        )
        self.play(FadeIn(explanation), run_time=2)
        self.wait(2)
        
        # Add solution equation (replaces previous equation)
        solution_eq = self.add_equation(
            r"P(x,t|x_0,0) = \frac{1}{\sqrt{4\pi D t}} \exp\left[-\frac{(x-x_0)^2}{4Dt}\right]",
            color=YELLOW,
            position='center'
        )
        self.play(Write(solution_eq), run_time=2)
        
        # Update explanation (replaces previous explanation)
        solution_explanation = self.add_explanation(
            "Solution: Gaussian probability distribution spreading over time",
            color=YELLOW,
            position='bottom'
        )
        self.play(FadeIn(solution_explanation), run_time=1)
        self.wait(2)
        
        # Store
        self.diffusion_eq = diffusion_eq
        self.solution_eq = solution_eq
    
    def einstein_relation(self):
        """[95-115s] Einstein's relation."""
        # Transition
        self.transition_section(
            new_title="Einstein's Relation",
            keep_equations=False,
            fade_time=2
        )
        
        # Add equation
        einstein_eq = self.add_equation(
            r"D = \frac{k_B T}{6\pi \eta a}",
            color=WHITE,
            position='center'
        )
        self.play(Write(einstein_eq), run_time=2)
        
        # Add explanation
        explanation = self.add_explanation(
            "k_B: Boltzmann constant\n"
            "T: temperature\n"
            "η: viscosity\n"
            "a: particle radius",
            color=BLUE,
            position='bottom'
        )
        self.play(FadeIn(explanation), run_time=2)
        self.wait(1)
        
        # Add connection equation (replaces previous)
        heat_eq = self.add_equation(
            r"\frac{\partial u}{\partial t} = \alpha \nabla^2 u",
            color=GREEN,
            position='center'
        )
        self.play(Write(heat_eq), run_time=1.5)
        
        # Update explanation
        connection = self.add_explanation(
            "Same mathematical structure!\n"
            "Probability density ↔ Temperature",
            color=GREEN,
            position='bottom'
        )
        self.play(FadeIn(connection), run_time=2)
        self.wait(2)
    
    def conclusion(self):
        """[115-120s] Conclusion."""
        # Clear all text except title
        self.clear_all_text(keep_title=False, fade_out=True)
        
        # Final message
        conclusion = self.add_title(
            "Brownian motion connects\n"
            "microscopic randomness to\n"
            "macroscopic diffusion",
            color=GOLD
        )
        self.safe_position(conclusion, position='center')
        
        self.play(Write(conclusion), run_time=2)
        self.wait(1)

