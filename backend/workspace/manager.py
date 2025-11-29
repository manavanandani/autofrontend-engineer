import os
import json
import shutil
from datetime import datetime
from ..orchestrator.state import ProjectState

class WorkspaceManager:
    def __init__(self, base_dir: str = "workspaces"):
        self.base_dir = base_dir
        # Ensure base dir exists (relative to project root usually, but we'll use abs path if needed)
        # For now, assume running from project root
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    def create_workspace(self, run_id: str) -> str:
        """Creates a new workspace folder for the run."""
        path = os.path.join(self.base_dir, run_id)
        os.makedirs(path, exist_ok=True)
        
        # Create subfolders
        os.makedirs(os.path.join(path, "src", "components"), exist_ok=True)
        os.makedirs(os.path.join(path, "tests"), exist_ok=True)
        os.makedirs(os.path.join(path, "docs"), exist_ok=True)
        os.makedirs(os.path.join(path, "preview"), exist_ok=True)
        
        return path

    def save_file(self, run_id: str, relative_path: str, content: str):
        """Saves a file to the workspace."""
        full_path = os.path.join(self.base_dir, run_id, relative_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        return full_path

    def write_meta(self, run_id: str, state: ProjectState):
        """Writes the meta.json file."""
        # Convert pydantic model to dict
        data = state.model_dump()
        path = os.path.join(self.base_dir, run_id, "meta.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)
