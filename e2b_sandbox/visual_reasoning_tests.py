"""
Visual Reasoning Test Suite for KimiK2 in E2B Sandbox

This module tests KimiK2's ability to reason through visual mathematical concepts
and generate appropriate Manim visualizations.
"""

import asyncio
import sys
from pathlib import Path
from typing import Dict, List
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.prerequisite_explorer_kimi import KimiPrerequisiteExplorer
from agents.enrichment_chain import KimiEnrichmentPipeline
from logger import get_logger
from e2b_sandbox.sandbox_config import SandboxConfig, setup_sandbox_environment

logger = get_logger()


class VisualReasoningTest:
    """Test case for visual reasoning capabilities."""

    def __init__(
        self,
        name: str,
        concept: str,
        expected_visual_elements: List[str],
        description: str
    ):
        self.name = name
        self.concept = concept
        self.expected_visual_elements = expected_visual_elements
        self.description = description
        self.result = None
        self.passed = False

    async def run(self, explorer: KimiPrerequisiteExplorer, pipeline: KimiEnrichmentPipeline) -> Dict:
        """Run the test case."""
        logger.info(f"\n{'='*60}")
        logger.info(f"Test: {self.name}")
        logger.info(f"Description: {self.description}")
        logger.info(f"Concept: {self.concept}")
        logger.info(f"{'='*60}\n")

        start_time = datetime.now()

        try:
            # Step 1: Explore prerequisites
            logger.info("Building knowledge tree...")
            tree = await explorer.explore_async(self.concept, depth=2, verbose=True)

            # Step 2: Run enrichment pipeline
            logger.info("Running enrichment pipeline...")
            enrichment_result = await pipeline.run_async(tree)

            # Step 3: Analyze visual specifications
            visual_specs = self._extract_visual_specs(enrichment_result.enriched_tree)

            # Step 4: Validate visual elements
            found_elements = self._check_visual_elements(visual_specs)

            elapsed = (datetime.now() - start_time).total_seconds()

            # Determine pass/fail
            self.passed = len(found_elements) >= len(self.expected_visual_elements) * 0.6  # 60% threshold

            self.result = {
                "name": self.name,
                "concept": self.concept,
                "passed": self.passed,
                "elapsed_seconds": elapsed,
                "expected_elements": self.expected_visual_elements,
                "found_elements": found_elements,
                "visual_specs": visual_specs,
                "narrative_length": len(enrichment_result.narrative) if enrichment_result.narrative else 0,
                "tree_depth": self._count_depth(enrichment_result.enriched_tree),
            }

            # Log results
            status = "PASSED" if self.passed else "FAILED"
            logger.info(f"\n{status} - {self.name}")
            logger.info(f"  Found: {len(found_elements)}/{len(self.expected_visual_elements)} expected elements")
            logger.info(f"  Time: {elapsed:.1f}s")

            return self.result

        except Exception as e:
            logger.error(f"Test failed with error: {e}")
            self.result = {
                "name": self.name,
                "concept": self.concept,
                "passed": False,
                "error": str(e)
            }
            return self.result

    def _extract_visual_specs(self, node, specs=None) -> List[Dict]:
        """Recursively extract visual specifications from tree."""
        if specs is None:
            specs = []

        if node.visual_spec:
            specs.append({
                "concept": node.concept,
                "spec": node.visual_spec
            })

        for prereq in node.prerequisites:
            self._extract_visual_specs(prereq, specs)

        return specs

    def _check_visual_elements(self, visual_specs: List[Dict]) -> List[str]:
        """Check which expected visual elements are present."""
        found = []

        # Convert all specs to lowercase strings for searching
        all_specs_text = " ".join(
            str(spec["spec"]).lower()
            for spec in visual_specs
        )

        for element in self.expected_visual_elements:
            if element.lower() in all_specs_text:
                found.append(element)

        return found

    def _count_depth(self, node, max_depth=0) -> int:
        """Count maximum depth of tree."""
        if not node.prerequisites:
            return max_depth

        return max(
            self._count_depth(prereq, max_depth + 1)
            for prereq in node.prerequisites
        )


