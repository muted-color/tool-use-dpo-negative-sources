from __future__ import annotations

import argparse
import csv
from pathlib import Path

from .paths import ARTIFACTS, REPRODUCED


POINT_IDS = {
    ("r028", "step50"): "A",
    ("r028", "final"): "B",
    ("r029", "step50"): "C",
    ("r029", "final"): "D",
    ("s3d001", "step50"): "E",
    ("s3d001", "final"): "F",
    ("s3d002", "step50"): "G",
    ("s3d002", "final"): "H",
}

COLORS = {"noised_gold": "#2364aa", "behavior": "#c43b3b"}


def read_points(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def pct(value: str) -> float:
    return 100.0 * float(value)


def build_svg(points: list[dict[str, str]]) -> str:
    width, height = 1120, 560
    margin_left, margin_right, margin_top, margin_bottom = 72, 32, 48, 70
    panel_gap = 78
    panel_w = (width - margin_left - margin_right - panel_gap) / 2
    panel_h = height - margin_top - margin_bottom
    x_min, x_max = -12.5, 0.8
    y_ranges = [(-1.3, 6.2), (-1.3, 5.8)]
    panels = [
        ("BFCL core vs guardrail regression", "bfcl_core_delta", "BFCL core delta"),
        ("When2Call macro F1 vs guardrail regression", "when2call_macro_f1_delta", "When2Call macro F1 delta"),
    ]

    def sx(x: float, panel_idx: int) -> float:
        left = margin_left + panel_idx * (panel_w + panel_gap)
        return left + (x - x_min) / (x_max - x_min) * panel_w

    def sy(y: float, panel_idx: int) -> float:
        y_min, y_max = y_ranges[panel_idx]
        return margin_top + panel_h - (y - y_min) / (y_max - y_min) * panel_h

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<style>text{font-family:Arial,sans-serif}.title{font-weight:700;font-size:15px}.axis{font-size:12px}.point{font-size:12px;font-weight:700}</style>',
    ]
    for idx, (title, y_col, y_label) in enumerate(panels):
        left = margin_left + idx * (panel_w + panel_gap)
        right = left + panel_w
        bottom = margin_top + panel_h
        lines.extend(
            [
                f'<text class="title" x="{left + panel_w / 2:.1f}" y="24" text-anchor="middle">{title}</text>',
                f'<line x1="{left:.1f}" y1="{bottom:.1f}" x2="{right:.1f}" y2="{bottom:.1f}" stroke="#333"/>',
                f'<line x1="{left:.1f}" y1="{margin_top:.1f}" x2="{left:.1f}" y2="{bottom:.1f}" stroke="#333"/>',
                f'<line x1="{sx(0, idx):.1f}" y1="{margin_top:.1f}" x2="{sx(0, idx):.1f}" y2="{bottom:.1f}" stroke="#999" stroke-width="0.8"/>',
                f'<line x1="{left:.1f}" y1="{sy(0, idx):.1f}" x2="{right:.1f}" y2="{sy(0, idx):.1f}" stroke="#999" stroke-width="0.8"/>',
                f'<text class="axis" x="{left + panel_w / 2:.1f}" y="{height - 20}" text-anchor="middle">IFEval prompt-strict delta vs SFT baseline (pp)</text>',
                f'<text class="axis" x="{left - 48:.1f}" y="{margin_top + panel_h / 2:.1f}" text-anchor="middle" transform="rotate(-90 {left - 48:.1f} {margin_top + panel_h / 2:.1f})">{y_label} vs SFT baseline (pp)</text>',
            ]
        )
        for run_id in ["r028", "r029", "s3d001", "s3d002"]:
            group = sorted([p for p in points if p["run_id"] == run_id], key=lambda p: p["adapter_label"])
            if len(group) == 2:
                step = next(p for p in group if p["adapter_label"] == "step50")
                final = next(p for p in group if p["adapter_label"] == "final")
                lines.append(
                    f'<line x1="{sx(pct(step["ifeval_prompt_strict_delta"]), idx):.1f}" y1="{sy(pct(step[y_col]), idx):.1f}" '
                    f'x2="{sx(pct(final["ifeval_prompt_strict_delta"]), idx):.1f}" y2="{sy(pct(final[y_col]), idx):.1f}" '
                    f'stroke="{COLORS[step["source"]]}" stroke-width="1.2" opacity="0.55"/>'
                )
        for point in points:
            x = sx(pct(point["ifeval_prompt_strict_delta"]), idx)
            y = sy(pct(point[y_col]), idx)
            label = POINT_IDS[(point["run_id"], point["adapter_label"])]
            color = COLORS[point["source"]]
            if point["cleanliness"] == "clean":
                lines.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6.5" fill="{color}" stroke="white" stroke-width="1"/>')
            else:
                lines.append(f'<rect x="{x - 6.5:.1f}" y="{y - 6.5:.1f}" width="13" height="13" fill="{color}" stroke="white" stroke-width="1"/>')
            lines.append(f'<text class="point" x="{x + 9:.1f}" y="{y - 7:.1f}">{label}</text>')
    lines.append("</svg>")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=ARTIFACTS / "stage4" / "pareto" / "pareto_points.csv")
    parser.add_argument("--output", type=Path, default=REPRODUCED / "figures" / "pareto_2panel.svg")
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(build_svg(read_points(args.input)), encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

