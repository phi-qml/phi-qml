"""
Φ‑QML Web Application — Dashboard and REST API

Provides a web interface for the Φ‑QML ecosystem:
- Real‑time elegance reports
- Holographic field visualization
- Program execution via API
- Network map of connected nodes
"""

import sys
import os
import json
import time
from pathlib import Path

# Add the parent directory to the path so we can import phi_qml
sys.path.insert(0, str(Path(__file__).parent.parent))

from flask import Flask, render_template_string, jsonify, request

from phi_qml.interpreter import Interpreter
from phi_qml.lexer import Lexer
from phi_qml.parser import Parser
from phi_qml.holographic_field import HolographicField
from phi_qml.substrate_modulo import SubstrateModuloEngine
from phi_qml.elegance_tracker import EleganceTracker


app = Flask(__name__)

# Global state
interpreter = Interpreter()
modulo_engine = SubstrateModuloEngine()
elegance_tracker = EleganceTracker(min_phi=0.5)
field = HolographicField(N=8, seed=42)
execution_history = []


# ─── HTML Template ─────────────────────────────────────────────────

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Φ‑QML Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background: #0a0a1a; color: #e0e0e0; font-family: 'Courier New', monospace; min-height: 100vh; display: flex; flex-direction: column; align-items: center; }
        .header { text-align: center; padding: 30px 20px; border-bottom: 2px solid #ffd700; width: 100%; }
        .header h1 { color: #ffd700; font-size: 2.5em; text-shadow: 0 0 20px rgba(255,215,0,0.5); }
        .dashboard { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 20px; padding: 20px; max-width: 1200px; width: 100%; }
        .card { background: #1a1a2e; border: 1px solid #333; border-radius: 10px; padding: 20px; }
        .card h2 { color: #ffd700; margin-bottom: 15px; border-bottom: 1px solid #333; padding-bottom: 10px; }
        .metric { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #222; }
        .metric-label { color: #888; }
        .metric-value { color: #ffd700; font-weight: bold; }
        textarea { width: 100%; height: 200px; background: #0d0d1a; color: #e0e0e0; border: 1px solid #333; border-radius: 5px; padding: 12px; font-family: 'Courier New', monospace; resize: vertical; }
        button { padding: 12px 20px; background: #ffd700; color: #0a0a1a; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; font-family: 'Courier New', monospace; margin-top: 10px; }
        button:hover { background: #ffed4a; }
        #output { background: #0d0d1a; border: 1px solid #333; border-radius: 5px; padding: 12px; min-height: 100px; max-height: 300px; overflow-y: auto; white-space: pre-wrap; margin-top: 10px; }
        .footer { margin-top: auto; padding: 20px; color: #555; text-align: center; width: 100%; border-top: 1px solid #333; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Φ‑QML Dashboard</h1>
        <p>Substrate* Native Quantum Meta‑Language</p>
    </div>
    <div class="dashboard">
        <div class="card">
            <h2>Execute Program</h2>
            <textarea id="source" placeholder="Enter Φ‑QML code...">
fn main() {
    println("Hello, Substrate*!");
    let r = mod(2^256 + 123456789, 997);
    println("mod result: " + r);
}
            </textarea>
            <button onclick="runProgram()">▶️ Run</button>
            <div id="output"></div>
        </div>
        <div class="card">
            <h2>System Status</h2>
            <div class="metric"><span class="metric-label">Field qubits</span><span class="metric-value" id="field-n">8</span></div>
            <div class="metric"><span class="metric-label">Modulo cache</span><span class="metric-value" id="mod-cache">0</span></div>
            <div class="metric"><span class="metric-label">Average Φ</span><span class="metric-value" id="avg-phi">1.0</span></div>
            <div class="metric"><span class="metric-label">Elegance Debt</span><span class="metric-value" id="debt">0.0</span></div>
        </div>
        <div class="card">
            <h2>Holographic Field</h2>
            <div id="field-info">
                <p>Field size: <span id="hf-size">8</span> qubits</p>
                <p>States: 2^8 = <span id="hf-states">256</span></p>
                <p>Parameters: <span id="hf-params">16</span></p>
                <p>Compression: <span id="hf-compression">16x</span></p>
            </div>
            <button onclick="collapseField()">🎲 Collapse Field</button>
            <div id="collapse-result" style="margin-top:10px;"></div>
        </div>
    </div>
    <div class="footer">
        <p>Φ‑QML v1.0 | MIT License | Φ</p>
    </div>
    <script>
        async function runProgram() {
            const source = document.getElementById('source').value;
            const outputDiv = document.getElementById('output');
            outputDiv.textContent = 'Running...';
            try {
                const resp = await fetch('/api/run', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({source: source})
                });
                const data = await resp.json();
                if (data.error) {
                    outputDiv.textContent = 'Error: ' + data.error;
                } else {
                    outputDiv.textContent = data.output;
                }
                updateStatus();
            } catch(e) {
                outputDiv.textContent = 'Request failed: ' + e.message;
            }
        }

        async function updateStatus() {
            const resp = await fetch('/api/status');
            const data = await resp.json();
            document.getElementById('field-n').textContent = data.field_qubits;
            document.getElementById('mod-cache').textContent = data.mod_cache_size;
            document.getElementById('avg-phi').textContent = data.avg_phi.toFixed(3);
            document.getElementById('debt').textContent = data.elegance_debt.toFixed(2);
        }

        async function collapseField() {
            const resp = await fetch('/api/collapse');
            const data = await resp.json();
            document.getElementById('collapse-result').textContent =
                'Collapsed to: ' + data.result;
            updateStatus();
        }

        updateStatus();
    </script>
</body>
</html>
"""


# ─── Routes ────────────────────────────────────────────────────────

@app.route('/')
def index():
    """Serve the dashboard."""
    return render_template_string(HTML_TEMPLATE)


@app.route('/mobile')
def mobile():
    """Serve the mobile monitor interface."""
    return app.send_static_file('mobile.html')


@app.route('/api/status')
def api_status():
    """Return system status."""
    return jsonify({
        'field_qubits': field.N,
        'field_states': 1 << field.N,
        'field_params': 2 * field.N,
        'field_compression': field.get_compression_ratio(),
        'mod_cache_size': len(modulo_engine.cache),
        'avg_phi': elegance_tracker.get_average_phi(),
        'elegance_debt': elegance_tracker.get_elegance_debt(),
    })


@app.route('/api/run', methods=['POST'])
def api_run():
    """Execute a Φ‑QML program and return the output."""
    source = request.json.get('source', '')
    if not source.strip():
        return jsonify({'error': 'No source code provided'})

    # Capture print output
    import io
    old_stdout = sys.stdout
    sys.stdout = captured = io.StringIO()

    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter(field=field)
        interpreter.interpret(ast)
        output = captured.getvalue()
        captured.close()
        sys.stdout = old_stdout

        # Record execution
        execution_history.append({
            'time': time.time(),
            'source': source[:200],
            'output': output[:500],
        })

        return jsonify({'output': output})
    except Exception as e:
        captured.close()
        sys.stdout = old_stdout
        return jsonify({'error': 'Execution failed'})


@app.route('/api/collapse')
def api_collapse():
    """Collapse the holographic field and return the result."""
    result = field.collapse()
    return jsonify({'result': result})


# ─── Main ─────────────────────────────────────────────────────────

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    print(f"Φ‑QML Dashboard running at http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
