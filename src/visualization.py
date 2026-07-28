"""Render the profile banner.

The banner reads left to right as the pipeline that actually produced it:
PREPARE (the circuit) -> MEASURE (the shot histogram) -> INFER (the network's
four output neurons). Every number on it comes from that run; nothing is
decorative. One SVG is written per palette so the README can serve the variant
matching the reader's GitHub theme.
"""

from __future__ import annotations

import base64
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from theme import PALETTES, Palette

ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = ROOT / "assets" / "fonts"
OUT_DIR = ROOT / "assets"

env = Environment(
    loader=FileSystemLoader(ROOT / "templates"),
    undefined=StrictUndefined,
    autoescape=True,
)

# ---------------------------------------------------------------- geometry --

W, H = 880, 314
LEFT, RIGHT = 2, 876

RULE_TOP = 38.5
RULE_BOTTOM = 240.5
LABEL_Y = 62
SUBLABEL_Y = 216
FLOW_Y = 141

ZONE_A = (2, 286)
ZONE_B = (314, 592)
ZONE_C = (624, 878)

# PREPARE — three qubit wires and the six gate columns of the circuit
WIRE_X0, WIRE_X1 = 26, 280  # wires stop at the measurement gate
ROWS_A = (109, 141, 173)
GATE_CX = (78, 116, 154, 192, 230, 268)
GATE_W, GATE_H = 24, 22

# MEASURE — one row per computational basis state.
# Source Code Pro advances 0.6em per glyph, so the ket brackets can be placed
# exactly. They are drawn as strokes rather than set as text: the font has no
# U+27E9, and a fallback glyph would break the column alignment.
ROW_B0, ROW_B_STEP = 90, 15
KET_X = 314
KET_DIGITS_X = 318
KET_CLOSE_X = 339
BAR_X, BAR_W, BAR_H = 352, 160, 8
PCT_X = 592

# INFER — one row per output neuron
ROW_C0, ROW_C_STEP = 96, 30
NEURON_X = 624
METER_X, METER_W, METER_H = 650, 120, 6
VALUE_X = 808
BIT_X = 876  # right-aligns with the rules and the header timestamp

# The circuit from quantum_circuit_qiskit.create_circuit, as drawing
# instructions. Controls are filled dots, targets are the XOR symbol.


@dataclass(frozen=True)
class BoxGate:
    """A single-qubit gate drawn as a labelled box."""

    row: int
    label: str
    note: str | None = None


@dataclass(frozen=True)
class MultiGate:
    """An entangling gate: filled control dots joined to an XOR target."""

    controls: tuple[int, ...]
    target: int


@dataclass(frozen=True)
class MeasureGate:
    """The measurement column, where the circuit hands off to the histogram."""

    rows: tuple[int, ...]


Gate = BoxGate | MultiGate | MeasureGate

CIRCUIT: tuple[Gate, ...] = (
    BoxGate(row=0, label="H"),
    MultiGate(controls=(0,), target=1),
    BoxGate(row=1, label="H"),
    BoxGate(row=2, label="Ry", note="π/3"),
    MultiGate(controls=(0, 1), target=2),
    MeasureGate(rows=(0, 1, 2)),
)


@dataclass(frozen=True)
class BannerData:
    """Everything the banner displays, all of it measured this run."""

    timestamp: str
    qubits: int
    depth: int
    gate_count: int
    distribution: list[tuple[str, float]]  # (bitstring, probability)
    shots: int
    entropy: float
    activations: list[float]
    threshold: float
    bits: list[int]
    index: int
    action_count: int
    action: str


# Positioned counterparts of the gates above. The template branches on `kind`
# and reads these attributes directly, so every coordinate it needs is resolved
# here rather than computed in Jinja.


@dataclass(frozen=True)
class BoxColumn:
    cx: float
    x: float
    y: float
    text_y: float
    label: str
    note: str | None
    note_y: float
    kind: str = "box"


@dataclass(frozen=True)
class MultiColumn:
    cx: float
    controls_y: tuple[float, ...]
    target_y: float
    y0: float
    y1: float
    kind: str = "multi"


@dataclass(frozen=True)
class MeasureBox:
    x: float
    y: float
    text_y: float


@dataclass(frozen=True)
class MeasureColumn:
    cx: float
    boxes: tuple[MeasureBox, ...]
    kind: str = "measure"


Column = BoxColumn | MultiColumn | MeasureColumn


@dataclass(frozen=True)
class HistogramRow:
    """One measured basis state: label, bar geometry and formatted percentage."""

    bits: str
    text_y: float
    bar_y: float
    width: float
    pct: str
    ket_open: str
    ket_close: str


@dataclass(frozen=True)
class NeuronRow:
    """One output neuron: meter geometry, activation and the bit it produced."""

    label: str
    text_y: float
    meter_y: float
    width: float
    value: str
    bit: str
    on: bool


def _font_face(weight: int) -> str:
    data = (FONT_DIR / f"source-code-pro-{weight}.woff2").read_bytes()
    b64 = base64.b64encode(data).decode("ascii")
    return (
        "@font-face{font-family:'SCP';font-style:normal;"
        f"font-weight:{weight};src:url(data:font/woff2;base64,{b64}) format('woff2')}}"
    )


