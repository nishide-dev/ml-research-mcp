"""Common type definitions for ML Research MCP plotting tools.

This module defines Pydantic models for plot configuration and data input.
These types ensure type safety and automatic validation across all plotting tools.
"""

from typing import Literal

from pydantic import BaseModel, Field


class PlotOutputConfig(BaseModel):
    """Configuration for plot output format and dimensions.

    Attributes:
        format: Output format (png for raster, pdf/svg for vector)
        width: Figure width in centimeters
        height: Figure height in centimeters
        dpi: Resolution for raster formats (only affects PNG)
    """

    format: Literal["png", "pdf", "svg"] = Field(
        default="png",
        description="Output format: png (raster), pdf/svg (vector)",
    )
    width: float = Field(
        default=15.0,
        description="Figure width in cm",
        gt=0,
    )
    height: float = Field(
        default=10.0,
        description="Figure height in cm",
        gt=0,
    )
    dpi: int = Field(
        default=300,
        description="DPI for raster formats (PNG only)",
        gt=0,
    )


class PlotStyleConfig(BaseModel):
    """Configuration for plot styling and appearance.

    Attributes:
        colormap: Colormap name (e.g., 'viridis', 'plasma', 'RdBu')
        title: Plot title
        xlabel: X-axis label
        ylabel: Y-axis label
        grid: Whether to show grid lines
        alpha: Transparency level (0.0 to 1.0)
    """

    colormap: str | None = Field(
        default=None,
        description="Colormap name for data visualization",
    )
    title: str | None = Field(
        default=None,
        description="Plot title",
    )
    xlabel: str | None = Field(
        default=None,
        description="X-axis label",
    )
    ylabel: str | None = Field(
        default=None,
        description="Y-axis label",
    )
    grid: bool = Field(
        default=True,
        description="Show grid lines",
    )
    alpha: float | None = Field(
        default=None,
        description="Transparency level (0.0 to 1.0)",
        ge=0.0,
        le=1.0,
    )


class DataInput(BaseModel):
    """Configuration for data input source.

    Either file_path or data must be provided, but not both.

    Attributes:
        file_path: Path to data file (CSV, JSON, etc.)
        data: Direct data input as dictionary

    Examples:
        File input:
        >>> DataInput(file_path="experiment.csv")

        Direct data input:
        >>> DataInput(data={"x": [1, 2, 3], "y": [4, 5, 6]})
    """

    file_path: str | None = Field(
        default=None,
        description="Path to data file (CSV, JSON, etc.)",
    )
    data: dict | None = Field(
        default=None,
        description="Direct data input as JSON/dict",
    )
