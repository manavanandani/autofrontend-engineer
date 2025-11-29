# 🚀 AutoFrontend Engineer

**An Autonomous Multi-Agent System for React Component Generation**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

AutoFrontend Engineer is a sophisticated autonomous engineering system that transforms natural language requirements into production-ready React components using a multi-agent architecture powered by GPT-4.

![AutoFrontend Engineer Dashboard](docs/images/dashboard-preview.png)

## ✨ Features

- 🤖 **7 Specialized AI Agents** working in orchestrated collaboration
- ⚡ **Real-Time Progress Tracking** with live agent status updates
- 🎨 **Professional Web UI** with dark mode and glassmorphism design
- 📦 **Complete Component Packages** including:
  - TypeScript + React code
  - Tailwind CSS styling
  - Jest + React Testing Library tests
  - Markdown documentation
  - Live HTML preview
- 🔄 **Reproducible Workspaces** with full metadata tracking
- 🔌 **Pluggable LLM Backend** (OpenAI now, custom models later)

## 🏗️ Architecture

### Multi-Agent Pipeline

```
User Input → Clarifier → Planner → UI Architect → Coder → Tester → Docs → Preview → Output
```

Each agent specializes in one task:

1. **Requirement Clarifier**: Structures vague input into precise JSON specs
2. **Planning Agent**: Creates step-by-step implementation plans
3. **UI Architect**: Designs component hierarchy and Tailwind classes
4. **Coding Agent**: Writes React + TypeScript code
5. **Test Generator**: Creates comprehensive Jest tests
6. **Documentation Agent**: Generates professional Markdown docs
7. **Preview Agent**: Builds standalone HTML previews

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- OpenAI API Key
- Modern web browser

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/autofrontend-engineer.git
   cd autofrontend-engineer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

4. **Start the server**
   ```bash
   python3 backend/api_server.py
   ```

5. **Open the dashboard**
   ```
   Navigate to http://localhost:5001
   ```

## 💻 Usage

### Web Interface (Recommended)

1. Click **"New Run"** in the dashboard
2. Describe your component (e.g., "Create a pricing table with 3 tiers")
3. Click **"Generate Component"**
4. Watch the agents work in real-time!
5. View the generated preview, code, and tests

### Command Line

```bash
python3 backend/main.py "Create a modern login form with email validation"
```

## 📁 Project Structure

```
autofrontend-engineer/
├── backend/
│   ├── agents/           # 7 specialized AI agents
│   ├── llm/              # LLM client abstraction
│   ├── orchestrator/     # Workflow controller
│   ├── prompts/          # Agent system prompts
│   ├── workspace/        # File management
│   ├── main.py           # CLI entry point
│   └── api_server.py     # Flask API server
├── frontend/
│   └── preview-shell/    # Web dashboard UI
├── workspaces/           # Generated components (auto-created)
├── docs/                 # Documentation
└── requirements.txt
```

## 🎯 Example Output

Each run creates a structured workspace:

```
workspaces/run_2025-11-29_01-45-38/
├── meta.json                          # Run metadata
├── src/components/LoginForm.tsx       # React component
├── tests/LoginForm.test.tsx           # Jest tests
├── docs/LoginForm.md                  # Documentation
└── preview/index.html                 # Live preview
```

## 🔧 Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)

### Customization

- **Prompts**: Edit files in `backend/prompts/` to customize agent behavior
- **Model**: Change model in `backend/llm/openai_client.py` (default: `gpt-4o`)
- **Port**: Modify port in `backend/api_server.py` (default: `5001`)

## 📊 System Requirements

- **Memory**: 2GB+ RAM
- **Disk**: 500MB+ free space
- **Network**: Internet connection for OpenAI API

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/)
- Powered by [OpenAI GPT-4](https://openai.com/)
- UI components from [Tailwind CSS](https://tailwindcss.com/)
- Icons from [Lucide](https://lucide.dev/)

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Made with ❤️ for autonomous software engineering**
