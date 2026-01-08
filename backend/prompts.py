import textwrap
from typing import List, Tuple
from .models import DesignRequest


def build_design_prompt(
    req: DesignRequest,
    patterns: List[Tuple[str, str, float, str]],
) -> str:
    """
    Domain-agnostic, cloud-aware architecture prompt.
    Enforces:
    - Non-empty components
    - Non-empty connected Mermaid diagram
    - Explicit cloud_service field (never missing)
    - Pattern authority when selected
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
    # STRICT JSON SCHEMA (DO NOT DEVIATE)
    # -------------------------------------------------------
    json_schema_hint = """
{
  "normalized_requirements": {},
  "chosen_pattern": "string",
  "architecture_description": "string",
  "mermaid_diagram": "string",
  "components": [
    {
      "name": "string",
      "type": "frontend | api_gateway | backend | auth | messaging | analytics | monitoring | db | storage | caching",
      "cloud_service": "string",
      "description": "string"
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
  "notes": "string"
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
They must NEVER override the user's requirements unless explicitly selected.

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

Infer system capabilities ONLY from the requirements.
Do NOT assume a predefined domain.

Capabilities must be expressed as concrete responsibilities.

Examples (not exhaustive):
- browsing
- order_processing
- payment_processing
- fraud_detection
- audit_logging
- streaming_ingestion
- analytics
- authentication
- storage

====================================================================
TASK 3 — CHOOSE PATTERN (STRICT & AUTHORITATIVE)
====================================================================

Select a pattern if it clearly fits.

STRICT OVERRIDE RULE:
When a pattern is selected:
- You MUST NOT invent alternative architectures
- You MUST NOT remove or rename Mandatory Components
- You MUST follow DIAGRAM_HINTS EXACTLY

When selected:
- `chosen_pattern` MUST be the pattern name
- ALL Mandatory Components MUST appear
- ALL Required Connections MUST appear

If no pattern fits:
- Set `"chosen_pattern": null`

IMPORTANT:
Even if `chosen_pattern` is null, architecture generation MUST continue.

====================================================================
MANDATORY ARCHITECTURE GENERATION RULE
====================================================================

Even when `"chosen_pattern": null`:

- You MUST define components
- You MUST generate a connected mermaid_diagram
- You MUST satisfy all user requirements

Null pattern does NOT mean no architecture.

====================================================================
CRITICAL TWO-PHASE ARCHITECTURE RULE
====================================================================

----------------------------
PHASE 1 — COMPONENT FINALIZATION
----------------------------

Finalize ALL components FIRST.

If a pattern is selected:
- Start by adding ALL Mandatory Components from the pattern
- Then add any additional components required by user requirements


Rules:
- `components` is the SINGLE source of truth
- Each component has exactly ONE responsibility
- Use ONLY allowed types

Allowed component types:
- frontend
- api_gateway
- backend
- auth
- messaging
- analytics
- monitoring
- db
- storage
- caching

MANDATORY COMPONENT FIELD RULE:
Every component object MUST include:
- name
- type
- cloud_service
- description

If unknown → explicitly set to an empty string "".
Null values are NOT allowed anywhere in the output.

MANDATORY API GATEWAY RULE:
If a selected pattern includes an API Gateway → it MUST exist.

STRICT RULES:
- No placeholder services
- No merged responsibilities
- If async/event-driven → messaging REQUIRED
- If APIs/users exist → authentication REQUIRED

----------------------------
PHASE 2 — CONNECTION FINALIZATION
----------------------------

Every component MUST appear in at least one connection.

Connection semantics:
- Frontend → API Gateway / Backend
- API Gateway → Backend
- Backend → Database / Storage
- Backend → Messaging
- Messaging → Backend
- Monitoring / Audit consume events asynchronously

No isolated components allowed.

====================================================================
CRITICAL FAILURE CONDITION
====================================================================

`mermaid_diagram` MUST be non-empty and connected.

Invalid if:
- empty
- missing
- only `graph TD`

====================================================================
MANDATORY PATTERN COMPONENT INJECTION RULE (CRITICAL)
====================================================================

If `chosen_pattern` is NOT null:

- You MUST extract ALL "Mandatory Components" from the selected pattern
- You MUST insert EVERY Mandatory Component into the main `components` list
- These components are NOT optional
- They MUST NOT be renamed, merged, or omitted
- They MUST obey the same component rules as all others:
  - exactly one responsibility
  - valid component type
  - cloud_service assigned (or null)
  - description provided

Pattern Mandatory Components MUST:
- appear in `components`
- appear in `mermaid_diagram`
- participate in at least one connection

FAILURE TO INCLUDE ANY mandatory pattern component is INVALID OUTPUT.


====================================================================
TASK 4 — ARCHITECTURE DESCRIPTION
====================================================================

Explain:
- Architecture style
- Responsibility separation
- Scalability & availability
- Sync vs async flows
- Consistency strategy

====================================================================
TASK 5 — MERMAID DIAGRAM (MANDATORY)
====================================================================

Rules:
- Use `graph TD`
- Allowed arrows ONLY:
  A --> B
  A -->|label| B
  A -.-> B
  A -.->|label| B

STRICT PROHIBITIONS:
- NO `->>`
- NO external actors (User, Client)
- NO undeclared nodes
- Node names MUST match `components`

If a pattern is selected:
- The diagram MUST include ALL Mandatory Components from the pattern
- Missing even one mandatory component is INVALID


====================================================================
TASK 6 — NON-FUNCTIONAL CONSIDERATIONS
====================================================================

List NFRs:
- scalability
- availability
- latency
- security
- observability
- compliance

====================================================================
TASK 7 — TECH STACK
====================================================================

Propose realistic stack aligned with architecture.

====================================================================
TASK 8 — COST ESTIMATE
====================================================================

Provide:
- total
- dev / uat / prod
- assumptions

====================================================================
TASK 9 — API & INFRASTRUCTURE STUBS
====================================================================

Provide:
- api_spec_stub (string)
- infra_as_code_stub (string)

IMPORTANT:
- The field name MUST be exactly "infra_as_code_stub"
- DO NOT invent alternative field names
- DO NOT add suffixes like "_terraform" or "_bicep"

====================================================================
CLOUD AWARENESS & SERVICE SELECTION
====================================================================

For EVERY component, `cloud_service` MUST be present.

The value MAY be:
- a valid managed cloud service for **{req.cloud.upper()}**
- OR null

If assigned:
- MUST match component type
- MUST be a real managed service
- MUST belong to selected cloud

DO NOT:
- Invent services
- Mix clouds
- Assign infra tools (Docker, Terraform)
- Assign SaaS products (Stripe, Snowflake)

====================================================================
ABSOLUTE OUTPUT RULES
====================================================================

- Output MUST be valid JSON
- MUST start with '{{' and end with '}}'
- NO markdown
- NO explanations
- MUST conform EXACTLY to this schema:

GLOBAL CONSTRAINT:
- The value null is NOT allowed anywhere in the JSON.
- If information is unknown or not applicable, use "" (empty string).

Follow the json schema strictly
{json_schema_hint}

Return ONLY the JSON object.
"""

    return textwrap.dedent(prompt)
