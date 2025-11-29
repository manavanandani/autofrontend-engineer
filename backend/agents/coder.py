import os
import re
from ..llm.client_base import LLMClient
from ..orchestrator.state import ProjectState

class CodingAgent:
    def __init__(self, llm: LLMClient):
        self.llm = llm
        prompt_path = os.path.join(os.path.dirname(__file__), "../prompts/coder.txt")
        with open(prompt_path, "r") as f:
            self.system_prompt = f.read()

    def clean_code(self, code: str) -> str:
        """Clean and validate the generated code"""
        # Remove markdown code blocks
        if "```tsx" in code:
            code = code.split("```tsx")[1].split("```")[0]
        elif "```typescript" in code:
            code = code.split("```typescript")[1].split("```")[0]
        elif "```" in code:
            # Try to extract code from any code block
            parts = code.split("```")
            if len(parts) >= 3:
                code = parts[1]
                # Remove language identifier if present
                if '\n' in code:
                    lines = code.split('\n')
                    if lines[0].strip() in ['tsx', 'typescript', 'ts', 'javascript', 'js', 'react']:
                        code = '\n'.join(lines[1:])
        
        code = code.strip()
        
        # Ensure it starts with import or const
        if not (code.startswith('import') or code.startswith('const') or code.startswith('function') or code.startswith('export')):
            # Try to find the first import or function
            lines = code.split('\n')
            start_idx = 0
            for i, line in enumerate(lines):
                if line.strip().startswith(('import', 'const', 'function', 'export', 'interface')):
                    start_idx = i
                    break
            code = '\n'.join(lines[start_idx:])
        
        # Ensure it has an export
        if 'export default' not in code and 'export {' not in code:
            # Try to add export to the main component
            # Find the component function
            component_match = re.search(r'function\s+(\w+)', code)
            if component_match:
                component_name = component_match.group(1)
                code += f'\n\nexport default {component_name};'
        
        return code.strip()

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
        code = self.clean_code(response)
        
        # Validate that we have some code
        if len(code) < 50:
            print("⚠️  Warning: Generated code seems too short, using fallback...")
            # Return a minimal working component as fallback
            component_name = state.clarified_requirement.component_name
            code = f"""import React from 'react';

interface {component_name}Props {{
  // Add props here
}}

export default function {component_name}(props: {component_name}Props) {{
  return (
    <div className="max-w-md mx-auto p-6 bg-white border border-gray-200 rounded-lg">
      <h2 className="text-2xl font-semibold text-gray-900 mb-4">{component_name}</h2>
      <p className="text-gray-700">Component implementation coming soon...</p>
    </div>
  );
}}"""
        
        return code

