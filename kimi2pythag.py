from manim import *

class PythagoreanTheorem(Scene):
    def construct(self):
        # --- Setup ---
        # Set background and create grid
        self.camera.background_color = WHITE
        grid = NumberPlane(
            x_range=[-10, 10, 1],
            y_range=[-10, 10, 1],
            background_line_style={
                "stroke_color": LIGHT_GRAY,
                "stroke_width": 1,
            }
        )
        self.add(grid)
        
        # --- Create 3-4-5 Right Triangle ---
        # Points for the triangle (right angle at origin)
        right_angle = np.array([0, 0, 0])
        point_a = np.array([3, 0, 0])  # Horizontal leg (a = 3)
        point_b = np.array([0, 4, 0])  # Vertical leg (b = 4)
        
        # Create colored sides
        side_a = Line(right_angle, point_a, color=BLUE, stroke_width=4)
        side_b = Line(right_angle, point_b, color=GREEN, stroke_width=4)
        side_c = Line(point_a, point_b, color=RED, stroke_width=4)
        
        triangle = VGroup(side_a, side_b, side_c)
        
        # --- Create Squares on Each Side ---
        # Square on side a (blue) - extends downward
        square_a = Polygon(
            right_angle,
            point_a,
            point_a + np.array([0, -3, 0]),
            right_angle + np.array([0, -3, 0]),
            color=BLUE,
            fill_color=BLUE,
            fill_opacity=0.3,
            stroke_width=2
        )
        
        # Square on side b (green) - extends leftward
        square_b = Polygon(
            right_angle,
            point_b,
            point_b + np.array([-4, 0, 0]),
            right_angle + np.array([-4, 0, 0]),
            color=GREEN,
            fill_color=GREEN,
            fill_opacity=0.3,
            stroke_width=2
        )
        
        # Square on side c (red) - extends outward (north-east direction)
        square_c = Polygon(
            point_a,
            point_b,
            point_b + np.array([4, 3, 0]),
            point_a + np.array([4, 3, 0]),
            color=RED,
            fill_color=RED,
            fill_opacity=0.3,
            stroke_width=2
        )
        
        squares = VGroup(square_a, square_b, square_c)
        
        # --- Create Labels ---
        # Side labels
        label_a = MathTex("a", color=BLUE).next_to(side_a, DOWN, buff=0.2)
        label_b = MathTex("b", color=GREEN).next_to(side_b, LEFT, buff=0.2)
        label_c = MathTex("c", color=RED).next_to(side_c, RIGHT, buff=0.2)
        side_labels = VGroup(label_a, label_b, label_c)
        
        # Area labels for squares
        area_a = MathTex("a^2", color=BLUE).move_to(square_a)
        area_b = MathTex("b^2", color=GREEN).move_to(square_b)
        area_c = MathTex("c^2", color=RED).move_to(square_c)
        area_labels = VGroup(area_a, area_b, area_c)
        
        # Main equation
        equation = MathTex("a^2 + b^2 = c^2", color=BLACK).scale(1.5)
        
        # --- Positioning ---
        # Center the visual elements and position equation below
        visual_elements = VGroup(triangle, squares, side_labels, area_labels)
        visual_elements.center()
        equation.next_to(visual_elements, DOWN, buff=0.5)
        
        # --- Animation Sequence ---
        # 1. Draw triangle starting from right angle
        self.play(Create(side_a), run_time=1)
        self.play(Create(side_b), run_time=1)
        self.play(Create(side_c), run_time=1)
        
        # 2. Build squares outward with smooth animation
        self.play(
            Create(square_a),
            Create(square_b),
            Create(square_c),
            run_time=2
        )
        
        # 3. Add side labels
        self.play(Write(side_labels), run_time=1)
        
        # 4. Add area labels
        self.play(Write(area_labels), run_time=1)
        
        # 5. Fade in the equation below
        self.play(Write(equation), run_time=1.5)
        
        # 6. Pulse squares to emphasize area relationship
        self.play(
            squares.animate.set_fill(opacity=0.6),
            rate_func=there_and_back,
            run_time=2
        )
        
        # 7. Camera zoom to focus on triangle relationship
        # Scale the visual elements to create a zoom effect
        self.play(
            visual_elements.animate.scale(1.4),
            equation.animate.scale(1.4),
            run_time=2
        )
        
        self.wait(0.5)
