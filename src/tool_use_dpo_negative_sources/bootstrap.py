from __future__ import annotations

import argparse
import csv
import random
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Callable

from .paths import REPO_ROOT, REPRODUCED


COMPARISONS = [
    ("clean_vs_unfiltered_step50", "r028", "s3d001", "step50", "step50"),
    ("clean_vs_unfiltered_step50", "r029", "s3d002", "step50", "step50"),
    ("clean_vs_unfiltered_final", "r028", "s3d001", "final", "final"),
    ("clean_vs_unfiltered_final", "r029", "s3d002", "final", "final"),
    ("step50_vs_final", "r028", "r028", "step50", "final"),
    ("step50_vs_final", "r029", "r029", "step50", "final"),
    ("step50_vs_final", "s3d001", "s3d001", "step50", "final"),
    ("step50_vs_final", "s3d002", "s3d002", "step50", "final"),
    ("source_axis_step50", "r028", "r029", "step50", "step50"),
    ("source_axis_step50", "s3d001", "s3d002", "step50", "step50"),
]

METRICS = [
    "BFCL_core_accuracy",
    "When2Call_behavior_accuracy",
    "When2Call_macro_F1",
    "strict_parse_success",
    "tool_call_accuracy_on_sft_dev",
    "behavior_accuracy_on_sft_dev",
    "nontrivial_error_rate",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def truthy(value: str | bool | None) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes"}


def f1_macro(labels: list[str], preds: list[str]) -> float:
    classes = sorted(set(labels) | set(preds) | {"tool_call", "follow_up", "unable", "direct_answer"})
    scores: list[float] = []
    for cls in classes:
        tp = sum(1 for y, p in zip(labels, preds) if y == cls and p == cls)
        fp = sum(1 for y, p in zip(labels, preds) if y != cls and p == cls)
        fn = sum(1 for y, p in zip(labels, preds) if y == cls and p != cls)
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        scores.append(2 * precision * recall / (precision + recall) if precision + recall else 0.0)
    return mean(scores) if scores else 0.0


def metric_value(rows: list[dict[str, str]], metric: str) -> float:
    if metric == "BFCL_core_accuracy":
        subset = [row for row in rows if row["task"] == "bfcl"]
        return sum(truthy(row["exact_match"]) for row in subset) / len(subset) if subset else 0.0
    if metric == "When2Call_behavior_accuracy":
        subset = [row for row in rows if row["task"] == "when2call"]
        return sum(truthy(row["exact_match"]) for row in subset) / len(subset) if subset else 0.0
    if metric == "When2Call_macro_F1":
        subset = [row for row in rows if row["task"] == "when2call"]
        return f1_macro([row["expected_behavior"] for row in subset], [row["observed_behavior"] for row in subset])
    if metric == "strict_parse_success":
        subset = [row for row in rows if row["task"] == "sft_dev" and row["expected_behavior"] == "tool_call"]
        return sum(truthy(row["strict_parse_success"]) for row in subset) / len(subset) if subset else 0.0
    if metric == "tool_call_accuracy_on_sft_dev":
        subset = [row for row in rows if row["task"] == "sft_dev" and row["expected_behavior"] == "tool_call"]
        return sum(truthy(row["exact_match"]) for row in subset) / len(subset) if subset else 0.0
    if metric == "behavior_accuracy_on_sft_dev":
        subset = [row for row in rows if row["task"] == "sft_dev"]
        return sum(truthy(row["exact_match"]) for row in subset) / len(subset) if subset else 0.0
    if metric == "nontrivial_error_rate":
        subset = [row for row in rows if row["task"] in {"bfcl", "when2call"}]
        return sum(truthy(row["nontrivial_error"]) for row in subset) / len(subset) if subset else 0.0
    raise KeyError(metric)


def load_rows(run_id: str, checkpoint: str) -> list[dict[str, str]]:
    return read_csv(REPO_ROOT / "results" / "per_example" / "primary" / f"{run_id}_{checkpoint}.csv")


def group_rows(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[row.get("prompt_id") or row.get("prompt_hash") or str(len(groups))].append(row)
    return groups


def grouped_bootstrap_delta(
    a_rows: list[dict[str, str]],
    b_rows: list[dict[str, str]],
    metric: str,
    iterations: int,
    seed: int,
) -> dict[str, object]:
    a_groups = group_rows(a_rows)
    b_groups = group_rows(b_rows)
    groups = sorted(set(a_groups) & set(b_groups))
    if not groups:
        return {"status": "no_shared_groups", "point_delta": "", "ci95_low": "", "ci95_high": "", "groups": 0, "iterations": iterations}
    rng = random.Random(seed)
    deltas: list[float] = []
    for _ in range(iterations):
        sampled = [rng.choice(groups) for _ in groups]
        a_sample = [row for group in sampled for row in a_groups[group]]
        b_sample = [row for group in sampled for row in b_groups[group]]
        deltas.append(metric_value(a_sample, metric) - metric_value(b_sample, metric))
    deltas.sort()
    return {
        "status": "complete",
        "point_delta": metric_value(a_rows, metric) - metric_value(b_rows, metric),
        "ci95_low": deltas[int(0.025 * (len(deltas) - 1))],
        "ci95_high": deltas[int(0.975 * (len(deltas) - 1))],
        "groups": len(groups),
        "iterations": iterations,
    }


def compute(iterations: int) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for comparison, a_run, b_run, a_checkpoint, b_checkpoint in COMPARISONS:
        a_rows = load_rows(a_run, a_checkpoint)
        b_rows = load_rows(b_run, b_checkpoint)
        for metric in METRICS:
            boot = grouped_bootstrap_delta(
                a_rows,
                b_rows,
                metric,
                iterations,
                seed=20260603 + len(rows) * 97,
            )
            rows.append(
                {
                    "comparison": comparison,
                    "a_run": a_run,
                    "b_run": b_run,
                    "a_adapter": a_checkpoint,
                    "b_adapter": b_checkpoint,
                    "metric": metric,
                    **boot,
                }
            )
    return rows


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bootstrap-iterations", type=int, default=1000)
    parser.add_argument("--output", type=Path, default=REPRODUCED / "bootstrap" / "pairwise_bootstrap_ci.csv")
    args = parser.parse_args()
    rows = compute(args.bootstrap_iterations)
    write_rows(args.output, rows)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

