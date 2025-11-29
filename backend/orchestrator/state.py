from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class ClarifiedRequirement(BaseModel):
    component_name: str
    purpose: str
    fields: List[Dict[str, str]] = Field(default_factory=list)
    actions: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)

class ImplementationPlan(BaseModel):
    steps: List[str]
    acceptance_criteria: List[str]

class UIBlueprint(BaseModel):
    component_tree: Dict[str, Any]
    tailwind_map: Dict[str, str]

class TestResults(BaseModel):
    passed: bool
    output: str
    failed_tests: List[str] = Field(default_factory=list)

class ProjectState(BaseModel):
    raw_input: str
    run_id: str
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    
    # Agent Outputs
    clarified_requirement: Optional[ClarifiedRequirement] = None
    plan: Optional[ImplementationPlan] = None
    ui_blueprint: Optional[UIBlueprint] = None
    
    # File Paths (relative to workspace root)
    code_files: List[str] = Field(default_factory=list)
    test_files: List[str] = Field(default_factory=list)
    docs_file: Optional[str] = None
    preview_file: Optional[str] = None
    
    # Status
    test_results: Optional[TestResults] = None
    iterations: int = 0
    model_used: str = "gpt-4o"
