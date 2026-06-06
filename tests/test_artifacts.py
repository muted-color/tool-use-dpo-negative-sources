from pathlib import Path

from tool_use_dpo_negative_sources.figures import build_svg, read_points
from tool_use_dpo_negative_sources.paths import ARTIFACTS, CONFIGS
from tool_use_dpo_negative_sources.tables import build_source_axis_table, read_csv
from tool_use_dpo_negative_sources.verify import run_checks


def test_release_manifest_passes():
    result = run_checks(CONFIGS / "artifact_manifest.json")
    assert result["status"] == "pass", result["errors"]


def test_source_axis_table_has_primary_rows():
    rows = read_csv(ARTIFACTS / "stage4" / "bootstrap" / "pairwise_bootstrap_ci.csv")
    table = build_source_axis_table(rows)
    assert len(table) == 6
    assert any(row["metric"] == "BFCL_core_accuracy" for row in table)


def test_figure_svg_is_nonempty():
    points = read_points(ARTIFACTS / "stage4" / "pareto" / "pareto_points.csv")
    svg = build_svg(points)
    assert svg.startswith("<svg")
    assert "BFCL core" in svg
    assert len(svg) > 1000

