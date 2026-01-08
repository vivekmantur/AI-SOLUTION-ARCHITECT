import re
from typing import List
from .models import ArchitectureComponent


def normalize_mermaid(
    diagram: str,
    components: List[ArchitectureComponent] | None = None,
) -> str:
    if not diagram:
        return diagram

    diagram = diagram.strip()

    # --------------------------------------------------
    # 1. Remove semicolons
    # --------------------------------------------------
    diagram = diagram.replace(";", "")

    # --------------------------------------------------
    # 2. Normalize arrows (FINAL, SAFE)
    # --------------------------------------------------

    # Solid arrows
    diagram = diagram.replace("->>", "-->")
    diagram = diagram.replace("-->>", "-->")
    diagram = diagram.replace("--->", "-->")
    diagram = re.sub(r"(?<!-)->(?!>)", "-->", diagram)

    # 🔥 Dash arrows — collapse ALL malformed variants to '-.->'
    diagram = re.sub(r"-\.+-+>", "-.->", diagram)
    diagram = re.sub(r"-\.+>", "-.->", diagram)
    diagram = diagram.replace("-.-->", "-.->")
    diagram = diagram.replace("-.->>", "-.->")

    # --------------------------------------------------
    # 3. Remove header completely
    # --------------------------------------------------
    diagram = re.sub(
        r"^graph\s+TD\s*\n?",
        "",
        diagram,
        flags=re.IGNORECASE,
    )

    # --------------------------------------------------
    # 4. Extract alias map (A[Label])
    # --------------------------------------------------
    alias_map = {}

    def alias(match):
        alias_map[match.group(1)] = match.group(2)
        return match.group(2)

    diagram = re.sub(r"\b([A-Z])\[(.*?)\]", alias, diagram)

    # --------------------------------------------------
    # 5. Replace alias references (B, C, D → Labels)
    # --------------------------------------------------
    for k, v in alias_map.items():
        diagram = re.sub(rf"\b{k}\b", v, diagram)

    # --------------------------------------------------
    # 6. Extract raw edges ONLY
    # --------------------------------------------------
    raw_edges = []
    for line in diagram.splitlines():
        if "-->" in line or "-.->" in line:
            raw_edges.append(line.strip())

    # --------------------------------------------------
    # 7. Canonicalize nodes
    # --------------------------------------------------
    name_to_node = {}
    if components:
        for c in components:
            nid = (
                c.name.lower()
                .replace(" ", "_")
                .replace("-", "_")
                .replace("/", "_")
            )
            name_to_node[c.name] = f'{nid}["{c.name}"]'

       # --------------------------------------------------
    # 8. Build clean edges (ONE PER LINE)
    # --------------------------------------------------
    clean_edges = []

    for edge in raw_edges:
        # Split arrow
        if "-.->" in edge:
            left, right = edge.split("-.->", 1)
            arrow = "-.->"
        else:
            left, right = edge.split("-->", 1)
            arrow = "-->"

        left = left.strip()
        right = right.strip()

        # Replace nodes
        for name, node in name_to_node.items():
            left = re.sub(rf"\b{re.escape(name)}\b", node, left)
            right = re.sub(rf"\b{re.escape(name)}\b", node, right)

        # Normalize edge-label spacing
        left = re.sub(r"\s*\|\s*([^|]+?)\s*\|\s*", r"|\\1|", left)
        right = re.sub(r"\s*\|\s*([^|]+?)\s*\|\s*", r"|\\1|", right)

        # 🔥 DROP edges without a valid source node
        if not re.search(r'\["[^"]+"\]', left):
            continue

        # 🔥 DROP edges without a valid target node
        if not re.search(r'\["[^"]+"\]', right):
            continue

        clean_edges.append(f"{left}{arrow}{right}")


    # --------------------------------------------------
    # 9. FINAL authoritative sanitize (PIPELINE REBUILD)
    # --------------------------------------------------
    if components:
        # Preferred logical order for analytics platforms
        preferred_order = [
            "Data Ingestion Service",
            "ETL Pipeline",
            "Data Lake",
            "Data Warehouse",
            "BI Dashboard Service",
            "Reporting",
        ]

        def node_id(name: str) -> str:
            return (
                name.lower()
                .replace(" ", "_")
                .replace("-", "_")
                .replace("/", "_")
            )

        component_names = [c.name for c in components]

        # Keep only components that actually exist
        ordered = [n for n in preferred_order if n in component_names]

        # Fallback: preserve component order if heuristic fails
        if not ordered:
            ordered = component_names

        lines = ["flowchart LR", ""]

        # Emit nodes
        for name in ordered:
            lines.append(f'{node_id(name)}["{name}"]')

        lines.append("")

        # Emit edges (linear pipeline)
        for i in range(len(ordered) - 1):
            lines.append(
                f"{node_id(ordered[i])} --> {node_id(ordered[i + 1])}"
            )

        return "\n".join(lines)

    # --------------------------------------------------
    # 10. Fallback (no components)
    # --------------------------------------------------
    return diagram

