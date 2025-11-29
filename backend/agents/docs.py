import os
from ..llm.client_base import LLMClient
from ..orchestrator.state import ProjectState

class DocumentationAgent:
    def __init__(self, llm: LLMClient):
        self.llm = llm
        prompt_path = os.path.join(os.path.dirname(__file__), "../prompts/docs.txt")
        with open(prompt_path, "r") as f:
            self.system_prompt = f.read()

    def run(self, state: ProjectState, component_code: str) -> str:
        print("📝 Writing documentation...")
        req_json = state.clarified_requirement.model_dump_json(indent=2)
        
        user_prompt = f"""
        Requirement: {req_json}
        Component Code:
        {component_code}
        """
        
        response = self.llm.generate(self.system_prompt, user_prompt)
        return response.strip()
