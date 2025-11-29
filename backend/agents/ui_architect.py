import json
import os
from ..llm.client_base import LLMClient
from ..orchestrator.state import ProjectState, UIBlueprint

class UIArchitectAgent:
    def __init__(self, llm: LLMClient):
        self.llm = llm
        prompt_path = os.path.join(os.path.dirname(__file__), "../prompts/ui_architect.txt")
        with open(prompt_path, "r") as f:
            self.system_prompt = f.read()

    def run(self, state: ProjectState) -> UIBlueprint:
        print("🎨 Designing UI architecture...")
        req_json = state.clarified_requirement.model_dump_json(indent=2)
        plan_json = state.plan.model_dump_json(indent=2)
        
        user_prompt = f"Requirement:\n{req_json}\n\nPlan:\n{plan_json}"
        
        response = self.llm.generate(self.system_prompt, user_prompt)
        cleaned = response.replace("```json", "").replace("```", "").strip()
        
        try:
            data = json.loads(cleaned)
            return UIBlueprint(**data)
        except Exception as e:
            print(f"Error parsing UI blueprint: {e}")
            return UIBlueprint(component_tree={}, tailwind_map={})
