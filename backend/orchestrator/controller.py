from ..llm.client_base import LLMClient
from ..workspace.manager import WorkspaceManager
from ..orchestrator.state import ProjectState
from ..agents.clarifier import RequirementClarifierAgent
from ..agents.planner import PlanningAgent
from ..agents.ui_architect import UIArchitectAgent
from ..agents.coder import CodingAgent
from ..agents.tester import TestGenerationAgent
from ..agents.docs import DocumentationAgent
from ..agents.preview import PreviewAgent

class Orchestrator:
    def __init__(self, llm: LLMClient, workspace_manager: WorkspaceManager):
        self.llm = llm
        self.workspace = workspace_manager
        
        # Initialize Agents
        self.clarifier = RequirementClarifierAgent(llm)
        self.planner = PlanningAgent(llm)
        self.ui_architect = UIArchitectAgent(llm)
        self.coder = CodingAgent(llm)
        self.tester = TestGenerationAgent(llm)
        self.docs = DocumentationAgent(llm)
        self.preview = PreviewAgent(llm)

    def run(self, state: ProjectState) -> ProjectState:
        print(f"🎬 Orchestrator started for run: {state.run_id}")
        
        # 1. Clarify
        state.clarified_requirement = self.clarifier.run(state)
        
        # 2. Plan
        state.plan = self.planner.run(state)
        
        # 3. UI Architecture
        state.ui_blueprint = self.ui_architect.run(state)
        
        # 4. Code
        code = self.coder.run(state)
        # Save Code
        filename = f"{state.clarified_requirement.component_name}.tsx"
        path = self.workspace.save_file(state.run_id, f"src/components/{filename}", code)
        state.code_files.append(path)
        
        # 5. Tests
        tests = self.tester.run(state, code)
        test_filename = f"{state.clarified_requirement.component_name}.test.tsx"
        test_path = self.workspace.save_file(state.run_id, f"tests/{test_filename}", tests)
        state.test_files.append(test_path)
        
        # 6. Docs
        docs = self.docs.run(state, code)
        doc_filename = f"{state.clarified_requirement.component_name}.md"
        doc_path = self.workspace.save_file(state.run_id, f"docs/{doc_filename}", docs)
        state.docs_file = doc_path
        
        # 7. Preview
        preview_html = self.preview.run(state, code)
        preview_path = self.workspace.save_file(state.run_id, "preview/index.html", preview_html)
        state.preview_file = preview_path
        
        # 8. Finalize
        self.workspace.write_meta(state.run_id, state)
        
        print(f"🏁 Run complete! Workspace: {state.run_id}")
        return state
