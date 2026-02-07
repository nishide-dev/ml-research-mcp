"""2D plotting tools: heatmap, contour, and pcolormesh.

This module provides 2D visualization capabilities for matrix data,
spatial data, and multi-dimensional relationships.
"""

from typing import Literal

import numpy as np
import polars as pl
from PIL import Image

from ml_research_mcp.data.loaders import extract_column, load_data
from ml_research_mcp.plotting.core import create_plot_figure, save_plot_to_image
from ml_research_mcp.plotting.formatters import apply_style, get_colormap_name
from ml_research_mcp.server import mcp


@mcp.tool()
def plot_heatmap(
    data: str | list[list[float]],
    data_input: dict | None = None,
    x_labels: list[str] | None = None,
    y_labels: list[str] | None = None,
    annotate: bool = False,
    style: dict | None = None,
    output: dict | None = None,
) -> Image.Image | bytes:
    """Create a heatmap for visualizing matrix data.

    This tool generates a heatmap with optional annotations, ideal for
    correlation matrices, confusion matrices, or any 2D data.

    Args:
        data: For direct input, 2D list (matrix). For file input, column name.
        data_input: Optional. {"file_path": "path/to/file.csv"} or {"data": {...}}
        x_labels: Optional labels for x-axis (columns)
        y_labels: Optional labels for y-axis (rows)
        annotate: If True, show values in each cell
        style: Optional. {"title": "...", "xlabel": "...", "ylabel": "...", "colormap": "viridis"}
        output: Optional. {"format": "png/pdf/svg", "width": 15, "height": 10, "dpi": 300}

    Returns:
        PIL Image object or bytes containing the plot

    Examples:
        Correlation matrix:
        >>> plot_heatmap(
        ...     data=[[1.0, 0.8, 0.3], [0.8, 1.0, 0.5], [0.3, 0.5, 1.0]],
        ...     x_labels=["A", "B", "C"],
        ...     y_labels=["A", "B", "C"],
        ...     annotate=True,
        ...     style={"title": "Correlation Matrix", "colormap": "RdBu"}
        ... )

        From file:
        >>> plot_heatmap(
        ...     data="matrix",
        ...     data_input={"file_path": "data_matrix.csv"},
        ...     style={"colormap": "plasma"}
        ... )
    """
    # Parse configuration
    style = style or {}
    output = output or {}

    # Load data if needed
    df = None
    if data_input:
        df = load_data(**data_input)

    # Extract data and convert to numpy array
    if df is not None:
        if isinstance(data, str):
            series = extract_column(df, data)
            assert isinstance(series, pl.Series)  # Type guard for ty
            data_values = series.to_numpy()
        else:
            data_values = np.array(data)
    else:
        data_values = np.array(data)

    # Ensure 2D
    if data_values.ndim == 1:
        # Reshape if 1D
        n = int(np.sqrt(len(data_values)))
        data_values = data_values.reshape(n, n)

    # Create figure
    width = output.get("width", 15.0)
    height = output.get("height", 10.0)
    fig, ax = create_plot_figure(width_cm=width, height_cm=height)

    # Plot heatmap
    cmap = get_colormap_name(style.get("colormap"))
    im = ax.imshow(data_values, cmap=cmap, aspect="auto")

    # Add colorbar
    fig.colorbar(im, ax=ax)

    # Set labels if provided
    if x_labels:
        ax.set_xticks(np.arange(len(x_labels)))
        ax.set_xticklabels(x_labels)
    if y_labels:
        ax.set_yticks(np.arange(len(y_labels)))
        ax.set_yticklabels(y_labels)

    # Annotate if requested
    if annotate:
        for i in range(data_values.shape[0]):
            for j in range(data_values.shape[1]):
                ax.text(
                    j,
                    i,
                    f"{data_values[i, j]:.2f}",
                    ha="center",
                    va="center",
                    color="white"
                    if data_values[i, j] < data_values.mean()
                    else "black",
                )

    # Apply style
    apply_style(
        ax,
        title=style.get("title"),
        xlabel=style.get("xlabel"),
        ylabel=style.get("ylabel"),
        grid=False,  # No grid for heatmaps
        colormap=style.get("colormap"),
    )

    # Save and return
    format_type = output.get("format", "png")
    dpi = output.get("dpi", 300)
    return save_plot_to_image(fig, fmt=format_type, dpi=dpi)


