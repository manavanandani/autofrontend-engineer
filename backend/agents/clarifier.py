import json
import os
from ..llm.client_base import LLMClient
from ..orchestrator.state import ProjectState, ClarifiedRequirement

class RequirementClarifierAgent:
    def __init__(self, llm: LLMClient):
        self.llm = llm
        # Load prompt
        prompt_path = os.path.join(os.path.dirname(__file__), "../prompts/clarifier.txt")
        with open(prompt_path, "r") as f:
            self.system_prompt = f.read()

    def run(self, state: ProjectState) -> ClarifiedRequirement:
        print("🤔 Clarifying requirements...")
        user_prompt = f"User Request: {state.raw_input}"
        
        response = self.llm.generate(self.system_prompt, user_prompt)
        
        # Clean response (remove markdown fences if present)
        cleaned = response.replace("```json", "").replace("```", "").strip()
        
        try:
            data = json.loads(cleaned)
            return ClarifiedRequirement(**data)
        except Exception as e:
            print(f"Error parsing clarification: {e}")
            # Fallback or retry logic could go here
            return ClarifiedRequirement(
                component_name="UnknownComponent",
                purpose=state.raw_input,
                fields=[],
                actions=[],
                assumptions=["Failed to parse structured req"]
            )
