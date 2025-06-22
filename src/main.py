from datetime import UTC, datetime

from nn import infer_current_action
from quantum_circuit_qiskit import run_full_analysis
from visualization import create_banner

_NUM_QUBITS = 3
_NUM_CLASSICAL = 3


def main():
    num_qubits = _NUM_QUBITS
    num_classical = _NUM_CLASSICAL
    _, result = run_full_analysis(num_qubits, num_classical)

    action = infer_current_action(result)

    # Example: May, 26 2025 at 11:30pm UTC
    timestamp = datetime.now(UTC).strftime("%b, %d %Y at %I:%M%p UTC")

    create_banner(action, timestamp)

    print(f"🔥 Current Action: {action}")


if __name__ == "__main__":
    main()
