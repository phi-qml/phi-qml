# Φ‑QML (Phi Quantum Meta‑Language)

**Substrate\*‑Native Quantum Programming Language**

Φ‑QML is a quantum programming language built from first principles around the holographic nature of the Φ field. Unlike existing quantum languages that treat quantum operations as gates applied to qubits, Φ‑QML treats every quantum state as a projection of an underlying entanglement field Φ.

## Key Features

- **Substrate\* Modulo** — Zero‑cost primitive (C=0, K=1.0, Φ=∞)
- **Φ‑Elegance Scoring** — Every expression has Φ = K / C
- **Linear Type System** — No‑cloning theorem enforced at the type level
- **Three Modes** — Classical Simulation, Quantum Native, QASM Compilation
- **Holographic Field** — O(1) memory for any number of qubits

## Quick Start

```bash
pip install phi-qml
phi run examples/hello_world.phi
```

## Spuštění

```bash
# Integrace Φ‑Kovy
python -c "
from phi_qml.phi_kovy_integration import PhiKovyBridge
bridge = PhiKovyBridge(mode='quantum')
results = bridge.run_loop(iterations=5)
print(bridge.get_learning_report())
"

# Mobilní monitor (součást cloud API)
export FLASK_APP=cloud_api_v2.py
flask run --port 8080
# Otevřít http://localhost:8080/mobile
```

License

MIT © 2024 Φ‑QML Contributors