def _circuit_columns() -> list[Column]:
    """Resolve the circuit description into positioned drawing instructions."""
    columns: list[Column] = []
    for cx, gate in zip(GATE_CX, CIRCUIT, strict=True):
        if isinstance(gate, BoxGate):
            row_y = ROWS_A[gate.row]
            columns.append(
                BoxColumn(
                    cx=cx,
                    x=cx - GATE_W / 2,
                    y=row_y - GATE_H / 2,
                    text_y=row_y + 4,
                    label=gate.label,
                    note=gate.note,
                    note_y=ROWS_A[-1] + 22,
                )
            )
        elif isinstance(gate, MultiGate):
            ys = [ROWS_A[i] for i in (*gate.controls, gate.target)]
            columns.append(
                MultiColumn(
                    cx=cx,
                    controls_y=tuple(ROWS_A[i] for i in gate.controls),
                    target_y=ROWS_A[gate.target],
                    y0=min(ys),
                    y1=max(ys),
                )
            )
        else:
            columns.append(
                MeasureColumn(
                    cx=cx,
                    boxes=tuple(
                        MeasureBox(
                            x=cx - GATE_W / 2,
                            y=ROWS_A[i] - GATE_H / 2,
                            text_y=ROWS_A[i] + 4,
                        )
                        for i in gate.rows
                    ),
                )
            )
    return columns


def _histogram(data: BannerData) -> list[HistogramRow]:
    peak = max(p for _, p in data.distribution) or 1.0
    rows: list[HistogramRow] = []
    for i, (bitstring, prob) in enumerate(data.distribution):
        y = ROW_B0 + i * ROW_B_STEP
        rows.append(
            HistogramRow(
                bits=bitstring,
                text_y=y + 3.5,
                bar_y=y - BAR_H / 2,
                width=max(1.0, prob / peak * BAR_W),
                pct=f"{prob * 100:.1f}%",
                ket_open=f"M{KET_X} {y - 5} V{y + 4.5}",
                ket_close=(
                    f"M{KET_CLOSE_X} {y - 5} "
                    f"L{KET_CLOSE_X + 4.2} {y - 0.25} "
                    f"L{KET_CLOSE_X} {y + 4.5}"
                ),
            )
        )
    return rows


def _neurons(data: BannerData) -> list[NeuronRow]:
    rows: list[NeuronRow] = []
    for i, value in enumerate(data.activations):
        y = ROW_C0 + i * ROW_C_STEP
        rows.append(
            NeuronRow(
                label=f"b{i}",
                text_y=y + 3.5,
                meter_y=y - METER_H / 2,
                width=max(1.0, min(1.0, value) * METER_W),
                value=f"{value:.3f}",
                bit=str(data.bits[i]),
                on=bool(data.bits[i]),
            )
        )
    return rows


def _context(data: BannerData, palette: Palette) -> dict[str, Any]:
    return {
        "c": palette,
        "w": W,
        "h": H,
        "left": LEFT,
        "right": RIGHT,
        "rule_top": RULE_TOP,
        "rule_bottom": RULE_BOTTOM,
        "label_y": LABEL_Y,
        "sublabel_y": SUBLABEL_Y,
        "flow_y": FLOW_Y,
        "zone_a": ZONE_A,
        "zone_b": ZONE_B,
        "zone_c": ZONE_C,
        "font_faces": _font_face(400) + _font_face(600),
        # PREPARE
        "wire_x0": WIRE_X0,
        "wire_x1": WIRE_X1,
        "rows_a": ROWS_A,
        "gate_w": GATE_W,
        "gate_h": GATE_H,
        "columns": _circuit_columns(),
        # MEASURE
        "ket_digits_x": KET_DIGITS_X,
        "bar_x": BAR_X,
        "bar_w": BAR_W,
        "bar_h": BAR_H,
        "pct_x": PCT_X,
        "histogram": _histogram(data),
        # INFER
        "neuron_x": NEURON_X,
        "meter_x": METER_X,
        "meter_w": METER_W,
        "meter_h": METER_H,
        "value_x": VALUE_X,
        "bit_x": BIT_X,
        "neurons": _neurons(data),
        "threshold_x": METER_X + data.threshold * METER_W,
        # copy
        "timestamp": data.timestamp,
        "prepare_note": f"depth {data.depth} · {data.qubits} qubits"
        f" · {data.gate_count} gates",
        "measure_note": f"{data.shots} shots · entropy {data.entropy:.2f}"
        f" / {data.qubits} bits",
        "infer_note": f"threshold {data.threshold:.3f} · state {data.index}"
        f" / {data.action_count}",
        "action": data.action,
        "cadence": "RECOMPUTED EVERY 12 HOURS",
    }


def create_banner(data: BannerData) -> list[Path]:
    """Write one banner SVG per palette. Returns the paths written."""
    template = env.get_template("banner.svg.jinja")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    written = []
    for palette in PALETTES:
        path = OUT_DIR / f"banner-{palette.name}.svg"
        path.write_text(template.render(**_context(data, palette)), encoding="utf-8")
        written.append(path)
    return written
