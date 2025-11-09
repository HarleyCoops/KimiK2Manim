# Ultimate Artistic Rhombicosidodecahedron - Fractal Edition
# Render with: manim -pql this_file.py UltimateArtisticRhombicosidodecahedron

from manim import *
import numpy as np
from math import sqrt

class UltimateArtisticRhombicosidodecahedron(ThreeDScene):
    def construct(self):
        # Configuration
        self.camera.background_color = "#000814"
        config.disable_caching = False
        config.frame_rate = 30
        
        # Constants from McCooey's data
        C0 = (1 + sqrt(5)) / 4
        C1 = (3 + sqrt(5)) / 4
        C2 = (1 + sqrt(5)) / 2
        C3 = (5 + sqrt(5)) / 4
        C4 = (2 + sqrt(5)) / 2

        # Vertex data (60 vertices)
        vertices = [
            np.array([ 0.5,  0.5,   C4]),  # V0
            np.array([ 0.5,  0.5,  -C4]),  # V1
            np.array([ 0.5, -0.5,   C4]),  # V2
            np.array([ 0.5, -0.5,  -C4]),  # V3
            np.array([-0.5,  0.5,   C4]),  # V4
            np.array([-0.5,  0.5,  -C4]),  # V5
            np.array([-0.5, -0.5,   C4]),  # V6
            np.array([-0.5, -0.5,  -C4]),  # V7
            np.array([  C4,  0.5,  0.5]),  # V8
            np.array([  C4,  0.5, -0.5]),  # V9
            np.array([  C4, -0.5,  0.5]),  # V10
            np.array([  C4, -0.5, -0.5]),  # V11
            np.array([ -C4,  0.5,  0.5]),  # V12
            np.array([ -C4,  0.5, -0.5]),  # V13
            np.array([ -C4, -0.5,  0.5]),  # V14
            np.array([ -C4, -0.5, -0.5]),  # V15
            np.array([ 0.5,   C4,  0.5]),  # V16
            np.array([ 0.5,   C4, -0.5]),  # V17
            np.array([ 0.5,  -C4,  0.5]),  # V18
            np.array([ 0.5,  -C4, -0.5]),  # V19
            np.array([-0.5,   C4,  0.5]),  # V20
            np.array([-0.5,   C4, -0.5]),  # V21
            np.array([-0.5,  -C4,  0.5]),  # V22
            np.array([-0.5,  -C4, -0.5]),  # V23
            np.array([ 0.0,   C1,   C3]),  # V24
            np.array([ 0.0,   C1,  -C3]),  # V25
            np.array([ 0.0,  -C1,   C3]),  # V26
            np.array([ 0.0,  -C1,  -C3]),  # V27
            np.array([  C3,  0.0,   C1]),  # V28
            np.array([  C3,  0.0,  -C1]),  # V29
            np.array([ -C3,  0.0,   C1]),  # V30
            np.array([ -C3,  0.0,  -C1]),  # V31
            np.array([  C1,   C3,  0.0]),  # V32
            np.array([  C1,  -C3,  0.0]),  # V33
            np.array([ -C1,   C3,  0.0]),  # V34
            np.array([ -C1,  -C3,  0.0]),  # V35
            np.array([  C1,   C0,   C2]),  # V36
            np.array([  C1,   C0,  -C2]),  # V37
            np.array([  C1,  -C0,   C2]),  # V38
            np.array([  C1,  -C0,  -C2]),  # V39
            np.array([ -C1,   C0,   C2]),  # V40
            np.array([ -C1,   C0,  -C2]),  # V41
            np.array([ -C1,  -C0,   C2]),  # V42
            np.array([ -C1,  -C0,  -C2]),  # V43
            np.array([  C2,   C1,   C0]),  # V44
            np.array([  C2,   C1,  -C0]),  # V45
            np.array([  C2,  -C1,   C0]),  # V46
            np.array([  C2,  -C1,  -C0]),  # V47
            np.array([ -C2,   C1,   C0]),  # V48
            np.array([ -C2,   C1,  -C0]),  # V49
            np.array([ -C2,  -C1,   C0]),  # V50
            np.array([ -C2,  -C1,  -C0]),  # V51
            np.array([  C0,   C2,   C1]),  # V52
            np.array([  C0,   C2,  -C1]),  # V53
            np.array([  C0,  -C2,   C1]),  # V54
            np.array([  C0,  -C2,  -C1]),  # V55
            np.array([ -C0,   C2,   C1]),  # V56
            np.array([ -C0,   C2,  -C1]),  # V57
            np.array([ -C0,  -C2,   C1]),  # V58
            np.array([ -C0,  -C2,  -C1]),  # V59
        ]

        # Face data (62 faces: 12 pentagons, 30 squares, 20 triangles)
        faces = [
            # Pentagons
            [24, 52, 16, 20, 56], [25, 57, 21, 17, 53], [26, 58, 22, 18, 54],
            [27, 55, 19, 23, 59], [28, 36,  0,  2, 38], [29, 39,  3,  1, 37],
            [30, 42,  6,  4, 40], [31, 41,  5,  7, 43], [32, 44,  8,  9, 45],
            [33, 47, 11, 10, 46], [34, 49, 13, 12, 48], [35, 50, 14, 15, 51],
            # Squares
            [ 0, 36, 52, 24], [ 1, 25, 53, 37], [ 2, 26, 54, 38], [ 3, 39, 55, 27],
            [ 4, 24, 56, 40], [ 5, 41, 57, 25], [ 6, 42, 58, 26], [ 7, 27, 59, 43],
            [ 8, 44, 36, 28], [ 9, 29, 37, 45], [10, 28, 38, 46], [11, 47, 39, 29],
            [12, 30, 40, 48], [13, 49, 41, 31], [14, 50, 42, 30], [15, 31, 43, 51],
            [16, 52, 44, 32], [17, 32, 45, 53], [18, 33, 46, 54], [19, 55, 47, 33],
            [20, 34, 48, 56], [21, 57, 49, 34], [22, 58, 50, 35], [23, 35, 51, 59],
            [ 0,  4,  6,  2], [ 1,  3,  7,  5], [ 8, 10, 11,  9],
            [12, 13, 15, 14], [16, 17, 21, 20], [18, 22, 23, 19],
            # Triangles
            [24,  4,  0], [25,  1,  5], [26,  2,  6], [27,  7,  3],
            [28, 10,  8], [29,  9, 11], [30, 12, 14], [31, 15, 13],
            [32, 17, 16], [33, 18, 19], [34, 20, 21], [35, 23, 22],
            [36, 44, 52], [37, 53, 45], [38, 54, 46], [39, 47, 55],
            [40, 56, 48], [41, 49, 57], [42, 50, 58], [43, 59, 51]
        ]

        # Create edge sets by face type
        pentagon_edges, square_edges, triangle_edges = set(), set(), set()
        all_edges = set()

        for i, face in enumerate(faces):
            n = len(face)
            for j in range(n):
                v1, v2 = sorted([face[j], face[(j+1)%n]])
                edge = (v1, v2)
                if edge not in all_edges:
                    all_edges.add(edge)
                    if i < 12: pentagon_edges.add(edge)
                    elif i < 42: square_edges.add(edge)
                    else: triangle_edges.add(edge)

        # **1. FRACTAL HIERARCHY**
        master_group = VGroup()
        scales = [2.0, 0.6, 0.18]  # 3 iterations for performance
        opacities = [1.0, 0.6, 0.3]
        
        for i, (scale, opacity) in enumerate(zip(scales, opacities)):
            poly = self.create_enhanced_polyhedron(
                vertices, 
                pentagon_edges, 
                square_edges, 
                triangle_edges,
                scale=scale,
                opacity=opacity,
                iteration=i
            )
            # Offset inner iterations for visual depth
            if i > 0:
                poly.shift(i * 0.5 * OUT)
            master_group.add(poly)

        # **2. ATMOSPHERIC LIGHTING**
        lights = self.create_dynamic_lights()
        
        # **3. NEBULA BACKGROUND**
        nebula = self.create_nebula_background()

        # **4. INITIAL CAMERA SETUP**
        self.setup_cinematic_camera()

        # Composition
        self.add(nebula, lights, master_group)

        # **5. ANIMATION SEQUENCES**
        # Phase 1: Emergence (0-5s)
        self.play(LaggedStart(
            *[Write(p, stroke_width=0.1) for p in master_group],
            lag_ratio=0.4
        ), run_time=5)

        # Phase 2: Fractal breathing & rotation (5-18s)
        master_group.add_updater(lambda m, dt: self.fractal_breath(m, dt))
        self.wait(13)

        # Phase 3: Camera journey (18-25s)
        self.execute_camera_journey()

        # Phase 4: Dissolution (25-28s)
        self.play(
            master_group.animate.scale(0).set_opacity(0),
            nebula.animate.set_opacity(0),
            run_time=3,
            rate_func=rate_functions.ease_in_cubic
        )
        self.wait(1)

    def create_enhanced_polyhedron(self, vertices, pentagon_edges, square_edges, triangle_edges, 
                                   scale=1.0, opacity=1.0, iteration=0):
        """Factory for polyhedron at different scales with gradient effects"""
        
        def create_gradient_edges(edges, color_palette, stroke_width):
            group = VGroup()
            for idx, (v1, v2) in enumerate(edges):
                # Create color gradient with iteration-specific hue shift
                base_color = color_palette[idx % len(color_palette)]
                shifted_color = interpolate_color(base_color, WHITE, iteration * 0.3)
                
                line = Line3D(
                    start=vertices[v1] * scale,
                    end=vertices[v2] * scale,
                    color=shifted_color,
                    stroke_width=stroke_width * (1 - iteration * 0.2),
                    stroke_opacity=0.9 * opacity
                )
                
                # **PULSE EFFECT** - varying stroke width over time
                line.add_updater(lambda l, dt, base=stroke_width, i=iteration: 
                    l.set_stroke(width=base * (1 + 0.3 * np.sin(self.time * 4 + i))))
                group.add(line)
            return group

        # Color palettes for each iteration
        pentagon_colors = [ORANGE, GOLD_A, MAROON_A, PURE_RED]
        square_colors = [TEAL_E, BLUE_B, GREEN_B, PURPLE_B]
        triangle_colors = [PINK, LAVENDER, PURPLE_A, LIGHT_PINK]

        pentagons = create_gradient_edges(pentagon_edges, pentagon_colors, 2.5)
        squares = create_gradient_edges(square_edges, square_colors, 2.0)
        triangles = create_gradient_edges(triangle_edges, triangle_colors, 1.5)

        # **GLOWING VERTICES** with iteration-specific size
        vertex_group = VGroup()
        for v in vertices:
            core = Sphere(radius=0.05 * scale, color=WHITE, resolution=(6, 6)).move_to(v * scale)
            halo = Sphere(radius=0.12 * scale, color=WHITE, resolution=(6, 6)).set_opacity(0.12 * opacity).move_to(v * scale)
            vertex_group.add(core, halo)

        return VGroup(pentagons, squares, triangles, vertex_group)

    def create_dynamic_lights(self):
        """Setup moving lights with different intensities and colors"""
        # Key light - bright, moves in circular pattern
        key_light = PointLight(
            color=BLUE_B,
            intensity=2.5,
            distance=25,
            shadow_softness=0.3
        ).move_to(6 * UP + 4 * RIGHT)
        
        # Rim light - dramatic edge illumination
        rim_light = PointLight(
            color=RED_B,
            intensity=1.8,
            distance=30,
            shadow_softness=0.5
        ).move_to(6 * OUT + 5 * LEFT)
        
        # Fill light - soft ambient
        fill_light = AmbientLight(color=WHITE, intensity=0.25)
        
        # **ANIMATED LIGHT MOVEMENT**
        key_light.add_updater(lambda l, dt: l.move_to(
            6 * np.array([np.sin(self.time * 0.4), np.cos(self.time * 0.3), 0.4]) + 4 * RIGHT
        ))
        
        rim_light.add_updater(lambda l, dt: l.move_to(
            6 * np.array([np.cos(self.time * 0.35), np.sin(self.time * 0.5), 1]) + 5 * LEFT
        ))
        
        return VGroup(key_light, rim_light, fill_light)

    def create_nebula_background(self):
        """Create atmospheric background gradient"""
        return FullScreenRectangle().set_color(
            color_gradient(["#000814", "#001d3d", "#003566", "#000814"], 4)
        ).set_opacity(0.5).scale(1.5)

    def setup_cinematic_camera(self):
        """Initial camera setup with orbital motion"""
        self.set_camera_orientation(
            phi=65 * DEGREES,
            theta=-45 * DEGREES,
            distance=10,
            frame_center=ORIGIN
        )
        # Slow continuous orbital rotation
        self.camera.add_updater(lambda c, dt: c.increment_theta(0.08 * dt))

    def fractal_breath(self, group, dt):
        """Complex breathing pattern with phase differences for each iteration"""
        time = self.time
        
        for i, poly in enumerate(group):
            # Each iteration breathes at different frequency/phase
            breath_scale = 1 + 0.04 * np.sin(2 * time + i * PI / 3)
            current_scale = poly.scale_factor if hasattr(poly, 'scale_factor') else 1.0
            
            # Apply new scale relative to original
            poly.scale(breath_scale / current_scale)
            poly.scale_factor = breath_scale
            
            # **INDIVIDUAL ROTATION** for inner iterations
            if i > 0:
                poly.rotate(dt * (1 + i * 0.5), axis=OUT)

    def execute_camera_journey(self):
        """Execute dramatic camera movement sequence"""
        # Clear existing updater for controlled movement
        self.camera.clear_updaters()
        
        # **DOLLY ZOOM** - approach while widening FOV effect
        self.play(
            self.camera.animate.set_distance(4).set_phi(40 * DEGREES),
            run_time=4,
            rate_func=rate_functions.ease_in_out_quad
        )
        
        # **ORBITAL SWING** around the object
        def orbital_swing():
            for i in range(90):  # 3 seconds at 30fps
                angle = self.time * 0.3
                radius = 4
                self.camera.move_to(np.array([
                    radius * np.cos(angle),
                    radius * np.sin(angle),
                    2 * np.sin(angle * 2)
                ]))
                self.camera.look_at(ORIGIN)
                self.wait(1/30)
        
        orbital_swing()
        
        # **FINAL DRAMATIC ZOOM** into core
        self.play(
            self.camera.animate.set_distance(2).set_phi(25 * DEGREES),
            run_time=3,
            rate_func=rate_functions.ease_in_expo
        )
        self.wait(2)


def normalize(v):
    """Helper function for vector normalization"""
    return v / np.linalg.norm(v)