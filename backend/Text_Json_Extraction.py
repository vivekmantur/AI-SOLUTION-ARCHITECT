import re

def _strip_log_prefix(line: str) -> str:
    """
    Removes docker log prefix ONLY if line starts like:
    ai-solution-architect  |  ....
    Otherwise returns line unchanged (important for Mermaid |label|).
    """
    m = re.match(r"^\s*[a-zA-Z0-9\-_]+\s+\|\s+(.*)$", line)
    return m.group(1).rstrip() if m else line.rstrip()


def _clean_line(line: str) -> str:
    s = line.strip()
    s = s.replace("**", "")
    s = re.sub(r"\s+", " ", s)
    return s.strip()

def _normalize_component_key(k: str) -> str:
    k = k.strip().lower()
    k = k.replace(" ", "_")
    k = k.replace("-", "_")
    return k

def _parse_task1_to_dict(lines: list[str]) -> dict:
    """
    Converts Task-1 lines like:
    Business goal: ...
    Primary users: ...
    into a dict.
    """
    out = {}
    for ln in lines:
        if ":" not in ln:
            continue
        k, v = [x.strip() for x in ln.split(":", 1)]
        key = k.lower().replace(" ", "_")
        out[key] = v
    return out

def parse_olmo_output_to_tasks(raw_text: str) -> dict:
    raw_text = raw_text.replace("INFO:", "\nINFO:")

    lines = []
    for ln in raw_text.splitlines():
        ln = _strip_log_prefix(ln)
        if not ln.strip():
            continue
        if "POST /design" in ln or "Internal Server Error" in ln:
            continue
        lines.append(ln)

    tasks = {
        "task_1_normalize_requirement": {},
        "task_2_platform_architecture_high_level": "",
        "task_3_architecture_flow_diagram_text_view": "",
        "task_4_best_architecture_recommendation": "",
        "task_5_key_design_decisions": "",
        "task_6_components": [],
        "task_7_mermaid_diagram": ""
    }

    section = None
    current_component = None

    t1, t2, t3, t4, t5, t7 = [], [], [], [], [], []
    components = []

    def flush_component():
        nonlocal current_component
        if current_component:
            # ensure required keys exist
            current_component.setdefault("name", "")
            current_component.setdefault("type", "")
            current_component.setdefault("cloud_service", "")
            current_component.setdefault("description", "")
            components.append(current_component)
            current_component = None

    for line in lines:
        clean = _clean_line(line)
        low = clean.lower()

        # section detection
        if low.startswith("task 1"):
            flush_component()
            section = "t1"
            continue
        if low.startswith("task 2"):
            flush_component()
            section = "t2"
            continue
        if low.startswith("task 3"):
            flush_component()
            section = "t3"
            continue
        if low.startswith("task 4"):
            flush_component()
            section = "t4"
            continue
        if low.startswith("task 5"):
            flush_component()
            section = "t5"
            continue
        if low.startswith("task 6"):
            flush_component()
            section = "t6"
            continue
        if low.startswith("task 7"):
            flush_component()
            section = "t7"
            continue

        # parsing
        if section == "t1":
            t1.append(clean)

        elif section == "t2":
            t2.append(clean)

        elif section == "t3":
            if clean.strip() in ["v", "V", "↓"]:
                t3.append(":")
                t3.append("v")
            else:
                t3.append(clean)

        elif section == "t4":
            t4.append(clean)

        elif section == "t5":
            t5.append(clean)

        elif section == "t6":
            if clean.lower() == "component:":
                flush_component()
                current_component = {}
                continue

            if current_component is not None and ":" in clean:
                k, v = [x.strip() for x in clean.split(":", 1)]
                nk = _normalize_component_key(k)

                # normalize common variations
                if nk in ("cloudservice", "cloud_service_name", "service"):
                    nk = "cloud_service"

                if nk == "cloud_service":
                    current_component["cloud_service"] = v
                elif nk == "name":
                    current_component["name"] = v
                elif nk == "type":
                    current_component["type"] = v
                elif nk == "description":
                    current_component["description"] = v
                else:
                    current_component[nk] = v

        elif section == "t7":
            raw_line = line.strip()

            # remove docker prefix only if present
            raw_line = _strip_log_prefix(raw_line)

            raw_line = raw_line.replace("**", "").strip()
            raw_line = raw_line.replace("|>", "|")
            raw_line = raw_line.replace("||", "|")

            t7.append(raw_line)




    flush_component()
    while len(t3) >= 2 and t3[-2] == ":" and t3[-1].lower() == "v":
     t3 = t3[:-2]

    # Final mapping
    tasks["task_1_normalize_requirement"] = _parse_task1_to_dict(t1)
    tasks["task_2_platform_architecture_high_level"] = "\n".join(t2).strip()
    tasks["task_3_architecture_flow_diagram_text_view"] = "\n".join(t3).strip()
    tasks["task_4_best_architecture_recommendation"] = "\n".join(t4).strip()
    tasks["task_5_key_design_decisions"] = "\n".join(t5).strip()
    tasks["task_6_components"] = components
    tasks["task_7_mermaid_diagram"] = "\n".join(t7).strip()

    return tasks
