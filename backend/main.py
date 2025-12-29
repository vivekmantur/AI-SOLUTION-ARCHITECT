from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

import json
import re
from pathlib import Path

from .validators import (
    validate_diagram_matches_components,
    extract_diagram_components,
    validate_domain_isolation,
)

from .models import (
    DesignRequest,
    DesignResponse,
    SolutionDesign,
    ArchitectureComponent,
    CostEstimate,
    EnvironmentCost,
)

from .patterns_store import pattern_store
from .prompts import build_design_prompt
from .llm_client import call_llm
from .report_generator import generate_pdf_report


app = FastAPI(title="AI Solution Architect API")

# -------------------------------------------------------------------
# CORS
# -------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------------------
# Frontend (React build)
# -------------------------------------------------------------------
FRONTEND_BUILD_DIR = Path(__file__).parent.parent / "frontend" / "build"

if FRONTEND_BUILD_DIR.exists():
    app.mount(
        "/static",
        StaticFiles(directory=str(FRONTEND_BUILD_DIR / "static")),
        name="static",
    )

# -------------------------------------------------------------------
# Mermaid sanitization
# -------------------------------------------------------------------
def sanitize_mermaid_diagram(diagram: str) -> str:
    if not diagram or not diagram.strip():
        return "graph TD"

    diagram = re.sub(r'^```mermaid\s*\n?', '', diagram, flags=re.MULTILINE)
    diagram = re.sub(r'\n?```\s*$', '', diagram, flags=re.MULTILINE)

    diagram = re.sub(r'-->\|([^|]+)\|>', r'-->|\1|', diagram)
    diagram = re.sub(r'-\.\->\|([^|]+)\|>', r'-.->|\1|', diagram)
    diagram = re.sub(r'==>\|([^|]+)\|>', r'==>|\1|', diagram)

    diagram = re.sub(r'--+>', '-->', diagram)
    diagram = re.sub(r'-\.\.+>', '-.->', diagram)
    diagram = re.sub(r'==+>', '==>', diagram)

    diagram = re.sub(r';\s*$', '', diagram, flags=re.MULTILINE)

    if not re.match(r'^\s*graph\s+TD', diagram, re.IGNORECASE):
        diagram = "graph TD\n" + diagram

    return diagram.strip()

# -------------------------------------------------------------------
# Diagram ↔ Component reconciliation
# -------------------------------------------------------------------
def reconcile_components_with_diagram(mermaid: str, components: list):
    diagram_nodes = extract_diagram_components(mermaid)
    component_names = {c.name for c in components}

    missing = diagram_nodes - component_names

    for name in missing:
        if "Cache" in name or "Redis" in name:
            inferred_type = "caching"
        elif "Database" in name or "DB" in name:
            inferred_type = "db"
        elif "Queue" in name or "Bus" in name:
            inferred_type = "messaging"
        elif "Gateway" in name:
            inferred_type = "api_gateway"
        else:
            inferred_type = "backend"

        components.append(
            ArchitectureComponent(
                name=name,
                type=inferred_type,
                cloud_service=None,
                description="Auto-added from diagram to maintain consistency",
            )
        )

def reconcile_diagram_with_components(mermaid: str, components: list) -> str:
    diagram_nodes = extract_diagram_components(mermaid)
    component_names = {c.name for c in components}

    missing = component_names - diagram_nodes
    if not missing:
        return mermaid

    lines = mermaid.splitlines()
    if not lines:
        lines = ["graph TD"]

    next_id = ord("A") + len(diagram_nodes)
    for name in sorted(missing):
        lines.append(f"  {chr(next_id)}[{name}]")
        next_id += 1

    return "\n".join(lines)

# -------------------------------------------------------------------
# JSON sanitization
# -------------------------------------------------------------------
def sanitize_llm_json(raw: str) -> str:
    if not raw:
        return raw

    raw = re.sub(r"^```(?:json)?\s*", "", raw.strip(), flags=re.IGNORECASE)
    raw = re.sub(r"\s*```$", "", raw.strip())

    start = raw.find("{")
    end = raw.rfind("}")
    if start != -1 and end != -1:
        raw = raw[start : end + 1]

    return raw.strip()

# -------------------------------------------------------------------
# Health
# -------------------------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

