import textwrap
from typing import List, Tuple
from .models import DesignRequest


def build_design_prompt(
    req: DesignRequest,
    patterns: List[Tuple[str, str, float, str]],
) -> str:
    """
    Domain-agnostic, cloud-aware architecture prompt.
    Enforces full output up to section 9 and guarantees
    a non-empty, connected Mermaid diagram.
    """

    # -------------------------------------------------------
    # Reference patterns (optional guidance only)
    # -------------------------------------------------------
    patterns_snippet = ""
    for name, text, score, category in patterns:
        patterns_snippet += (
            f"\n=== REFERENCE PATTERN: {name} "
            f"(category={category}, similarity={score:.2f}) ===\n{text}\n"
        )

    # -------------------------------------------------------
    # STRICT JSON SCHEMA
    # -------------------------------------------------------
    json_schema_hint = """
{
  "normalized_requirements": {},
  "chosen_pattern": "string or null",
  "architecture_description": "string",
  "mermaid_diagram": "string",
  "components": [
    {
      "name": "string",
      "type": "frontend | api_gateway | backend | auth | messaging | analytics | monitoring | db | storage | caching",
      "cloud_service": "string or null",
      "description": "string or null"
    }
  ],
  "non_functional_considerations": ["string"],
  "tech_stack": ["string"],
  "cost_estimate": {
    "total_monthly_usd": 0,
    "per_environment": [
      { "environment": "dev", "monthly_usd": 0 },
      { "environment": "uat", "monthly_usd": 0 },
      { "environment": "prod", "monthly_usd": 0 }
    ],
    "notes": "string or null"
  },
  "api_spec_stub": "string",
  "infra_as_code_stub": "string",
  "notes": "string or null"
}
"""

    # -------------------------------------------------------
    # PROMPT
    # -------------------------------------------------------
    prompt = f"""
You are a **senior cloud solution architect**.

Target cloud selected by the user: **{req.cloud.upper()}**

The user has provided the following requirements:

\"\"\"{req.requirements}\"\"\"


The following architecture patterns may be used as **optional references only**.
They must NEVER override the user's requirements.

{patterns_snippet}

====================================================================
TASK 1 — NORMALIZE REQUIREMENTS
====================================================================

Convert the raw input into a structured, domain-agnostic form:

- Business goal
- Primary users / clients / devices
- Interaction style (request-response, event-driven, real-time, batch)
- Scale characteristics:
  - traffic pattern
  - concurrency
  - growth expectation
- Data characteristics:
  - data types
  - consistency needs
  - latency sensitivity
- Security and compliance needs
- Deployment constraints

Store this under `normalized_requirements`.

====================================================================
TASK 2 — INFER DOMAIN CAPABILITIES (NO HARDCODING)
====================================================================

- Infer system capabilities ONLY from the requirements
- Do NOT assume a predefined domain
- Capabilities must come from user intent
- Examples (not exhaustive):
  - browsing
  - cart management
  - ordering
  - payments
  - real-time messaging
  - ingestion
  - analytics
  - authentication
  - storage

====================================================================
TASK 3 — CHOOSE PATTERN (OPTIONAL)
====================================================================

- Select a pattern ONLY if it clearly fits
- Otherwise set `"chosen_pattern": null`
- Justify briefly in `notes`

====================================================================
CRITICAL TWO-PHASE ARCHITECTURE RULE (MANDATORY)
====================================================================

----------------------------
PHASE 1 — COMPONENT FINALIZATION
----------------------------

- Finalize ALL components FIRST
- `components` is the SINGLE source of truth
- Each component MUST:
  - Have exactly ONE responsibility
  - Use ONE allowed type:
    frontend | api_gateway | backend | auth | messaging |
    analytics | monitoring | db | storage | caching

- Do NOT merge responsibilities
- If the system is real-time or event-driven → messaging is REQUIRED
- If users or APIs exist → authentication is REQUIRED
- Backend services MUST NOT be isolated

----------------------------
PHASE 2 — CONNECTION FINALIZATION (MANDATORY)
----------------------------

Before drawing the diagram, you MUST mentally finalize ALL connections.

Rules:
- Every component MUST appear in at least one connection
- No standalone components are allowed
- Frontend → API Gateway or Backend
- API Gateway → at least one Backend
- Backend → Backend OR Database OR Storage OR Messaging
- Messaging → at least one producer AND one consumer
- Database / Storage / Cache → at least one Backend

If any component is unconnected, the architecture is INVALID.

====================================================================
CRITICAL FAILURE CONDITION (NON-NEGOTIABLE)
====================================================================

The `mermaid_diagram` field MUST contain a COMPLETE diagram.

If `mermaid_diagram` is:
- an empty string
- missing
- or contains only `graph TD` with no edges

THEN THE OUTPUT IS INVALID AND MUST BE REGENERATED.

INVALID EXAMPLE (DO NOT DO THIS):
graph TD
A[Web Frontend]

VALID MINIMUM EXAMPLE:
graph TD
A[Web Frontend] --> B[API Gateway]

====================================================================
TASK 4 — ARCHITECTURE DESCRIPTION
====================================================================

Write a concise architecture overview explaining:
- Architecture style
- Responsibility separation
- Scalability and availability
- Sync vs async interactions

====================================================================
TASK 5 — MERMAID DIAGRAM (MANDATORY)
====================================================================

Generate a valid Mermaid diagram:

- Use `graph TD`
- Allowed arrows ONLY:
  A --> B
  A -->|label| B
  A -.-> B
  A -.->|label| B
- No markdown fences
- No actors like User / Client
- No generic nodes

RULES:
- EVERY component MUST appear
- EVERY component MUST be connected
- Names MUST match components EXACTLY
- Diagrams with isolated nodes are INVALID

====================================================================
TASK 6 — NON-FUNCTIONAL CONSIDERATIONS
====================================================================

List NFRs such as:
- scalability
- availability
- latency
- security
- observability
- fault tolerance

====================================================================
TASK 7 — TECH STACK
====================================================================

Propose a realistic tech stack:
- languages
- frameworks
- messaging
- databases
- infrastructure tools

====================================================================
TASK 8 — COST ESTIMATE
====================================================================

Provide a rough monthly estimate:
- total
- dev / uat / prod
- assumptions in notes

====================================================================
TASK 9 — API & INFRASTRUCTURE STUBS
====================================================================

- Provide 2–3 API endpoints
- Provide an IaC stub (Terraform / Bicep / CloudFormation)

====================================================================
CLOUD AWARENESS RULE
====================================================================

- If `cloud_service` is set:
  - It MUST be valid for **{req.cloud.upper()}**
  - It MUST match the component type
- If unsure, set it to null

====================================================================
ABSOLUTE OUTPUT RULES (NON-NEGOTIABLE)
====================================================================

- Output MUST be valid JSON
- Output MUST start with '{{' and end with '}}'
- Do NOT include markdown
- Do NOT include explanations
- JSON MUST conform EXACTLY to this schema:

{json_schema_hint}

Return ONLY the JSON object.
"""

    return textwrap.dedent(prompt)
