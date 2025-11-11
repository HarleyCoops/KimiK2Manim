"""
Minimal Surfaces Pipeline - 3D Visualization

Generates enriched content for a 3D Manim animation on Minimal Surfaces.
Emphasizes ThreeDScene rendering and artistic 3D presentation.
"""

import asyncio
import json
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

from agents.prerequisite_explorer_kimi import KimiPrerequisiteExplorer
from agents.enrichment_chain import KimiEnrichmentPipeline
from logger import get_logger, reset_logger


async def main():
    """Run the complete pipeline for Minimal Surfaces with 3D emphasis."""
    
    # Reset logger
    reset_logger()
    logger = get_logger(use_colors=True, verbose=True)
    
    # Concept with explicit 3D emphasis
    concept = "Minimal Surfaces: Mathematical Soap Films in 3D Space"
    
    # Enhanced prompt emphasizing 3D visualization
    enhanced_concept = (
        "Minimal Surfaces: Mathematical Soap Films in 3D Space. "
        "This animation MUST use Manim's ThreeDScene class for full 3D rendering. "
        "Focus on visualizing surfaces in three-dimensional space with dynamic camera movements, "
        "lighting effects, and artistic presentation. Show surfaces like catenoid, helicoid, "
        "Costa surface, and Enneper surface as translucent 3D objects that can be viewed "
        "from multiple angles. Emphasize depth, perspective, and immersive 3D experience."
    )
    
    logger.info("="*70)
    logger.info("Minimal Surfaces - 3D Visualization Pipeline")
    logger.info("="*70)
    logger.info(f"\nExploring concept: {concept}")
    logger.info("\nEmphasis: ThreeDScene, 3D rendering, artistic presentation")
    logger.info("="*70)
    
    # Setup output directory
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    # Stage 1: Prerequisite Exploration
    logger.stage("Building Prerequisite Tree", 1, 3)
    explorer = KimiPrerequisiteExplorer(
        max_depth=3,
        use_tools=True,
        logger=logger
    )
    
    tree = await explorer.explore_async(enhanced_concept, verbose=True)
    logger.success(f"Tree built: {tree.depth} levels deep")
    
    # Save intermediate tree
    tree_file_intermediate = output_dir / f"{concept.replace(' ', '_').replace(':', '_')}_prerequisite_tree.json"
    with open(tree_file_intermediate, 'w', encoding='utf-8') as f:
        json.dump(tree.to_dict(), f, indent=2, ensure_ascii=False)
    logger.success(f"Saved prerequisite tree: {tree_file_intermediate}")
    
    # Print tree structure
    if logger.verbose:
        try:
            tree.print_tree()
        except UnicodeEncodeError:
            logger.warning("Skipping tree visualization due to encoding issues")
    
    # Stage 2-4: Enrichment Pipeline
    logger.stage("Running Enrichment Pipeline (Math → Visual → Narrative)", 2, 3)
    logger.info("\nThis will:")
    logger.info("  - Enrich with mathematical content (equations, definitions)")
    logger.info("  - Design 3D visual specifications (ThreeDScene, camera movements)")
    logger.info("  - Compose narrative prompt (emphasizing 3D rendering)")
    logger.info("\nNote: This may take several minutes...")
    
    # Create pipeline
    pipeline = KimiEnrichmentPipeline(logger=logger)
    
    # Override the visual designer's _design_node method to use 3D-focused system prompt
    original_design_node = pipeline.visual._design_node
    
    async def three_d_design_node(self, node, parent_spec=None):
        """Design node with 3D emphasis."""
        from agents.enrichment_chain import VISUAL_DESIGN_TOOL, _extract_tool_payload, _parse_json_fallback, VisualSpec
        
        # Check cache first (same as original)
        if node.concept in self.cache:
            cached_spec = self.cache[node.concept]
            if node.visual_spec is None:
                node.visual_spec = {}
            node.visual_spec.update(cached_spec.to_dict())
            for prereq in node.prerequisites:
                await self._design_node(prereq, cached_spec)
            return cached_spec
        
        # Build previous info
        previous_info = ""
        if parent_spec:
            if hasattr(parent_spec, 'concept'):
                previous_info = (
                    f"Previous concept: {parent_spec.concept}\n"
                    f"Previous visual: {parent_spec.visual_description}\n"
                    f"Previous colors: {parent_spec.color_scheme}\n"
                )
            elif isinstance(parent_spec, dict):
                previous_info = (
                    f"Previous visual: {parent_spec.get('visual_description', '')}\n"
                    f"Previous colors: {parent_spec.get('color_scheme', '')}\n"
                )
        
        # 3D-focused system prompt
        system_prompt = (
            "You are a 3D visual designer specializing in ThreeDScene animations for Manim. "
            "CRITICAL: All animations MUST use ThreeDScene (not Scene) for full 3D rendering.\n\n"
            
            "3D REQUIREMENTS:\n"
            "- Use ThreeDAxes, Sphere, Surface, ParametricSurface for 3D objects\n"
            "- Dynamic camera movements: orbits, rotations, zooms around 3D objects\n"
            "- Show objects from multiple viewing angles\n"
            "- Include depth cues: shadows, lighting, perspective\n"
            "- Create immersive 3D experiences with artistic flair\n\n"
            
            "For Minimal Surfaces:\n"
            "- Visualize surfaces as translucent 3D objects\n"
            "- Show wireframes and surface meshes in 3D space\n"
            "- Demonstrate transformations between surfaces\n"
            "- Use lighting to show curvature and form\n"
            "- Include 3D coordinate systems\n"
            "- Create cinematic, artistic presentations\n\n"
            
            "Focus on describing the 3D visual content and effects, not specific implementation "
            "details. Manim ThreeDScene will handle the rendering automatically. Respond by calling "
            "the 'design_visual_plan' tool."
        )
        
        user_prompt = (
            f"Concept: {node.concept}\n"
            f"Depth: {node.depth}\n"
            f"Is foundational: {node.is_foundation}\n"
            f"Equations to feature: {node.equations or 'None provided'}\n"
            f"Prerequisites: {[p.concept for p in node.prerequisites]}\n"
            f"{previous_info}\n"
            "Describe what should appear visually in 3D space: what objects, shapes, or surfaces should be shown. "
            "Emphasize ThreeDScene rendering, 3D geometry, and artistic presentation. "
            "Describe colors in natural language (e.g., 'red and blue', 'gold'). "
            "Describe animations as visual effects (e.g., 'slowly rotate', 'fade in', 'zoom into'). "
            "Do NOT specify Manim classes like MathTex or VGroup - just describe what should be visible in 3D. "
            "Estimate duration in seconds."
        )
        
        self.logger.info(f"Designing 3D visual: '{node.concept}' (depth {node.depth})", prefix="VISUAL")
        response = self.client.chat_completion(
            messages=[{"role": "user", "content": user_prompt}],
            system=system_prompt,
            tools=[VISUAL_DESIGN_TOOL],
            tool_choice="auto",
            temperature=0.4,
            max_tokens=1200,
        )
        
        payload = _extract_tool_payload(response)
        if payload is None:
            payload = _parse_json_fallback(self.client.get_text_content(response)) or {}
        
        visual_desc = payload.get('visual_description', '')[:150]
        color_scheme = payload.get('color_scheme', 'N/A')
        animation = payload.get('animation_description', 'N/A')[:100]
        duration = payload.get('duration', 'N/A')
        self.logger.success(f"Extracted 3D visual spec for '{node.concept}': {duration}s duration")
        if self.logger.verbose:
            self.logger.debug(f"  Visual: {visual_desc}...")
            self.logger.debug(f"  Colors: {color_scheme}")
            self.logger.debug(f"  Animation: {animation}...")
        
        visual_spec = VisualSpec.from_payload(node.concept, payload)
        
        if node.visual_spec is None:
            node.visual_spec = {}
        node.visual_spec.update(visual_spec.to_dict())
        
        self.cache[node.concept] = visual_spec
        
        # Process prerequisites
        for prereq in node.prerequisites:
            await self._design_node(prereq, visual_spec)
        
        return visual_spec
    
    # Replace the method
    pipeline.visual._design_node = three_d_design_node.__get__(pipeline.visual, type(pipeline.visual))
    
    # Run enrichment
    result = await pipeline.run_async(tree)
    
    # Stage 3: Save results
    logger.stage("Saving Results", 3, 3)
    
    # Save final enriched tree
    tree_file = output_dir / f"{concept.replace(' ', '_').replace(':', '_')}_enriched.json"
    with open(tree_file, 'w', encoding='utf-8') as f:
        json.dump(tree.to_dict(), f, indent=2, ensure_ascii=False)
    logger.success(f"Saved enriched tree: {tree_file}")
    
    # Save narrative
    narrative_file = output_dir / f"{concept.replace(' ', '_').replace(':', '_')}_narrative.txt"
    with open(narrative_file, 'w', encoding='utf-8') as f:
        f.write(result.narrative.verbose_prompt)
    logger.success(f"Saved narrative: {narrative_file}")
    
    # Print summary
    logger.info("\n" + "="*70)
    logger.success("Pipeline Complete!")
    logger.info("="*70)
    logger.info(f"\nTotal duration estimate: {result.narrative.total_duration} seconds")
    logger.info(f"Narrative length: {len(result.narrative.verbose_prompt)} characters")
    logger.info(f"Scene count: {result.narrative.scene_count}")
    
    if logger.verbose:
        logger.info("\nNarrative preview (first 500 chars):")
        logger.info("-" * 70)
        preview = result.narrative.verbose_prompt[:500]
        logger.info(preview + "..." if len(result.narrative.verbose_prompt) > 500 else preview)
    
    logger.info("\n" + "="*70)
    logger.info("Next Steps:")
    logger.info("="*70)
    logger.info("1. Review the enriched JSON:", tree_file)
    logger.info("2. Review the narrative:", narrative_file)
    logger.info("3. Create Manim ThreeDScene using ManagedBoundedScene")
    logger.info("4. Render with: python -m manim -pql minimal_surfaces_scene.py MinimalSurfaces3D")
    logger.info("="*70)
    
    # Print logger summary
    logger.summary()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

