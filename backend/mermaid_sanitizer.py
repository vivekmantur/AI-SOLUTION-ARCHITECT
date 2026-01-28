import re
from typing import List, Optional
from collections import defaultdict

from .models import ArchitectureComponent


def _to_node_id(name: str) -> str:
    """
    Converts a human-readable node label into a Mermaid-safe node ID.

    Rules:
    - Lowercase
    - Remove content inside parentheses (e.g., "(ADF)")
    - Replace non-alphanumeric characters with underscores
    - Ensure a non-empty ID
    """

    if not name:
        return "node"

    nid = name.lower().strip()

    # Remove text inside parentheses for cleaner IDs
    nid = re.sub(r"\(.*?\)", "", nid)

    # Replace invalid characters with underscore
    nid = re.sub(r"[^a-z0-9]+", "_", nid)

    # Remove leading/trailing underscores
    nid = nid.strip("_")

    return nid or "node"


def normalize_mermaid(
    diagram: str,
    components: Optional[List[ArchitectureComponent]] = None,
) -> str:
    """
    Normalizes and sanitizes Mermaid diagram text produced by LLMs.

    Responsibilities:
    - Fix invalid arrows and labels
    - Ensure valid Mermaid header
    - Normalize node IDs
    - Group nodes into columns using components (if provided)
    - Produce a render-safe Mermaid flowchart
    """

    if not diagram:
        return ""

    diagram = diagram.strip()

    # ---------------------------------------------------------
    # 1) Remove invalid Mermaid characters
    # ---------------------------------------------------------
    diagram = diagram.replace(";", "")

    # Fix invalid label terminator: |label|>
    diagram = diagram.replace("|>", "|")

    # Sometimes |>| becomes || after replacement
    diagram = diagram.replace("||", "|")

    # ---------------------------------------------------------
    # 2) Normalize arrow syntax
    # ---------------------------------------------------------
    diagram = diagram.replace("->>", "-->")
    diagram = diagram.replace("-->>", "-->")
    diagram = diagram.replace("--->", "-->")

    # Replace single arrows (->) with Mermaid arrows (-->)
    diagram = re.sub(r"(?<!-)->(?!>)", "-->", diagram)

    # ---------------------------------------------------------
    # 3) Ensure Mermaid header exists
    # ---------------------------------------------------------
    lines = [ln.strip() for ln in diagram.splitlines() if ln.strip()]

    if not lines:
        return "flowchart LR\n"

    first = lines[0].lower()

    # Convert "graph TD" → "flowchart TD"
    if first.startswith("graph "):
        direction = first.split()[-1].upper() if len(first.split()) > 1 else "LR"
        lines[0] = f"flowchart {direction}"

    # Add default header if missing
    elif not first.startswith("flowchart "):
        lines.insert(0, "flowchart LR")

    header = lines[0]
    body = lines[1:]

    # ---------------------------------------------------------
    # 4) Extract valid edge lines
    # ---------------------------------------------------------
    edge_lines = [ln for ln in body if "-->" in ln or "-.->" in ln]

    # Mapping from node label → node ID
    label_to_id = {}

    def get_node_id(label: str) -> str:
        """
        Returns a stable node ID for a given label.
        """
        label = label.strip().strip('"').strip("'")
        if label not in label_to_id:
            label_to_id[label] = _to_node_id(label)
        return label_to_id[label]

    clean_edges = []

    for edge in edge_lines:
        # Detect arrow type
        arrow = "-.->" if "-.->" in edge else "-->"

        # Split edge
        left, right = edge.split(arrow, 1)
        left = left.strip()
        right = right.strip()

        # Support labeled edges: A -->|label| B
        label = None
        m = re.match(r"^\|(.+?)\|\s*(.+)$", right)
        if m:
            label = m.group(1).strip()
            right = m.group(2).strip()

        # Remove stray pipes from right node
        right = right.lstrip("|").strip()

        # Skip invalid edges
        if not left or not right:
            continue

        # Skip self-loops
        if left.lower() == right.lower():
            continue

        left_id = get_node_id(left)
        right_id = get_node_id(right)

        # Build Mermaid edge
        if label:
            clean_edges.append(
                f'{left_id}["{left}"] {arrow}|{label}| {right_id}["{right}"]'
            )
        else:
            clean_edges.append(
                f'{left_id}["{left}"] {arrow} {right_id}["{right}"]'
            )

    # ---------------------------------------------------------
    # 5) Group nodes into columns using component types
    # ---------------------------------------------------------
    layers = defaultdict(list)

    if components:
        for c in components:
            if not c.name:
                continue

            layer = c.type or "Other"
            nid = _to_node_id(c.name)

            layers[layer].append((nid, c.name))
            label_to_id[c.name] = nid

    # ---------------------------------------------------------
    # 6) Fallback: no components → flat diagram
    # ---------------------------------------------------------
    if not layers:
        out = [header, ""]

        for label, nid in label_to_id.items():
            out.append(f'{nid}["{label}"]')

        out.append("")
        out.extend(clean_edges)

        return "\n".join(out) + "\n"

    # ---------------------------------------------------------
    # 7) Build layered (column-based) diagram
    # ---------------------------------------------------------
    out = ["flowchart LR", ""]

    ordered_layers = list(layers.keys())

    # Create subgraphs (vertical columns)
    for layer in ordered_layers:
        safe_layer = f"layer_{_to_node_id(layer)}"

        out.append(f'subgraph {safe_layer}["{layer}"]')
        out.append("  direction TB")

        for nid, label in layers[layer]:
            out.append(f'  {nid}["{label}"]')

        out.append("end\n")

    # ---------------------------------------------------------
    # 8) Connect layers horizontally
    # ---------------------------------------------------------
    for i in range(len(ordered_layers) - 1):
        left_nodes = layers[ordered_layers[i]]
        right_nodes = layers[ordered_layers[i + 1]]

        if left_nodes and right_nodes:
            out.append(f"{left_nodes[0][0]} --> {right_nodes[0][0]}")

    return "\n".join(out) + "\n"
