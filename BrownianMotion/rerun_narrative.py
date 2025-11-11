#!/usr/bin/env python3
"""
Re-run narrative composition for Brownian Motion.

This script loads the enriched tree and re-runs only the narrative composition step
to recover the missing narrative text.
"""

import asyncio
import json
import sys
from pathlib import Path

from dotenv import load_dotenv

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

load_dotenv()

from agents.prerequisite_explorer_kimi import KnowledgeNode
from agents.enrichment_chain import KimiNarrativeComposer
from logger import get_logger, reset_logger


def load_tree_from_json(path: Path) -> KnowledgeNode:
    """Load a KnowledgeNode from JSON."""
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    
    def _dict_to_node(d: dict) -> KnowledgeNode:
        node = KnowledgeNode(
            concept=d["concept"],
            depth=d["depth"],
            is_foundation=d["is_foundation"],
            prerequisites=[_dict_to_node(p) for p in d.get("prerequisites", [])],
        )
        # Restore enrichment data
        node.equations = d.get("equations")
        node.definitions = d.get("definitions")
        node.visual_spec = d.get("visual_spec")
        node.narrative = d.get("narrative")
        return node
    
    return _dict_to_node(data)


async def main():
    """Re-run narrative composition."""
    reset_logger()
    logger = get_logger(use_colors=True, verbose=True)
    
    logger.info("=" * 70)
    logger.info("Re-running Narrative Composition for Brownian Motion")
    logger.info("=" * 70)
    
    # Load enriched tree
    enriched_file = Path(__file__).parent / "output/Brownian_Motion_and_Einstein's_Heat_Equation_enriched.json"
    if not enriched_file.exists():
        logger.error(f"Enriched tree not found: {enriched_file}")
        sys.exit(1)
    
    logger.info(f"Loading enriched tree from: {enriched_file}")
    tree = load_tree_from_json(enriched_file)
    logger.success(f"Loaded tree with {len(tree.prerequisites)} top-level prerequisites")
    
    # Re-run narrative composition
    logger.info("\nRe-composing narrative...")
    composer = KimiNarrativeComposer(logger=logger)
    narrative = await composer.compose_async(tree)
    
    # Save narrative
    output_dir = Path(__file__).parent / "output"
    narrative_file = output_dir / "Brownian_Motion_and_Einstein's_Heat_Equation_narrative.txt"
    narrative_file.write_text(narrative.verbose_prompt, encoding="utf-8")
    logger.success(f"Saved narrative to {narrative_file}")
    
    logger.info("\n" + "=" * 70)
    logger.success("Narrative composition complete!")
    logger.info("=" * 70)
    logger.info(f"Narrative length: {len(narrative.verbose_prompt)} characters")
    logger.info(f"Total duration: {narrative.total_duration}s")
    logger.info(f"Scene count: {narrative.scene_count}")
    
    if logger.verbose:
        logger.info("\nNarrative preview (first 500 chars):")
        logger.info("-" * 70)
        preview = narrative.verbose_prompt[:500]
        logger.info(preview + "..." if len(narrative.verbose_prompt) > 500 else preview)
    
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