@mcp.tool()
def plot_contour(
    x: str | list[float],
    y: str | list[float],
    z: str | list[list[float]],
    data_input: dict | None = None,
    levels: int = 10,
    filled: bool = True,
    style: dict | None = None,
    output: dict | None = None,
) -> Image.Image | bytes:
    """Create a contour plot for 3D data visualization in 2D.

    This tool generates contour lines (or filled contours) showing
    levels of a third variable (z) across x-y coordinates.

    Args:
        x: X coordinates. Column name or list of values.
        y: Y coordinates. Column name or list of values.
        z: Z values (2D array). Column name or 2D list.
        data_input: Optional. {"file_path": "path/to/file.csv"} or {"data": {...}}
        levels: Number of contour levels (default: 10)
        filled: If True, create filled contours (contourf), else lines only
        style: Optional. {"title": "...", "xlabel": "...", "ylabel": "...", "colormap": "viridis"}
        output: Optional. {"format": "png/pdf/svg", "width": 15, "height": 10, "dpi": 300}

    Returns:
        PIL Image object or bytes containing the plot

    Examples:
        Filled contour plot:
        >>> x = [1, 2, 3, 4, 5]
        >>> y = [1, 2, 3, 4, 5]
        >>> z = [[i+j for j in range(5)] for i in range(5)]
        >>> plot_contour(x=x, y=y, z=z, levels=15, filled=True)

        Line contours only:
        >>> plot_contour(
        ...     x="longitude",
        ...     y="latitude",
        ...     z="temperature",
        ...     data_input={"file_path": "climate_data.csv"},
        ...     filled=False,
        ...     levels=20
        ... )
    """
    # Parse configuration
    style = style or {}
    output = output or {}

    # Load data if needed
    df = None
    if data_input:
        df = load_data(**data_input)

    # Extract data
    if df is not None:
        x_series = extract_column(df, x)
        y_series = extract_column(df, y)
        z_series = extract_column(df, z)
        assert isinstance(x_series, pl.Series)  # Type guard for ty
        assert isinstance(y_series, pl.Series)  # Type guard for ty
        assert isinstance(z_series, pl.Series)  # Type guard for ty
        x_data = x_series.to_numpy()
        y_data = y_series.to_numpy()
        z_data = z_series.to_numpy()
    else:
        x_data = np.array(x)
        y_data = np.array(y)
        z_data = np.array(z)

    # Ensure z is 2D
    if z_data.ndim == 1:
        # Try to reshape
        n = int(np.sqrt(len(z_data)))
        z_data = z_data.reshape(n, n)

    # Create meshgrid if x and y are 1D
    if x_data.ndim == 1 and y_data.ndim == 1:
        x_mesh, y_mesh = np.meshgrid(x_data, y_data)
    else:
        x_mesh, y_mesh = x_data, y_data

    # Create figure
    width = output.get("width", 15.0)
    height = output.get("height", 10.0)
    fig, ax = create_plot_figure(width_cm=width, height_cm=height)

    # Plot contour
    cmap = get_colormap_name(style.get("colormap"))

    if filled:
        cs = ax.contourf(x_mesh, y_mesh, z_data, levels=levels, cmap=cmap)
    else:
        cs = ax.contour(x_mesh, y_mesh, z_data, levels=levels, cmap=cmap)

    # Add colorbar
    fig.colorbar(cs, ax=ax)

    # Apply style
    apply_style(
        ax,
        title=style.get("title"),
        xlabel=style.get("xlabel"),
        ylabel=style.get("ylabel"),
        grid=style.get("grid", True),
        colormap=style.get("colormap"),
    )

    # Save and return
    format_type = output.get("format", "png")
    dpi = output.get("dpi", 300)
    return save_plot_to_image(fig, fmt=format_type, dpi=dpi)


