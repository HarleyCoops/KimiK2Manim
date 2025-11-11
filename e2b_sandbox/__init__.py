"""
KimiK2Manim E2B Sandbox Package

A comprehensive sandbox environment for exploring KimiK2 thinking capabilities,
visual reasoning, and Manim animation generation.

Example usage:
    >>> from e2b_sandbox import setup_and_explore
    >>> result = await setup_and_explore("quantum mechanics")

Modules:
    - sandbox_config: Configuration and environment setup
    - interactive_explorer: Main exploration interface
    - visual_reasoning_tests: Automated test suite for visual reasoning
    - manim_renderer: Manim rendering utilities
    - tools: File management and utility tools
"""

__version__ = "0.1.0"
__author__ = "KimiK2Manim Team"

from e2b_sandbox.sandbox_config import (
    SandboxConfig,
    SandboxMode,
    setup_sandbox_environment,
    validate_sandbox_config
)

from e2b_sandbox.interactive_explorer import InteractiveExplorer

from e2b_sandbox.manim_renderer import ManimRenderer

from e2b_sandbox.tools import SandboxTools

__all__ = [
    "SandboxConfig",
    "SandboxMode",
    "setup_sandbox_environment",
    "validate_sandbox_config",
    "InteractiveExplorer",
    "ManimRenderer",
    "SandboxTools",
    "quick_explore",
    "run_visual_tests",
]


async def quick_explore(
    concept: str,
    thinking_mode: str = "heavy",
    depth: int = 3,
    enrichment: bool = True
):
    """
    Quickly explore a concept with default settings.

    Args:
        concept: Concept to explore
        thinking_mode: Thinking mode (heavy, medium, light)
        depth: Maximum prerequisite depth
        enrichment: Whether to run full enrichment pipeline

    Returns:
        Exploration result dictionary

    Example:
        >>> result = await quick_explore("fourier transform")
        >>> print(result['narrative'])
    """
    config = SandboxConfig.from_env()
    config.thinking_mode = thinking_mode
    config.max_depth = depth

    explorer = InteractiveExplorer(config)

    return await explorer.explore_concept(
        concept=concept,
        depth=depth,
        enrichment=enrichment,
        save_output=True
    )


async def run_visual_tests():
    """
    Run the complete visual reasoning test suite.

    Returns:
        Test suite results dictionary

    Example:
        >>> results = await run_visual_tests()
        >>> print(f"Pass rate: {results['pass_rate']}%")
    """
    from e2b_sandbox.visual_reasoning_tests import run_visual_reasoning_suite

    config = setup_sandbox_environment()
    return await run_visual_reasoning_suite(config)
