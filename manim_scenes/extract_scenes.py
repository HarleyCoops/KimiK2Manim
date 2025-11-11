#!/usr/bin/env python3
"""
Extract and render all Scene classes from a Manim file.

This script:
1. Parses a Python file to find all Scene classes
2. Renders each class separately as MP4 files
3. Uses Manim CLI to render each scene
"""

import ast
import subprocess
import sys
from pathlib import Path
from typing import List


def find_scene_classes(file_path: Path) -> List[str]:
    """
    Parse Python file and find all Scene class names.
    
    Args:
        file_path: Path to Python file
        
    Returns:
        List of class names that inherit from Scene
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        source = f.read()
    
    tree = ast.parse(source)
    scene_classes = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            # Check if class inherits from Scene
            for base in node.bases:
                if isinstance(base, ast.Name) and base.id == 'Scene':
                    scene_classes.append(node.name)
                elif isinstance(base, ast.Attribute):
                    # Handle cases like ThreeDScene, MovingCameraScene, etc.
                    if base.attr == 'Scene' or 'Scene' in base.attr:
                        scene_classes.append(node.name)
    
    return scene_classes


def render_scene(file_path: Path, scene_name: str, quality: str = 'ql'):
    """
    Render a specific Scene class using Manim CLI.
    
    Args:
        file_path: Path to Python file containing the scene
        scene_name: Name of the Scene class to render
        quality: Quality setting ('ql' for low, 'qm' for medium, 'qh' for high)
    """
    print(f"\n{'='*70}")
    print(f"Rendering: {scene_name}")
    print(f"{'='*70}")
    
    # Build manim command
    cmd = [
        'manim',
        f'-p{quality}',  # Preview and quality
        str(file_path),
        scene_name
    ]
    
    print(f"Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=False,  # Show output in real-time
            text=True
        )
        print(f"\n[OK] Successfully rendered {scene_name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n[FAIL] Failed to render {scene_name}: {e}")
        return False
    except FileNotFoundError:
        print("\n[FAIL] Error: 'manim' command not found")
        print("   Make sure Manim is installed and in your PATH")
        print("   Or use: uv run manim ...")
        return False


def main():
    """Main function to extract and render all Scene classes."""
    if len(sys.argv) < 2:
        print("Usage: python extract_scenes.py <manim_file.py> [quality]")
        print("\nQuality options:")
        print("  ql - Low quality (fast, preview)")
        print("  qm - Medium quality")
        print("  qh - High quality (slow, best)")
        print("\nExample:")
        print("  python extract_scenes.py KimiNewton.py ql")
        sys.exit(1)
    
    file_path = Path(sys.argv[1])
    quality = sys.argv[2] if len(sys.argv) > 2 else 'ql'
    
    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        sys.exit(1)
    
    print(f"\n{'='*70}")
    print(f"Extracting Scene classes from: {file_path}")
    print(f"{'='*70}")
    
    # Find all Scene classes
    scene_classes = find_scene_classes(file_path)
    
    if not scene_classes:
        print("\n✗ No Scene classes found in file")
        print("   Make sure your classes inherit from Scene, ThreeDScene, etc.")
        sys.exit(1)
    
    print(f"\nFound {len(scene_classes)} Scene class(es):")
    for i, cls_name in enumerate(scene_classes, 1):
        print(f"  {i}. {cls_name}")
    
    # Render each scene
    print(f"\n{'='*70}")
    print(f"Rendering {len(scene_classes)} scene(s) with quality: {quality}")
    print(f"{'='*70}")
    
    success_count = 0
    for scene_name in scene_classes:
        if render_scene(file_path, scene_name, quality):
            success_count += 1
    
    # Summary
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    print(f"Total scenes: {len(scene_classes)}")
    print(f"Successfully rendered: {success_count}")
    print(f"Failed: {len(scene_classes) - success_count}")
    
    if success_count > 0:
        print(f"\n[OK] Rendered videos saved to: media/videos/{file_path.stem}/")
    
    print()


if __name__ == "__main__":
    main()

