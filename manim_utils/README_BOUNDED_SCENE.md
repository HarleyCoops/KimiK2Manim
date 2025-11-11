# Manim Frame Boundary Solution

## The Universal Problem

Manim renders content outside frame boundaries because:
- Default frame: **14.2 units wide × 8 units tall** (16:9 aspect ratio)
- Objects can easily exceed these bounds with large font sizes or absolute coordinates
- No automatic boundary checking exists
- Content gets cut off or extends beyond visible area

## The Solution

A comprehensive system to automatically constrain all content within safe frame boundaries:

### 1. **BoundedScene Base Class** (`manim_utils/bounded_scene.py`)

A base Scene class that provides:
- `bounded_text()` - Text that auto-scales to fit
- `bounded_math_tex()` - MathTex that auto-scales to fit
- `bounded_vgroup()` - VGroups constrained to boundaries
- `constrain_to_safe_area()` - Constrain any mobject
- `safe_position()` - Position mobjects safely
- `create_safe_axes()` - Axes that fit within boundaries

### 2. **Frame Configuration** (`manim_utils/frame_config.py`)

Centralized constants:
- Frame dimensions (14.2 × 8.0)
- Safe area (90% of frame = 12.78 × 7.2)
- Coordinate boundaries
- Default font sizes

### 3. **Safe Boundaries**

```
Full Frame:     14.2 × 8.0 units
Safe Area:      12.78 × 7.2 units (90% margin)
X Range:         -7.1 to +7.1 (full), -6.39 to +6.39 (safe)
Y Range:        -4.0 to +4.0 (full), -3.6 to +3.6 (safe)
```

## Usage

### Basic Example

```python
from manim_utils.bounded_scene import BoundedScene

class MyScene(BoundedScene):
    def construct(self):
        # Title automatically fits
        title = self.bounded_text(
            "My Very Long Title That Would Overflow",
            font_size=48,
            color=GOLD
        )
        self.safe_position(title, position='top')
        
        # Equation automatically fits
        eq = self.bounded_math_tex(
            r"\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}",
            font_size=60,
            color=WHITE
        )
        self.safe_position(eq, position='center')
        
        # Axes automatically fit
        axes = self.create_safe_axes(
            x_range=(-5, 5, 1),
            y_range=(-3, 3, 1)
        )
        
        self.play(Write(title), Write(eq), Create(axes))
```

### Position Options

```python
# Predefined positions
self.safe_position(mobject, position='top')
self.safe_position(mobject, position='bottom')
self.safe_position(mobject, position='left')
self.safe_position(mobject, position='right')
self.safe_position(mobject, position='center')
self.safe_position(mobject, position='top_left')
self.safe_position(mobject, position='top_right')
self.safe_position(mobject, position='bottom_left')
self.safe_position(mobject, position='bottom_right')

# Custom coordinates (automatically clamped)
self.safe_position(mobject, x=5.0, y=3.0)
```

### Constraining Existing Objects

```python
# Constrain any mobject
from manim_utils.bounded_scene import constrain_mobject

my_object = Text("Some text", font_size=100)
my_object = constrain_mobject(my_object)  # Auto-scales to fit
```

## Key Methods

### `bounded_text(text, font_size, max_width, max_height, **kwargs)`
Creates text that automatically scales down if too large.

### `bounded_math_tex(tex_string, font_size, max_width, max_height, **kwargs)`
Creates MathTex that automatically scales down if too large.

### `constrain_to_safe_area(mobject)`
Scales and repositions a mobject to fit within safe boundaries.

### `safe_position(mobject, x, y, position)`
Positions a mobject safely, clamping coordinates to safe range.

### `create_safe_axes(x_range, y_range, width, height, **kwargs)`
Creates axes that fit within safe boundaries.

## Migration Guide

### Before (Unbounded)
```python
class MyScene(Scene):
    def construct(self):
        title = Text("Title", font_size=48)
        title.to_edge(UP)  # May overflow!
        
        eq = MathTex(r"x^2 + y^2 = r^2", font_size=80)
        eq.move_to(ORIGIN)  # May overflow!
```

### After (Bounded)
```python
from manim_utils.bounded_scene import BoundedScene

class MyScene(BoundedScene):
    def construct(self):
        title = self.bounded_text("Title", font_size=48)
        self.safe_position(title, position='top')  # Always fits!
        
        eq = self.bounded_math_tex(r"x^2 + y^2 = r^2", font_size=80)
        self.safe_position(eq, position='center')  # Always fits!
```

## Example: Brownian Motion Scene

See `BrownianMotion/brownian_motion_bounded.py` for a complete example showing:
- Bounded titles and subtitles
- Bounded equations
- Bounded axes and graphs
- Constrained particle positions
- Safe positioning throughout

## Benefits

1. **No Overflow**: Content never renders outside frame
2. **Automatic Scaling**: Large content auto-scales to fit
3. **Consistent Layout**: Safe positioning ensures consistency
4. **Easy Migration**: Simple to convert existing scenes
5. **Flexible**: Can still use absolute positioning when needed

## Technical Details

- Safe area is 90% of full frame (leaves 5% margin on each side)
- Scaling preserves aspect ratio
- Position clamping prevents edge cutoff
- Works with all Manim mobjects (Text, MathTex, VGroup, Axes, etc.)

## Testing

To test that content fits:

```python
# Add this to your scene's construct() method
def construct(self):
    # ... your content ...
    
    # Debug: Show safe boundaries
    safe_rect = Rectangle(
        width=SAFE_WIDTH,
        height=SAFE_HEIGHT,
        color=RED,
        stroke_width=2
    )
    safe_rect.set_fill(RED, opacity=0.1)
    self.add(safe_rect)  # Visual guide for safe area
```

## Future Enhancements

- [ ] Automatic font size calculation based on text length
- [ ] Smart layout algorithms for multiple objects
- [ ] Warning system for objects that need manual adjustment
- [ ] Support for custom frame sizes/aspect ratios

