"""Pytest configuration and fixtures for ML Research MCP tests."""

from pathlib import Path

import polars as pl
import pytest


@pytest.fixture
def test_data_dir() -> Path:
    """Return path to test data directory."""
    return Path(__file__).parent / "data"


@pytest.fixture
def sample_csv_path(test_data_dir: Path) -> Path:
    """Return path to sample CSV file."""
    return test_data_dir / "sample_line.csv"


@pytest.fixture
def sample_scatter_csv_path(test_data_dir: Path) -> Path:
    """Return path to sample scatter CSV file."""
    return test_data_dir / "sample_scatter.csv"


@pytest.fixture
def sample_json_path(test_data_dir: Path) -> Path:
    """Return path to sample JSON file."""
    return test_data_dir / "sample.json"


@pytest.fixture
def sample_dataframe() -> pl.DataFrame:
    """Return a sample Polars DataFrame."""
    return pl.DataFrame({"x": [1, 2, 3, 4, 5], "y": [1, 4, 9, 16, 25]})


@pytest.fixture
def sample_direct_data() -> dict:
    """Return sample direct data as dict."""
    return {"x": [1, 2, 3], "y": [1, 4, 9]}
