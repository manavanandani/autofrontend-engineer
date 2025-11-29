import sys
import os
import json
from datetime import datetime
from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
from dotenv import load_dotenv
import threading
import queue

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.orchestrator.state import ProjectState
from backend.workspace.manager import WorkspaceManager
from backend.llm.openai_client import OpenAIClient
from backend.orchestrator.controller import Orchestrator

app = Flask(__name__, static_folder='../frontend/preview-shell', static_url_path='')
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Enable CORS for all origins

load_dotenv()

# Global progress tracking
progress_queues = {}

@app.route('/')
def index():
    """Serve the dashboard"""
    return app.send_static_file('index.html')

@app.route('/workspaces/<path:filename>')
def serve_workspace(filename):
    """Serve workspace files"""
    from flask import send_from_directory
    return send_from_directory('../workspaces', filename)

@app.route('/api/runs', methods=['GET'])
def get_runs():
    """Get list of all runs"""
    workspace_mgr = WorkspaceManager()
    runs = []
    
    if os.path.exists(workspace_mgr.base_dir):
        for run_dir in sorted(os.listdir(workspace_mgr.base_dir), reverse=True):
            run_path = os.path.join(workspace_mgr.base_dir, run_dir)
            meta_path = os.path.join(run_path, 'meta.json')
            
            if os.path.isdir(run_path) and os.path.exists(meta_path):
                import json
                with open(meta_path, 'r') as f:
                    meta = json.load(f)
                    runs.append({
                        'run_id': meta.get('run_id'),
                        'component_name': meta.get('clarified_requirement', {}).get('component_name', 'Unknown'),
                        'timestamp': meta.get('timestamp'),
                        'input': meta.get('raw_input'),
                        'status': 'success' if meta.get('code_files') else 'failed'
                    })
    
    return jsonify({'runs': runs})

@app.route('/api/progress/<run_id>')
def progress_stream(run_id):
    """Stream progress updates for a run"""
    def generate():
        q = progress_queues.get(run_id)
        if not q:
            yield f"data: {json.dumps({'error': 'Run not found'})}\n\n"
            return
        
        while True:
            try:
                msg = q.get(timeout=30)
                if msg == 'DONE':
                    break
                yield f"data: {json.dumps(msg)}\n\n"
            except queue.Empty:
                yield f"data: {json.dumps({'type': 'heartbeat'})}\n\n"
    
    return Response(stream_with_context(generate()), mimetype='text/event-stream')

@app.route('/api/generate', methods=['POST'])
def generate_component():
    """Generate a new component"""
    data = request.json
    user_input = data.get('prompt', '')
    
    if not user_input:
        return jsonify({'error': 'Prompt is required'}), 400
    
    # Create run
    run_id = f"run_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
    
    # Create progress queue
    progress_queues[run_id] = queue.Queue()
    
    def run_generation():
        try:
            q = progress_queues[run_id]
            
            q.put({'type': 'status', 'agent': 'init', 'message': 'Initializing workspace...'})
            
            state = ProjectState(raw_input=user_input, run_id=run_id)
            workspace_mgr = WorkspaceManager()
            workspace_path = workspace_mgr.create_workspace(run_id)
            llm_client = OpenAIClient()
            
            q.put({'type': 'status', 'agent': 'clarifier', 'message': '🤔 Clarifying requirements...'})
            orchestrator = Orchestrator(llm_client, workspace_mgr)
            
            # Monkey-patch to emit progress
            original_run = orchestrator.run
            def run_with_progress(state):
                q.put({'type': 'status', 'agent': 'planner', 'message': '📅 Creating implementation plan...'})
                result = original_run(state)
                q.put({'type': 'status', 'agent': 'complete', 'message': '✅ Generation complete!'})
                return result
            
            orchestrator.run = run_with_progress
            final_state = orchestrator.run(state)
            
            q.put({
                'type': 'complete',
                'run_id': run_id,
                'component_name': final_state.clarified_requirement.component_name if final_state.clarified_requirement else 'Unknown',
                'workspace_path': workspace_path
            })
            q.put('DONE')
            
        except Exception as e:
            q.put({'type': 'error', 'message': str(e)})
            q.put('DONE')
    
    # Start generation in background thread
    thread = threading.Thread(target=run_generation)
    thread.daemon = True
    thread.start()
    
    return jsonify({'success': True, 'run_id': run_id})

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'model': 'gpt-4o'})

if __name__ == '__main__':
    print("🚀 Starting AutoFrontend Engineer API Server...")
    print("📡 Server running at http://localhost:5001")
    print("🌐 Open http://localhost:5001 in your browser")
    app.run(debug=True, port=5001, host='127.0.0.1')

