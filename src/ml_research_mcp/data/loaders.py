"""Data loaders for various file formats using Polars.

This module provides functions to load data from CSV, JSON files,
or direct dictionary input into Polars DataFrames.
"""

from pathlib import Path
from typing import overload

import polars as pl


def load_data(
    file_path: str | None = None,
    data: dict | None = None,
) -> pl.DataFrame:
    """Load data from file or direct input into a Polars DataFrame.

    Either file_path or data must be provided, but not both.

    Args:
        file_path: Path to CSV, JSON, or other supported file format
        data: Direct data as dictionary (column_name -> values)

    Returns:
        Polars DataFrame containing the loaded data

    Raises:
        ValueError: If neither or both inputs are provided
        ValueError: If both file_path and data are provided
        FileNotFoundError: If file doesn't exist
        ValueError: If unsupported file format

    Examples:
        Load from CSV file:
        >>> df = load_data(file_path="experiment.csv")

        Load from JSON file:
        >>> df = load_data(file_path="data.json")

        Load from direct data:
        >>> df = load_data(data={"x": [1, 2, 3], "y": [4, 5, 6]})
    """
    # Validation: exactly one input must be provided
    if file_path and data:
        msg = (
            "Provide either file_path or data, not both. "
            "Use file_path for loading from files, or data for direct input."
        )
        raise ValueError(msg)

    if not file_path and not data:
        msg = (
            "Must provide either file_path or data. "
            "Please specify a file to load or provide data directly."
        )
        raise ValueError(msg)

    # Load from file
    if file_path:
        path = Path(file_path).resolve()

        if not path.exists():
            msg = (
                f"File not found: {file_path}. "
                "Please check the file path or provide data directly using the 'data' parameter."
            )
            raise FileNotFoundError(msg)

        # Determine file type and load accordingly
        suffix = path.suffix.lower()

        if suffix == ".csv":
            try:
                return pl.read_csv(path)
            except Exception as e:
                msg = (
                    f"Failed to read CSV file '{file_path}': {e}. "
                    "Please ensure the file is a valid CSV format."
                )
                raise ValueError(msg) from e

        elif suffix == ".json":
            try:
                return pl.read_json(path)
            except Exception as e:
                msg = (
                    f"Failed to read JSON file '{file_path}': {e}. "
                    "Please ensure the file is a valid JSON format."
                )
                raise ValueError(msg) from e

        else:
            msg = (
                f"Unsupported file format: {suffix}. "
                f"Supported formats are: .csv, .json. "
                f"File: {file_path}"
            )
            raise ValueError(msg)

    # Load from direct data
    try:
        return pl.DataFrame(data)
    except Exception as e:
        msg = (
            f"Failed to create DataFrame from provided data: {e}. "
            "Please ensure data is a valid dictionary with column names as keys "
            "and lists of values."
        )
        raise ValueError(msg) from e


@overload
def extract_column(df: pl.DataFrame, column: str) -> pl.Series: ...


@overload
def extract_column(df: pl.DataFrame, column: list) -> list: ...


def extract_column(
    df: pl.DataFrame,
    column: str | list,
) -> pl.Series | list:
    """Extract a column from DataFrame or return the list as-is.

    Args:
        df: Polars DataFrame
        column: Column name (string) or direct data (list)

    Returns:
        Polars Series if column is string, or the input list

    Raises:
        ValueError: If column name doesn't exist in DataFrame

    Examples:
        Extract by column name:
        >>> df = pl.DataFrame({"x": [1, 2, 3]})
        >>> extract_column(df, "x")
        Series: x [i64]
        [1, 2, 3]

        Direct list:
        >>> extract_column(df, [1, 2, 3])
        [1, 2, 3]
    """
    if isinstance(column, str):
        if column not in df.columns:
            available = ", ".join(df.columns)
            msg = f"Column '{column}' not found in data. Available columns: {available}"
            raise ValueError(msg)
        return df[column]

    # If it's already a list, return as-is
    return column
