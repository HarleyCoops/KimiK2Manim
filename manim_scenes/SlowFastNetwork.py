"""
Slow-Fast Network Architecture (Hypernetwork) - PhD-Level Explanation

This Manim animation explains the meta-learning architecture where a SLOW network
programs the weights of a FAST network through outer products of KEY and VALUE vectors.

Key concepts:
- Hypernetwork: SLOW network generates weights for FAST network
- Outer products: W_fast = KEY ⊗ VALUE (k * v^T)
- Meta-learning: Learning how to learn/configure task-specific networks
- Applications: Few-shot learning, continual learning, contextual modulation
"""

from manim import *
import numpy as np


class SlowFastNetworkPhD(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        # Track current text elements to prevent overlapping
        self.current_text_elements = []
        
        # Title
        title = Text(
            "Slow-Fast Network Architecture",
            font_size=48,
            color=BLACK,
            weight=BOLD
        ).to_edge(UP)
        subtitle = Text(
            "Hypernetwork Meta-Learning System",
            font_size=32,
            color=GRAY,
        ).next_to(title, DOWN, buff=0.2)
        
        self.play(Write(title), Write(subtitle))
        self.wait(1)
        
        # Section 1: Architecture Overview
        self.section_architecture_overview(title, subtitle)
        
        # Section 2: SLOW Network Details
        self.section_slow_network()
        
        # Section 3: FAST Network Details
        self.section_fast_network()
        
        # Section 4: Outer Product Mechanism
        self.section_outer_products()
        
        # Section 5: Mathematical Formulation
        self.section_mathematical_formulation()
        
        # Section 6: Applications and Implications
        self.section_applications()
        
        # Final summary
        self.section_summary()
    
    def clear_text_area(self, position="BOTTOM"):
        """Clear text elements in a specific area to prevent overlapping."""
        if not self.current_text_elements:
            return
        
        elements_to_remove = []
        for elem in self.current_text_elements:
            if position == "BOTTOM" and elem.get_bottom()[1] < -2:
                elements_to_remove.append(elem)
            elif position == "CENTER" and abs(elem.get_center()[1]) < 1:
                elements_to_remove.append(elem)
        
        if elements_to_remove:
            self.play(FadeOut(VGroup(*elements_to_remove)))
            for elem in elements_to_remove:
                if elem in self.current_text_elements:
                    self.current_text_elements.remove(elem)

    def section_architecture_overview(self, title, subtitle):
        """Show the complete architecture diagram."""
        self.play(FadeOut(title), FadeOut(subtitle))
        
        section_title = Text("1. Architecture Overview", font_size=36, color=BLACK, weight=BOLD).to_edge(UP)
        self.play(Write(section_title))
        
        # Node properties
        node_radius = 0.15
        slow_input_color = WHITE
        slow_hidden_color = LIGHT_GRAY
        slow_value_start = "#FFC0CB"  # Light Pink
        slow_value_end = RED
        slow_key_start = "#ADD8E6"    # Light Blue
        slow_key_end = BLUE
        fast_input_color = BLUE_D
        fast_output_color = RED_D
        
        # SLOW Network
        slow_input = VGroup(*[
            Circle(radius=node_radius, color=BLACK, fill_color=slow_input_color, 
                   fill_opacity=1, stroke_width=2) 
            for _ in range(4)
        ]).arrange(DOWN, buff=0.4).shift(LEFT * 5.5)
        
        slow_hidden = VGroup(*[
            Circle(radius=node_radius, color=BLACK, fill_color=slow_hidden_color,
                   fill_opacity=1, stroke_width=2)
            for _ in range(4)
        ]).arrange(DOWN, buff=0.4).shift(LEFT * 3.5)
        
        slow_value = VGroup(*[
            Circle(radius=node_radius, color=BLACK,
                   fill_color=interpolate_color(
                       ManimColor(slow_value_start),
                       ManimColor(slow_value_end),
                       i / 2.0
                   ),
                   fill_opacity=1, stroke_width=2)
            for i in range(3)
        ]).arrange(DOWN, buff=0.4).shift(LEFT * 1.5 + UP * 1.2)
        
        slow_key = VGroup(*[
            Circle(radius=node_radius, color=BLACK,
                   fill_color=interpolate_color(
                       ManimColor(slow_key_start),
                       ManimColor(slow_key_end),
                       i / 2.0
                   ),
                   fill_opacity=1, stroke_width=2)
            for i in range(3)
        ]).arrange(DOWN, buff=0.4).shift(LEFT * 1.5 + DOWN * 1.2)
        
        # FAST Network
        fast_input = VGroup(*[
            Circle(radius=node_radius, color=BLACK, fill_color=fast_input_color,
                   fill_opacity=1, stroke_width=2)
            for _ in range(4)
        ]).arrange(DOWN, buff=0.4).shift(RIGHT * 3.5 + DOWN * 1.2)
        
        fast_output = VGroup(*[
            Circle(radius=node_radius, color=BLACK, fill_color=fast_output_color,
                   fill_opacity=1, stroke_width=2)
            for _ in range(4)
        ]).arrange(DOWN, buff=0.4).shift(RIGHT * 3.5 + UP * 1.2)
        
        # Labels
        slow_label = Text("SLOW", font_size=28, color=BLACK, weight=BOLD).next_to(slow_input, UP, buff=0.3)
        fast_label = Text("FAST", font_size=28, color=BLACK, weight=BOLD).next_to(fast_output, UP, buff=0.3)
        value_label = Text("VALUE", font_size=20, color=RED, weight=BOLD).next_to(slow_value, RIGHT, buff=0.2)
        key_label = Text("KEY", font_size=20, color=BLUE, weight=BOLD).next_to(slow_key, RIGHT, buff=0.2)
        
        # Animate nodes appearing
        self.play(
            FadeIn(slow_input, shift=LEFT),
            FadeIn(slow_hidden, shift=LEFT),
            run_time=1
        )
        self.play(
            FadeIn(slow_value, shift=LEFT),
            FadeIn(slow_key, shift=LEFT),
            Write(value_label),
            Write(key_label),
            Write(slow_label),
            run_time=1
        )
        self.play(
            FadeIn(fast_input, shift=RIGHT),
            FadeIn(fast_output, shift=RIGHT),
            Write(fast_label),
            run_time=1
        )
        
        # SLOW network connections (solid)
        slow_conns = VGroup()
        for inp in slow_input:
            for hid in slow_hidden:
                slow_conns.add(
                    Arrow(inp.get_right(), hid.get_left(), buff=0.05,
                          color=BLACK, stroke_width=1.5, max_tip_length_to_length_ratio=0.15)
                )
        for hid in slow_hidden:
            for val in slow_value:
                slow_conns.add(
                    Arrow(hid.get_right(), val.get_left(), buff=0.05,
                          color=BLACK, stroke_width=1.5, max_tip_length_to_length_ratio=0.15)
                )
            for key in slow_key:
                slow_conns.add(
                    Arrow(hid.get_right(), key.get_left(), buff=0.05,
                          color=BLACK, stroke_width=1.5, max_tip_length_to_length_ratio=0.15)
                )
        
        self.play(Create(slow_conns), run_time=2)
        self.wait(1)
        
        # FAST network connections (dashed - programmed weights)
        fast_conns = VGroup()
        for fi in fast_input:
            for fo in fast_output:
                fast_conns.add(
                    DashedLine(fi.get_top(), fo.get_bottom(), buff=0.05,
                              color=BLACK, stroke_width=1.5, dash_length=0.08)
                )
        
        self.play(Create(fast_conns), run_time=2)
        self.wait(1)
        
        # Programming connections (dotted)
        prog_conns = VGroup()
        # VALUE to FAST output (red)
        for val in slow_value:
            for fo in fast_output:
                prog_conns.add(
                    DashedLine(val.get_right(), fo.get_left(), buff=0.05,
                              color=RED, stroke_width=1.2, dash_length=0.1)
                )
        # KEY to FAST input (blue)
        for key in slow_key:
            for fi in fast_input:
                prog_conns.add(
                    DashedLine(key.get_right(), fi.get_left(), buff=0.05,
                              color=BLUE, stroke_width=1.2, dash_length=0.1)
                )
        
        self.play(Create(prog_conns), run_time=2)
        self.wait(1)
        
        # Explanatory text
        explanation = Text(
            "FAST weights programmed by SLOW network\nthrough outer products: W = KEY ⊗ VALUE",
            font_size=24,
            color=BLACK
        ).to_edge(DOWN, buff=0.5)
        
        self.play(Write(explanation))
        self.wait(2)
        
        # Store for later
        self.architecture_group = VGroup(
            slow_input, slow_hidden, slow_value, slow_key,
            fast_input, fast_output,
            slow_label, fast_label, value_label, key_label,
            slow_conns, fast_conns, prog_conns, explanation
        )
        
        self.play(FadeOut(section_title), FadeOut(self.architecture_group))

    def section_slow_network(self):
        """Explain the SLOW network in detail."""
        section_title = Text("2. SLOW Network: The Hypernetwork", font_size=36, color=BLACK, weight=BOLD).to_edge(UP)
        self.play(Write(section_title))
        
        # Create simplified SLOW network
        input_layer = VGroup(*[
            Circle(radius=0.2, color=BLACK, fill_color=WHITE, fill_opacity=1, stroke_width=2)
            for _ in range(4)
        ]).arrange(DOWN, buff=0.5).shift(LEFT * 3)
        
        hidden_layer = VGroup(*[
            Circle(radius=0.2, color=BLACK, fill_color=LIGHT_GRAY, fill_opacity=1, stroke_width=2)
            for _ in range(4)
        ]).arrange(DOWN, buff=0.5).shift(ORIGIN)
        
        output_layer = VGroup(*[
            Circle(radius=0.2, color=BLACK, fill_color=BLUE, fill_opacity=0.7, stroke_width=2)
            for _ in range(6)
        ]).arrange(DOWN, buff=0.3).shift(RIGHT * 3)
        
        # Labels
        input_label = Text("Input\nx in R^n", font_size=20, color=BLACK).next_to(input_layer, DOWN, buff=0.3)
        hidden_label = Text("Hidden\nh in R^m", font_size=20, color=BLACK).next_to(hidden_layer, DOWN, buff=0.3)
        output_label = Text("KEY & VALUE\nk, v in R^d", font_size=20, color=BLACK).next_to(output_layer, DOWN, buff=0.3)
        
        self.play(
            FadeIn(input_layer),
            Write(input_label),
            run_time=1
        )
        self.play(
            FadeIn(hidden_layer),
            Write(hidden_label),
            run_time=1
        )
        self.play(
            FadeIn(output_layer),
            Write(output_label),
            run_time=1
        )
        
        # Connections
        conns1 = VGroup(*[
            Arrow(inp.get_right(), hid.get_left(), buff=0.1, color=BLACK, stroke_width=2)
            for inp in input_layer for hid in hidden_layer
        ])
        conns2 = VGroup(*[
            Arrow(hid.get_right(), out.get_left(), buff=0.1, color=BLACK, stroke_width=2)
            for hid in hidden_layer for out in output_layer
        ])
        
        self.play(Create(conns1), run_time=1.5)
        self.play(Create(conns2), run_time=1.5)
        
        # Mathematical description - clear any existing bottom text first
        self.clear_text_area("BOTTOM")
        math_desc = VGroup(
            MathTex(r"\text{SLOW Network: } f_\theta: x \mapsto (k, v)", font_size=32, color=BLACK),
            MathTex(r"\theta \text{ updated slowly (meta-learning)", font_size=24, color=GRAY),
            MathTex(r"k, v \in \mathbb{R}^d \text{ (KEY and VALUE vectors)", font_size=24, color=BLACK)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.5)
        
        self.play(Write(math_desc[0]))
        self.current_text_elements.append(math_desc[0])
        self.wait(1)
        self.play(Write(math_desc[1]))
        self.current_text_elements.append(math_desc[1])
        self.wait(1)
        self.play(Write(math_desc[2]))
        self.current_text_elements.append(math_desc[2])
        self.wait(2)
        
        # Clear tracked text elements
        for elem in math_desc:
            if elem in self.current_text_elements:
                self.current_text_elements.remove(elem)
        
        self.play(FadeOut(VGroup(
            input_layer, hidden_layer, output_layer,
            input_label, hidden_label, output_label,
            conns1, conns2, math_desc, section_title
        )))

    def section_fast_network(self):
        """Explain the FAST network."""
        section_title = Text("3. FAST Network: Task-Specific Network", font_size=36, color=BLACK, weight=BOLD).to_edge(UP)
        self.play(Write(section_title))
        
        # FAST network
        fast_in = VGroup(*[
            Circle(radius=0.2, color=BLACK, fill_color=BLUE_D, fill_opacity=1, stroke_width=2)
            for _ in range(4)
        ]).arrange(DOWN, buff=0.5).shift(LEFT * 2)
        
        fast_out = VGroup(*[
            Circle(radius=0.2, color=BLACK, fill_color=RED_D, fill_opacity=1, stroke_width=2)
            for _ in range(4)
        ]).arrange(DOWN, buff=0.5).shift(RIGHT * 2)
        
        # Dashed connections (programmed weights)
        fast_conns = VGroup(*[
            DashedLine(fi.get_right(), fo.get_left(), buff=0.1,
                      color=BLACK, stroke_width=2, dash_length=0.1)
            for fi in fast_in for fo in fast_out
        ])
        
        # Labels
        in_label = Text("Input\ny in R^n", font_size=20, color=BLACK).next_to(fast_in, DOWN, buff=0.3)
        out_label = Text("Output\ny_hat in R^m", font_size=20, color=BLACK).next_to(fast_out, DOWN, buff=0.3)
        weight_label = Text("W (programmed)", font_size=20, color=BLACK, weight=BOLD).move_to(ORIGIN + UP * 0.5)
        
        self.play(
            FadeIn(fast_in),
            FadeIn(fast_out),
            Write(in_label),
            Write(out_label),
            run_time=1
        )
        self.play(Create(fast_conns), Write(weight_label), run_time=2)
        
        # Mathematical description - clear any existing bottom text first
        self.clear_text_area("BOTTOM")
        math_desc = VGroup(
            MathTex(r"\text{FAST Network: } \hat{y} = W \cdot y", font_size=32, color=BLACK),
            MathTex(r"W \text{ is NOT learned via backpropagation}", font_size=24, color=RED),
            MathTex(r"\mathbf{W} \text{ is PROGRAMMED by SLOW network}", font_size=24, color=BLUE)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.5)
        
        self.play(Write(math_desc[0]))
        self.current_text_elements.append(math_desc[0])
        self.wait(1)
        self.play(Write(math_desc[1]))
        self.current_text_elements.append(math_desc[1])
        self.wait(1)
        self.play(Write(math_desc[2]))
        self.current_text_elements.append(math_desc[2])
        self.wait(2)
        
        # Clear tracked text elements
        for elem in math_desc:
            if elem in self.current_text_elements:
                self.current_text_elements.remove(elem)
        
        self.play(FadeOut(VGroup(
            fast_in, fast_out, fast_conns,
            in_label, out_label, weight_label,
            math_desc, section_title
        )))

    def section_outer_products(self):
        """Explain the outer product mechanism."""
        section_title = Text("4. Weight Programming: Outer Products", font_size=36, color=BLACK, weight=BOLD).to_edge(UP)
        self.play(Write(section_title))
        
        # KEY vector
        key_vec = Matrix([["k_1"], ["k_2"], ["k_3"]], bracket_v_buff=0.2, bracket_h_buff=0.1,
                         element_alignment_corner=ORIGIN).scale(0.8)
        key_label = Text("KEY", font_size=24, color=BLUE, weight=BOLD).next_to(key_vec, UP, buff=0.2)
        key_group = VGroup(key_label, key_vec).shift(LEFT * 3)
        
        # VALUE vector
        value_vec = Matrix([["v_1"], ["v_2"], ["v_3"]], bracket_v_buff=0.2, bracket_h_buff=0.1,
                           element_alignment_corner=ORIGIN).scale(0.8)
        value_label = Text("VALUE", font_size=24, color=RED, weight=BOLD).next_to(value_vec, UP, buff=0.2)
        value_group = VGroup(value_label, value_vec).shift(RIGHT * 3)
        
        self.play(
            FadeIn(key_group),
            FadeIn(value_group),
            run_time=1
        )
        
        # Outer product symbol
        outer_symbol = MathTex(r"\otimes", font_size=48, color=BLACK).move_to(ORIGIN)
        self.play(Write(outer_symbol))
        self.wait(1)
        
        # Show the operation
        operation = MathTex(r"W = k \otimes v = k \cdot v^T", font_size=36, color=BLACK).next_to(outer_symbol, DOWN, buff=0.5)
        self.play(Write(operation))
        self.wait(1)
        
        # Show matrix result
        result_matrix = Matrix([
            ["k_1 v_1", "k_1 v_2", "k_1 v_3"],
            ["k_2 v_1", "k_2 v_2", "k_2 v_3"],
            ["k_3 v_1", "k_3 v_2", "k_3 v_3"]
        ], bracket_v_buff=0.2, bracket_h_buff=0.1).scale(0.7)
        result_label = Text("Weight Matrix W", font_size=24, color=BLACK, weight=BOLD).next_to(result_matrix, UP, buff=0.2)
        result_group = VGroup(result_label, result_matrix).next_to(operation, DOWN, buff=0.5)
        
        self.play(Write(result_group))
        self.wait(2)
        
        # Explanation - clear any existing bottom text first
        self.clear_text_area("BOTTOM")
        explanation = VGroup(
            Text("• Outer product creates rank-1 matrix", font_size=20, color=BLACK),
            Text("• Low-rank approximation of full weight matrix", font_size=20, color=BLACK),
            Text("• Enables efficient parameter generation", font_size=20, color=BLACK),
            Text("• Context-dependent weight modulation", font_size=20, color=BLACK)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.5)
        
        self.play(Write(explanation))
        self.current_text_elements.extend(explanation)
        self.wait(3)
        
        # Clear tracked text elements
        for elem in explanation:
            if elem in self.current_text_elements:
                self.current_text_elements.remove(elem)
        
        self.play(FadeOut(VGroup(
            key_group, value_group, outer_symbol, operation,
            result_group, explanation, section_title
        )))

    def section_mathematical_formulation(self):
        """Show complete mathematical formulation."""
        section_title = Text("5. Complete Mathematical Formulation", font_size=36, color=BLACK, weight=BOLD).to_edge(UP)
        self.play(Write(section_title))
        
        # Step-by-step formulation - clear center area first
        self.clear_text_area("CENTER")
        steps = VGroup(
            MathTex(r"\text{1. SLOW Network: } (k, v) = f_\theta(x)", font_size=28, color=BLACK),
            MathTex(r"\text{2. Weight Generation: } W = k \cdot v^T \in \mathbb{R}^{d \times d}", font_size=28, color=BLACK),
            MathTex(r"\text{3. FAST Network: } \hat{y} = W \cdot y = (k \cdot v^T) \cdot y", font_size=28, color=BLACK),
            MathTex(r"\text{4. Equivalent: } \hat{y} = k \cdot (v^T \cdot y) = k \cdot \langle v, y \rangle", font_size=28, color=BLACK),
            MathTex(r"\text{5. Interpretation: Attention mechanism with KEY-VALUE pairs}", font_size=28, color=BLACK)
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT).shift(UP * 0.5)
        
        for step in steps:
            self.play(Write(step))
            self.current_text_elements.append(step)
            self.wait(1.5)
        
        # Key insight box
        insight_box = SurroundingRectangle(
            steps[3],
            color=BLUE,
            buff=0.2,
            stroke_width=3
        )
        insight_text = Text(
            "KEY insight: Inner product <v,y> acts as attention score",
            font_size=20,
            color=BLUE,
            weight=BOLD
        ).next_to(insight_box, DOWN, buff=0.3)
        
        self.play(Create(insight_box), Write(insight_text))
        self.current_text_elements.append(insight_text)
        self.wait(2)
        
        # Clear tracked text elements
        for elem in steps:
            if elem in self.current_text_elements:
                self.current_text_elements.remove(elem)
        if insight_text in self.current_text_elements:
            self.current_text_elements.remove(insight_text)
        
        self.play(FadeOut(VGroup(steps, insight_box, insight_text, section_title)))

    def section_applications(self):
        """Discuss applications and implications."""
        section_title = Text("6. Applications & Implications", font_size=36, color=BLACK, weight=BOLD).to_edge(UP)
        self.play(Write(section_title))
        
        applications = VGroup(
            VGroup(
                Text("Few-Shot Learning", font_size=24, color=BLACK, weight=BOLD),
                Text("SLOW network learns to configure FAST network\nfor new tasks with minimal examples", font_size=18, color=GRAY)
            ),
            VGroup(
                Text("Continual Learning", font_size=24, color=BLACK, weight=BOLD),
                Text("Task-specific weights generated without\ncatastrophic forgetting", font_size=18, color=GRAY)
            ),
            VGroup(
                Text("Contextual Modulation", font_size=24, color=BLACK, weight=BOLD),
                Text("SLOW network encodes context (task ID, environment)\ninto KEY-VALUE pairs", font_size=18, color=GRAY)
            ),
            VGroup(
                Text("Memory Mechanisms", font_size=24, color=BLACK, weight=BOLD),
                Text("KEY-VALUE pairs act as external memory\nfor rapid adaptation", font_size=18, color=GRAY)
            )
        ).arrange_in_grid(2, 2, buff=0.8, aligned_widths=True).scale(0.9)
        
        for app in applications:
            app[0].next_to(app[1], UP, buff=0.1)
            app.arrange(DOWN, buff=0.1)
        
        for app in applications:
            self.play(FadeIn(app, shift=UP))
            self.wait(1.5)
        
        # Research implications - clear bottom area first to avoid overlap
        self.clear_text_area("BOTTOM")
        implications = VGroup(
            Text("Research Implications:", font_size=24, color=BLACK, weight=BOLD),
            Text("• Meta-learning: Learning how to learn", font_size=20, color=BLACK),
            Text("• Parameter efficiency: Low-rank weight generation", font_size=20, color=BLACK),
            Text("• Transfer learning: SLOW network transfers across tasks", font_size=20, color=BLACK),
            Text("• Scalability: Fast adaptation without full retraining", font_size=20, color=BLACK)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(DOWN, buff=0.5)
        
        self.play(Write(implications))
        self.current_text_elements.extend(implications)
        self.wait(3)
        
        # Clear tracked text elements
        for elem in implications:
            if elem in self.current_text_elements:
                self.current_text_elements.remove(elem)
        
        self.play(FadeOut(VGroup(applications, implications, section_title)))

    def section_summary(self):
        """Final summary."""
        # Clear all previous text before summary
        if self.current_text_elements:
            self.play(FadeOut(VGroup(*self.current_text_elements)))
            self.current_text_elements.clear()
        
        summary_title = Text("Summary", font_size=48, color=BLACK, weight=BOLD).to_edge(UP)
        self.play(Write(summary_title))
        
        summary_points = VGroup(
            Text("1. SLOW Network: Hypernetwork that learns to generate parameters", font_size=24, color=BLACK),
            Text("2. KEY & VALUE: Vectors output by SLOW network", font_size=24, color=BLACK),
            Text("3. Outer Products: W = k ⊗ v programs FAST network weights", font_size=24, color=BLACK),
            Text("4. FAST Network: Task-specific network with dynamic weights", font_size=24, color=BLACK),
            Text("5. Meta-Learning: Enables rapid adaptation and few-shot learning", font_size=24, color=BLACK)
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT).shift(UP * 0.5)
        
        for point in summary_points:
            self.play(Write(point))
            self.current_text_elements.append(point)
            self.wait(1)
        
        # Final equation
        final_eq = MathTex(
            r"\mathbf{\hat{y}} = f_\theta(x) \cdot \text{KEY} \cdot \text{VALUE}^T \cdot y",
            font_size=36,
            color=BLUE
        ).next_to(summary_points, DOWN, buff=0.8)
        
        self.play(Write(final_eq))
        self.current_text_elements.append(final_eq)
        self.wait(3)
        
        # Fade out - also clear tracked elements
        self.play(FadeOut(VGroup(summary_title, summary_points, final_eq)))
        if self.current_text_elements:
            self.current_text_elements.clear()
        self.wait(1)


# Alternative: More detailed version with animations
class SlowFastNetworkDetailed(Scene):
    """More detailed version with step-by-step animations."""
    
    def construct(self):
        self.camera.background_color = WHITE
        # Similar structure but with more detailed animations
        # Can be extended based on specific requirements
        pass

