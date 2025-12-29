import re

def extract_diagram_components(mermaid: str) -> set[str]:
    """
    Extracts component names from Mermaid diagram.
    Normalizes labels like:
    'Web Frontend (frontend)' -> 'Web Frontend'
    """
    components = set()

    for line in mermaid.splitlines():
        matches = re.findall(r'\[(.*?)\]', line)
        for label in matches:
            clean = re.sub(r'\s*\(.*?\)\s*', '', label).strip()
            components.add(clean)

    return components



def extract_mandatory_components(pattern_text: str) -> list[str]:
    components = []
    capture = False

    for line in pattern_text.splitlines():
        line = line.strip()
        if line.lower() == "## mandatory components":
            capture = True
            continue
        if capture:
            if line.startswith("-"):
                components.append(line.replace("-", "").strip())
            elif line.startswith("##"):
                break

    return components

def validate_domain_isolation(components):
    forbidden = {
        "order": ["payment", "inventory", "cart"],
        "payment": ["order", "inventory"],
        "inventory": ["order", "payment"],
    }

    for c in components:
        name = c.name.lower()
        desc = (c.description or "").lower()

        for domain, forbidden_terms in forbidden.items():
            if domain in name:
                for term in forbidden_terms:
                    if term in desc:
                        raise ValueError(
                            f"{c.name} violates domain isolation by handling '{term}'"
                        )


def validate_domain_completeness(
    chosen_pattern: str,
    patterns: list,
    components: list
):
    """
    Enforces mandatory domain components.
    Only applies to DOMAIN patterns.
    """
    # Find the selected pattern text + category
    selected = None
    for name, text, score, category in patterns:
        if name == chosen_pattern:
            selected = (text, category)
            break

    if not selected:
        return  # no validation if pattern not found

    pattern_text, category = selected

    # Only enforce for domain patterns
    if category != "domain":
        return

    required = extract_mandatory_components(pattern_text)
    actual = {c.name for c in components}

    missing = [r for r in required if r not in actual]

    if missing:
        raise ValueError(
            f"Architecture INVALID. Missing mandatory domain components: {missing}"
        )

def validate_diagram_matches_components(mermaid: str, components: list):
    diagram_nodes = extract_diagram_components(mermaid)
    component_names = {c.name for c in components}

    missing_in_diagram = component_names - diagram_nodes
    extra_in_diagram = diagram_nodes - component_names

    if missing_in_diagram or extra_in_diagram:
        raise ValueError(
            f"Diagram mismatch.\n"
            f"Missing in diagram: {missing_in_diagram}\n"
            f"Extra in diagram: {extra_in_diagram}"
        )

# validators.py
AZURE_SERVICE_MAP = {
    "frontend": {
        "Azure Static Web Apps",
        "Azure App Service"
    },
    "api_gateway": {
        "Azure API Management"
    },
    "backend": {
        "Azure App Service",
        "Azure Container Apps",
        "Azure Kubernetes Service",
        "Azure Functions"
    },
    "messaging": {
        "Azure Service Bus",
        "Azure Event Grid",
        "Azure Event Hubs"
    },
    "analytics": {
        "Azure Synapse Analytics",
        "Azure Data Explorer"
    },
    "db": {
        "Azure SQL Database",
        "Azure Cosmos DB"
    },
    "storage": {
        "Azure Blob Storage",
        "Azure Data Lake Storage"
    },
    "caching": {
        "Azure Cache for Redis"
    },
    "monitoring": {
        "Azure Monitor",
        "Application Insights"
    },
    "auth": {
        "Azure AD",
        "Microsoft Entra ID"
    }
}




def validate_azure_services(components):
    """
    Ensures each component uses a valid Azure service
    according to its architectural role.
    """
    errors = []

    for c in components:
        if not c.cloud_service:
            continue  # optional, but allowed

        allowed_services = AZURE_SERVICE_MAP.get(c.type)

        if not allowed_services:
            continue  # unknown type, skip

        if c.cloud_service not in allowed_services:
            errors.append(
                f"{c.name} ({c.type}) uses invalid Azure service: "
                f"{c.cloud_service}. Allowed: {allowed_services}"
            )

    if errors:
        raise ValueError(" | ".join(errors))
