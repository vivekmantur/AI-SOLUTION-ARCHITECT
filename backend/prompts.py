import textwrap
from typing import List, Tuple
from .models import DesignRequest


def build_design_prompt(
    req: DesignRequest,
    patterns: List[Tuple[str, str, float, str]],  # keep as-is (no change in calling code)
) -> str:
    """
    Domain-agnostic, cloud-aware architecture prompt.
    Output in STRICT NORMAL TEXT DRAFT (NOT JSON, NOT Markdown, NOT LaTeX)
    """

    prompt = f"""
You are a senior cloud solution architect.

Target cloud selected by the user: {req.cloud.upper()}

User Requirements:
{req.requirements}

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

Store this under section 1.

====================================================================
TASK 2 — INFER DOMAIN CAPABILITIES
====================================================================
Infer system capabilities ONLY from the requirements.
Do NOT assume a predefined domain.
Capabilities must be expressed as concrete responsibilities.

Store this under section 2.

====================================================================
TASK 3 — CHOOSE PATTERN (STRICT)
====================================================================
Do NOT use any external reference patterns.
chosen_pattern MUST be empty string "".

Store this under section 3.

====================================================================
CRITICAL TWO-PHASE ARCHITECTURE RULE
====================================================================

PHASE 1 — COMPONENT FINALIZATION
Finalize ALL components FIRST.

Allowed component types (ONLY):
frontend
api_gateway
backend
auth
messaging
analytics
monitoring
db
storage
caching

MANDATORY COMPONENT FIELD RULE:
Every component MUST include:
- name
- type
- cloud_service
- description

If unknown → set "" (empty string). Never use null.

STRICT RULES:
- No placeholder services
- No merged responsibilities
- If async/event-driven → messaging REQUIRED
- If APIs/users exist → authentication REQUIRED

Store this under section 4.

PHASE 2 — CONNECTION FINALIZATION
Every component MUST appear in at least one connection.
No isolated components allowed.

====================================================================
TASK 4 — ARCHITECTURE DESCRIPTION
====================================================================
Explain:
- Architecture style
- Responsibility separation
- Scalability & availability
- Sync vs async flows
- Consistency strategy

Store this under section 5.

====================================================================
TASK 5 — MERMAID DIAGRAM (MANDATORY)
====================================================================
Rules:
- MUST start with graph TD
- Allowed arrows ONLY:
  A --> B
  A -->|label| B
  A -.-> B
  A -.->|label| B

STRICT PROHIBITIONS:
- NO ->>
- NO external actors (User, Client)
- NO undeclared nodes
- Node names MUST match component names EXACTLY

Diagram MUST be non-empty and connected.
Every component MUST appear in at least one connection.

Store this under section 6.

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

Store this under section 7.

====================================================================
TASK 7 — TECH STACK
====================================================================
Store this under section 8.

====================================================================
TASK 8 — COST ESTIMATE
====================================================================
Provide:
- total monthly cost estimate
- dev / uat / prod cost breakdown
- assumptions

Store this under section 9.

====================================================================
TASK 9 — API & INFRASTRUCTURE STUBS
====================================================================
Provide:
- api_spec_stub (basic endpoints + payload structure)
- infra_as_code_stub (sample IaC skeleton)

Store this under section 10 and 11.

IMPORTANT:
The section title MUST be exactly: 11) Infra as Code Stub

====================================================================
CLOUD AWARENESS & SERVICE SELECTION
====================================================================
For EVERY component, cloud_service MUST be present.
Value MUST be:
- a valid managed cloud service for {req.cloud.upper()}
OR
- "" (empty string)

DO NOT:
- Invent services
- Mix clouds
- Assign infra tools (Docker, Terraform)
- Assign SaaS products (Stripe, Snowflake)

====================================================================
ABSOLUTE OUTPUT RULES (CRITICAL)
====================================================================

Return ONLY NORMAL TEXT DRAFT.

ABSOLUTE PROHIBITIONS:
- NO JSON output
- NO markdown formatting
- NO markdown headings (#, ##)
- NO markdown tables (pipes like |)
- NO code blocks using ``` anywhere
- NO LaTeX (\\boxed, \\begin, \\end, aligned, equation, \\text)
- NO bullet symbols like **bold**
- NO separators like --- 

You MUST output ALL sections from 1) to 12) in order.
Do NOT stop early.
If you run out of space, shorten the content but NEVER skip sections.

Use EXACTLY this output template:

1) Normalized Requirements
business_goal: ...
primary_users_clients_devices: ...
interaction_style: ...
scale_characteristics:
  traffic_pattern: ...
  concurrency: ...
  growth_expectation: ...
data_characteristics:
  data_types: ...
  consistency_needs: ...
  latency_sensitivity: ...
security_and_compliance_needs: ...
deployment_constraints: ...

2) Inferred Capabilities
capability: ...
capability: ...

3) Chosen Pattern
chosen_pattern: ...

4) Components (Finalized List)
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

5) Architecture Description
...

6) Mermaid Diagram
graph TD
A --> B

7) Non-Functional Considerations
nfr: ...
nfr: ...

8) Tech Stack
tech: ...
tech: ...

9) Cost Estimate
total_monthly_usd: ...
dev_monthly_usd: ...
uat_monthly_usd: ...
prod_monthly_usd: ...
assumptions: ...

10) API Spec Stub
...

11) Infra as Code Stub
...

12) Notes
...

FINAL OUTPUT CONTRACT (STRICT)
You MUST output EXACTLY 12 sections.
The first characters of your output MUST be:

1) Normalized Requirements

Start now.
"""

    return textwrap.dedent(prompt)
