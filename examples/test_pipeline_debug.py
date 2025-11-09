#!/usr/bin/env python3
"""Debug test for the full pipeline - tests each stage separately."""

import asyncio
import json
import sys
from pathlib import Path

from dotenv import load_dotenv

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

load_dotenv()

from agents.prerequisite_explorer_kimi import KimiPrerequisiteExplorer, KnowledgeNode
from agents.enrichment_chain import KimiEnrichmentPipeline, KimiNarrativeComposer
from kimi_client import KimiClient


def load_tree_from_json(path: Path) -> KnowledgeNode:
    """Load a KnowledgeNode from JSON."""
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    
    def _dict_to_node(d: dict) -> KnowledgeNode:
        return KnowledgeNode(
            concept=d["concept"],
            depth=d["depth"],
            is_foundation=d["is_foundation"],
            prerequisites=[_dict_to_node(p) for p in d.get("prerequisites", [])],
            equations=d.get("equations"),
            definitions=d.get("definitions"),
            visual_spec=d.get("visual_spec"),
            narrative=d.get("narrative"),
        )
    
    return _dict_to_node(data)


async def test_narrative_composer():
    """Test just the narrative composer with the enriched tree."""
    print("=" * 70)
    print("TESTING NARRATIVE COMPOSER")
    print("=" * 70)
    
    # Load the enriched tree
    tree_file = Path("output/pythagorean_enriched_tree.json")
    if not tree_file.exists():
        print(f"ERROR: {tree_file} not found!")
        return
    
    print(f"\nLoading enriched tree from {tree_file}")
    tree = load_tree_from_json(tree_file)
    
    print(f"Tree concept: {tree.concept}")
    print(f"Has equations: {bool(tree.equations)}")
    print(f"Has visual_spec: {bool(tree.visual_spec)}")
    print(f"Has narrative: {bool(tree.narrative)}")
    
    # Test narrative composer
    print("\n" + "-" * 70)
    print("Running narrative composer...")
    print("-" * 70)
    
    composer = KimiNarrativeComposer()
    
    try:
        narrative = await composer.compose_async(tree)
        
        print(f"\n[SUCCESS] Narrative composed!")
        print(f"  Length: {len(narrative.verbose_prompt)} characters")
        print(f"  Total duration: {narrative.total_duration}s")
        print(f"  Scene count: {narrative.scene_count}")
        print(f"  Concept order: {narrative.concept_order}")
        
        if narrative.verbose_prompt:
            print(f"\nFirst 500 characters:")
            print("-" * 70)
            print(narrative.verbose_prompt[:500])
            print("-" * 70)
        else:
            print("\n[WARNING] Narrative is empty!")
            
    except Exception as e:
        print(f"\n[ERROR] Failed to compose narrative: {e}")
        import traceback
        traceback.print_exc()


async def test_full_pipeline():
    """Test the complete pipeline from scratch."""
    print("\n" + "=" * 70)
    print("TESTING FULL PIPELINE")
    print("=" * 70)
    
    concept = "pythagorean theorem"
    
    # Stage 1: Build tree
    print(f"\n[1/4] Building prerequisite tree for: {concept}")
    explorer = KimiPrerequisiteExplorer(max_depth=2, use_tools=True)
    tree = await explorer.explore_async(concept, verbose=True)
    print(f"  [OK] Tree built: {tree.depth} levels, {len(tree.prerequisites)} prerequisites")
    
    # Stage 2: Math enrichment
    print(f"\n[2/4] Running math enrichment...")
    pipeline = KimiEnrichmentPipeline()
    await pipeline.math.enrich_tree(tree)
    print(f"  [OK] Math enriched: {len(tree.equations) if tree.equations else 0} equations")
    
    # Stage 3: Visual design
    print(f"\n[3/4] Running visual design...")
    await pipeline.visual.design_tree(tree)
    print(f"  [OK] Visual designed: {bool(tree.visual_spec)}")
    
    # Stage 4: Narrative composition
    print(f"\n[4/4] Running narrative composition...")
    narrative = await pipeline.narrative.compose_async(tree)
    print(f"  [OK] Narrative composed: {len(narrative.verbose_prompt)} characters")
    
    if narrative.verbose_prompt:
        print("\n" + "=" * 70)
        print("PIPELINE TEST SUCCESSFUL!")
        print("=" * 70)
        print(f"Narrative preview (first 300 chars):")
        print("-" * 70)
        print(narrative.verbose_prompt[:300])
        print("-" * 70)
        
        # Save results
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        with (output_dir / "pipeline_test_tree.json").open("w") as f:
            json.dump(tree.to_dict(), f, indent=2)
        
        (output_dir / "pipeline_test_narrative.txt").write_text(
            narrative.verbose_prompt, encoding="utf-8"
        )
        
        print(f"\nSaved to output/pipeline_test_tree.json")
        print(f"Saved to output/pipeline_test_narrative.txt")
    else:
        print("\n[FAILED] Narrative is empty - pipeline incomplete")


async def main():
    """Run tests."""
    # First test: Try to fix the existing enriched tree
    await test_narrative_composer()
    
    # Second test: Run full pipeline from scratch
    await test_full_pipeline()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nFATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

