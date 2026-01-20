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

from .mermaid_sanitizer import (
    normalize_mermaid,
)

from .patterns_store import pattern_store
from .prompts import build_design_prompt
from .json_schema_prompt import build_json_prompt
from .llm_client import call_llm
from .llama_client import call_llama
from .report_generator import generate_pdf_report


# ------------------------------------------------------------
# Azure Icon Mapping
# ------------------------------------------------------------
AZURE_ICON_MAP = {
    "Azure App Service": "compute/App_Service.png",
    "Azure Functions": "compute/Function_Apps.png",
    "Azure Kubernetes Service": "compute/Kubernetes_Services.png",
    "Azure Static Web Apps": "compute/Static_Web_Apps.png",

    "Azure Cosmos DB": "databases/Cosmos_DB.png",
    "Azure SQL Database": "databases/SQL_Database.png",
    "Azure Cache for Redis": "databases/Cache_For_Redis.png",

    "Azure Data Factory": "analytics/Data_Factory.png",
    "Azure Synapse Analytics": "analytics/Synapse_Analytics.png",
    "Azure Databricks": "analytics/Databricks.png",
    "Power BI": "analytics/Power_BI.png",

    "Application Insights": "analytics/Application_Insights.png",
    "Azure Monitor": "analytics/Monitor.png",
}


app = FastAPI(title="AI Solution Architect API")

# ------------------------------------------------------------
# CORS
# ------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------
# Azure Icons (SVG)
# ------------------------------------------------------------
# ------------------------------------------------------------
# Azure Icons (SVG)
# ------------------------------------------------------------
AZURE_ICONS_DIR = (
    Path(__file__).parent.parent / "frontend" / "build" / "azure-icons"
)

print("AZURE ICON DIR:", AZURE_ICONS_DIR)
print("EXISTS?", AZURE_ICONS_DIR.exists())

app.mount(
    "/azure-icons",
    StaticFiles(directory=str(AZURE_ICONS_DIR)),
    name="azure-icons",
)

# ------------------------------------------------------------
# Frontend build
# ------------------------------------------------------------
FRONTEND_BUILD_DIR = Path(__file__).parent.parent / "frontend" / "build"

if FRONTEND_BUILD_DIR.exists():
    app.mount(
        "/static",
        StaticFiles(directory=str(FRONTEND_BUILD_DIR / "static")),
        name="static",
    )
    
    
    
def normalize_solution_output(solution_json: dict) -> dict:
    # Normalize infra_as_code field
    if "infra_as_code_stub" not in solution_json:
        for key in list(solution_json.keys()):
            if key.startswith("infra_as_code"):
                solution_json["infra_as_code_stub"] = solution_json.pop(key)
                break
        else:
            solution_json["infra_as_code_stub"] = ""

    # Normalize api_spec_stub
    if "api_spec_stub" not in solution_json:
        solution_json["api_spec_stub"] = ""

    # Normalize notes
    if "notes" not in solution_json or solution_json["notes"] is None:
        solution_json["notes"] = ""

    # Normalize cost notes
    if "cost_estimate" in solution_json:
        if solution_json["cost_estimate"].get("notes") is None:
            solution_json["cost_estimate"]["notes"] = ""

    return solution_json


# ------------------------------------------------------------
# API
# ------------------------------------------------------------
@app.post("/design", response_model=DesignResponse)
def generate_design(req: DesignRequest):
    try:
        patterns = pattern_store.query(req.requirements, top_k=1) or []
        print("patterns\n",patterns)
        prompt = build_design_prompt(req, patterns)
        

        raw_olmo = call_llm(prompt).strip()
        print("RAW came from OLMo3\n", raw_olmo)

        if not raw_olmo:
            raise HTTPException(status_code=500, detail="OLMo3 returned empty output")

        # ✅ STEP 2: Build schema prompt for Llama3 using RAW OLMo output
        schema_prompt = build_json_prompt(req, patterns, raw_olmo)

        # ✅ STEP 3: Call Llama3 to convert RAW -> STRICT JSON
        raw_llama = call_llama(schema_prompt).strip()
        print("RAW came from Llama3 (JSON)\n", raw_llama)

        if not raw_llama:
            raise HTTPException(status_code=500, detail="Llama3 returned empty output")

        if not raw_llama.startswith("{"):
            raise HTTPException(
                status_code=500,
                detail=f"Llama3 output not JSON. First 200 chars: {raw_llama[:200]}"
            )

        # ✅ STEP 4: Convert JSON string -> dict
        solution_json = json.loads(raw_llama)


        # 🔒 REQUIRED normalization
        solution_json = normalize_solution_output(solution_json)

        components = [
            ArchitectureComponent(**c)
            for c in solution_json.get("components", [])
        ]

        diagram = normalize_mermaid(
            solution_json.get("mermaid_diagram", ""),
            components
        )

        cost = solution_json.get("cost_estimate", {})
        per_env = [EnvironmentCost(**e) for e in cost.get("per_environment", [])]

        solution = SolutionDesign(
            normalized_requirements=solution_json.get("normalized_requirements", {}),
            chosen_pattern=solution_json.get("chosen_pattern", ""),
            architecture_description=solution_json.get("architecture_description", ""),
            mermaid_diagram=diagram,
            components=components,
            non_functional_considerations=solution_json.get("non_functional_considerations", []),
            tech_stack=solution_json.get("tech_stack", []),
            cost_estimate=CostEstimate(
                total_monthly_usd=cost.get("total_monthly_usd", 0),
                per_environment=per_env,
                notes=cost.get("notes", "")
            ),
            api_spec_stub=solution_json.get("api_spec_stub", ""),
            infra_as_code_stub=solution_json.get("infra_as_code_stub", ""),
            notes=solution_json.get("notes", "")
        )

        return DesignResponse(request=req, solution=solution)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/{full_path:path}")
def serve_react_app(full_path: str):
    # Do NOT intercept static or API routes
    if full_path.startswith(("azure-icons", "static", "design")):
        raise HTTPException(status_code=404)

    index = FRONTEND_BUILD_DIR / "index.html"
    return FileResponse(index)


