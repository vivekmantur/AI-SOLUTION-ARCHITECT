import textwrap
from typing import List, Tuple
from .models import DesignRequest


def build_json_prompt(
    req: DesignRequest,
    patterns: List[Tuple[str, str, float, str]],
    raw_olmo_output: str,
) -> str:

    json_schema_hint = """
{
  "normalized_requirements": {
    "business_goal": "string",
    "primary_users_clients_devices": ["string"],
    "interaction_style": "string",
    "scale_characteristics": {
      "traffic_pattern": "string",
      "concurrency": "string",
      "growth_expectation": "string"
    },
    "data_characteristics": {
      "data_types": ["string"],
      "consistency_needs": "string",
      "latency_sensitivity": "string"
    },
    "security_and_compliance_needs": ["string"],
    "deployment_constraints": ["string"]
  },
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
    "notes": "string"
  },
  "api_spec_stub": "string",
  "infra_as_code_stub": "string",
  "notes": "string"
}
"""

    prompt = f"""
You are a senior cloud solution architect.

Target cloud selected by the user: {req.cloud.upper()}

User Requirements:
\"\"\"{req.requirements}\"\"\"

RAW_DRAFT_FROM_MODEL:
\"\"\"{raw_olmo_output}\"\"\"

====================================================================
TASK
====================================================================

Convert RAW_DRAFT_FROM_MODEL into a COMPLETE JSON solution.

CRITICAL RULES:
1) You MUST populate EVERY field in the schema.
2) Do NOT leave fields empty unless RAW_DRAFT truly has no info.
3) If some details are missing, infer realistic values from requirements.
4) normalized_requirements MUST NOT be empty {{}}.
5) mermaid_diagram MUST NOT be empty.
6) mermaid_diagram MUST be connected and start with "graph TD".
7) Every component must appear in mermaid_diagram.
8) Mermaid arrows MUST use ONLY:
   A --> B
   A -->|label| B
   A -.-> B
   A -.->|label| B
   NEVER use ->> or ==> or --->
9) Component type MUST be one of:
   frontend, api_gateway, backend, auth, messaging, analytics, monitoring, db, storage, caching
   If RAW uses "service", convert it to "backend".

STRICT OUTPUT:
- Output MUST be valid JSON only
- MUST start with '{{' and end with '}}'
- NO markdown, NO explanations, NO reasoning text
- null is NOT allowed anywhere
- if unknown use "" (empty string)

Follow this schema EXACTLY:
{json_schema_hint}

Return ONLY the JSON object.
"""

    return textwrap.dedent(prompt)
