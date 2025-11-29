import os
from ..llm.client_base import LLMClient
from ..orchestrator.state import ProjectState

class CodingAgent:
    def __init__(self, llm: LLMClient):
        self.llm = llm
        prompt_path = os.path.join(os.path.dirname(__file__), "../prompts/coder.txt")
        with open(prompt_path, "r") as f:
            self.system_prompt = f.read()

    def run(self, state: ProjectState) -> str:
        print("👨‍💻 Writing code...")
        req_json = state.clarified_requirement.model_dump_json(indent=2)
        plan_json = state.plan.model_dump_json(indent=2)
        ui_json = state.ui_blueprint.model_dump_json(indent=2)
        
        user_prompt = f"""
        Requirement: {req_json}
        Plan: {plan_json}
        UI Blueprint: {ui_json}
        """
        
        response = self.llm.generate(self.system_prompt, user_prompt)
        
        # Strip markdown code blocks if present
        code = response
        if "```tsx" in code:
            code = code.split("```tsx")[1].split("```")[0]
        elif "```typescript" in code:
            code = code.split("```typescript")[1].split("```")[0]
        elif "```" in code:
            code = code.split("```")[1].split("```")[0]
            
        return code.strip()
