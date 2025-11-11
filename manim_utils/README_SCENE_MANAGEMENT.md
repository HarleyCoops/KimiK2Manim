# Scene Management Documentation

## Problem: Text/Equation Overlaps

Manim scenes often have overlapping text and equations because:
1. No automatic cleanup of old content
2. No layer management for different text types
3. Manual positioning leads to overlaps
4. Explanatory text accumulates without removal

## Solution: Scene Management System

A complete scene management system that:
- **Tracks active content** by layer (title, explanation, equation, etc.)
- **Automatically removes** old content when new content is added
- **Prevents overlaps** through automatic positioning
- **Manages transitions** between sections

## Components

### 1. **SceneManager** (`scene_manager.py`)
Core management class that:
- Tracks active content by layer
- Handles fade-out transitions
- Prevents overlaps
- Manages content lifecycle

### 2. **ManagedBoundedScene** (`managed_scene.py`)
Complete scene class combining:
- Boundary constraints (from BoundedScene)
- Scene management (from SceneManager)
- Convenient methods for common operations

## Usage

### Basic Example

```python
from manim_utils.managed_scene import ManagedBoundedScene

class MyScene(ManagedBoundedScene):
    def construct(self):
        # Title automatically replaces previous titles
        title = self.add_title("My Title")
        self.play(Write(title))
        
        # Explanation automatically replaces previous explanations
        explanation = self.add_explanation("This is an explanation")
        self.play(FadeIn(explanation))
        
        # Equation automatically replaces previous equations
        eq = self.add_equation(r"E = mc^2")
        self.play(Write(eq))
        
        # Transition to new section (clears old content)
        self.transition_section("New Section")
```

### Key Methods

#### `add_title(text, fade_out_previous=True)`
Adds a title at the top. Automatically replaces previous titles.

#### `add_explanation(text, fade_out_previous=True, position=None)`
Adds explanatory text. Automatically replaces previous explanations.
- `position`: 'top', 'center', 'bottom', etc.

#### `add_equation(equation, fade_out_previous=True, position=None)`
Adds an equation. Automatically replaces previous equations.

#### `transition_section(new_title=None, keep_equations=False, fade_time=1.0)`
Transitions to a new section:
- Clears old explanatory text
- Optionally keeps equations visible
- Optionally sets new title

#### `clear_explanations(fade_out=True)`
Clears all explanatory text.

#### `clear_equations(fade_out=True)`
Clears all equations.

#### `clear_all_text(fade_out=True, keep_title=False)`
Clears all text content.

## Text Layers

Content is organized into layers:

- **TITLE**: Top of screen (-3.5 to -3.0)
- **SUBTITLE**: Below title (-2.5 to -2.0)
- **EQUATION**: Center zone (-1.0 to 1.0)
- **EXPLANATION**: Below equation (1.5 to 2.5)
- **LABEL**: Bottom zone (3.0 to 3.5)
- **ANNOTATION**: Floating (no fixed zone)

Each layer has its own vertical zone to prevent overlaps.

## Example: Section Transitions

```python
def section_one(self):
    # Add content
    self.add_title("Section 1")
    self.add_explanation("Explanation for section 1")
    self.add_equation(r"x^2 + y^2 = r^2")
    
    self.wait(3)
    
    # Transition to next section
    # Automatically clears explanations, keeps title if desired
    self.transition_section(
        new_title="Section 2",
        keep_equations=False,  # Clear equations too
        fade_time=1.5
    )

def section_two(self):
    # New content automatically positioned correctly
    self.add_explanation("Explanation for section 2")
    self.add_equation(r"E = \frac{1}{2}mv^2")
```

## Benefits

1. **No Overlaps**: Automatic positioning prevents text overlap
2. **Clean Transitions**: Old content automatically removed
3. **Layer Management**: Different text types in separate zones
4. **Easy to Use**: Simple methods replace manual management
5. **Consistent Layout**: Predictable positioning

## Migration Guide

### Before (Manual Management)
```python
class MyScene(Scene):
    def construct(self):
        title = Text("Title")
        explanation = Text("Explanation")
        equation = MathTex(r"x^2")
        
        # Manual positioning - may overlap!
        title.to_edge(UP)
        explanation.next_to(title, DOWN)
        equation.move_to(ORIGIN)
        
        # Manual cleanup - easy to forget!
        self.play(FadeOut(explanation))  # Must remember to remove
```

### After (Automatic Management)
```python
from manim_utils.managed_scene import ManagedBoundedScene

class MyScene(ManagedBoundedScene):
    def construct(self):
        # Automatic positioning, no overlaps
        title = self.add_title("Title")
        explanation = self.add_explanation("Explanation")
        equation = self.add_equation(r"x^2")
        
        # Automatic cleanup when adding new content
        new_explanation = self.add_explanation("New explanation")
        # Old explanation automatically removed!
```

## Complete Example

See `BrownianMotion/brownian_motion_managed.py` for a full example showing:
- Section transitions
- Automatic text management
- Overlap prevention
- Clean content lifecycle

