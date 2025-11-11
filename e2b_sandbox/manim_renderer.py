"""
Manim Renderer for E2B Sandbox
Provides utilities for rendering Manim animations within the sandbox environment.
"""

import asyncio
import subprocess
import sys
from pathlib import Path
from typing import Optional, List, Dict
from datetime import datetime
import json

sys.path.insert(0, str(Path(__file__).parent.parent))

from logger import get_logger
from e2b_sandbox.sandbox_config import SandboxConfig

logger = get_logger()


class ManimRenderer:
    """Handles Manim rendering in E2B sandbox."""

    def __init__(self, config: SandboxConfig):
        """Initialize the Manim renderer."""
        self.config = config
        self.media_dir = Path(config.media_dir)
        self.render_history = []

    def render_scene(
        self,
        scene_file: Path,
        scene_class: str,
        quality: Optional[str] = None,
        format: str = "mp4",
        output_name: Optional[str] = None
    ) -> Dict:
        """
        Render a Manim scene.

        Args:
            scene_file: Path to the Python file containing the scene
            scene_class: Name of the scene class to render
            quality: Quality setting (l, m, h, k)
            format: Output format (mp4 or gif)
            output_name: Optional custom output name

        Returns:
            Dictionary containing render information
        """
        quality = quality or self.config.manim_quality
        start_time = datetime.now()

        logger.info(f"🎬 Rendering Manim scene")
        logger.info(f"  File: {scene_file.name}")
        logger.info(f"  Class: {scene_class}")
        logger.info(f"  Quality: {quality}")
        logger.info(f"  Format: {format}")

        # Construct manim command
        cmd = [
            "manim",
            f"-q{quality}",  # Quality flag
            f"-p" if format == "mp4" else "-i",  # Preview or save
            str(scene_file),
            scene_class
        ]

        # Add output name if specified
        if output_name:
            cmd.extend(["-o", output_name])

        logger.info(f"📝 Command: {' '.join(cmd)}")

        try:
            # Run manim command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.config.max_render_time,
                cwd=str(scene_file.parent)
            )

            elapsed = (datetime.now() - start_time).total_seconds()

            if result.returncode == 0:
                logger.info(f"✅ Render complete in {elapsed:.1f}s")

                # Find output file
                output_file = self._find_output_file(scene_file, scene_class, quality)

                render_info = {
                    "success": True,
                    "scene_file": str(scene_file),
                    "scene_class": scene_class,
                    "quality": quality,
                    "format": format,
                    "elapsed_seconds": elapsed,
                    "output_file": str(output_file) if output_file else None,
                    "timestamp": start_time.isoformat()
                }

                if output_file:
                    logger.info(f"📹 Output: {output_file}")

                self.render_history.append(render_info)
                return render_info
            else:
                logger.error(f"❌ Render failed")
                logger.error(f"Error: {result.stderr}")

                render_info = {
                    "success": False,
                    "scene_file": str(scene_file),
                    "scene_class": scene_class,
                    "error": result.stderr,
                    "elapsed_seconds": elapsed,
                    "timestamp": start_time.isoformat()
                }

                self.render_history.append(render_info)
                return render_info

        except subprocess.TimeoutExpired:
            logger.error(f"❌ Render timed out after {self.config.max_render_time}s")
            return {
                "success": False,
                "error": f"Timeout after {self.config.max_render_time}s",
                "scene_file": str(scene_file),
                "scene_class": scene_class
            }

        except Exception as e:
            logger.error(f"❌ Render failed with error: {e}")
            return {
                "success": False,
                "error": str(e),
                "scene_file": str(scene_file),
                "scene_class": scene_class
            }

    def _find_output_file(
        self,
        scene_file: Path,
        scene_class: str,
        quality: str
    ) -> Optional[Path]:
        """Find the rendered output file."""
        # Manim output structure: media/videos/{scene_file_stem}/{quality}/
        quality_map = {
            "l": "480p15",
            "m": "720p30",
            "h": "1080p60",
            "k": "2160p60"
        }

        quality_dir = quality_map.get(quality, "480p15")

        # Look in expected output directory
        video_dir = self.media_dir / "videos" / scene_file.stem / quality_dir

        if video_dir.exists():
            # Find .mp4 file
            mp4_files = list(video_dir.glob(f"{scene_class}.mp4"))
            if mp4_files:
                return mp4_files[0]

        return None

    def render_from_narrative(
        self,
        narrative: str,
        concept_name: str,
        generate_code: bool = True
    ) -> Dict:
        """
        Generate and render a Manim scene from a narrative.

        This is a more advanced feature that would require additional
        AI-driven code generation from the narrative.

        Args:
            narrative: The narrative describing the animation
            concept_name: Name of the concept for file naming
            generate_code: Whether to automatically generate code (requires additional AI)

        Returns:
            Dictionary containing render information
        """
        logger.info(f"🎨 Generating Manim code from narrative")
        logger.info(f"  Concept: {concept_name}")
        logger.info(f"  Narrative length: {len(narrative)} chars")

        if generate_code:
            logger.warning("⚠️  Automatic code generation not yet implemented")
            logger.info("💡 Use the narrative as a prompt for manual scene creation")

        # For now, save the narrative for manual implementation
        narrative_file = Path(self.config.output_dir) / f"{concept_name}_narrative.txt"
        with open(narrative_file, "w") as f:
            f.write(narrative)

        logger.info(f"📝 Narrative saved: {narrative_file}")

        return {
            "narrative_file": str(narrative_file),
            "concept": concept_name,
            "code_generation": "manual",
            "next_steps": [
                "Review the narrative",
                "Create a Manim scene class",
                "Use ManimRenderer.render_scene() to render"
            ]
        }

    def list_available_scenes(self, scenes_dir: Optional[Path] = None) -> List[Dict]:
        """
        List all available Manim scenes in the project.

        Args:
            scenes_dir: Directory to search for scenes (default: manim_scenes/)

        Returns:
            List of scene information dictionaries
        """
        if scenes_dir is None:
            scenes_dir = Path(__file__).parent.parent / "manim_scenes"

        logger.info(f"🔍 Scanning for Manim scenes in: {scenes_dir}")

        scenes = []

        for py_file in scenes_dir.glob("*.py"):
            if py_file.name.startswith("_") or py_file.name == "README.md":
                continue

            # Extract scene classes (simplified - could use AST parsing)
            scene_info = {
                "file": str(py_file),
                "filename": py_file.name,
                "classes": self._extract_scene_classes(py_file)
            }

            if scene_info["classes"]:
                scenes.append(scene_info)

        logger.info(f"✅ Found {len(scenes)} scene files")
        return scenes

    def _extract_scene_classes(self, file_path: Path) -> List[str]:
        """Extract scene class names from a Python file."""
        try:
            with open(file_path, "r") as f:
                content = f.read()

            # Simple regex-based extraction
            import re
            pattern = r"class\s+(\w+)\s*\([^)]*Scene[^)]*\)"
            matches = re.findall(pattern, content)

            return matches

        except Exception as e:
            logger.error(f"Failed to extract classes from {file_path}: {e}")
            return []

    def batch_render(
        self,
        scenes: List[tuple],
        quality: Optional[str] = None
    ) -> List[Dict]:
        """
        Render multiple scenes in batch.

        Args:
            scenes: List of (scene_file, scene_class) tuples
            quality: Quality setting for all renders

        Returns:
            List of render results
        """
        logger.info(f"🚀 Batch rendering {len(scenes)} scenes")

        results = []
        for scene_file, scene_class in scenes:
            result = self.render_scene(
                scene_file=Path(scene_file),
                scene_class=scene_class,
                quality=quality
            )
            results.append(result)

        # Summary
        successful = sum(1 for r in results if r.get("success"))
        failed = len(results) - successful

        logger.info(f"\n📊 Batch render complete")
        logger.info(f"  Successful: {successful}")
        logger.info(f"  Failed: {failed}")

        return results

    def save_render_history(self):
        """Save render history to a file."""
        history_file = Path(self.config.output_dir) / "render_history.json"

        with open(history_file, "w") as f:
            json.dump(self.render_history, f, indent=2)

        logger.info(f"💾 Render history saved: {history_file}")


async def main():
    """Demo the Manim renderer."""
    from e2b_sandbox.sandbox_config import setup_sandbox_environment

    logger.info("🎬 Manim Renderer Demo")
    logger.info("="*60)

    config = setup_sandbox_environment()
    renderer = ManimRenderer(config)

    # List available scenes
    scenes = renderer.list_available_scenes()

    logger.info("\n📋 Available scenes:")
    for scene in scenes:
        logger.info(f"\n  📄 {scene['filename']}")
        for class_name in scene['classes']:
            logger.info(f"    - {class_name}")

    # Example: Render one of the existing scenes
    if scenes:
        example_scene = scenes[0]
        if example_scene['classes']:
            logger.info(f"\n🎬 Rendering example scene...")
            result = renderer.render_scene(
                scene_file=Path(example_scene['file']),
                scene_class=example_scene['classes'][0],
                quality='l'  # Low quality for faster demo
            )

            logger.info("\n✅ Demo complete!")

    renderer.save_render_history()


if __name__ == "__main__":
    asyncio.run(main())
