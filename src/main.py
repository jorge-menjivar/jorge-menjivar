from datetime import UTC, datetime

from nn import infer_current_action
from quantum_circuit_qiskit import run_full_analysis
from visualization import BannerData, create_banner

_NUM_QUBITS = 3
_NUM_CLASSICAL = 3
_SHOTS = 8192


def main():
    num_qubits = _NUM_QUBITS
    num_classical = _NUM_CLASSICAL
    report, result = run_full_analysis(num_qubits, num_classical)

    readout = infer_current_action(result)

    # Most probable state first, so the histogram reads as a ranking.
    distribution = sorted(result.probabilities.items(), key=lambda kv: -kv[1])

    # Example: 27 JUL 2026 · 17:46 UTC
    timestamp = datetime.now(UTC).strftime("%d %b %Y · %H:%M UTC").upper()

    written = create_banner(
        BannerData(
            timestamp=timestamp,
            qubits=num_qubits,
            depth=report.circuit_info.depth,
            gate_count=sum(
                count
                for gate, count in report.circuit_info.gates.items()
                if gate not in ("barrier", "measure")
            ),
            distribution=distribution,
            shots=sum(result.counts.values()),
            entropy=result.entropy,
            activations=readout.activations,
            threshold=readout.threshold,
            bits=readout.bits,
            index=readout.index,
            action_count=2 ** len(readout.bits),
            action=readout.action,
        )
    )

    for path in written:
        print(f"🎨 Wrote {path}")
    print(f"🔥 Current Action: {readout.action}")


if __name__ == "__main__":
    main()
