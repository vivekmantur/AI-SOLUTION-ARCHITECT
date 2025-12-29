import requests
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io

# Convert Mermaid diagram to PNG using QuickChart's API
def convert_mermaid_to_image(mermaid_code: str):
    url = "https://quickchart.io/graphviz"
    payload = {"graph": mermaid_code}

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return ImageReader(io.BytesIO(response.content))
    return None

def generate_pdf_report(solution: dict):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 18)
    c.drawString(30, height - 50, "AI-Generated Cloud Architecture Report")

    c.setFont("Helvetica", 10)
    c.drawString(30, height - 80, "Executive Summary")
    text = c.beginText(30, height - 100)
    text.setFont("Helvetica", 9)
    text.textLines(solution.get("architecture_description", ""))
    c.drawText(text)

    c.showPage()

    # System Diagram
    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, height - 50, "System Architecture Diagram")
    diagram = convert_mermaid_to_image(solution.get("mermaid_diagram", ""))
    if diagram:
        c.drawImage(diagram, 50, 200, width=500, preserveAspectRatio=True, mask='auto')

    c.showPage()

    # Components
    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, height - 50, "Cloud Components & Services")
    y = height - 80
    for comp in solution.get("components", []):
        c.setFont("Helvetica", 10)
        c.drawString(40, y, f"{comp['name']} → {comp.get('cloud_service')}")
        y -= 20
        if y < 100:
            c.showPage()
            y = height - 80

    # Cost Estimate
    c.showPage()
    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, height - 50, "Cost Estimate")
    c.setFont("Helvetica", 10)
    c.drawString(40, height - 80, f"Total: ${solution['cost_estimate']['total_monthly_usd']:.2f}")

    y = height - 120
    for env in solution["cost_estimate"]["per_environment"]:
        c.drawString(40, y, f"{env['environment']} → ${env['monthly_usd']:.2f}")
        y -= 20

    # API Spec
    c.showPage()
    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, height - 50, "API Specification Stub")
    text = c.beginText(30, height - 80)
    text.setFont("Helvetica", 9)
    text.textLines(solution.get("api_spec_stub", ""))
    c.drawText(text)

    # Terraform IaC
    c.showPage()
    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, height - 50, "Infrastructure-as-Code Stub (Terraform)")
    text = c.beginText(30, height - 80)
    text.setFont("Helvetica", 8)
    text.textLines(solution.get("infra_as_code_stub", ""))
    c.drawText(text)

    c.save()
    buffer.seek(0)
    return buffer
