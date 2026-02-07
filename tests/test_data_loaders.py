"""Tests for data loading functionality."""

from pathlib import Path

import polars as pl
import pytest

from ml_research_mcp.data.loaders import extract_column, load_data


def test_load_data_from_csv(sample_csv_path: Path) -> None:
    """Test loading data from CSV file."""
    df = load_data(file_path=str(sample_csv_path))
    assert isinstance(df, pl.DataFrame)
    assert df.shape == (5, 2)
    assert "x" in df.columns
    assert "y" in df.columns


def test_load_data_from_json(sample_json_path: Path) -> None:
    """Test loading data from JSON file."""
    df = load_data(file_path=str(sample_json_path))
    assert isinstance(df, pl.DataFrame)
    # JSON structure: {"x": [1,2,3,4,5], "y": [2,4,6,8,10]}
    # Polars reads this as 1 row with list columns
    assert df.shape[1] == 2  # 2 columns
    assert "x" in df.columns
    assert "y" in df.columns


def test_load_data_from_direct_data(sample_direct_data: dict) -> None:
    """Test loading data from direct dictionary input."""
    df = load_data(data=sample_direct_data)
    assert isinstance(df, pl.DataFrame)
    assert df.shape == (3, 2)
    assert df["x"].to_list() == [1, 2, 3]


def test_load_data_both_inputs_error() -> None:
    """Test that providing both file_path and data raises ValueError."""
    with pytest.raises(ValueError, match="Provide either file_path or data, not both"):
        load_data(file_path="test.csv", data={"x": [1, 2, 3]})


def test_load_data_no_inputs_error() -> None:
    """Test that providing neither input raises ValueError."""
    with pytest.raises(ValueError, match="Must provide either file_path or data"):
        load_data()


def test_load_data_nonexistent_file() -> None:
    """Test that loading nonexistent file raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError, match="File not found"):
        load_data(file_path="nonexistent_file.csv")


def test_load_data_unsupported_format(tmp_path: Path) -> None:
    """Test that unsupported file format raises ValueError."""
    unsupported_file = tmp_path / "test.txt"
    unsupported_file.write_text("some content")

    with pytest.raises(ValueError, match="Unsupported file format"):
        load_data(file_path=str(unsupported_file))


def test_extract_column_by_name(sample_dataframe: pl.DataFrame) -> None:
    """Test extracting column by name from DataFrame."""
    series = extract_column(sample_dataframe, "x")
    assert isinstance(series, pl.Series)
    assert series.to_list() == [1, 2, 3, 4, 5]


def test_extract_column_nonexistent(sample_dataframe: pl.DataFrame) -> None:
    """Test extracting nonexistent column raises ValueError."""
    with pytest.raises(ValueError, match="Column 'z' not found"):
        extract_column(sample_dataframe, "z")


def test_extract_column_direct_list(sample_dataframe: pl.DataFrame) -> None:
    """Test that passing a list directly returns it as-is."""
    data = [1, 2, 3]
    result = extract_column(sample_dataframe, data)
    assert result == data
