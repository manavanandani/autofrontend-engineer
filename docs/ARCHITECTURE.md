# AutoFrontend Engineer - Architecture

## Core Components

### 1. Orchestrator (`backend/orchestrator/`)
The brain of the operation.
- **Controller**: Manages the sequential execution of agents.
- **State**: Maintains the `ProjectState` (requirements, plan, files) across the lifecycle.

### 2. Agents (`backend/agents/`)
Specialized workers powered by LLMs.
- **Clarifier**: Refines user input into structured JSON.
- **Planner**: Breaks down the task into engineering steps.
- **UI Architect**: Decides on component hierarchy and Tailwind classes.
- **Coder**: Writes the React/TypeScript code.
- **Tester**: Writes Jest/RTL tests.
- **Docs**: Generates markdown documentation.
- **Preview**: Generates a standalone HTML preview.

### 3. Workspace Manager (`backend/workspace/`)
Handles the file system.
- Creates unique run folders (e.g., `workspaces/run_2023...`).
- Saves generated artifacts.
- Writes `meta.json` for reproducibility.

### 4. LLM Layer (`backend/llm/`)
Abstracts the model provider.
- **ClientBase**: Protocol definition.
- **OpenAIClient**: Implementation for OpenAI.
- **Future**: Easy slot for Fine-Tuned Model client.

## Data Flow

1. **User Input** -> `main.py`
2. `Orchestrator` initializes `ProjectState`.
3. `Clarifier` -> `ClarifiedRequirement` (JSON)
4. `Planner` -> `ImplementationPlan` (JSON)
5. `UIArchitect` -> `UIBlueprint` (JSON)
6. `Coder` -> `.tsx` file
7. `Tester` -> `.test.tsx` file
8. `Docs` -> `.md` file
9. `Preview` -> `.html` file
10. `WorkspaceManager` saves all to disk.

## Future Roadmap
- [ ] Self-Correction Loop (DebugAgent)
- [ ] Multi-file component generation
- [ ] Web-based Dashboard
