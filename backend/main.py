import sys
import os
import uuid
from datetime import datetime
from dotenv import load_dotenv

# Add backend to path so imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.orchestrator.state import ProjectState
from backend.workspace.manager import WorkspaceManager
from backend.llm.openai_client import OpenAIClient
# We will import the controller later when it's built
from backend.orchestrator.controller import Orchestrator

def main():
    load_dotenv()
    
    if len(sys.argv) < 2:
        print("Usage: python backend/main.py \"<Your Frontend Requirement>\"")
        sys.exit(1)

    user_input = sys.argv[1]
    run_id = f"run_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
    
    print(f"🚀 Starting AutoFrontend Engineer Run: {run_id}")
    print(f"📋 Requirement: {user_input}")

    # Initialize State
    state = ProjectState(
        raw_input=user_input,
        run_id=run_id
    )

    # Initialize Infrastructure
    workspace_mgr = WorkspaceManager()
    workspace_path = workspace_mgr.create_workspace(run_id)
    print(f"📂 Workspace created at: {workspace_path}")

    llm_client = OpenAIClient()

    # Initialize and run Orchestrator
    orchestrator = Orchestrator(llm_client, workspace_mgr)
    final_state = orchestrator.run(state)
    
    print("\n✅ Run Complete.")
    print(f"Check {workspace_path} for outputs.")

if __name__ == "__main__":
    main()
