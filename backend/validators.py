# validators.py

import re

def extract_diagram_components(mermaid: str) -> set[str]:
    """
    Extract component NAMES from Mermaid labels.
    Works ONLY with ID-based Mermaid diagrams.
    """
    return set(re.findall(r'\["([^"]+)"\]', mermaid))



def validate_diagram_matches_components(mermaid: str, components: list):
    diagram_components = extract_diagram_components(mermaid)
    component_names = {c.name for c in components}

    missing = diagram_components - component_names
    if missing:
        raise ValueError(
            f"Diagram references undefined components: {missing}"
        )


def validate_domain_isolation(components):
    """
    Detect domain isolation violations.
    DOES NOT raise — returns violations for auto-fix.
    """
    forbidden = {
        "order": ["payment", "inventory", "cart"],
        "payment": ["order", "inventory"],
        "inventory": ["order", "payment"],
    }

    violations = []

    for c in components:
        name = (c.name or "").lower()
        desc = (c.description or "").lower()

        for domain, forbidden_terms in forbidden.items():
            if domain in name:
                for term in forbidden_terms:
                    if term in desc:
                        violations.append({
                            "service": c,
                            "violated_domain": term
                        })

    return violations