def validate_no_isolated_components(mermaid: str, components: list):
    component_names = {c.name for c in components}
    connected = set()

    for line in mermaid.splitlines():
        if "-->" in line or "-.->" in line or "==>" in line:
            labels = re.findall(r'\[(.*?)\]', line)
            for label in labels:
                clean = re.sub(r'\s*\(.*?\)\s*', '', label).strip()
                if clean in component_names:
                    connected.add(clean)

    isolated = component_names - connected

    if isolated:
        raise ValueError(f"Isolated components found in diagram: {isolated}")


# -------------------------------------------------------------------
# Core design endpoint
# -------------------------------------------------------------------
@app.post("/design", response_model=DesignResponse)
def generate_design(req: DesignRequest):
    try:
        # 1. Retrieve patterns (context only, NOT enforced)
        patterns = pattern_store.query(req.requirements, top_k=2) or []
        print("patterns got: \n",patterns)

        # 2. Build prompt
        prompt = build_design_prompt(req, patterns)

        # 3. Call LLM
        raw = call_llm(prompt)
        print("raw came,\n",raw)

        # 4. Parse JSON ONCE (sanitized)
        sanitized = sanitize_llm_json(raw)
        try:
            solution_json = json.loads(sanitized)
        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Invalid JSON from LLM: {str(e)}",
            )

        # 5. Normalize non-functional considerations
        nfr = []
        for item in solution_json.get("non_functional_considerations", []):
            if isinstance(item, str):
                nfr.append(item)
            elif isinstance(item, dict):
                nfr.append(str(item.get("name", "")))
            elif isinstance(item, list) and item:
                nfr.append(str(item[0]))
        solution_json["non_functional_considerations"] = nfr

        # 6. Components
        components = [
            ArchitectureComponent(**c)
            for c in solution_json.get("components", [])
        ]

        # 7. Mermaid diagram handling
        raw_diagram = solution_json.get("mermaid_diagram", "")
        diagram = sanitize_mermaid_diagram(raw_diagram)

        reconcile_components_with_diagram(diagram, components)
        diagram = reconcile_diagram_with_components(diagram, components)
        validate_no_isolated_components(diagram, components)

        # 8. Structural validations
        validate_domain_isolation(components)
        validate_diagram_matches_components(diagram, components)

        # 9. Cost
        per_env = [
            EnvironmentCost(**c)
            for c in solution_json.get("cost_estimate", {}).get(
                "per_environment", []
            )
        ]
        cost_estimate = CostEstimate(
            total_monthly_usd=solution_json["cost_estimate"]["total_monthly_usd"],
            per_environment=per_env,
            notes=solution_json["cost_estimate"].get("notes"),
        )

        # 10. Final response
        solution = SolutionDesign(
            normalized_requirements=solution_json.get(
                "normalized_requirements", {}
            ),
            chosen_pattern=solution_json.get("chosen_pattern"),
            architecture_description=solution_json.get(
                "architecture_description", ""
            ),
            mermaid_diagram=diagram,
            components=components,
            non_functional_considerations=nfr,
            tech_stack=solution_json.get("tech_stack", []),
            cost_estimate=cost_estimate,
            api_spec_stub=solution_json.get("api_spec_stub", ""),
            infra_as_code_stub=solution_json.get("infra_as_code_stub", ""),
            notes=solution_json.get("notes"),
        )

        return DesignResponse(request=req, solution=solution)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------------------------------------------------------
# Patterns inspection
# -------------------------------------------------------------------
@app.get("/patterns")
def list_patterns():
    return {
        "count": len(pattern_store.pattern_names),
        "patterns": pattern_store.pattern_names,
    }

# -------------------------------------------------------------------
# PDF report
# -------------------------------------------------------------------
@app.post("/generate_report")
def download_report(req: DesignRequest):
    response = generate_design(req)
    pdf_buffer = generate_pdf_report(response.solution.dict())

    return FileResponse(
        pdf_buffer,
        media_type="application/pdf",
        filename="architecture_report.pdf",
    )

# -------------------------------------------------------------------
# Serve React app (last)
# -------------------------------------------------------------------
@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    file_path = FRONTEND_BUILD_DIR / full_path
    if file_path.is_file():
        return FileResponse(file_path)

    index_path = FRONTEND_BUILD_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path)

    return {
        "message": "React frontend not built.",
        "build_dir": str(FRONTEND_BUILD_DIR),
    }
