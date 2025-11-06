#!/usr/bin/env python3
"""Simple test that uses existing enriched tree and just tests narrative composition."""

import asyncio
import json
import sys
from pathlib import Path

from dotenv import load_dotenv

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

load_dotenv()

from agents.prerequisite_explorer_kimi import KnowledgeNode
from agents.enrichment_chain import KimiEnrichmentPipeline


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


async def test_narrative_only():
    """Test narrative composition on existing enriched tree."""
    print("=" * 70)
    print("TESTING NARRATIVE COMPOSITION")
    print("=" * 70)
    
    # Load enriched tree
    tree_file = Path("output/pythagorean_enriched_tree.json")
    if not tree_file.exists():
        print(f"ERROR: {tree_file} not found!")
        return
    
    print(f"\nLoading enriched tree from {tree_file}")
    tree = load_tree_from_json(tree_file)
    
    print(f"Concept: {tree.concept}")
    print(f"Equations: {len(tree.equations) if tree.equations else 0}")
    print(f"Visual spec: {bool(tree.visual_spec)}")
    print(f"Current narrative: {len(tree.narrative) if tree.narrative else 0} chars")
    
    # Run narrative composer
    print("\n" + "-" * 70)
    print("Composing narrative...")
    print("-" * 70)
    
    pipeline = KimiEnrichmentPipeline()
    
    try:
        narrative = await pipeline.narrative.compose_async(tree)
        
        print(f"\n[RESULT]")
        print(f"  Narrative length: {len(narrative.verbose_prompt)} characters")
        print(f"  Total duration: {narrative.total_duration}s")
        print(f"  Scene count: {narrative.scene_count}")
        print(f"  Concept order: {narrative.concept_order}")
        
        if narrative.verbose_prompt:
            print(f"\n[SUCCESS] Narrative generated!")
            print(f"\nFirst 500 characters:")
            print("-" * 70)
            print(narrative.verbose_prompt[:500])
            print("-" * 70)
            
            # Save
            output_dir = Path("output")
            output_dir.mkdir(exist_ok=True)
            (output_dir / "pythagorean_final_narrative.txt").write_text(
                narrative.verbose_prompt, encoding="utf-8"
            )
            print(f"\nSaved to output/pythagorean_final_narrative.txt")
            
            # Update tree
            tree.narrative = narrative.verbose_prompt
            with (output_dir / "pythagorean_final_tree.json").open("w") as f:
                json.dump(tree.to_dict(), f, indent=2)
            print(f"Saved complete tree to output/pythagorean_final_tree.json")
        else:
            print("\n[FAILED] Narrative is empty - check API response")
            
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    try:
        asyncio.run(test_narrative_only())
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nFATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

