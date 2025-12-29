from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class DesignRequest(BaseModel):
    requirements: str = Field(..., description="Raw business/technical requirement in natural language")
    cloud: str = Field("azure", description="Target cloud: azure|aws|gcp")
    detail_level: str = Field("high", description="Level of detail: high|medium|low")

class ArchitectureComponent(BaseModel):
    name: str
    type: str
    cloud_service: Optional[str] = None
    description: Optional[str] = None

class EnvironmentCost(BaseModel):
    environment: str  # dev / uat / prod
    monthly_usd: float

class CostEstimate(BaseModel):
    total_monthly_usd: float
    per_environment: List[EnvironmentCost]
    notes: Optional[str] = None

class SolutionDesign(BaseModel):
    normalized_requirements: Dict[str, Any]
    chosen_pattern: Optional[str]
    architecture_description: str
    mermaid_diagram: str
    components: List[ArchitectureComponent]
    non_functional_considerations: List[str]
    tech_stack: List[str]
    cost_estimate: CostEstimate
    api_spec_stub: str
    infra_as_code_stub: str
    notes: Optional[str] = None

class DesignResponse(BaseModel):
    request: DesignRequest
    solution: SolutionDesign
