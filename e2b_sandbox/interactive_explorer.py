"""
Interactive KimiK2 Explorer for E2B Sandbox
This script provides an interactive interface to explore concepts using KimiK2 thinking.
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Optional, List
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.prerequisite_explorer_kimi import KimiPrerequisiteExplorer
from agents.enrichment_chain import KimiEnrichmentPipeline
from logger import get_logger
from e2b_sandbox.sandbox_config import SandboxConfig, setup_sandbox_environment, validate_sandbox_config

logger = get_logger()


class InteractiveExplorer:
    """Interactive explorer for KimiK2 thinking in E2B sandbox."""

    def __init__(self, config: SandboxConfig):
        """Initialize the interactive explorer."""
        self.config = config
        self.explorer = KimiPrerequisiteExplorer(
            max_depth=config.max_depth,
            use_tools=config.use_tools
        )
        self.pipeline = KimiEnrichmentPipeline()
        self.session_history = []

    async def explore_concept(
        self,
        concept: str,
        depth: Optional[int] = None,
        enrichment: bool = True,
        save_output: bool = True
    ) -> dict:
        """
        Explore a concept using KimiK2 thinking.

        Args:
            concept: The concept to explore
            depth: Maximum depth for prerequisite exploration
            enrichment: Whether to run the enrichment pipeline
            save_output: Whether to save the output to files

        Returns:
            Dictionary containing the exploration results
        """
        logger.info(f"🔍 Exploring concept: {concept}")
        logger.info(f"📊 Mode: {self.config.thinking_mode} thinking")
        logger.info(f"🌳 Max depth: {depth or self.config.max_depth}")

        start_time = datetime.now()

        # Step 1: Explore prerequisites
        logger.info("📖 Stage 1: Building knowledge tree...")
        tree = await self.explorer.explore_async(
            concept=concept,
            depth=depth or self.config.max_depth,
            verbose=True
        )

        result = {
            "concept": concept,
            "timestamp": start_time.isoformat(),
            "config": self.config.to_dict(),
            "tree": self._serialize_tree(tree),
            "enriched": False,
            "narrative": None
        }

        # Step 2: Enrichment pipeline (optional)
        if enrichment:
            logger.info("🎨 Running enrichment pipeline...")
            logger.info("  Stage 2: Mathematical enrichment")
            logger.info("  Stage 3: Visual design")
            logger.info("  Stage 4: Narrative composition")

            enrichment_result = await self.pipeline.run_async(tree)

            result["enriched"] = True
            result["narrative"] = enrichment_result.narrative
            result["tree"] = self._serialize_tree(enrichment_result.enriched_tree)

        # Step 3: Save output
        if save_output:
            await self._save_results(result)

        elapsed = (datetime.now() - start_time).total_seconds()
        logger.info(f"✅ Exploration complete in {elapsed:.1f}s")

        # Add to session history
        self.session_history.append({
            "concept": concept,
            "timestamp": start_time.isoformat(),
            "elapsed_seconds": elapsed,
            "enriched": enrichment
        })

        return result

    async def batch_explore(
        self,
        concepts: List[str],
        enrichment: bool = False
    ) -> List[dict]:
        """
        Explore multiple concepts in batch.

        Args:
            concepts: List of concepts to explore
            enrichment: Whether to run enrichment pipeline

        Returns:
            List of exploration results
        """
        logger.info(f"🚀 Batch exploration: {len(concepts)} concepts")

        results = []
        for i, concept in enumerate(concepts, 1):
            logger.info(f"\n{'='*60}")
            logger.info(f"Concept {i}/{len(concepts)}: {concept}")
            logger.info(f"{'='*60}\n")

            try:
                result = await self.explore_concept(
                    concept=concept,
                    enrichment=enrichment,
                    save_output=True
                )
                results.append(result)
            except Exception as e:
                logger.error(f"❌ Failed to explore '{concept}': {e}")
                results.append({
                    "concept": concept,
                    "error": str(e),
                    "success": False
                })

        return results

    def _serialize_tree(self, node, depth=0) -> dict:
        """Serialize knowledge tree to dictionary."""
        serialized = {
            "concept": node.concept,
            "depth": node.depth,
            "is_foundation": node.is_foundation,
            "prerequisites": [],
        }

        # Add enrichments if present
        if node.equations:
            serialized["equations"] = node.equations
        if node.definitions:
            serialized["definitions"] = node.definitions
        if node.visual_spec:
            serialized["visual_spec"] = node.visual_spec
        if node.narrative:
            serialized["narrative"] = node.narrative

        # Recursively serialize prerequisites
        for prereq in node.prerequisites:
            serialized["prerequisites"].append(self._serialize_tree(prereq, depth + 1))

        return serialized

    async def _save_results(self, result: dict):
        """Save exploration results to files."""
        concept_slug = result["concept"].replace(" ", "_").lower()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save full result as JSON
        json_path = Path(self.config.output_dir) / f"{concept_slug}_{timestamp}.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        logger.info(f"💾 Saved JSON: {json_path}")

        # Save narrative if present
        if result.get("narrative"):
            narrative_path = Path(self.config.output_dir) / f"{concept_slug}_{timestamp}_narrative.txt"
            with open(narrative_path, "w", encoding="utf-8") as f:
                f.write(result["narrative"])
            logger.info(f"📝 Saved narrative: {narrative_path}")

    def print_summary(self):
        """Print session summary."""
        logger.info("\n" + "="*60)
        logger.info("📊 SESSION SUMMARY")
        logger.info("="*60)
        logger.info(f"Total concepts explored: {len(self.session_history)}")

        total_time = sum(item["elapsed_seconds"] for item in self.session_history)
        logger.info(f"Total time: {total_time:.1f}s")

        enriched_count = sum(1 for item in self.session_history if item["enriched"])
        logger.info(f"Enriched concepts: {enriched_count}")

        logger.info("\nConcepts explored:")
        for i, item in enumerate(self.session_history, 1):
            status = "🎨 Enriched" if item["enriched"] else "🌳 Tree only"
            logger.info(f"  {i}. {item['concept']} - {status} ({item['elapsed_seconds']:.1f}s)")


async def main():
    """Main entry point for interactive exploration."""
    logger.info("🚀 KimiK2 Interactive Explorer - E2B Sandbox Edition")
    logger.info("="*60)

    # Setup sandbox environment
    config = setup_sandbox_environment()
    validate_sandbox_config(config)

    logger.info(f"✅ Configuration loaded")
    logger.info(f"  Model: {config.model}")
    logger.info(f"  Thinking mode: {config.thinking_mode}")
    logger.info(f"  Max depth: {config.max_depth}")
    logger.info(f"  Tools enabled: {config.use_tools}")

    # Create explorer
    explorer = InteractiveExplorer(config)

    # Example explorations - demonstrating visual reasoning capabilities
    interesting_concepts = [
        "quantum entanglement",
        "fourier transform",
        "riemann hypothesis",
        "neural network backpropagation",
        "general relativity",
    ]

    logger.info(f"\n🎯 Ready to explore! Example concepts:")
    for i, concept in enumerate(interesting_concepts, 1):
        logger.info(f"  {i}. {concept}")

    # For demonstration, explore one concept with full enrichment
    demo_concept = "fourier transform"
    logger.info(f"\n🎬 Starting demo exploration: {demo_concept}")

    result = await explorer.explore_concept(
        concept=demo_concept,
        depth=2,  # Reasonable depth for demo
        enrichment=True,  # Full pipeline
        save_output=True
    )

    # Print summary
    explorer.print_summary()

    logger.info("\n✨ Exploration complete! Check the output directory for results.")
    logger.info(f"📁 Output directory: {config.output_dir}")

    return result


if __name__ == "__main__":
    asyncio.run(main())
