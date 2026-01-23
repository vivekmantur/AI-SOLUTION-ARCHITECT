from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class DesignRequest(BaseModel):
    requirements: str = Field(..., description="Raw business/technical requirement in natural language")
    cloud: str = Field("azure", description="Target cloud: azure|aws|gcp")
    detail_level: str = Field("high", description="Level of detail: high|medium|low")


class ArchitectureComponent(BaseModel):
    name: str
    type: str
    cloud_service: Optional[str] = ""
    description: Optional[str] = ""


class SolutionDesign(BaseModel):
    task_1_normalize_requirement: Dict[str, Any]
    task_2_platform_architecture_high_level: str
    task_3_architecture_flow_diagram_text_view: str
    task_4_best_architecture_recommendation: str
    task_5_key_design_decisions: str
    task_6_components: List[ArchitectureComponent]
    task_7_mermaid_diagram: str


class DesignResponse(BaseModel):
    request: DesignRequest
    solution: SolutionDesign
