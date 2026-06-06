from __future__ import annotations

import argparse
import csv
from pathlib import Path

from .paths import ARTIFACTS, REPO_ROOT, REPRODUCED


PRIMARY_METRICS = {
    "BFCL_core_accuracy",
    "When2Call_behavior_accuracy",
    "When2Call_macro_F1",
}

ABSOLUTE_SCORE_METRICS = [
    "BFCL_core_accuracy",
    "When2Call_behavior_accuracy",
    "When2Call_macro_F1",
    "ifeval_style.prompt_level_strict_accuracy",
    "strict_parse_success",
]

FUNCTIONCHAT_METRIC = "functionchat_bench.function_name_accuracy"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def percent(value: str | float | None) -> float | None:
    if value is None or value == "":
        return None
    return 100.0 * float(value)


def build_source_axis_table(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for row in rows:
        if row["comparison"] != "source_axis_step50" or row["metric"] not in PRIMARY_METRICS:
            continue
        out.append(
            {
                "comparison": f"{row['a_run']}/{row['a_adapter']} minus {row['b_run']}/{row['b_adapter']}",
                "metric": row["metric"],
                "delta_pp": percent(row["point_delta"]),
                "ci95_low_pp": percent(row["ci95_low"]),
                "ci95_high_pp": percent(row["ci95_high"]),
                "groups": row["groups"],
            }
        )
    return out


def build_clean_vs_unfiltered_table(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for row in rows:
        if row["comparison"] != "clean_vs_unfiltered_step50" or row["metric"] not in PRIMARY_METRICS:
            continue
        out.append(
            {
                "comparison": f"{row['a_run']}/{row['a_adapter']} minus {row['b_run']}/{row['b_adapter']}",
                "metric": row["metric"],
                "delta_pp": percent(row["point_delta"]),
                "ci95_low_pp": percent(row["ci95_low"]),
                "ci95_high_pp": percent(row["ci95_high"]),
                "groups": row["groups"],
            }
        )
    return out


def build_pareto_summary(points: list[dict[str, str]]) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for row in points:
        out.append(
            {
                "run_id": row["run_id"],
                "source": row["source"],
                "cleanliness": row["cleanliness"],
                "checkpoint": row["adapter_label"],
                "bfcl_core_delta_pp": percent(row["bfcl_core_delta"]),
                "when2call_macro_f1_delta_pp": percent(row["when2call_macro_f1_delta"]),
                "ifeval_prompt_strict_delta_pp": percent(row["ifeval_prompt_strict_delta"]),
            }
        )
    return out


def build_absolute_scores(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    keep = {
        ("r004", "sft_best"),
        ("r028", "step50"),
        ("r028", "final"),
        ("r029", "step50"),
        ("r029", "final"),
        ("s3d001", "step50"),
        ("s3d001", "final"),
        ("s3d002", "step50"),
        ("s3d002", "final"),
    }
    by_run = {
        (row["run_id"], row["checkpoint"], row["metric"]): row["score"]
        for row in rows
    }
    for run_id, checkpoint in sorted(keep):
        item: dict[str, object] = {"run_id": run_id, "checkpoint": checkpoint}
        for metric in ABSOLUTE_SCORE_METRICS:
            item[metric] = by_run[(run_id, checkpoint, metric)]
        out.append(item)
    return out


def build_budget_table(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for row in rows:
        if row["adapter_label"] != "final":
            continue
        out.append(
            {
                "run_id": row["run_id"],
                "pair_count": row["pair_count"],
                "steps": row["steps"],
                "loss_bearing_tokens_seen": row["loss_bearing_tokens_seen"],
                "padded_tokens_seen": row["padded_tokens_seen"],
                "train_wall_clock_seconds": row["train_wall_clock_seconds"],
                "peak_gpu_memory_gb": row["peak_gpu_memory_gb"],
            }
        )
    return out


def build_functionchat_table(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for row in rows:
        if row["metric"] != FUNCTIONCHAT_METRIC:
            continue
        out.append(
            {
                "run_id": row["run_id"],
                "checkpoint": row["checkpoint"],
                "function_name_delta_pp": percent(row["delta_vs_r004"]),
            }
        )
    return out


def build_source_risk_table(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for row in rows:
        out.append(
            {
                "source": row["source"],
                "audited_count": row["audited_count"],
                "reject_count": row["reject_count"],
                "reject_rate_pct": percent(row["reject_rate"]),
                "taxonomy_counts": row["taxonomy_counts"],
            }
        )
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=REPRODUCED / "tables")
    args = parser.parse_args()

    bootstrap = read_csv(ARTIFACTS / "stage4" / "bootstrap" / "pairwise_bootstrap_ci.csv")
    points = read_csv(ARTIFACTS / "stage4" / "pareto" / "pareto_points.csv")
    absolute = read_csv(REPO_ROOT / "results" / "aggregate" / "main_metrics_absolute.csv")
    deltas = read_csv(REPO_ROOT / "results" / "aggregate" / "main_metrics_delta_vs_sft.csv")
    costs = read_csv(ARTIFACTS / "stage3d" / "cost_table.csv")
    source_risk = read_csv(ARTIFACTS / "stage4" / "stage3b" / "stage3b_reject_taxonomy_summary.csv")

    write_csv(
        args.output_dir / "source_axis_step50.csv",
        build_source_axis_table(bootstrap),
        ["comparison", "metric", "delta_pp", "ci95_low_pp", "ci95_high_pp", "groups"],
    )
    write_csv(
        args.output_dir / "clean_vs_unfiltered_step50.csv",
        build_clean_vs_unfiltered_table(bootstrap),
        ["comparison", "metric", "delta_pp", "ci95_low_pp", "ci95_high_pp", "groups"],
    )
    write_csv(
        args.output_dir / "pareto_summary.csv",
        build_pareto_summary(points),
        [
            "run_id",
            "source",
            "cleanliness",
            "checkpoint",
            "bfcl_core_delta_pp",
            "when2call_macro_f1_delta_pp",
            "ifeval_prompt_strict_delta_pp",
        ],
    )
    write_csv(
        args.output_dir / "absolute_scores.csv",
        build_absolute_scores(absolute),
        ["run_id", "checkpoint", *ABSOLUTE_SCORE_METRICS],
    )
    write_csv(
        args.output_dir / "budget_accounting.csv",
        build_budget_table(costs),
        [
            "run_id",
            "pair_count",
            "steps",
            "loss_bearing_tokens_seen",
            "padded_tokens_seen",
            "train_wall_clock_seconds",
            "peak_gpu_memory_gb",
        ],
    )
    write_csv(
        args.output_dir / "functionchat_transfer.csv",
        build_functionchat_table(deltas),
        ["run_id", "checkpoint", "function_name_delta_pp"],
    )
    write_csv(
        args.output_dir / "source_risk.csv",
        build_source_risk_table(source_risk),
        ["source", "audited_count", "reject_count", "reject_rate_pct", "taxonomy_counts"],
    )
    print(args.output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
