from manim import *

class NewtonsSecondLawVisualization(Scene):
    def construct(self):
        # ===== TITLE SCENE (5 seconds) =====
        title = Text("Newton's Second Law", font_size=48, color=BLUE)
        subtitle = Text("Force = Mass × Acceleration", font_size=36, color=WHITE)
        
        title.to_edge(UP)
        subtitle.next_to(title, DOWN)
        
        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=DOWN))
        self.wait(1)
        
        # ===== SETUP BASE EQUATION (8 seconds) =====
        # Create the three components with colors
        force_text = Text("Force (F)", color=RED, font_size=32)
        mass_text = Text("Mass (m)", color=GREEN, font_size=32)
        accel_text = Text("Acceleration (a)", color=YELLOW, font_size=32)
        
        # Position them in a triangle formation
        force_text.shift(LEFT * 4 + UP * 2)
        mass_text.shift(RIGHT * 4 + UP * 2)
        accel_text.shift(DOWN * 2)
        
        # Animate them appearing
        self.play(
            LaggedStart(
                FadeIn(force_text, shift=RIGHT),
                FadeIn(mass_text, shift=LEFT),
                FadeIn(accel_text, shift=UP),
                lag_ratio=0.3
            )
        )
        self.wait(1)
        
        # ===== LAUNCH EQUATION (10 seconds) =====
        # Create the main equation with LaTeX
        equation = MathTex(
            r"\vec{F} = m \vec{a}",
            font_size=72,
            color=WHITE
        )
        equation.move_to(ORIGIN)
        
        # Show the equation emerging from the three concepts
        self.play(
            TransformMatchingShapes(VGroup(force_text, mass_text, accel_text), equation),
            run_time=2
        )
        self.wait(2)
        
        # ===== VISUAL METAPHOR (12 seconds) =====
        # Create a visual representation: pushing a box
        
        # Box (represents mass)
        box = Rectangle(height=1.5, width=1.5, color=GREEN, fill_opacity=0.7)
        box_label = Text("m", font_size=24, color=WHITE).move_to(box.get_center())
        mass_group = VGroup(box, box_label).shift(LEFT * 3)
        
        # Force arrow
        force_arrow = Arrow(
            start=LEFT * 5,
            end=LEFT * 3.5,
            color=RED,
            buff=0,
            stroke_width=8,
            max_tip_length_to_length_ratio=0.3
        )
        force_label = Text("F", font_size=24, color=RED).next_to(force_arrow, UP)
        
        # Acceleration arrow
        accel_arrow = Arrow(
            start=box.get_right(),
            end=RIGHT * 2,
            color=YELLOW,
            buff=0,
            stroke_width=6
        )
        accel_label = MathTex(r"\vec{a}", font_size=36, color=YELLOW).next_to(accel_arrow, UP)
        
        # Show the scene
        self.play(
            FadeOut(equation),
            FadeIn(mass_group, shift=RIGHT),
            FadeIn(force_arrow, shift=RIGHT),
            FadeIn(force_label, shift=RIGHT),
            FadeIn(accel_arrow, shift=RIGHT),
            FadeIn(accel_label, shift=RIGHT),
            run_time=1.5
        )
        self.wait(1)
        
        # ===== DYNAMIC DEMONSTRATION (8 seconds) =====
        # Show what happens when mass changes
        
        # Larger mass (slower acceleration)
        big_box = Rectangle(height=2, width=2, color=GREEN, fill_opacity=0.7)
        big_box_label = Text("2m", font_size=24, color=WHITE).move_to(big_box.get_center())
        big_mass_group = VGroup(big_box, big_box_label).shift(LEFT * 3)
        
        # Smaller acceleration arrow
        small_accel_arrow = Arrow(
            start=big_box.get_right(),
            end=RIGHT * 1,
            color=YELLOW,
            buff=0,
            stroke_width=4
        )
        small_accel_label = MathTex(r"\frac{1}{2}\vec{a}", font_size=36, color=YELLOW).next_to(small_accel_arrow, UP)
        
        # Transform to show the inverse relationship
        self.play(
            Transform(mass_group, big_mass_group),
            Transform(accel_arrow, small_accel_arrow),
            Transform(accel_label, small_accel_label),
            run_time=2
        )
        self.wait(1)
        
        # Add the equation back as a summary
        final_equation = MathTex(
            r"\vec{F} = m \vec{a} \implies \text{More mass} = \text{Less acceleration}",
            font_size=36,
            color=BLUE
        ).to_edge(DOWN)
        
        self.play(Write(final_equation), run_time=2)
        self.wait(2)
        
        # ===== FADE OUT (2 seconds) =====
        self.play(
            FadeOut(VGroup(
                mass_group, force_arrow, force_label,
                accel_arrow, accel_label, final_equation
            ))
        )
        self.wait(1)

# For 8th grade focus, we can create a simpler version too
class NewtvonsSecondLawSimple(Scene):
    def construct(self):
        # Simple, direct approach
        title = Text("Newton's Second Law", font_size=48, color=BLUE)
        equation = MathTex(r"\vec{F} = m\vec{a}", font_size=72, color=WHITE)
        
        VGroup(title, equation).arrange(DOWN, buff=1)
        
        self.play(Write(title))
        self.wait(1)
        self.play(Write(equation))
        self.wait(2)
        
        # Key insight
        insight = Text(
            "Push harder → more acceleration\nMore mass → less acceleration",
            font_size=28,
            line_spacing=1.5
        ).next_to(equation, DOWN, buff=1.5)
        
        insight.set_color_by_gradient(RED, GREEN)
        
        self.play(Write(insight))
        self.wait(3)