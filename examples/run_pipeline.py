#!/usr/bin/env python3
"""Run the full pipeline from a concept prompt."""

import asyncio
import json
import sys
from pathlib import Path

from dotenv import load_dotenv

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

load_dotenv()

from agents.prerequisite_explorer_kimi import KimiPrerequisiteExplorer
from agents.enrichment_chain import KimiEnrichmentPipeline


async def run_pipeline(concept: str):
    """Run the full pipeline: prerequisite tree → enrichment → narrative."""
    print("=" * 70)
    print(f"RUNNING PIPELINE FOR: {concept}")
    print("=" * 70)
    
    # Stage 1: Build prerequisite tree
    print("\n[1/3] Building prerequisite tree...")
    explorer = KimiPrerequisiteExplorer(max_depth=3, use_tools=True)
    tree = await explorer.explore_async(concept, verbose=True)
    
    print(f"\n✓ Tree built: {tree.depth} levels deep")
    tree.print_tree()
    
    # Stage 2: Run enrichment pipeline
    print("\n[2/3] Running enrichment pipeline (math → visuals → narrative)...")
    pipeline = KimiEnrichmentPipeline()
    result = await pipeline.run_async(tree)
    
    # Stage 3: Save results
    print("\n[3/3] Saving results...")
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Save enriched tree
    tree_file = output_dir / f"{concept.replace(' ', '_')}_enriched.json"
    with tree_file.open("w") as f:
        json.dump(result.enriched_tree.to_dict(), f, indent=2)
    print(f"✓ Saved enriched tree to {tree_file}")
    
    # Save narrative
    narrative_file = output_dir / f"{concept.replace(' ', '_')}_narrative.txt"
    narrative_file.write_text(result.narrative.verbose_prompt, encoding="utf-8")
    print(f"✓ Saved narrative to {narrative_file}")
    
    print("\n" + "=" * 70)
    print("PIPELINE COMPLETE!")
    print("=" * 70)
    print(f"Narrative length: {len(result.narrative.verbose_prompt)} characters")
    print(f"Total duration: {result.narrative.total_duration}s")
    print(f"Scene count: {result.narrative.scene_count}")
    print("\nNarrative preview (first 500 chars):")
    print("-" * 70)
    preview = result.narrative.verbose_prompt[:500]
    print(preview + "..." if len(result.narrative.verbose_prompt) > 500 else preview)


if __name__ == "__main__":
    # Extract concept from prompt
    prompt = "explain to me the pythagorean theorem"
    concept = "pythagorean theorem"  # Extract main concept
    
    try:
        asyncio.run(run_pipeline(concept))
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

