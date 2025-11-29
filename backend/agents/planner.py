import json
import os
from ..llm.client_base import LLMClient
from ..orchestrator.state import ProjectState, ImplementationPlan

class PlanningAgent:
    def __init__(self, llm: LLMClient):
        self.llm = llm
        prompt_path = os.path.join(os.path.dirname(__file__), "../prompts/planner.txt")
        with open(prompt_path, "r") as f:
            self.system_prompt = f.read()

    def run(self, state: ProjectState) -> ImplementationPlan:
        print("📅 Creating implementation plan...")
        req_json = state.clarified_requirement.model_dump_json(indent=2)
        user_prompt = f"Clarified Requirement:\n{req_json}"
        
        response = self.llm.generate(self.system_prompt, user_prompt)
        cleaned = response.replace("```json", "").replace("```", "").strip()
        
        try:
            data = json.loads(cleaned)
            return ImplementationPlan(**data)
        except Exception as e:
            print(f"Error parsing plan: {e}")
            return ImplementationPlan(steps=["Error parsing plan"], acceptance_criteria=[])
