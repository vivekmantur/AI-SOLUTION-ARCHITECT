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

from .Text_Json_Extraction import (
    _strip_log_prefix,
    parse_money_to_number,
    parse_olmo_output_to_json,
)
from .mermaid_sanitizer import (
    normalize_mermaid,
)

from .patterns_store import pattern_store
from .prompts import build_design_prompt
from .json_schema_prompt import build_json_prompt
from .llm_client import call_llm
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
# AWS Icons
# ------------------------------------------------------------
AWS_ICONS_DIR = (
    Path(__file__).parent.parent / "frontend" / "build" / "aws-icons"
)

print("AWS ICON DIR:", AWS_ICONS_DIR)
print("EXISTS?", AWS_ICONS_DIR.exists())

if AWS_ICONS_DIR.exists():
    app.mount(
        "/aws-icons",
        StaticFiles(directory=str(AWS_ICONS_DIR)),
        name="aws-icons",
    )

# ------------------------------------------------------------
# GCP Icons
# ------------------------------------------------------------
GCP_ICONS_DIR = (
    Path(__file__).parent.parent / "frontend" / "build" / "gcp-icons"
)

print("GCP ICON DIR:", GCP_ICONS_DIR)
print("EXISTS?", GCP_ICONS_DIR.exists())

if GCP_ICONS_DIR.exists():
    app.mount(
        "/gcp-icons",
        StaticFiles(directory=str(GCP_ICONS_DIR)),
        name="gcp-icons",
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

    # ✅ FIX: api_spec_stub must be STRING
    if isinstance(solution_json.get("api_spec_stub"), (dict, list)):
        solution_json["api_spec_stub"] = json.dumps(solution_json["api_spec_stub"], indent=2)

    # ✅ FIX: infra_as_code_stub must be STRING
    if isinstance(solution_json.get("infra_as_code_stub"), (dict, list)):
        solution_json["infra_as_code_stub"] = json.dumps(solution_json["infra_as_code_stub"], indent=2)

    # Normalize notes
    if "notes" not in solution_json or solution_json["notes"] is None:
        solution_json["notes"] = ""

    # Normalize cost notes
    if "cost_estimate" in solution_json:
        if solution_json["cost_estimate"].get("notes") is None:
            solution_json["cost_estimate"]["notes"] = ""

    return solution_json



def clean_olmo_text(text: str) -> str:
    text = re.sub(r"```[\s\S]*?```", "", text)
    text = "\n".join([line for line in text.splitlines() if not line.strip().startswith("|")])
    text = text.replace("---", "")

    # Convert common latex wrappers into plain text
    text = text.replace("\\boxed{", "")
    text = text.replace("\\begin{aligned}", "")
    text = text.replace("\\end{aligned}", "")
    text = text.replace("\\\\", "\n")

    # remove \text{...} but keep inside content
    text = re.sub(r"\\text\{([^}]*)\}", r"\1", text)

    # remove remaining braces that come from latex formatting
    text = text.replace("{", "").replace("}", "")

    return text.strip()



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
        raw_olmo = clean_olmo_text(raw_olmo)
        print("RAW came from OLMo3\n", raw_olmo)

        if not raw_olmo:
            raise HTTPException(status_code=500, detail="OLMo3 returned empty output")

        # ✅ STEP 2: Build schema prompt for Llama3 using RAW OLMo output
        solution_json = parse_olmo_output_to_json(raw_olmo)
        solution_json = normalize_solution_output(solution_json)


        # 🔒 REQUIRED normalization
        solution_json = normalize_solution_output(solution_json)

        components = [
            ArchitectureComponent(**c)
            for c in solution_json.get("components", [])
        ]
        print("components are \n",components)
        
        raw_diagram = solution_json.get("mermaid_diagram", "")
        raw_diagram = fix_mermaid_node_names(raw_diagram)

        diagram = normalize_mermaid(raw_diagram, components)

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
    
    
#mermaid syntax fixer

def fix_mermaid_node_names(diagram: str) -> str:
    """
    Fix Mermaid node names ONLY when the diagram uses plain text nodes like:
        API Gateway --> Catalog Service

    Do NOT modify lines already in Mermaid node syntax like:
        B[Data Ingestion Service] --> C[Data Lake]
        A((Circle)) --> B
        X["Label"] --> Y
    """

    if not diagram:
        return diagram

    fixed_lines = []

    for line in diagram.splitlines():
        raw = line
        line = line.strip()

        if not line:
            continue

        # keep graph direction line
        if line.startswith(("graph", "flowchart")):
            fixed_lines.append(line)
            continue

        # if already has node syntax, keep as-is
        # examples: A[Label], B("Label"), C{"Decision"}, D((Circle))
        if re.search(r"\w+\s*[\[\(\{]", line):
            fixed_lines.append(raw.strip())
            continue

        # match edges: A --> B OR A -->|label| B
        m = re.match(r"^(.+?)\s*-->\s*(.+)$", line)
        if not m:
            fixed_lines.append(raw.strip())
            continue

        left = m.group(1).strip()
        right = m.group(2).strip()

        # handle label syntax: A -->|text| B
        label_match = re.match(r"^\|(.+?)\|\s*(.+)$", right)
        label = None
        if label_match:
            label = label_match.group(1).strip()
            right = label_match.group(2).strip()

        def to_id(name: str) -> str:
            return re.sub(r"[^a-zA-Z0-9_]", "_", name).strip("_")

        left_id = to_id(left)
        right_id = to_id(right)

        if label:
            fixed_lines.append(f'{left_id}["{left}"] -->|{label}| {right_id}["{right}"]')
        else:
            fixed_lines.append(f'{left_id}["{left}"] --> {right_id}["{right}"]')

    return "\n".join(fixed_lines)


@app.get("/{full_path:path}")
def serve_react_app(full_path: str):
    # Do NOT intercept static or API routes
    if full_path.startswith(("azure-icons", "aws-icons", "gcp-icons", "static", "design")):
      raise HTTPException(status_code=404)


    index = FRONTEND_BUILD_DIR / "index.html"
    return FileResponse(index)


