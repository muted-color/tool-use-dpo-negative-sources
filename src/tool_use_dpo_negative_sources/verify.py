from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from .paths import CONFIGS, REPO_ROOT


FORBIDDEN_PATTERNS = [
    "pairs_*.jsonl",
    "*_private.jsonl",
    "*.key",
    ".env",
    ".env.*",
    "*.safetensors",
    "*eval_details*.jsonl",
    "*functionchat_details*.jsonl",
    "*ifeval_details*.jsonl",
]

MAX_FILE_SIZE_BYTES = 25 * 1024 * 1024


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_manifest(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def iter_repo_files() -> list[Path]:
    out: list[Path] = []
    for path in REPO_ROOT.rglob("*"):
        if path.is_file() and ".git" not in path.parts:
            out.append(path)
    return sorted(out)


def check_required_files(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for item in manifest["artifacts"]:
        path = REPO_ROOT / item["path"]
        if not path.exists():
            errors.append(f"missing required artifact: {item['path']}")
            continue
        expected = item.get("sha256")
        if expected:
            actual = sha256_file(path)
            if actual != expected:
                errors.append(f"sha256 mismatch for {item['path']}: {actual} != {expected}")
    return errors


def check_forbidden_files() -> list[str]:
    errors: list[str] = []
    for pattern in FORBIDDEN_PATTERNS:
        for path in REPO_ROOT.rglob(pattern):
            if path.is_file() and path.name != ".env.example":
                errors.append(f"forbidden public-release file matched {pattern}: {path.relative_to(REPO_ROOT)}")
    for path in iter_repo_files():
        if path.stat().st_size > MAX_FILE_SIZE_BYTES:
            errors.append(f"file exceeds public artifact size limit: {path.relative_to(REPO_ROOT)}")
    return errors


def run_checks(manifest_path: Path) -> dict[str, Any]:
    manifest = load_manifest(manifest_path)
    errors = check_required_files(manifest)
    errors.extend(check_forbidden_files())
    return {
        "status": "pass" if not errors else "fail",
        "errors": errors,
        "checked_artifacts": len(manifest["artifacts"]),
        "checked_files": len(iter_repo_files()),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=CONFIGS / "artifact_manifest.json")
    args = parser.parse_args()
    result = run_checks(args.manifest)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())

