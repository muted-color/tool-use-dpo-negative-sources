#!/usr/bin/env python
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
CLAIMS = REPO_ROOT / "artifacts" / "stage4" / "claims"
KEYS = [
    "namespaced_prompt_id",
    "normalized_user_utterance_hash",
    "normalized_tool_schema_hash",
    "combined_user_query_tool_schema_hash",
]
STAGE3D_RUNS = {
    "r028": "experiments/exp_07_stage3d_high_confidence_clean_dpo_main/artifacts/runs/r026/pairs_noised_gold_clean_3k.jsonl",
    "r029": "experiments/exp_07_stage3d_high_confidence_clean_dpo_main/artifacts/runs/r027b/pairs_behavior_clean_3k.jsonl",
    "s3d001": "experiments/exp_07_stage3d_high_confidence_clean_dpo_main/artifacts/runs/s3d001/pairs_noised_gold_unfiltered_3k.jsonl",
    "s3d002": "experiments/exp_07_stage3d_high_confidence_clean_dpo_main/artifacts/runs/s3d002/pairs_behavior_unfiltered_3k.jsonl",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def iter_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def sanitize_paths(obj: Any, workspace_root: Path) -> Any:
    if isinstance(obj, dict):
        return {key: sanitize_paths(value, workspace_root) for key, value in obj.items()}
    if isinstance(obj, list):
        return [sanitize_paths(value, workspace_root) for value in obj]
    if isinstance(obj, str):
        try:
            path = Path(obj)
            if path.is_absolute():
                return str(path.resolve().relative_to(workspace_root.resolve()))
        except Exception:
            return obj
    return obj


def copy_sanitized_report(source: Path, workspace_root: Path, report_kind: str) -> dict[str, Any]:
    payload = sanitize_paths(read_json(source), workspace_root)
    return {
        "report_kind": report_kind,
        "source_artifact": str(source.resolve().relative_to(workspace_root.resolve())),
        "source_sha256": sha256_bytes(source.read_bytes()),
        "payload": payload,
    }


def load_manifest_sets(path: Path, split: str | None = None) -> tuple[int, dict[str, set[str]]]:
    sets = {key: set() for key in KEYS}
    count = 0
    for row in iter_jsonl(path):
        if split is not None and row.get("split") != split:
            continue
        count += 1
        for key in KEYS:
            value = row.get(key)
            if value:
                sets[key].add(str(value))
    return count, sets


def pair_hash_fields(row: dict[str, Any]) -> dict[str, str]:
    user = normalize_text(str(row.get("user_query", "")))
    tools = normalize_text(json.dumps(row.get("tools", []), ensure_ascii=False, sort_keys=True, default=str))
    return {
        "namespaced_prompt_id": str(row.get("prompt_id", "")),
        "normalized_user_utterance_hash": sha256_text(user),
        "normalized_tool_schema_hash": sha256_text(tools),
        "combined_user_query_tool_schema_hash": sha256_text(user + "\n---tools---\n" + tools),
    }


def load_pair_sets(path: Path) -> tuple[int, dict[str, set[str]]]:
    sets = {key: set() for key in KEYS}
    count = 0
    for row in iter_jsonl(path):
        count += 1
        for key, value in pair_hash_fields(row).items():
            if value:
                sets[key].add(value)
    return count, sets


def recompute_stage3d_overlap(workspace_root: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    eval_path = REPO_ROOT / "manifests" / "eval" / "eval_slice_manifest.jsonl"
    sft_path = workspace_root / "experiments" / "exp_02_stage1_target_sft_pilot" / "artifacts" / "runs" / "r002" / "sft_split_manifest.jsonl"
    targets = {
        "eval_slice": load_manifest_sets(eval_path),
        "sft_dev": load_manifest_sets(sft_path, split="dev"),
        "sft_manifest_all": load_manifest_sets(sft_path),
    }
    report: dict[str, Any] = {
        "status": "pass",
        "report_kind": "stage3d_train_pool_overlap",
        "note": "Hash-only overlap check. Raw prompts, tool schemas, completions, and full DPO pairs are not redistributed.",
        "hash_keys": KEYS,
        "targets": {
            name: {"row_count": count, "unique_counts": {key: len(values) for key, values in sets.items()}}
            for name, (count, sets) in targets.items()
        },
        "runs": {},
    }
    summary_rows: list[dict[str, Any]] = []
    any_overlap = False
    for run_id, rel_path in STAGE3D_RUNS.items():
        path = workspace_root / rel_path
        pair_count, pair_sets = load_pair_sets(path)
        run_payload = {
            "pair_path": rel_path,
            "pair_sha256": sha256_bytes(path.read_bytes()),
            "pair_count": pair_count,
            "unique_counts": {key: len(values) for key, values in pair_sets.items()},
            "checks": {},
        }
        for target_name, (target_count, target_sets) in targets.items():
            run_payload["checks"][target_name] = {}
            for key in KEYS:
                overlap = pair_sets[key] & target_sets[key]
                overlap_count = len(overlap)
                any_overlap = any_overlap or overlap_count > 0
                run_payload["checks"][target_name][key] = {
                    "overlap_count": overlap_count,
                    "target_rows": target_count,
                }
                summary_rows.append(
                    {
                        "scope": "stage3d_train_pool",
                        "run_id": run_id,
                        "target": target_name,
                        "check_key": key,
                        "overlap_count": overlap_count,
                        "status": "pass" if overlap_count == 0 else "needs_review",
                    }
                )
        report["runs"][run_id] = run_payload
    if any_overlap:
        report["status"] = "needs_review"
    return report, summary_rows


def write_summary_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["scope", "run_id", "target", "check_key", "overlap_count", "status"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_combined_summary(path: Path, stage3d_rows: list[dict[str, Any]]) -> None:
    rows: list[dict[str, Any]] = []
    stage1 = read_json(CLAIMS / "stage1_contamination_report.json")["payload"]
    for key, payload in stage1["checks"].items():
        rows.append(
            {
                "scope": "stage1_sft_vs_eval",
                "source_artifact": "artifacts/stage4/claims/stage1_contamination_report.json",
                "status": stage1["status"],
                "check_key": key,
                "overlap_count": payload["overlap_count"],
                "notes": "hash-only Stage1 SFT/eval overlap check",
            }
        )
    stage2 = read_json(CLAIMS / "stage2_contamination_report.json")["payload"]
    for key, overlap_count in stage2["checks_after_filtering"].items():
        rows.append(
            {
                "scope": "stage2_prompt_pool_after_filtering",
                "source_artifact": "artifacts/stage4/claims/stage2_contamination_report.json",
                "status": stage2["status"],
                "check_key": key,
                "overlap_count": overlap_count,
                "notes": "hash-only Stage2 accepted prompt-pool overlap check after filtering",
            }
        )
    for row in stage3d_rows:
        rows.append(
            {
                "scope": f"{row['scope']}:{row['run_id']}:{row['target']}",
                "source_artifact": "artifacts/stage4/claims/stage3d_train_pool_overlap_report.json",
                "status": row["status"],
                "check_key": row["check_key"],
                "overlap_count": row["overlap_count"],
                "notes": "hash-only final Stage3d selected train-pool overlap check",
            }
        )
    fieldnames = ["scope", "source_artifact", "status", "check_key", "overlap_count", "notes"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def generate(workspace_root: Path) -> dict[str, Any]:
    stage1_src = workspace_root / "experiments" / "exp_02_stage1_target_sft_pilot" / "artifacts" / "runs" / "r002" / "contamination_report.json"
    stage2_src = workspace_root / "experiments" / "exp_03_stage2_negative_generation_pair_qa" / "artifacts" / "runs" / "r005" / "contamination_report.json"
    write_json(CLAIMS / "stage1_contamination_report.json", copy_sanitized_report(stage1_src, workspace_root, "stage1_sft_eval_contamination"))
    write_json(CLAIMS / "stage2_contamination_report.json", copy_sanitized_report(stage2_src, workspace_root, "stage2_prompt_pool_contamination"))
    stage3d_report, stage3d_rows = recompute_stage3d_overlap(workspace_root)
    write_json(CLAIMS / "stage3d_train_pool_overlap_report.json", stage3d_report)
    write_summary_csv(CLAIMS / "stage3d_train_pool_overlap_summary.csv", stage3d_rows)
    write_combined_summary(CLAIMS / "overlap_check_summary.csv", stage3d_rows)
    return verify_existing()


def verify_existing() -> dict[str, Any]:
    required = [
        CLAIMS / "stage1_contamination_report.json",
        CLAIMS / "stage2_contamination_report.json",
        CLAIMS / "stage3d_train_pool_overlap_report.json",
        CLAIMS / "stage3d_train_pool_overlap_summary.csv",
        CLAIMS / "overlap_check_summary.csv",
    ]
    errors: list[str] = []
    for path in required:
        if not path.exists():
            errors.append(f"missing overlap artifact: {path.relative_to(REPO_ROOT)}")
    for path in required[:3]:
        if path.exists():
            data = read_json(path)
            status = data.get("payload", data).get("status")
            if status not in {"pass", "prepared_hash_manifest_only"}:
                errors.append(f"non-pass status in {path.relative_to(REPO_ROOT)}: {status}")
    combined_path = CLAIMS / "overlap_check_summary.csv"
    if combined_path.exists():
        with combined_path.open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                overlap_count = int(row["overlap_count"])
                if overlap_count != 0 or row["status"] != "pass":
                    errors.append(
                        "non-zero overlap in "
                        f"{combined_path.relative_to(REPO_ROOT)}: "
                        f"{row['scope']} {row['check_key']}={overlap_count} status={row['status']}"
                    )
    return {
        "status": "pass" if not errors else "fail",
        "errors": errors,
        "checked_artifacts": [str(path.relative_to(REPO_ROOT)) for path in required],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace-root", type=Path, default=None, help="Project root containing private raw pair artifacts; enables recomputation.")
    parser.add_argument("--write-artifacts", action="store_true", help="Write sanitized overlap artifacts after recomputation.")
    args = parser.parse_args()
    if args.write_artifacts:
        if args.workspace_root is None:
            raise SystemExit("--write-artifacts requires --workspace-root")
        result = generate(args.workspace_root.resolve())
    else:
        result = verify_existing()
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
