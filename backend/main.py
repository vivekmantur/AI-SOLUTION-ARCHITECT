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
from .llm_client import call_llm
from .report_generator import generate_pdf_report


# ------------------------------------------------------------
# Azure Icon Mapping
# ------------------------------------------------------------
AZURE_ICON_MAP = {
    "Azure App Service": "compute/App_Service.svg",
    "Azure Functions": "compute/Function_Apps.svg",
    "Azure Stream Analytics": "analytics/Synapse_Analytics.svg",
    "Azure Time Series Insights": "analytics/Time_Series_Insights.svg",

    "Azure Kubernetes Service": "compute/Kubernetes_Services.svg",
    "Azure Static Web Apps": "compute/Static_Web_Apps.svg",

    "Azure Cosmos DB": "databases/Cosmos_DB.svg",
    "Azure SQL Database": "databases/SQL_Database.svg",
    "Azure Cache for Redis": "databases/Cache_For_Redis.svg",

    "Azure IoT Hub": "integration/IoT_Hub.svg",
    "Azure Event Hubs": "integration/Event_Hubs.svg",
    "Azure Service Bus": "integration/Service_Bus.svg",

    "Application Insights": "analytics/Application_Insights.svg",
    "Azure Monitor": "analytics/Monitor.svg",
    "Power BI": "analytics/Power_BI.svg",
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
AZURE_ICONS_DIR = (
    Path(__file__).parent.parent / "frontend" / "public" / "azure-icons"
)

if AZURE_ICONS_DIR.exists():
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

# ------------------------------------------------------------
# API
# ------------------------------------------------------------
@app.post("/design", response_model=DesignResponse)
def generate_design(req: DesignRequest):
    try:
        patterns = pattern_store.query(req.requirements, top_k=1) or []
        print("pattern patterns\n",patterns)
        prompt = build_design_prompt(req, patterns)
        raw = call_llm(prompt)
        print("raw from llm\n",raw)
        solution_json = json.loads(raw)

        components = [
            ArchitectureComponent(**c)
            for c in solution_json.get("components", [])
        ]
        diagram=solution_json.get("mermaid_diagram","")
        diagram = normalize_mermaid(diagram,components)
        print("sanitized diagram",diagram)

        cost = solution_json.get("cost_estimate", {})
        per_env = [EnvironmentCost(**e) for e in cost.get("per_environment", [])]

        solution = SolutionDesign(
            normalized_requirements=solution_json.get("normalized_requirements", {}),
            chosen_pattern=solution_json.get("chosen_pattern"),
            architecture_description=solution_json.get("architecture_description", ""),
            mermaid_diagram=diagram,
            components=components,
            non_functional_considerations=solution_json.get("non_functional_considerations", []),
            tech_stack=solution_json.get("tech_stack", []),
            cost_estimate=CostEstimate(
                total_monthly_usd=cost.get("total_monthly_usd", 0),
                per_environment=per_env,
                notes=cost.get("notes")
            ),
            api_spec_stub=solution_json.get("api_spec_stub"),
            infra_as_code_stub=solution_json.get("infra_as_code_stub"),
            notes=solution_json.get("notes"),
        )

        return DesignResponse(request=req, solution=solution)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/{full_path:path}")
def serve_react_app(full_path: str):
    index = FRONTEND_BUILD_DIR / "index.html"
    return FileResponse(index) if index.exists() else {"message": "Frontend not built"}
