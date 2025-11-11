from manim import *
import numpy as np
import random

class BrownianMotionAndEinsteinHeatEquation(Scene):
    """
    2-minute (120 second) animation demonstrating Brownian Motion 
    and its connection to Einstein's Heat Equation.
    
    Based on enriched JSON data from the KimiK2Manim pipeline.
    """
    
    def construct(self):
        # Set background
        self.camera.background_color = "#001122"
        
        # Timeline breakdown for 120 seconds:
        # [0-15s] Title and introduction
        # [15-45s] Microscopic Brownian motion visualization
        # [45-70s] Random walk trajectories and mean squared displacement
        # [70-95s] Diffusion equation derivation
        # [95-115s] Einstein's relation and connection to heat equation
        # [115-120s] Conclusion
        
        self.intro_sequence()  # 0-15s
        self.microscopic_brownian_motion()  # 15-45s
        self.random_walk_analysis()  # 45-70s
        self.diffusion_equation()  # 70-95s
        self.einstein_relation()  # 95-115s
        self.conclusion()  # 115-120s
    
    def intro_sequence(self):
        """[0-15s] Title and introduction."""
        title = Text(
            "Brownian Motion and Einstein's Heat Equation",
            font_size=48,
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
        
        # Transition
        self.play(
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(context),
            run_time=2
        )
        self.wait(1)
    
    def microscopic_brownian_motion(self):
        """[15-45s] Show microscopic view with pollen grains and water molecules."""
        # Create water molecules (small blue dots)
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
        
        # Create pollen grains (larger golden spheres)
        pollen_grains = VGroup()
        num_pollen = 5
        pollen_positions = []
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
            pollen_positions.append([x, y])
        
        # Label
        label = Text(
            "Microscopic View: Pollen grains in water",
            font_size=32,
            color=WHITE
        ).to_edge(UP, buff=0.3)
        
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
        
        # Animate Brownian motion
        # Water molecules move randomly
        water_animations = []
        for mol in water_molecules:
            for _ in range(10):
                new_x = mol.get_center()[0] + random.uniform(-0.5, 0.5)
                new_y = mol.get_center()[1] + random.uniform(-0.5, 0.5)
                new_x = np.clip(new_x, -6, 6)
                new_y = np.clip(new_y, -3, 3)
                water_animations.append(
                    mol.animate.move_to([new_x, new_y, 0])
                )
        
        # Pollen grains jiggle due to collisions
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
        
        # Animate motion
        for frame in range(20):
            # Move water molecules
            for mol in water_molecules:
                dx = random.uniform(-0.3, 0.3)
                dy = random.uniform(-0.3, 0.3)
                new_pos = mol.get_center() + np.array([dx, dy, 0])
                new_pos[0] = np.clip(new_pos[0], -6, 6)
                new_pos[1] = np.clip(new_pos[1], -3, 3)
                mol.move_to(new_pos)
            
            # Move pollen grains (jiggle)
            for i, pollen in enumerate(pollen_grains):
                dx = random.uniform(-0.2, 0.2)
                dy = random.uniform(-0.2, 0.2)
                new_pos = pollen.get_center() + np.array([dx, dy, 0])
                new_pos[0] = np.clip(new_pos[0], -5, 5)
                new_pos[1] = np.clip(new_pos[1], -2.5, 2.5)
                pollen.move_to(new_pos)
            
            self.wait(0.1)
        
        self.wait(2)
        
        # Store for later use
        self.water_molecules = water_molecules
        self.pollen_grains = pollen_grains
        self.pollen_trajectories = pollen_trajectories
        self.label = label
    
    def random_walk_analysis(self):
        """[45-70s] Show random walk trajectories and mean squared displacement."""
        # Transition
        self.play(
            FadeOut(self.water_molecules),
            FadeOut(self.pollen_grains),
            FadeOut(self.pollen_trajectories),
            FadeOut(self.label),
            run_time=2
        )
        
        # New title
        title = Text(
            "Random Walk Analysis",
            font_size=40,
            color=GOLD
        ).to_edge(UP, buff=0.3)
        self.play(Write(title), run_time=1)
        
        # Create axes for trajectory plot
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-3, 3, 1],
            x_length=6,
            y_length=4,
            axis_config={"color": WHITE},
            tips=False
        ).shift(LEFT * 2 + DOWN * 0.5)
        
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
        
        # Animate trajectory drawing
        self.play(Create(trajectory), run_time=3)
        self.wait(1)
        
        # Add MSD graph on the right
        msd_title = Text(
            "Mean Squared Displacement",
            font_size=28,
            color=WHITE
        ).next_to(axes, RIGHT, buff=0.5).shift(UP * 1.5)
        
        msd_axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 2, 0.5],
            x_length=4,
            y_length=3,
            axis_config={"color": WHITE},
            tips=False
        ).next_to(msd_title, DOWN, buff=0.3)
        
        msd_x_label = msd_axes.get_x_axis_label("t", direction=DOWN)
        msd_y_label = msd_axes.get_y_axis_label("MSD", direction=LEFT)
        
        self.play(
            Write(msd_title),
            Create(msd_axes),
            FadeIn(msd_x_label),
            FadeIn(msd_y_label),
            run_time=2
        )
        
        # Plot MSD = 2Dt (linear relationship)
        D = 0.1  # Diffusion coefficient
        msd_points = [
            msd_axes.coords_to_point(t, 2 * D * t)
            for t in np.linspace(0, 10, 50)
        ]
        
        msd_curve = VMobject()
        msd_curve.set_points_as_corners(msd_points)
        msd_curve.set_stroke(color=GREEN, width=4)
        
        self.play(Create(msd_curve), run_time=2)
        
        # Show equation
        msd_eq = MathTex(
            r"\langle x^2(t) \rangle = 2Dt",
            font_size=36,
            color=GREEN
        ).next_to(msd_axes, DOWN, buff=0.5)
        
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
        """[70-95s] Derive and show the diffusion equation."""
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
        
        # Title
        title = Text(
            "The Diffusion Equation",
            font_size=40,
            color=GOLD
        ).to_edge(UP, buff=0.3)
        self.play(Write(title), run_time=1)
        
        # Show the PDE
        diffusion_eq = MathTex(
            r"\frac{\partial P}{\partial t} = D \nabla^2 P",
            font_size=48,
            color=WHITE
        ).shift(UP * 1)
        
        self.play(Write(diffusion_eq), run_time=2)
        
        # Explanation
        explanation = VGroup(
            Text("P(x,t): probability density", font_size=24, color=BLUE),
            Text("D: diffusion coefficient", font_size=24, color=BLUE),
            Text("∇²: Laplacian operator", font_size=24, color=BLUE)
        ).arrange(DOWN, buff=0.3).next_to(diffusion_eq, DOWN, buff=0.8)
        
        self.play(*[FadeIn(exp) for exp in explanation], run_time=2)
        
        # Show solution (Gaussian spreading)
        solution_title = Text(
            "Solution: Gaussian spreading",
            font_size=32,
            color=YELLOW
        ).next_to(explanation, DOWN, buff=0.8)
        
        solution_eq = MathTex(
            r"P(x,t|x_0,0) = \frac{1}{\sqrt{4\pi D t}} \exp\left[-\frac{(x-x_0)^2}{4Dt}\right]",
            font_size=36,
            color=WHITE
        ).next_to(solution_title, DOWN, buff=0.5)
        
        self.play(Write(solution_title), run_time=1)
        self.play(Write(solution_eq), run_time=2)
        
        # Visualize Gaussian spreading
        gaussian_axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 1.5, 0.5],
            x_length=6,
            y_length=3,
            axis_config={"color": WHITE},
            tips=False
        ).next_to(solution_eq, DOWN, buff=0.8)
        
        self.play(Create(gaussian_axes), run_time=1)
        
        # Animate Gaussian spreading over time
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
        """[95-115s] Show Einstein's relation and connection to heat equation."""
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
        
        # Title
        title = Text(
            "Einstein's Relation",
            font_size=40,
            color=GOLD
        ).to_edge(UP, buff=0.3)
        self.play(Write(title), run_time=1)
        
        # Stokes-Einstein relation
        einstein_eq = MathTex(
            r"D = \frac{k_B T}{6\pi \eta a}",
            font_size=48,
            color=WHITE
        ).shift(UP * 1)
        
        self.play(Write(einstein_eq), run_time=2)
        
        # Definitions
        definitions = VGroup(
            MathTex(r"k_B: \text{Boltzmann constant}", font_size=28, color=BLUE),
            MathTex(r"T: \text{temperature}", font_size=28, color=BLUE),
            MathTex(r"\eta: \text{viscosity}", font_size=28, color=BLUE),
            MathTex(r"a: \text{particle radius}", font_size=28, color=BLUE)
        ).arrange(DOWN, buff=0.3).next_to(einstein_eq, DOWN, buff=0.8)
        
        self.play(*[FadeIn(defn) for defn in definitions], run_time=2)
        
        # Connection to heat equation
        connection_title = Text(
            "Connection to Heat Equation",
            font_size=32,
            color=YELLOW
        ).next_to(definitions, DOWN, buff=0.8)
        
        heat_eq = MathTex(
            r"\frac{\partial u}{\partial t} = \alpha \nabla^2 u",
            font_size=44,
            color=WHITE
        ).next_to(connection_title, DOWN, buff=0.5)
        
        connection_text = Text(
            "Same mathematical structure!\n"
            "Probability density ↔ Temperature",
            font_size=24,
            color=GREEN,
            line_spacing=1.2
        ).next_to(heat_eq, DOWN, buff=0.5)
        
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
        """[115-120s] Conclusion."""
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
        
        # Final message
        conclusion = Text(
            "Brownian motion connects\n"
            "microscopic randomness to\n"
            "macroscopic diffusion",
            font_size=36,
            color=GOLD,
            line_spacing=1.3
        )
        
        self.play(Write(conclusion), run_time=2)
        self.wait(1)

