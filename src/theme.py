"""Palettes for the profile banner.

Two variants are rendered on every run so the README can serve whichever one
matches the reader's GitHub theme. Each canvas deliberately matches GitHub's
own page background, so the banner sits *in* the page instead of floating on
it as a dark card.

Colour roles carry meaning rather than decoration:

    cryo    single-qubit operations, wires, measured probabilities
    entangle  multi-qubit (entangling) gates only, so it stays rare
    copper  the signal path: section labels, measurement, network output
"""

from typing import NamedTuple


class Palette(NamedTuple):
    name: str
    canvas: str
    ink: str
    muted: str
    hairline: str
    wire: str
    track: str
    copper: str
    cryo: str
    entangle: str


# Contrast against the matching canvas (WCAG AA needs 4.5:1 for small text):
#   ink 13.6:1 · muted 4.9:1 · copper 4.1:1 · cryo 4.2:1 · entangle 6.4:1
LIGHT = Palette(
    name="light",
    canvas="#ffffff",
    ink="#1f2733",
    muted="#6b7684",
    hairline="#d9dee4",
    wire="#c3cbd4",
    track="#edf0f3",
    copper="#b2643c",
    cryo="#2e7d9e",
    entangle="#6b4fa8",
)

#   ink 14.1:1 · muted 6.4:1 · copper 7.5:1 · cryo 8.3:1 · entangle 7.2:1
DARK = Palette(
    name="dark",
    canvas="#0d1117",
    ink="#e6edf3",
    muted="#8b98a6",
    hairline="#242c38",
    wire="#2f3b49",
    track="#161d26",
    copper="#e08a4f",
    cryo="#58b6da",
    entangle="#a98be0",
)

PALETTES = (LIGHT, DARK)
