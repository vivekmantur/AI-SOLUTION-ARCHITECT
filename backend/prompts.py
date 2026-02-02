import textwrap
from .models import DesignRequest


def build_7task_architecture_prompt(req: DesignRequest) -> str:
    """
    7-task domain-agnostic architecture prompt.
    Output in STRICT NORMAL TEXT (NOT JSON, NOT Markdown, NOT LaTeX)
    """

    prompt = f"""
You are a senior cloud solution architect.

Target cloud selected by the user: {req.cloud.upper()}

User Requirements:
{req.requirements}

====================================================================
TASK 1 — NORMALIZE REQUIREMENT (Structured Understanding)
====================================================================
Rewrite the requirement in a structured format showing what you understood.
Keep it short but complete.
Must include:
- Business goal
- Primary users
- Input systems / data sources
- Expected outputs (dashboards, reports, APIs, apps, etc.)
- Interaction style (batch, real-time, event-driven, request-response)
- Data characteristics (volume, velocity, variety)
- Quality and reliability expectations
- Performance expectations
- Security, privacy, or compliance needs (if implied)
- Cost or operational constraints (if implied)

Store this under Task 1 output.

====================================================================
TASK 2 — SELECTED DOMAIN PLATFORM ARCHITECTURE (High Level)
====================================================================
Identify the most relevant domain based on the requirement.

Then provide a "Platform Architecture (High Level)" using numbered sections like:

1) ...
2) ...
3) ...
...
N) Monitoring + Governance + Optimization

Rules:
- Each section must be concise (2–5 lines max)
- Must cover full end-to-end flow
- Must be domain-appropriate
- The final section MUST cover monitoring, governance, and optimization

Store this under Task 2 output.

====================================================================
TASK 3 — ARCHITECTURE FLOW DIAGRAM (Text View)
====================================================================
Provide ONLY a text-based flow diagram in this format:

[Component / Layer]
   | (optional short label)
   v
[Next Component / Layer]

Rules:
- No explanations here
- Must represent Task 2 accurately
- Must be fully connected from start to end
- Keep it readable and compact
- TASK 3 must describe ONLY the primary end-to-end data flow.
- Do NOT include security, governance, monitoring, cataloging, or side dependencies.

Store this under Task 3 output.

====================================================================
TASK 4 — BEST ARCHITECTURE RECOMMENDATION
====================================================================
Recommend the best overall architecture approach for this requirement.

Must include:
- Architecture style or approach name
- Why it fits the domain
- How it balances correctness, scalability, resilience, and operational efficiency
- Trade-offs if any

Keep this to 4–7 lines.

Store this under Task 4 output.

====================================================================
TASK 5 — KEY DESIGN DECISIONS (Domain-Driven)
====================================================================
Identify the MOST IMPORTANT design decision categories for this system
based strictly on the requirement and selected domain.

Rules:
- Choose 3 to 5 categories dynamically
- Each category must have a clear heading
- Under each heading, provide 2–4 concise decision points
- Categories MUST vary depending on the requirement/domain
- Do NOT force generic categories if they are not relevant

Store this under Task 5 output.

====================================================================
TASK 6 — COMPONENTS (Finalized List)
====================================================================
Finalize a complete list of architecture components needed.

Component type rules:
- Component "type" MUST be a lowercase snake_case identifier
- Type MUST describe the component’s primary responsibility
- Types MUST be domain-appropriate and requirement-driven

Examples (not exhaustive):
- data_sources
- ingestion
- streaming
- processing
- batch_processing
- real_time_processing
- storage
- warehouse
- lakehouse
- semantic_layer
- api_backend
- backend_service
- frontend
- auth
- messaging
- event_router
- event_processing
- bi_reporting
- ml_training
- ml_inference
- caching
- monitoring
- governance
- security
- orchestration

MANDATORY COMPONENT FIELD RULE:
Every component MUST include:
- name
- type
- cloud_service
- description

If unknown → set "" (empty string). Never use null.

STRICT RULES:
- No placeholder components
- No mixing cloud providers
- Do NOT merge unrelated responsibilities into one component
- Components MUST align with Task 2 architecture flow
- Components MUST be granular enough to be diagrammed clearly

Store this under Task 6 output.


====================================================================
TASK 7 — MERMAID DIAGRAM (MANDATORY)
====================================================================
Create a Mermaid diagram that connects ALL components from Task 6.

Rules:
- MUST start with: graph TD
- Allowed arrows ONLY:
  A --> B
  A -->|label| B
  A -.-> B
  A -.->|label| B

STRICT PROHIBITIONS:
- NO ->>
- NO external actors (User, Client, Analyst)
- NO undeclared nodes
- Node names MUST match component names EXACTLY from Task 6

Diagram MUST be non-empty and connected.
Every component MUST appear in at least one connection.

Store this under Task 7 output.

====================================================================
CLOUD AWARENESS & SERVICE SELECTION
====================================================================
For EVERY component, cloud_service MUST be present.
Value MUST be:
- a valid managed cloud service for {req.cloud.upper()}
OR
- "" (empty string)

DO NOT:
- Mix clouds
- Invent services
- Assign infra tools (Docker, Terraform) as cloud_service
- Assign SaaS products (Snowflake, Databricks) as cloud_service

====================================================================
ABSOLUTE OUTPUT RULES (STRICT)
====================================================================
Return ONLY NORMAL TEXT.
DO NOT output JSON.
DO NOT output Markdown.
DO NOT use markdown headings (#, ##).
DO NOT use code blocks using ``` anywhere.
DO NOT use tables.

Output MUST follow EXACTLY this template:

TASK 1 — NORMALIZE REQUIREMENT
...

TASK 2 — SELECTED DOMAIN PLATFORM ARCHITECTURE (High Level)
...

TASK 3 — ARCHITECTURE FLOW DIAGRAM (Text View)
...

TASK 4 — BEST ARCHITECTURE RECOMMENDATION
...

TASK 5 — KEY DESIGN DECISIONS
Category Name:
- ...
- ...

Category Name:
- ...
- ...

Category Name:
- ...
- ...

TASK 6 — COMPONENTS (Finalized List)
component:
name: ...
type: ...
cloud_service: ...
description: ...

component:
name: ...
type: ...
cloud_service: ...
description: ...

TASK 7 — MERMAID DIAGRAM
graph TD
A --> B

Start now.
"""

    return textwrap.dedent(prompt)
