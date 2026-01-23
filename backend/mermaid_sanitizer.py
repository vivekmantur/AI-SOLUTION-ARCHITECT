import re
from typing import List, Optional
from .models import ArchitectureComponent


def _to_node_id(name: str) -> str:
    if not name:
        return "node"

    nid = name.lower().strip()
    nid = re.sub(r"\(.*?\)", "", nid)  # remove (ADF) etc from ID only
    nid = re.sub(r"[^a-z0-9]+", "_", nid)
    nid = nid.strip("_")
    return nid or "node"


def normalize_mermaid(
    diagram: str,
    components: Optional[List[ArchitectureComponent]] = None,
) -> str:
    if not diagram:
        return ""

    diagram = diagram.strip()

    # 1) Remove semicolons
    diagram = diagram.replace(";", "")

    # 2) Fix invalid Mermaid label terminator: |label|>
    diagram = diagram.replace("|>", "|")

    # ✅ IMPORTANT: after fixing |>, it becomes || sometimes
    diagram = diagram.replace("||", "|")

    # 3) Normalize arrows
    diagram = diagram.replace("->>", "-->")
    diagram = diagram.replace("-->>", "-->")
    diagram = diagram.replace("--->", "-->")
    diagram = re.sub(r"(?<!-)->(?!>)", "-->", diagram)

    # 4) Ensure header exists
    lines = [ln.strip() for ln in diagram.splitlines() if ln.strip()]
    if not lines:
        return "flowchart LR\n"

    first = lines[0].lower()
    if first.startswith("graph "):
        direction = first.split()[-1].upper() if len(first.split()) > 1 else "LR"
        lines[0] = f"flowchart {direction}"
    elif not first.startswith("flowchart "):
        lines.insert(0, "flowchart LR")

    header = lines[0]
    body = lines[1:]

    # 5) Extract edge lines
    edge_lines = [ln for ln in body if "-->" in ln or "-.->" in ln]

    if not edge_lines:
        return header + "\n"

    label_to_id = {}

    def get_node_id(label: str) -> str:
        label = label.strip().strip('"').strip("'")
        if label not in label_to_id:
            label_to_id[label] = _to_node_id(label)
        return label_to_id[label]

    clean_edges = []

    for edge in edge_lines:
        arrow = "-.->" if "-.->" in edge else "-->"

        left, right = edge.split(arrow, 1)
        left = left.strip()
        right = right.strip()

        # support arrow labels: A -->|label| B
        label = None
        m = re.match(r"^\|(.+?)\|\s*(.+)$", right)
        if m:
            label = m.group(1).strip()
            right = m.group(2).strip()

        # fix if right starts with stray "|"
        right = right.lstrip("|").strip()

        if not left or not right:
            continue

        # drop self-loops
        if left.lower() == right.lower():
            continue

        left_id = get_node_id(left)
        right_id = get_node_id(right)

        if label:
            clean_edges.append(
                f'{left_id}["{left}"] {arrow}|{label}| {right_id}["{right}"]'
            )
        else:
            clean_edges.append(
                f'{left_id}["{left}"] {arrow} {right_id}["{right}"]'
            )

    if not clean_edges:
        return header + "\n"

    # 6) Emit nodes (from components + from edges)
    node_lines = []

    if components:
        for c in components:
            if not c.name:
                continue
            nid = _to_node_id(c.name)
            node_lines.append(f'{nid}["{c.name}"]')
            label_to_id[c.name] = nid

    for label, nid in label_to_id.items():
        node_lines.append(f'{nid}["{label}"]')

    # remove duplicates
    seen = set()
    final_nodes = []
    for n in node_lines:
        if n not in seen:
            final_nodes.append(n)
            seen.add(n)

    out = [header, ""]
    out.extend(final_nodes)
    out.append("")
    out.extend(clean_edges)

    return "\n".join(out) + "\n"
