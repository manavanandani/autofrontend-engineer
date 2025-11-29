import os
from ..llm.client_base import LLMClient
from ..orchestrator.state import ProjectState

class PreviewAgent:
    def __init__(self, llm: LLMClient):
        self.llm = llm
        prompt_path = os.path.join(os.path.dirname(__file__), "../prompts/preview.txt")
        with open(prompt_path, "r") as f:
            self.system_prompt = f.read()

    def run(self, state: ProjectState, component_code: str) -> str:
        print("🖼 Generating preview...")
        
        user_prompt = f"""
        Component Code:
        {component_code}
        """
        
        response = self.llm.generate(self.system_prompt, user_prompt)
        
        # Strip markdown
        html = response
        if "```html" in html:
            html = html.split("```html")[1].split("```")[0]
        elif "```" in html:
            html = html.split("```")[1].split("```")[0]
            
        return html.strip()
