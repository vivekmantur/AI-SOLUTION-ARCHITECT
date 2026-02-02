from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse
from .pdf_report import generate_pdf_report
import json
import re
from pathlib import Path

# -----------------------------
# Pydantic models
# -----------------------------
from .models import (
    DesignRequest,
    DesignResponse,
    SolutionDesign,
    ArchitectureComponent,
)

# -----------------------------
# LLM output parsing utilities
# -----------------------------
from .Text_Json_Extraction import (
    _clean_line,
    _strip_log_prefix,
    parse_olmo_output_to_tasks,
    _normalize_component_key,
)

# -----------------------------
# Mermaid sanitization
# -----------------------------
from .mermaid_sanitizer import normalize_mermaid

# -----------------------------
# Supporting modules
# -----------------------------
from .patterns_store import pattern_store
from .prompts import build_7task_architecture_prompt
from .llm_client import call_llm


# ------------------------------------------------------------
# Azure Icon Mapping (used by frontend)
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


# ------------------------------------------------------------
# FastAPI app initialization
# ------------------------------------------------------------
app = FastAPI(title="AI Solution Architect API")

# ------------------------------------------------------------
# CORS configuration
# ------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # Open for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------
# Azure Icons static mount
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
# AWS Icons static mount
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
# GCP Icons static mount
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
# React frontend build
# ------------------------------------------------------------
FRONTEND_BUILD_DIR = Path(__file__).parent.parent / "frontend" / "build"

if FRONTEND_BUILD_DIR.exists():
    app.mount(
        "/static",
        StaticFiles(directory=str(FRONTEND_BUILD_DIR / "static")),
        name="static",
    )


# ------------------------------------------------------------
# Utility: Clean raw LLM output
# ------------------------------------------------------------
def clean_olmo_text(text: str) -> str:
    """
    Cleans raw LLM output by removing markdown blocks,
    LaTeX artifacts, and formatting noise while preserving
    Mermaid diagram syntax.
    """

    # Remove fenced code blocks
    text = re.sub(r"```[\s\S]*?```", "", text)

    # Remove common markdown artifacts
    text = text.replace("---", "")
    text = text.replace("**", "")

    # Normalize LaTeX wrappers
    text = text.replace("\\boxed{", "")
    text = text.replace("\\begin{aligned}", "")
    text = text.replace("\\end{aligned}", "")
    text = text.replace("\\\\", "\n")

    # Convert \text{} blocks into plain text
    text = re.sub(r"\\text\{([^}]*)\}", r"\1", text)

    # Remove leftover braces
    text = text.replace("{", "").replace("}", "")

    return text.strip()


# ------------------------------------------------------------
# Main API endpoint
# ------------------------------------------------------------
@app.post("/design", response_model=DesignResponse)
def generate_design(req: DesignRequest):
    """
    Generates a complete cloud architecture design using LLM output.
    """

    try:
        # Retrieve similar architecture patterns
        # patterns = pattern_store.query(req.requirements, top_k=1) or []
        # print("patterns\n", patterns)

        # Build structured prompt
        prompt = build_7task_architecture_prompt(req)

        # Call LLM
        raw_olmo = call_llm(prompt).strip()

        # Clean model output
        raw_olmo = clean_olmo_text(raw_olmo)
        print("RAW came from OLMo3\n", raw_olmo)

        if not raw_olmo:
            raise HTTPException(status_code=500, detail="LLM returned empty output")

        # Parse task-based response
        solution_json = parse_olmo_output_to_tasks(raw_olmo)

        # Extract Task 6 components
        components = [
            ArchitectureComponent(**c)
            for c in solution_json.get("task_6_components", [])
        ]
        print("components are \n", components)

        # Extract Task 7 Mermaid diagram
        raw_diagram = solution_json.get("task_7_mermaid_diagram", "")
        print("diagram before fixing mermaid node names\n", raw_diagram)

        # Normalize Mermaid syntax
        diagram = normalize_mermaid(raw_diagram, components)
        print("diagram after sanitization\n", diagram)

        # Build solution model
        solution = SolutionDesign(
            task_1_normalize_requirement=solution_json.get("task_1_normalize_requirement", {}),
            task_2_platform_architecture_high_level=solution_json.get("task_2_platform_architecture_high_level", ""),
            task_3_architecture_flow_diagram_text_view=solution_json.get("task_3_architecture_flow_diagram_text_view", ""),
            task_4_best_architecture_recommendation=solution_json.get("task_4_best_architecture_recommendation", ""),
            task_5_key_design_decisions=solution_json.get("task_5_key_design_decisions", ""),
            task_6_components=components,
            task_7_mermaid_diagram=diagram
        )

        return DesignResponse(request=req, solution=solution)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ------------------------------------------------------------
# Mermaid node-name fixer (currently unused)
# ------------------------------------------------------------
def fix_mermaid_node_names(diagram: str) -> str:
    """
    Fixes invalid Mermaid node names and edge labels
    to prevent rendering errors.
    """

    if not diagram:
        return diagram

    fixed_lines = []

    for line in diagram.splitlines():
        raw = line
        line = line.strip()

        if not line:
            continue

        # Preserve graph direction
        if line.startswith(("graph", "flowchart")):
            fixed_lines.append(line)
            continue

        # Keep existing node syntax
        if re.search(r"\w+\s*[\[\(\{]", line):
            fixed_lines.append(raw.strip())
            continue

        # Parse Mermaid edges
        m = re.match(r"^(.+?)\s*-->\s*(.+)$", line)
        if not m:
            fixed_lines.append(raw.strip())
            continue

        left = m.group(1).strip()
        right = m.group(2).strip()

        # Fix invalid label terminator
        right = right.replace("|>", "|")

        # Extract edge labels
        label_match = re.match(r"^\|(.+?)\|\s*(.+)$", right)
        label = None
        if label_match:
            label = label_match.group(1).strip()
            right = label_match.group(2).strip()

        # Normalize IDs
        def to_id(name: str) -> str:
            return re.sub(r"[^a-zA-Z0-9_]", "_", name).strip("_")

        left_id = to_id(left)
        right_id = to_id(right)

        if label:
            fixed_lines.append(f'{left_id}["{left}"] -->|{label}| {right_id}["{right}"]')
        else:
            fixed_lines.append(f'{left_id}["{left}"] --> {right_id}["{right}"]')

    return "\n".join(fixed_lines)

@app.post("/download-report")
def download_report(solution: SolutionDesign):
    pdf_buffer = generate_pdf_report(solution)

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=architecture-report.pdf"
        }
    )


# ------------------------------------------------------------
# Catch-all route for React SPA
# ------------------------------------------------------------
@app.get("/{full_path:path}")
def serve_react_app(full_path: str):
    """
    Serves React index.html for all non-API routes.
    """

    # Avoid intercepting API and static routes
    if full_path.startswith(("azure-icons", "aws-icons", "gcp-icons", "static", "design")):
        raise HTTPException(status_code=404)

    index = FRONTEND_BUILD_DIR / "index.html"
    return FileResponse(index)
