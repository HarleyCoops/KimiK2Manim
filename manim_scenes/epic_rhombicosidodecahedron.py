from manim import *

import numpy as np

from math import sqrt


class EpicRhombicosidodecahedron(ThreeDScene):
    """
    Epic Rhombicosidodecahedron animation enhanced with KimiK2 pipeline.
    
    Visual Design: A large rhombicosidodecahedron rotating in 3D space, showing its 62 faces clearly - triangular faces...
    Color Scheme: Gold for triangular faces, silver for square faces, deep blue for pentagonal faces, white for edges and equations, with subtle glow effects
    Animation: The rhombicosidodecahedron slowly rotates on multiple axes while individual face types pulse with subtle light - triangles glow brighter gold, squares shimmer silver, and pentagons pulse deep blue. The equations fade in sequentially as the corresponding geometric features are highlighted. Camera gently orbits around the polyhedron to show all angles.
    Camera: Smooth orbital camera movement around the rotating polyhedron, occasionally zooming in to highlight specific face configurations
    """

    def construct(self):
        # Epic Configuration - Enhanced Background
        self.camera.background_color = BLACK
        
        # Constants from McCooey's data
        C0 = (1 + sqrt(5)) / 4
        C1 = (3 + sqrt(5)) / 4
        C2 = (1 + sqrt(5)) / 2
        C3 = (5 + sqrt(5)) / 4
        C4 = (2 + sqrt(5)) / 2

        # Vertex data
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

        # Face data
        faces = [
            # Pentagons (first 12 faces)
            [24, 52, 16, 20, 56], [25, 57, 21, 17, 53], [26, 58, 22, 18, 54],
            [27, 55, 19, 23, 59], [28, 36,  0,  2, 38], [29, 39,  3,  1, 37],
            [30, 42,  6,  4, 40], [31, 41,  5,  7, 43], [32, 44,  8,  9, 45],
            [33, 47, 11, 10, 46], [34, 49, 13, 12, 48], [35, 50, 14, 15, 51],
            # Squares (next 30 faces)
            [ 0, 36, 52, 24], [ 1, 25, 53, 37], [ 2, 26, 54, 38], [ 3, 39, 55, 27],
            [ 4, 24, 56, 40], [ 5, 41, 57, 25], [ 6, 42, 58, 26], [ 7, 27, 59, 43],
            [ 8, 44, 36, 28], [ 9, 29, 37, 45], [10, 28, 38, 46], [11, 47, 39, 29],
            [12, 30, 40, 48], [13, 49, 41, 31], [14, 50, 42, 30], [15, 31, 43, 51],
            [16, 52, 44, 32], [17, 32, 45, 53], [18, 33, 46, 54], [19, 55, 47, 33],
            [20, 34, 48, 56], [21, 57, 49, 34], [22, 58, 50, 35], [23, 35, 51, 59],
            [ 0,  4,  6,  2], [ 1,  3,  7,  5], [ 8, 10, 11,  9],
            [12, 13, 15, 14], [16, 17, 21, 20], [18, 22, 23, 19],
            # Triangles (last 20 faces)
            [24,  4,  0], [25,  1,  5], [26,  2,  6], [27,  7,  3],
            [28, 10,  8], [29,  9, 11], [30, 12, 14], [31, 15, 13],
            [32, 17, 16], [33, 18, 19], [34, 20, 21], [35, 23, 22],
            [36, 44, 52], [37, 53, 45], [38, 54, 46], [39, 47, 55],
            [40, 56, 48], [41, 49, 57], [42, 50, 58], [43, 59, 51]
        ]

        # Create edge groups
        pentagon_edges = set()
        square_edges = set()
        triangle_edges = set()
        all_edges = set()

        for i, face in enumerate(faces):
            n = len(face)
            face_type = "pentagon" if i < 12 else "square" if i < 42 else "triangle"
            for j in range(n):
                v1, v2 = sorted([face[j], face[(j+1)%n]])
                edge = (v1, v2)
                if edge not in all_edges:
                    all_edges.add(edge)
                    if face_type == "pentagon":
                        pentagon_edges.add(edge)
                    elif face_type == "square":
                        square_edges.add(edge)
                    else:
                        triangle_edges.add(edge)

        def create_edges(edges, color, stroke_width, glow=False):
            group = VGroup()
            for (v1, v2) in edges:
                line = Line3D(
                    start=vertices[v1],
                    end=vertices[v2],
                    color=color,
                    stroke_width=stroke_width,
                    stroke_opacity=0.95
                )
                if glow:
                    # Add glow effect
                    glow_line = Line3D(
                        start=vertices[v1],
                        end=vertices[v2],
                        color=color,
                        stroke_width=stroke_width * 2.5,
                        stroke_opacity=0.2
                    )
                    group.add(glow_line)
                group.add(line)
            return group

        # Enhanced colors based on KimiK2 recommendations
        # Apply color scheme: Gold for triangular faces, silver for square faces, deep blue for pentagonal faces, white for edges and equations, with subtle glow effects
        pentagons = create_edges(pentagon_edges, GOLD, 3.0, glow=True)
        squares = create_edges(square_edges, BLUE, 2.5, glow=True)
        triangles = create_edges(triangle_edges, RED, 2.0, glow=True)

        # Enhanced glowing vertices with pulsing effect
        vertex_group = VGroup()
        for v in vertices:
            # Outer glow
            outer_halo = Sphere(
                radius=0.2,
                color=WHITE,
                resolution=(12, 12)
            ).set_opacity(0.1).move_to(v)
            
            # Middle glow
            middle_halo = Sphere(
                radius=0.12,
                color=YELLOW,
                resolution=(12, 12)
            ).set_opacity(0.3).move_to(v)
            
            # Core
            core = Sphere(
                radius=0.08,
                color=WHITE,
                resolution=(12, 12)
            ).move_to(v)
            
            vertex_group.add(outer_halo, middle_halo, core)

        # Build final object
        polyhedron = VGroup(pentagons, squares, triangles, vertex_group)
        polyhedron.scale(2.2).move_to(ORIGIN)

        # Epic camera setup with dynamic movement
        # Camera movement: Smooth orbital camera movement around the rotating polyhedron, occasionally zooming in to highlight specific face configurations
        self.set_camera_orientation(
            phi=70 * DEGREES,
            theta=-45 * DEGREES,
            distance=10,
            frame_center=ORIGIN
        )
        self.camera.set_zoom(1.8)

        # Enhanced animated rotation with multiple axes
        rotation_speed = 0.8
        polyhedron.add_updater(lambda m, dt: m.rotate(
            rotation_speed * dt,
            axis=normalize(
                np.sin(self.time * 0.4) * UP +
                np.cos(self.time * 0.3) * RIGHT +
                np.sin(self.time * 0.2) * OUT
            )
        ))

        # Epic background with gradient and stars
        bg = FullScreenRectangle()
        bg.set_color([BLACK, "#001122", "#002244", "#001122", BLACK])
        bg.set_opacity(1)
        
        # Add starfield effect
        stars = VGroup()
        for _ in range(100):
            star = Dot(
                point=np.array([
                    np.random.uniform(-7, 7),
                    np.random.uniform(-4, 4),
                    np.random.uniform(-5, 5)
                ]),
                radius=0.02,
                color=WHITE
            ).set_opacity(np.random.uniform(0.3, 0.8))
            stars.add(star)
        
        stars.add_updater(lambda m, dt: m.rotate(
            0.1 * dt,
            axis=UP
        ))

        # Add title if equations are available
        title_group = VGroup()
        if equations:
            title = Text("Rhombicosidodecahedron", font_size=48, color=GOLD)
            title.to_edge(UP, buff=0.5)
            title_group.add(title)

        # Animation sequence - Epic entrance
        # Animation: The rhombicosidodecahedron slowly rotates on multiple axes while individual face types pulse with subtle light - triangles glow brighter gold, squares shimmer silver, and pentagons pulse deep blue. The equations fade in sequentially as the corresponding geometric features are highlighted. Camera gently orbits around the polyhedron to show all angles.
        self.add(bg, stars)
        
        # Fade in stars
        self.play(FadeIn(stars), run_time=2)
        
        # Epic reveal of polyhedron
        polyhedron.set_opacity(0)
        self.play(
            FadeIn(polyhedron),
            FadeIn(title_group),
            run_time=4,
            rate_func=smooth
        )
        
        # Dynamic camera movement
        self.play(
            self.camera.frame.animate.set_zoom(1.5),
            run_time=3
        )
        
        # Rotate camera around
        self.play(
            self.camera.frame.animate.rotate(PI/4, axis=UP),
            run_time=5
        )
        
        # Main rotation sequence
        self.wait(12)
        
        # Zoom in for detail
        self.play(
            self.camera.frame.animate.set_zoom(2.5),
            run_time=3
        )
        
        self.wait(5)
        
        # Pull back
        self.play(
            self.camera.frame.animate.set_zoom(1.2),
            run_time=3
        )
        
        self.wait(3)
        
        # Epic exit
        self.play(
            FadeOut(polyhedron),
            FadeOut(title_group),
            run_time=4,
            rate_func=smooth
        )
        
        self.wait(1)


def normalize(v):
    return v / np.linalg.norm(v)
