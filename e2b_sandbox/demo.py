#!/usr/bin/env python3
"""
KimiK2Manim E2B Sandbox Demo

This script demonstrates the full capabilities of the E2B sandbox environment
for exploring concepts with KimiK2 thinking and generating Manim animations.
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from e2b_sandbox import (
    setup_sandbox_environment,
    validate_sandbox_config,
    InteractiveExplorer,
    ManimRenderer,
    SandboxTools,
    quick_explore,
    run_visual_tests
)
from logger import get_logger

logger = get_logger()


async def demo_basic_exploration():
    """Demonstrate basic concept exploration."""
    logger.info("\n" + "="*60)
    logger.info("DEMO 1: Basic Concept Exploration")
    logger.info("="*60)

    result = await quick_explore(
        concept="pythagorean theorem",
        thinking_mode="medium",
        depth=2,
        enrichment=True
    )

    logger.info(f"\nExploration complete!")
    logger.info(f"  Concept: {result['concept']}")
    logger.info(f"  Narrative length: {len(result.get('narrative', ''))} chars")
    logger.info(f"  Tree nodes: {count_nodes(result['tree'])}")

    return result


async def demo_visual_reasoning():
    """Demonstrate visual reasoning capabilities."""
    logger.info("\n" + "="*60)
    logger.info("DEMO 2: Visual Reasoning Tests")
    logger.info("="*60)

    # Run just a few tests for demo purposes
    from e2b_sandbox.visual_reasoning_tests import VisualReasoningTest
    from agents.prerequisite_explorer_kimi import KimiPrerequisiteExplorer
    from agents.enrichment_chain import KimiEnrichmentPipeline

    config = setup_sandbox_environment()

    explorer = KimiPrerequisiteExplorer(
        max_depth=config.max_depth,
        use_tools=config.use_tools
    )
    pipeline = KimiEnrichmentPipeline()

    # Create a simple test
    test = VisualReasoningTest(
        name="Demo Visual Test",
        concept="unit circle",
        expected_visual_elements=["circle", "radius", "angle", "sine", "cosine"],
        description="Test visualization of unit circle and trigonometry"
    )

    logger.info(f"Running test: {test.name}")
    result = await test.run(explorer, pipeline)

    logger.info(f"\n{'PASSED' if result['passed'] else 'FAILED'}")
    logger.info(f"  Found: {len(result['found_elements'])} / {len(result['expected_elements'])} elements")

    return result


async def demo_batch_exploration():
    """Demonstrate batch concept exploration."""
    logger.info("\n" + "="*60)
    logger.info("DEMO 3: Batch Exploration")
    logger.info("="*60)

    config = setup_sandbox_environment()
    config.thinking_mode = "light"  # Use light mode for faster demo

    explorer = InteractiveExplorer(config)

    concepts = [
        "fibonacci sequence",
        "golden ratio",
        "euler's identity"
    ]

    logger.info(f"Exploring {len(concepts)} concepts in batch...")

    results = await explorer.batch_explore(
        concepts=concepts,
        enrichment=False  # Skip enrichment for faster demo
    )

    logger.info("\nBatch exploration complete!")
    for i, result in enumerate(results, 1):
        logger.info(f"  {i}. {result.get('concept', 'Unknown')}")

    explorer.print_summary()

    return results


async def demo_manim_rendering():
    """Demonstrate Manim rendering capabilities."""
    logger.info("\n" + "="*60)
    logger.info("DEMO 4: Manim Rendering")
    logger.info("="*60)

    config = setup_sandbox_environment()
    renderer = ManimRenderer(config)

    # List available scenes
    logger.info("Scanning for available Manim scenes...")
    scenes = renderer.list_available_scenes()

    logger.info(f"\nFound {len(scenes)} scene files:")
    for scene in scenes:
        logger.info(f"  {scene['filename']}")
        for class_name in scene['classes']:
            logger.info(f"     - {class_name}")

    # Optionally render one scene (commented out to avoid long demo time)
    # if scenes and scenes[0]['classes']:
    #     logger.info(f"\nRendering example scene...")
    #     result = renderer.render_scene(
    #         scene_file=Path(scenes[0]['file']),
    #         scene_class=scenes[0]['classes'][0],
    #         quality='l'
    #     )
    #
    #     if result['success']:
    #         logger.info(f"Render successful: {result['output_file']}")

    return scenes


def demo_sandbox_tools():
    """Demonstrate sandbox utility tools."""
    logger.info("\n" + "="*60)
    logger.info("DEMO 5: Sandbox Tools")
    logger.info("="*60)

    tools = SandboxTools()

    # List outputs
    logger.info("Listing recent outputs...")
    outputs = tools.list_outputs()
    logger.info(f"  Found {len(outputs)} output files")

    for output in outputs[:5]:  # Show first 5
        logger.info(f"    - {output.name}")

    # Storage usage
    logger.info("\nStorage usage:")
    storage = tools.get_storage_usage()
    logger.info(f"  Output: {storage['output_dir_mb']:.2f} MB ({storage['output_files']} files)")
    logger.info(f"  Media:  {storage['media_dir_mb']:.2f} MB ({storage['media_files']} files)")
    logger.info(f"  Total:  {storage['total_mb']:.2f} MB")

    # Generate report
    logger.info("\nGenerating exploration report...")
    report = tools.create_exploration_report()

    logger.info("Tools demo complete!")

    return storage


async def demo_advanced_features():
    """Demonstrate advanced sandbox features."""
    logger.info("\n" + "="*60)
    logger.info("DEMO 6: Advanced Features")
    logger.info("="*60)

    config = setup_sandbox_environment()

    # 1. Custom configuration
    logger.info("\n1. Custom Configuration")
    logger.info(f"  Thinking mode: {config.thinking_mode}")
    logger.info(f"  Max depth: {config.max_depth}")
    logger.info(f"  Use tools: {config.use_tools}")
    logger.info(f"  Sandbox mode: {config.mode.value}")

    # 2. Different thinking modes
    logger.info("\n2. Thinking Mode Comparison")
    explorer = InteractiveExplorer(config)

    concept = "prime numbers"

    for mode in ["light", "medium"]:  # Skip heavy for demo speed
        logger.info(f"\n  Testing '{mode}' thinking mode...")
        config.thinking_mode = mode

        result = await explorer.explore_concept(
            concept=concept,
            depth=1,
            enrichment=False,
            save_output=False
        )

        logger.info(f"    Completed in {result.get('elapsed_seconds', 0):.1f}s")

    logger.info("\nAdvanced features demo complete!")


def count_nodes(tree_dict):
    """Count nodes in a tree dictionary."""
    count = 1
    for prereq in tree_dict.get('prerequisites', []):
        count += count_nodes(prereq)
    return count


async def run_all_demos():
    """Run all demonstration scenarios."""
    logger.info("KimiK2Manim E2B Sandbox - Complete Demo")
    logger.info("="*60)
    logger.info("This demo will showcase all sandbox capabilities:")
    logger.info("  1. Basic concept exploration")
    logger.info("  2. Visual reasoning tests")
    logger.info("  3. Batch exploration")
    logger.info("  4. Manim rendering")
    logger.info("  5. Sandbox tools")
    logger.info("  6. Advanced features")
    logger.info("="*60)

    # Setup environment
    logger.info("\nSetting up environment...")
    config = setup_sandbox_environment()

    try:
        validate_sandbox_config(config)
        logger.info("Configuration validated")
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        logger.error("Please ensure .env file is configured correctly")
        return

    # Run demos
    demos = [
        ("Basic Exploration", demo_basic_exploration),
        ("Visual Reasoning", demo_visual_reasoning),
        ("Batch Exploration", demo_batch_exploration),
        ("Manim Rendering", demo_manim_rendering),
        ("Sandbox Tools", demo_sandbox_tools),
        ("Advanced Features", demo_advanced_features),
    ]

    results = {}

    for name, demo_func in demos:
        try:
            if asyncio.iscoroutinefunction(demo_func):
                result = await demo_func()
            else:
                result = demo_func()

            results[name] = {"success": True, "result": result}

        except Exception as e:
            logger.error(f"\nDemo '{name}' failed: {e}")
            results[name] = {"success": False, "error": str(e)}

    # Final summary
    logger.info("\n" + "="*60)
    logger.info("DEMO SUMMARY")
    logger.info("="*60)

    successful = sum(1 for r in results.values() if r.get("success"))
    total = len(results)

    logger.info(f"Completed: {successful}/{total} demos")
    logger.info("\nResults:")

    for name, result in results.items():
        status = "PASS" if result.get("success") else "FAIL"
        logger.info(f"  {status} {name}")

    logger.info("\n" + "="*60)
    logger.info("Demo complete! Check the output/ directory for results.")
    logger.info("="*60)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="KimiK2Manim E2B Sandbox Demo"
    )
    parser.add_argument(
        "--demo",
        choices=["all", "basic", "visual", "batch", "manim", "tools", "advanced"],
        default="all",
        help="Which demo to run (default: all)"
    )

    args = parser.parse_args()

    # Run selected demo
    if args.demo == "all":
        asyncio.run(run_all_demos())
    elif args.demo == "basic":
        asyncio.run(demo_basic_exploration())
    elif args.demo == "visual":
        asyncio.run(demo_visual_reasoning())
    elif args.demo == "batch":
        asyncio.run(demo_batch_exploration())
    elif args.demo == "manim":
        asyncio.run(demo_manim_rendering())
    elif args.demo == "tools":
        demo_sandbox_tools()
    elif args.demo == "advanced":
        asyncio.run(demo_advanced_features())


if __name__ == "__main__":
    main()