# Define visual reasoning test cases
VISUAL_REASONING_TESTS = [
    VisualReasoningTest(
        name="Geometric Transformations",
        concept="rotation matrices in 3D space",
        expected_visual_elements=[
            "rotation", "axis", "angle", "transformation",
            "3D", "coordinate", "matrix"
        ],
        description="Test ability to visualize 3D rotations and transformations"
    ),
    VisualReasoningTest(
        name="Wave Phenomena",
        concept="fourier series",
        expected_visual_elements=[
            "wave", "sine", "cosine", "frequency", "amplitude",
            "decomposition", "harmonic"
        ],
        description="Test ability to visualize wave decomposition and harmonics"
    ),
    VisualReasoningTest(
        name="Calculus Concepts",
        concept="riemann sum",
        expected_visual_elements=[
            "rectangle", "area", "curve", "interval", "limit",
            "integration", "approximation"
        ],
        description="Test ability to visualize integration through rectangular approximation"
    ),
    VisualReasoningTest(
        name="Linear Algebra",
        concept="eigenvalues and eigenvectors",
        expected_visual_elements=[
            "vector", "transformation", "scaling", "direction",
            "matrix", "space", "arrow"
        ],
        description="Test ability to visualize linear transformations and eigenvectors"
    ),
    VisualReasoningTest(
        name="Complex Analysis",
        concept="complex plane mapping",
        expected_visual_elements=[
            "complex", "plane", "mapping", "transformation",
            "real", "imaginary", "point"
        ],
        description="Test ability to visualize complex function mappings"
    ),
    VisualReasoningTest(
        name="Topology",
        concept="homeomorphism",
        expected_visual_elements=[
            "continuous", "deformation", "shape", "topology",
            "mapping", "transformation", "space"
        ],
        description="Test ability to visualize topological equivalences"
    ),
]


async def run_visual_reasoning_suite(config: SandboxConfig) -> Dict:
    """
    Run the complete visual reasoning test suite.

    Args:
        config: Sandbox configuration

    Returns:
        Dictionary containing test suite results
    """
    logger.info("KIMIK2 VISUAL REASONING TEST SUITE")
    logger.info("="*60)
    logger.info(f"Total tests: {len(VISUAL_REASONING_TESTS)}")
    logger.info(f"Thinking mode: {config.thinking_mode}")
    logger.info(f"Max depth: {config.max_depth}")
    logger.info("="*60)

    # Initialize agents
    explorer = KimiPrerequisiteExplorer(
        max_depth=config.max_depth,
        use_tools=config.use_tools
    )
    pipeline = KimiEnrichmentPipeline()

    # Run tests
    results = []
    start_time = datetime.now()

    for test in VISUAL_REASONING_TESTS:
        result = await test.run(explorer, pipeline)
        results.append(result)

    elapsed = (datetime.now() - start_time).total_seconds()

    # Calculate statistics
    passed = sum(1 for r in results if r.get("passed", False))
    failed = len(results) - passed
    pass_rate = (passed / len(results)) * 100

    # Print summary
    logger.info("\n" + "="*60)
    logger.info("TEST SUITE SUMMARY")
    logger.info("="*60)
    logger.info(f"Total tests: {len(results)}")
    logger.info(f"Passed: {passed}")
    logger.info(f"Failed: {failed}")
    logger.info(f"Pass rate: {pass_rate:.1f}%")
    logger.info(f"Total time: {elapsed:.1f}s")
    logger.info(f"Average time per test: {elapsed/len(results):.1f}s")

    logger.info("\nIndividual Results:")
    for result in results:
        status = "PASS" if result.get("passed") else "FAIL"
        logger.info(f"  {status} {result['name']}")

    summary = {
        "timestamp": start_time.isoformat(),
        "total_tests": len(results),
        "passed": passed,
        "failed": failed,
        "pass_rate": pass_rate,
        "elapsed_seconds": elapsed,
        "results": results,
        "config": config.to_dict()
    }

    # Save results
    output_path = Path(config.output_dir) / f"visual_reasoning_tests_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    import json
    with open(output_path, "w") as f:
        json.dump(summary, f, indent=2)

    logger.info(f"\nResults saved to: {output_path}")

    return summary


async def main():
    """Main entry point for visual reasoning tests."""
    # Setup sandbox environment
    config = setup_sandbox_environment()

    # Run test suite
    results = await run_visual_reasoning_suite(config)

    return results


if __name__ == "__main__":
    asyncio.run(main())
