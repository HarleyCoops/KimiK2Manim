import json
from pathlib import Path

def count_nodes(node):
    """Recursively count all nodes in the tree."""
    count = 1
    for prereq in node.get('prerequisites', []):
        count += count_nodes(prereq)
    return count

def count_by_depth(node, depth=0):
    """Count nodes at each depth level."""
    counts = {}
    counts[depth] = counts.get(depth, 0) + 1
    for prereq in node.get('prerequisites', []):
        sub_counts = count_by_depth(prereq, depth + 1)
        for d, c in sub_counts.items():
            counts[d] = counts.get(d, 0) + c
    return counts

def count_foundation_nodes(node):
    """Count foundation nodes."""
    count = 1 if node.get('is_foundation', False) else 0
    for prereq in node.get('prerequisites', []):
        count += count_foundation_nodes(prereq)
    return count

# Load the prerequisite tree
tree_file = Path("BrownianMotion/output/Brownian_Motion_and_Einstein's_Heat_Equation_prerequisite_tree.json")
with open(tree_file, 'r', encoding='utf-8') as f:
    tree = json.load(f)

total_nodes = count_nodes(tree)
foundation_nodes = count_foundation_nodes(tree)
non_foundation_nodes = total_nodes - foundation_nodes
depth_counts = count_by_depth(tree)

print("="*70)
print("Brownian Motion Pipeline API Call Estimation")
print("="*70)
print(f"\nTotal nodes in tree: {total_nodes}")
print(f"Foundation nodes: {foundation_nodes}")
print(f"Non-foundation nodes: {non_foundation_nodes}")
print(f"\nNodes by depth:")
for depth in sorted(depth_counts.keys()):
    print(f"  Depth {depth}: {depth_counts[depth]} nodes")

# Calculate API calls
# Stage 1: Prerequisite exploration
# - Foundation check: 1 call per node (but foundation nodes return early)
# - Prerequisites discovery: 1 call per non-foundation node only
stage1_foundation_checks = total_nodes  # All nodes get checked
stage1_prerequisites = non_foundation_nodes  # Only non-foundation get prerequisites discovered
stage1_calls = stage1_foundation_checks + stage1_prerequisites

# Stage 2: Mathematical enrichment - 1 call per node
stage2_calls = total_nodes

# Stage 3: Visual design - 1 call per node  
stage3_calls = total_nodes

# Stage 4: Narrative composition - 1 call total
stage4_calls = 1

total_calls = stage1_calls + stage2_calls + stage3_calls + stage4_calls

print(f"\n" + "="*70)
print("API Call Breakdown:")
print("="*70)
print(f"Stage 1 (Prerequisites): {stage1_calls} calls")
print(f"  - Foundation checks: {stage1_foundation_checks} calls")
print(f"  - Prerequisites discovery: {stage1_prerequisites} calls")
print(f"Stage 2 (Math Enrichment): {stage2_calls} calls")
print(f"Stage 3 (Visual Design): {stage3_calls} calls")
print(f"Stage 4 (Narrative): {stage4_calls} call")
print(f"\nTOTAL ESTIMATED API CALLS: {total_calls}")
print("="*70)

