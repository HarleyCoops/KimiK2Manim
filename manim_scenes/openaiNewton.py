from manim import *
import numpy as np

class ForceEquation(Scene):
    def construct(self):
        # Title and core equation
        title = Text("Newton's Second Law", weight=BOLD, font_size=56)
        eq = MathTex("F", "=", "m", "a", font_size=80)
        eq.set_color_by_tex_to_color_map({"F": YELLOW, "m": BLUE, "a": RED})
        title.to_edge(UP)
        self.play(FadeIn(title, shift=UP))
        self.play(Write(eq))
        self.wait(0.5)

        # Conceptual annotation under the equation
        concept = VGroup(
            Text("Force causes acceleration.", font_size=28),
            Text("For a fixed mass, acceleration grows with force.", font_size=28),
            Text("For a fixed force, acceleration shrinks with mass.", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT)
        concept.next_to(eq, DOWN, buff=0.6)
        self.play(FadeIn(concept, lag_ratio=0.1))
        self.wait(0.5)

        # --- Physical demo: a block pushed by a force ---
        ground = Line(LEFT*6, RIGHT*6).shift(DOWN*2)
        self.play(Create(ground))

        block = RoundedRectangle(corner_radius=0.15, width=2.0, height=1.2)
        block.set_fill(GRAY_E, opacity=1.0).set_stroke(WHITE, 2)
        block.move_to(LEFT*3 + DOWN*1.4)

        # Trackers for F and m (SI-like units)
        F_tracker = ValueTracker(2.0)
        m_tracker = ValueTracker(1.0)

        # Acceleration a = F/m
        def get_a():
            m = max(m_tracker.get_value(), 1e-6)
            return F_tracker.get_value() / m

        # Force arrow (rightward)
        def force_arrow():
            F = F_tracker.get_value()
            length = np.clip(0.6 + 0.2*F, 0.4, 3.5)
            arr = Arrow(start=block.get_right(), end=block.get_right()+RIGHT*length, buff=0.1)
            arr.set_color(YELLOW)
            label = MathTex("F", font_size=36, color=YELLOW)
            label.next_to(arr, UP, buff=0.1)
            return VGroup(arr, label)

        F_vec = always_redraw(force_arrow)

        # Acceleration arrow above block
        def accel_arrow():
            a = get_a()
            # scale arrow length to a (allow negative too, but here positive)
            length = np.clip(0.6 + 0.4*a, 0.3, 4.0)
            arr = Arrow(start=block.get_top(), end=block.get_top()+RIGHT*length, buff=0.1)
            arr.set_color(RED)
            label = MathTex("a", font_size=36, color=RED)
            label.next_to(arr, UP, buff=0.1)
            return VGroup(arr, label)

        a_vec = always_redraw(accel_arrow)

        # Numeric readout panel
        panel = RoundedRectangle(corner_radius=0.15, width=4.8, height=1.6)
        panel.set_stroke(GRAY_D, 2).set_fill(BLACK, 0.1)
        panel.to_corner(UR).shift(DOWN*0.4 + LEFT*0.2)

        F_read = always_redraw(lambda: VGroup(
            MathTex("F=", font_size=32, color=YELLOW),
            DecimalNumber(F_tracker.get_value(), num_decimal_places=2, include_sign=False, font_size=32, color=YELLOW)
        ).arrange(RIGHT, buff=0.1).next_to(panel.get_left(), RIGHT, buff=0.3).shift(UP*0.35))

        m_read = always_redraw(lambda: VGroup(
            MathTex("m=", font_size=32, color=BLUE),
            DecimalNumber(m_tracker.get_value(), num_decimal_places=2, include_sign=False, font_size=32, color=BLUE)
        ).arrange(RIGHT, buff=0.1).next_to(panel.get_left(), RIGHT, buff=0.3).shift(DOWN*0.35))

        a_read = always_redraw(lambda: VGroup(
            MathTex("a=", font_size=32, color=RED),
            DecimalNumber(get_a(), num_decimal_places=2, include_sign=False, font_size=32, color=RED)
        ).arrange(RIGHT, buff=0.1).next_to(panel, RIGHT, buff=0.25).shift(LEFT*2.8))

        # Put everything on screen
        self.play(FadeIn(block), FadeIn(F_vec), FadeIn(a_vec))
        self.play(FadeIn(panel), FadeIn(F_read), FadeIn(m_read), FadeIn(a_read))
        self.wait(0.2)

        # --- Sequence 1: Fix mass, increase force -> a increases proportionally ---
        seq1_label = Text("Fix mass, increase force", font_size=28)
        seq1_label.next_to(concept, DOWN, buff=0.4)
        self.play(FadeIn(seq1_label))
        self.play(m_tracker.animate.set_value(2.0), run_time=0.8)
        self.wait(0.2)
        self.play(F_tracker.animate.set_value(1.0), run_time=0.8)
        self.play(F_tracker.animate.set_value(5.0), run_time=2.0)
        self.wait(0.4)

        # --- Sequence 2: Fix force, increase mass -> a decreases inversely ---
        self.play(FadeOut(seq1_label))
        seq2_label = Text("Fix force, increase mass", font_size=28)
        seq2_label.next_to(concept, DOWN, buff=0.4)
        self.play(FadeIn(seq2_label))
        self.play(F_tracker.animate.set_value(3.0), run_time=0.8)
        self.play(m_tracker.animate.set_value(1.0), run_time=0.8)
        self.play(m_tracker.animate.set_value(6.0), run_time=2.0)
        self.wait(0.4)
        self.play(FadeOut(seq2_label))

        # --- Graphical view: F vs a line with slope m ---
        axes = Axes(
            x_range=[0, 6, 1], y_range=[0, 10, 2], 
            x_length=5, y_length=3.2,
            axis_config={"include_tip": True}
        )
        axes.to_edge(DOWN).shift(RIGHT*1.0)
        x_label = axes.get_x_axis_label(MathTex("a"))
        y_label = axes.get_y_axis_label(MathTex("F"))
        graph_group = VGroup(axes, x_label, y_label)
        self.play(FadeIn(graph_group))

        slope_text = always_redraw(lambda: VGroup(
            MathTex("F = m a\\; (\\text{slope }=m)", font_size=32)
        ).next_to(axes, UP, buff=0.2))
        self.play(FadeIn(slope_text))

        def line_for_current_m():
            # F = m a => y = m x
            m = m_tracker.get_value()
            def func(a):
                return m * a
            graph = axes.plot(lambda x: func(x), x_range=[0, 6])
            graph.set_color(BLUE)
            return graph

        line_graph = always_redraw(line_for_current_m)
        self.play(Create(line_graph))

        # Marker showing current (a, F)
        dot = always_redraw(lambda: Dot(
            axes.c2p(np.clip(get_a(), 0, 6), np.clip(F_tracker.get_value(), 0, 10)),
            color=YELLOW
        ))
        self.play(FadeIn(dot))

        # Move through states to show changing slope and point
        self.play(m_tracker.animate.set_value(2.0), run_time=1.2)
        self.play(F_tracker.animate.set_value(8.0), run_time=1.2)
        self.play(m_tracker.animate.set_value(4.0), run_time=1.2)
        self.play(F_tracker.animate.set_value(4.0), run_time=1.2)
        self.wait(0.6)

        # Final summary callouts
        box = SurroundingRectangle(eq, color=WHITE, buff=0.2)
        summary = VGroup(
            Text("Proportional: a ∝ F", font_size=30, color=YELLOW),
            Text("Inverse: a ∝ 1/m", font_size=30, color=BLUE),
        ).arrange(DOWN, buff=0.2).next_to(eq, RIGHT, buff=0.6)
        self.play(Create(box), FadeIn(summary, lag_ratio=0.1))
        self.wait(1.2)

        # Outro
        self.play(*map(FadeOut, [box, summary, dot, line_graph, slope_text, graph_group, panel, F_vec, a_vec, block, concept]))
        self.play(eq.animate.to_edge(UP), title.animate.to_edge(UP))
        thanks = Text("F = m a ties force, mass, and acceleration.", font_size=36)
        self.play(Write(thanks))
        self.wait(1.5)
        self.play(FadeOut(thanks), FadeOut(eq), FadeOut(title), FadeOut(ground))
        self.wait(0.5)
