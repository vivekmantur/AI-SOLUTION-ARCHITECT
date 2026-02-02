from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    Preformatted,
    ListFlowable,
    ListItem,
)
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
import json
import datetime
import re


# -------------------------------------------------
# Unicode cleanup (MUST BE FIRST)
# -------------------------------------------------
def normalize_text(text: str) -> str:
    if not text:
        return ""
    return (
        text
        .replace("\u00a0", " ")
        .replace("\u00ad", "")
        .replace("\u2011", "-")
        .replace("\u2013", "-")
        .replace("\u2014", "-")
        .replace("\u2018", "'")
        .replace("\u2019", "'")
        .replace("\u201c", '"')
        .replace("\u201d", '"')
        .replace("\u202f", " ")
    )


# -------------------------------------------------
# Font
# -------------------------------------------------
pdfmetrics.registerFont(
    TTFont("Inter", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
)


# -------------------------------------------------
# Styles
# -------------------------------------------------
TITLE = ParagraphStyle(
    "Title", fontName="Inter", fontSize=22, leading=26, spaceAfter=18
)

H2 = ParagraphStyle(
    "H2", fontName="Inter", fontSize=15, leading=20, spaceBefore=18, spaceAfter=12
)

BODY = ParagraphStyle(
    "Body", fontName="Inter", fontSize=11, leading=15, spaceAfter=6
)

CODE = ParagraphStyle(
    "Code",
    fontName="Courier",
    fontSize=9,
    leading=12,
    backColor=colors.HexColor("#F3F4F6"),
    leftIndent=10,
    rightIndent=10,
    spaceAfter=14,
)


# -------------------------------------------------
# PDF Generator
# -------------------------------------------------
def generate_pdf_report(solution):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    elements = []

    # -------------------------------------------------
    # Cover Page
    # -------------------------------------------------
    elements.append(Paragraph("AI Solution Architecture Report", TITLE))
    elements.append(
        Paragraph(
            f"Generated on: {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}",
            BODY,
        )
    )
    elements.append(PageBreak())

    # -------------------------------------------------
    # Task 1 — Clean JSON
    # -------------------------------------------------
    elements.append(Paragraph("Task 1 — Normalized Requirement", H2))

    pretty_json = json.dumps(
        solution.task_1_normalize_requirement,
        indent=2,
        ensure_ascii=False,
    )

    elements.append(
        Preformatted(
            normalize_text(pretty_json),
            CODE,
            maxLineLength=95,
        )
    )

    # -------------------------------------------------
    # Task 2 — Platform Architecture (ROBUST POINTS)
    # -------------------------------------------------
    elements.append(Paragraph("Task 2 — Platform Architecture (High Level)", H2))

    raw_task2 = normalize_text(
        solution.task_2_platform_architecture_high_level or ""
    )

    task2_points = [
        p.strip()
        for p in re.split(r"\n|\d+\)", raw_task2)
        if p.strip()
    ]

    elements.append(
        ListFlowable(
            [ListItem(Paragraph(p, BODY)) for p in task2_points],
            bulletType="1",
            start="1",
            leftIndent=18,
        )
    )

    # -------------------------------------------------
    # Task 3 — Architecture Flow (ASCII ONLY)
    # -------------------------------------------------
    elements.append(Spacer(1, 14))
    elements.append(Paragraph("Task 3 — Architecture Flow", H2))

    raw_flow = normalize_text(
        solution.task_3_architecture_flow_diagram_text_view or ""
    )

    flow_steps = [
        s.strip()
        for s in re.split(r"\||->", raw_flow)
        if s.strip()
    ]

    elements.append(
        ListFlowable(
            [ListItem(Paragraph(step, BODY)) for step in flow_steps],
            bulletType="bullet",
            leftIndent=18,
        )
    )

    # -------------------------------------------------
    # Task 4 — Recommendation
    # -------------------------------------------------
    elements.append(Spacer(1, 14))
    elements.append(Paragraph("Task 4 — Best Architecture Recommendation", H2))
    elements.append(
        Paragraph(
            normalize_text(solution.task_4_best_architecture_recommendation or "N/A"),
            BODY,
        )
    )

    # -------------------------------------------------
    # Task 5 — Key Design Decisions
    # -------------------------------------------------
    elements.append(Spacer(1, 14))
    elements.append(Paragraph("Task 5 — Key Design Decisions", H2))

    raw_task5 = normalize_text(
        solution.task_5_key_design_decisions or ""
    )

    task5_points = [
        p.strip()
        for p in re.split(r"\n|\. ", raw_task5)
        if p.strip()
    ]

    elements.append(
        ListFlowable(
            [ListItem(Paragraph(p, BODY)) for p in task5_points],
            bulletType="bullet",
            leftIndent=18,
        )
    )

    elements.append(PageBreak())

    # -------------------------------------------------
    # Task 6 — Components (UNCHANGED)
    # -------------------------------------------------
    elements.append(Paragraph("Task 6 — Components", H2))

    def cell(text):
        return Paragraph(normalize_text(text or "N/A"), BODY)

    table_data = [
        [
            Paragraph("<b>Name</b>", BODY),
            Paragraph("<b>Type</b>", BODY),
            Paragraph("<b>Cloud Service</b>", BODY),
            Paragraph("<b>Description</b>", BODY),
        ]
    ]

    for c in solution.task_6_components:
        table_data.append([
            cell(c.name),
            cell(c.type),
            cell(c.cloud_service),
            cell(c.description),
        ])

    table = Table(
        table_data,
        colWidths=[90, 85, 130, 245],
        repeatRows=1,
    )

    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E5E7EB")),
            ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#9CA3AF")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ])
    )

    elements.append(table)

   # -------------------------------------------------
    # Task 7 — Architecture Diagram (Readable Flow)
    # -------------------------------------------------
    if solution.task_7_mermaid_diagram:
        elements.append(PageBreak())
        elements.append(Paragraph("Task 7 — Architecture Diagram", H2))

        # Convert Mermaid to readable vertical flow
        raw = normalize_text(solution.task_7_mermaid_diagram)

        lines = []
        for line in raw.splitlines():
            line = line.strip()

            # Skip mermaid keywords
            if not line or line.startswith(("flowchart", "subgraph", "end", "direction")):
                continue

            # Extract node labels
            if "[" in line and "]" in line:
                label = line.split("[", 1)[1].split("]", 1)[0]
                label = label.replace('"', "").replace("_", " ").title()
                lines.append(label)

        # Remove duplicates while preserving order
        seen = set()
        ordered = []
        for l in lines:
            if l not in seen:
                seen.add(l)
                ordered.append(l)

        # Build vertical flow
        flow_text = "\n\n".join(
            f"{step}\n  |\n  v" if i < len(ordered) - 1 else step
            for i, step in enumerate(ordered)
        )

        elements.append(
            Preformatted(
                flow_text,
                CODE,
                maxLineLength=80,
            )
        )


    doc.build(elements)
    buffer.seek(0)
    return buffer
