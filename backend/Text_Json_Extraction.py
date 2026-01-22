import re
import json

def _strip_log_prefix(line: str) -> str:
    # removes: "ai-solution-architect  | "
    return re.sub(r"^.*?\|\s*", "", line).rstrip()


def parse_money_to_number(value: str) -> float:
    # "$800 (example estimate)" -> 800
    if not value:
        return 0
    m = re.search(r"(\d+(\.\d+)?)", value.replace(",", ""))
    return float(m.group(1)) if m else 0


def parse_olmo_output_to_json(raw_text: str) -> dict:
    """
    Converts OLMo point-wise output into your expected JSON dict.
    No Llama3 required.
    """

    # clean repeated garbage logs
    raw_text = raw_text.replace("INFO:", "\nINFO:")

    lines = []
    for ln in raw_text.splitlines():
        ln = _strip_log_prefix(ln)
        if not ln.strip():
            continue
        # remove repeated "INFO: ... POST /design ..." lines
        if "POST /design" in ln or "Internal Server Error" in ln:
            continue
        lines.append(ln)

    result = {
        "normalized_requirements": {},
        "chosen_pattern": "",
        "architecture_description": "",
        "mermaid_diagram": "",
        "components": [],
        "non_functional_considerations": [],
        "tech_stack": [],
        "cost_estimate": {
            "total_monthly_usd": 0,
            "per_environment": [],
            "notes": ""
        },
        "api_spec_stub": "",
        "infra_as_code_stub": "",
        "notes": ""
    }

    section = None
    current_component = None

    arch_lines = []
    mermaid_lines = []
    api_lines = []
    iac_lines = []
    notes_lines = []

    inferred_capabilities = []

    def flush_component():
        nonlocal current_component
        if current_component:
            # fill missing required fields for your Pydantic model
            current_component.setdefault("inputs", [])
            current_component.setdefault("outputs", [])
            current_component.setdefault("dependencies", [])
            current_component.setdefault("purpose", current_component.get("description", ""))
            current_component.setdefault("technology", current_component.get("cloud_service", current_component.get("name", "")))
            result["components"].append(current_component)
            current_component = None

    for line in lines:
        low = line.lower().strip()

        # -----------------------------
        # Section detection
        # -----------------------------
        if re.match(r"^\d+\)\s*normalized requirements", low):
            section = "normalized_requirements"
            continue

        if re.match(r"^\d+\)\s*inferred capabilities", low):
            section = "inferred_capabilities"
            continue

        if re.match(r"^\d+\)\s*chosen pattern", low):
            section = "chosen_pattern"
            continue

        if re.match(r"^\d+\)\s*components", low):
            section = "components"
            continue

        if re.match(r"^\d+\)\s*architecture description", low):
            flush_component()
            section = "architecture_description"
            continue

        if re.match(r"^\d+\)\s*mermaid diagram", low):
            flush_component()
            section = "mermaid_diagram"
            continue

        if re.match(r"^\d+\)\s*non-functional considerations", low):
            flush_component()
            section = "nfr"
            continue

        if re.match(r"^\d+\)\s*tech stack", low):
            flush_component()
            section = "tech_stack"
            continue

        if re.match(r"^\d+\)\s*cost estimate", low):
            flush_component()
            section = "cost_estimate"
            continue

        if re.match(r"^\d+\)\s*api spec stub", low):
            flush_component()
            section = "api_spec"
            continue

        if re.match(r"^\d+\)\s*infra as code stub", low):
            flush_component()
            section = "infra_as_code"
            continue

        if re.match(r"^\d+\)\s*notes", low):
            flush_component()
            section = "notes"
            continue

        # -----------------------------
        # Parsing per section
        # -----------------------------
        if section == "normalized_requirements":
            # key: value OR nested YAML-like indentation
            # Example:
            # scale_characteristics:
            #   traffic_pattern: ...
            if ":" in line:
                # indentation-based nesting
                indent = len(line) - len(line.lstrip(" "))
                key, val = [x.strip() for x in line.split(":", 1)]
                if val == "":
                    # start of nested object
                    # create dict if not exists
                    result["normalized_requirements"][key] = {}
                    current_parent = key
                    continue

                # if it's nested (2+ spaces), attach to last parent dict
                if indent >= 2:
                    # find last dict key that has dict value
                    parent_keys = [k for k, v in result["normalized_requirements"].items() if isinstance(v, dict)]
                    if parent_keys:
                        parent = parent_keys[-1]
                        result["normalized_requirements"][parent][key] = val
                    else:
                        result["normalized_requirements"][key] = val
                else:
                    result["normalized_requirements"][key] = val

        elif section == "inferred_capabilities":
            # capability: ....
            if line.startswith("capability:"):
                inferred_capabilities.append(line.split(":", 1)[1].strip())

        elif section == "chosen_pattern":
            # chosen_pattern: IoT Real-Time Processing
            if line.startswith("chosen_pattern:"):
                result["chosen_pattern"] = line.split(":", 1)[1].strip()

        elif section == "components":

            # FORMAT-1
            if line.strip() == "component:":
                flush_component()
                current_component = {}
                continue

            if current_component is not None and ":" in line:
                k, v = [x.strip() for x in line.split(":", 1)]

                if k == "name":
                    current_component["name"] = v
                elif k == "type":
                    current_component["type"] = v
                elif k == "cloud_service":
                    current_component["cloud_service"] = v   # ✅ FIX
                elif k == "description":
                    current_component["description"] = v     # ✅ FIX
                else:
                    current_component[k] = v

                continue

            # FORMAT-2 Emoji style
            if line.startswith("🔹"):
                flush_component()
                current_component = {
                    "name": line.replace("🔹", "").strip(),
                    "type": "service",
                    "cloud_service": "",
                    "description": "",
                    "inputs": [],
                    "outputs": [],
                    "dependencies": []
                }
                continue

            if current_component is not None:

                if not line.startswith(("☁️", "📄")) and ":" not in line:
                    if current_component.get("type") in ("service", "", None):
                        current_component["type"] = line.strip()
                    continue

                if line.startswith("☁️"):
                    svc = line.split(":", 1)[1].strip() if ":" in line else ""
                    if svc.upper() == "N/A":
                        svc = ""
                    current_component["cloud_service"] = svc  # ✅ FIX
                    continue

                if line.startswith("📄"):
                    desc = line.replace("📄", "").strip()
                    if "no description" in desc.lower():
                        desc = ""
                    current_component["description"] = desc   # ✅ FIX
                    continue



        elif section == "architecture_description":
            arch_lines.append(line)

        elif section == "mermaid_diagram":
            mermaid_lines.append(line)

        elif section == "nfr":
            if line.startswith("nfr:"):
                result["non_functional_considerations"].append(line.split(":", 1)[1].strip())

        elif section == "tech_stack":
            if line.startswith("tech:"):
                result["tech_stack"].append(line.split(":", 1)[1].strip())

        elif section == "cost_estimate":
            # total_monthly_usd: $800 (example estimate)
            if ":" in line:
                k, v = [x.strip() for x in line.split(":", 1)]
                if k == "total_monthly_usd":
                    result["cost_estimate"]["total_monthly_usd"] = parse_money_to_number(v)
                elif k.endswith("_monthly_usd"):
                    # dev/uat/prod
                    env = k.replace("_monthly_usd", "")
                    result["cost_estimate"]["per_environment"].append({
                        "environment": env.upper(),
                        "monthly_usd": parse_money_to_number(v)
                    })
                elif k == "assumptions":
                    result["cost_estimate"]["notes"] = v

        elif section == "api_spec":
            api_lines.append(line)

        elif section == "infra_as_code":
            iac_lines.append(line)

        elif section == "notes":
            notes_lines.append(line)

    # flush last component
    flush_component()

    # finalize architecture description
    if arch_lines:
        # remove "architecture style:" line prefix but keep full text
        result["architecture_description"] = "\n".join(arch_lines).strip()

    # finalize mermaid
    if mermaid_lines:
        result["mermaid_diagram"] = "\n".join(mermaid_lines).strip()

    # store api spec and iac as string (your model expects string)
    if api_lines:
        result["api_spec_stub"] = "\n".join(api_lines).strip()

    if iac_lines:
        result["infra_as_code_stub"] = "\n".join(iac_lines).strip()

    # notes
    if notes_lines:
        # remove "Notes on the architecture:" prefix
        joined = "\n".join(notes_lines).strip()
        joined = re.sub(r"^Notes on the architecture:\s*", "", joined, flags=re.IGNORECASE)
        result["notes"] = joined.strip()

    # optionally append inferred capabilities into notes
    if inferred_capabilities:
        result["notes"] += ("\n\nInferred Capabilities:\n- " + "\n- ".join(inferred_capabilities))

    return result