@mcp.tool()
def plot_pcolormesh(
    x: str | list[float],
    y: str | list[float],
    z: str | list[list[float]],
    data_input: dict | None = None,
    shading: Literal["auto", "flat", "nearest", "gouraud"] = "auto",
    style: dict | None = None,
    output: dict | None = None,
) -> Image.Image | bytes:
    """Create a pseudocolor plot with a non-regular rectangular grid.

    This tool generates a fast pseudocolor plot using pcolormesh,
    ideal for large datasets and irregular grids.

    Args:
        x: X coordinates. Column name or list of values.
        y: Y coordinates. Column name or list of values.
        z: Z values (2D array). Column name or 2D list.
        data_input: Optional. {"file_path": "path/to/file.csv"} or {"data": {...}}
        shading: Shading method ("auto", "flat", "nearest", "gouraud")
        style: Optional. {"title": "...", "xlabel": "...", "ylabel": "...", "colormap": "viridis"}
        output: Optional. {"format": "png/pdf/svg", "width": 15, "height": 10, "dpi": 300}

    Returns:
        PIL Image object or bytes containing the plot

    Examples:
        Basic pcolormesh:
        >>> x = [1, 2, 3, 4]
        >>> y = [1, 2, 3, 4]
        >>> z = [[1, 2, 3, 4], [2, 4, 6, 8], [3, 6, 9, 12], [4, 8, 12, 16]]
        >>> plot_pcolormesh(x=x, y=y, z=z, shading="gouraud")

        From file with custom colormap:
        >>> plot_pcolormesh(
        ...     x="x_coord",
        ...     y="y_coord",
        ...     z="intensity",
        ...     data_input={"file_path": "field_data.csv"},
        ...     style={"colormap": "plasma", "title": "Field Intensity"}
        ... )
    """
    # Parse configuration
    style = style or {}
    output = output or {}

    # Load data if needed
    df = None
    if data_input:
        df = load_data(**data_input)

    # Extract data
    if df is not None:
        x_series = extract_column(df, x)
        y_series = extract_column(df, y)
        z_series = extract_column(df, z)
        assert isinstance(x_series, pl.Series)  # Type guard for ty
        assert isinstance(y_series, pl.Series)  # Type guard for ty
        assert isinstance(z_series, pl.Series)  # Type guard for ty
        x_data = x_series.to_numpy()
        y_data = y_series.to_numpy()
        z_data = z_series.to_numpy()
    else:
        x_data = np.array(x)
        y_data = np.array(y)
        z_data = np.array(z)

    # Ensure z is 2D
    if z_data.ndim == 1:
        n = int(np.sqrt(len(z_data)))
        z_data = z_data.reshape(n, n)

    # Create meshgrid if x and y are 1D
    if x_data.ndim == 1 and y_data.ndim == 1:
        x_mesh, y_mesh = np.meshgrid(x_data, y_data)
    else:
        x_mesh, y_mesh = x_data, y_data

    # Create figure
    width = output.get("width", 15.0)
    height = output.get("height", 10.0)
    fig, ax = create_plot_figure(width_cm=width, height_cm=height)

    # Plot pcolormesh
    cmap = get_colormap_name(style.get("colormap"))
    mesh = ax.pcolormesh(x_mesh, y_mesh, z_data, shading=shading, cmap=cmap)

    # Add colorbar
    fig.colorbar(mesh, ax=ax)

    # Apply style
    apply_style(
        ax,
        title=style.get("title"),
        xlabel=style.get("xlabel"),
        ylabel=style.get("ylabel"),
        grid=style.get("grid", True),
        colormap=style.get("colormap"),
    )

    # Save and return
    format_type = output.get("format", "png")
    dpi = output.get("dpi", 300)
    return save_plot_to_image(fig, fmt=format_type, dpi=dpi)
