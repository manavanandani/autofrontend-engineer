import os
import re
from ..llm.client_base import LLMClient
from ..orchestrator.state import ProjectState

class PreviewAgent:
    def __init__(self, llm: LLMClient):
        self.llm = llm
        prompt_path = os.path.join(os.path.dirname(__file__), "../prompts/preview.txt")
        with open(prompt_path, "r") as f:
            self.system_prompt = f.read()

    def clean_html(self, html: str) -> str:
        """Clean and validate the generated HTML"""
        # Strip markdown
        if "```html" in html:
            html = html.split("```html")[1].split("```")[0]
        elif "```" in html:
            parts = html.split("```")
            if len(parts) >= 3:
                html = parts[1]
                # Remove language identifier
                if '\n' in html:
                    lines = html.split('\n')
                    if lines[0].strip() in ['html', 'HTML']:
                        html = '\n'.join(lines[1:])
        
        html = html.strip()
        
        # Ensure it starts with <!DOCTYPE
        if not html.startswith('<!DOCTYPE') and not html.startswith('<html'):
            # Try to find the start
            if '<!DOCTYPE' in html:
                html = html[html.index('<!DOCTYPE'):]
            elif '<html' in html:
                html = html[html.index('<html'):]
        
        return html

    def create_fallback_preview(self, component_code: str, component_name: str) -> str:
        """Create a working fallback preview"""
        # Convert component code for browser
        browser_code = component_code
        # Remove imports
        browser_code = re.sub(r"import.*?;?\n", "", browser_code)
        # Remove export
        browser_code = re.sub(r"export\s+default\s+", "", browser_code)
        
        # Add React hooks if needed
        react_hooks = "const { useState, useEffect } = React;"
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{component_name} Preview</title>
    <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {{
            margin: 0;
            padding: 40px 20px;
            min-height: 100vh;
            background: #f3f4f6;
            font-family: system-ui, -apple-system, sans-serif;
        }}
    </style>
</head>
<body>
    <div id="root"></div>
    <script type="text/babel">
        {react_hooks}

        {browser_code}

        const App = () => {{
            const handleAction = (data) => {{
                console.log('Action:', data);
                alert(JSON.stringify(data, null, 2));
            }};

            return <{component_name} onAction={{handleAction}} onSubmit={{handleAction}} />;
        }};

        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<App />);
    </script>
</body>
</html>"""

    def run(self, state: ProjectState, component_code: str) -> str:
        print("🖼 Generating preview...")
        
        user_prompt = f"""
        Component Code:
        {component_code}
        """
        
        response = self.llm.generate(self.system_prompt, user_prompt)
        html = self.clean_html(response)
        
        # Validate HTML
        if len(html) < 100 or '<!DOCTYPE' not in html or '<script type="text/babel">' not in html:
            print("⚠️  Warning: Generated preview seems invalid, using fallback...")
            component_name = state.clarified_requirement.component_name
            html = self.create_fallback_preview(component_code, component_name)
        
        return html

