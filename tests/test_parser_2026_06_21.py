"""Parser tests added 2026-06-21 (Lane 2 of grade recovery plan)."""
import os
import tempfile
from pathlib import Path
import pytest
import pandas as pd
from phillies_intel_hub.report_parser import PhilliesAnalyticsParser


SAMPLE_HTML = """<!DOCTYPE html>
<html>
<head><title>Phillies Game Report - 2026-05-23</title></head>
<body>
<h1>Phillies vs Mets</h1>
<p>Final Score: PHI 6 - NYM 3</p>
<table id="batting">
<thead><tr><th>Player</th><th>AB</th><th>H</th><th>RBI</th></tr></thead>
<tbody>
<tr><td>Bryce Harper</td><td>4</td><td>2</td><td>1</td></tr>
<tr><td>JT Realmuto</td><td>4</td><td>1</td><td>0</td></tr>
</tbody>
</table>
<table id="pitching">
<thead><tr><th>Pitcher</th><th>IP</th><th>ER</th><th>K</th></tr></thead>
<tbody>
<tr><td>Zack Wheeler</td><td>7</td><td>2</td><td>9</td></tr>
</tbody>
</table>
</body>
</html>
"""


@pytest.fixture
def parser_with_tmp(tmp_path):
    """Parser pointed at a temporary reports directory."""
    return PhilliesAnalyticsParser(reports_dir=str(tmp_path))


@pytest.fixture
def sample_html_file(tmp_path):
    fp = tmp_path / "phillies_report_2026-05-23.html"
    fp.write_text(SAMPLE_HTML)
    return str(fp)


def test_parser_init_accepts_custom_dir(parser_with_tmp):
    """Parser should accept a reports_dir override (Lane 2: was hard-coded to a real path)."""
    assert parser_with_tmp.reports_dir is not None
    assert Path(parser_with_tmp.reports_dir).exists()


def test_parse_html_file_returns_dict(sample_html_file):
    """parse_html_file should return a structured dict from a valid HTML file."""
    parser = PhilliesAnalyticsParser(reports_dir=str(Path(sample_html_file).parent))
    report = parser.parse_html_file(sample_html_file)
    assert isinstance(report, dict)
    assert "filepath" in report
    assert "filename" in report


def test_parse_all_reports_empty_dir(tmp_path):
    """parse_all_reports should return [] when no files match (not crash)."""
    parser = PhilliesAnalyticsParser(reports_dir=str(tmp_path))
    assert parser.parse_all_reports() == []


def test_extract_key_metrics_handles_missing_keys():
    """extract_key_metrics should be defensive against partial reports."""
    parser = PhilliesAnalyticsParser(reports_dir="/tmp")
    result = parser.extract_key_metrics({"score": "PHI 6 - NYM 3"})
    assert isinstance(result, dict)