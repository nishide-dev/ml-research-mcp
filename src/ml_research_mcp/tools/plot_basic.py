"""Basic plotting tools: line, scatter, and bar plots.

This module provides fundamental plotting capabilities for
time series data, scatter relationships, and categorical comparisons.
"""

from typing import Literal

from PIL import Image

from ml_research_mcp.data.loaders import extract_column, load_data
from ml_research_mcp.plotting.core import create_plot_figure, save_plot_to_image
from ml_research_mcp.plotting.formatters import apply_style, get_colormap_name
from ml_research_mcp.server import mcp


@mcp.tool()
def plot_line(
    x: str | list[float],
    y: str | list[float],
    data_input: dict | None = None,
    style: dict | None = None,
    output: dict | None = None,
) -> Image.Image | bytes:
    """Create a line plot from data.

    This tool generates a line plot using UltraPlot/Matplotlib. You can provide
    data either as a file path (CSV/JSON) or directly as lists.

    Args:
        x: X-axis data. Column name (string) if using data file, or list of values.
        y: Y-axis data. Column name (string) if using data file, or list of values.
        data_input: Optional. {"file_path": "path/to/file.csv"} or {"data": {...}}
        style: Optional. {"title": "...", "xlabel": "...", "ylabel": "...", "colormap": "...", "grid": True}
        output: Optional. {"format": "png/pdf/svg", "width": 15, "height": 10, "dpi": 300}

    Returns:
        PIL Image object or bytes containing the plot

    Examples:
        Basic line plot with direct data:
        >>> plot_line(x=[1, 2, 3], y=[1, 4, 9])

        Line plot from CSV file:
        >>> plot_line(
        ...     x="time",
        ...     y="temperature",
        ...     data_input={"file_path": "experiment.csv"},
        ...     style={"title": "Temperature Over Time", "xlabel": "Time (s)"}
        ... )

        High-resolution PDF output:
        >>> plot_line(
        ...     x=[1, 2, 3],
        ...     y=[1, 4, 9],
        ...     output={"format": "pdf", "width": 20, "height": 15}
        ... )
    """
    # Parse configuration
    style = style or {}
    output = output or {}

    # Load data if needed
    df = None
    if data_input:
        df = load_data(**data_input)

    # Extract x and y data
    if df is not None:
        x_data = extract_column(df, x)
        y_data = extract_column(df, y)
    else:
        x_data = x
        y_data = y

    # Create figure
    width = output.get("width", 15.0)
    height = output.get("height", 10.0)
    fig, ax = create_plot_figure(width_cm=width, height_cm=height)

    # Plot data
    ax.plot(x_data, y_data, linewidth=2)

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
def plot_scatter(
    x: str | list[float],
    y: str | list[float],
    data_input: dict | None = None,
    size: str | list[float] | float | None = None,
    color: str | list[float] | None = None,
    style: dict | None = None,
    output: dict | None = None,
) -> Image.Image | bytes:
    """Create a scatter plot with optional size and color mapping.

    This tool generates a scatter plot where point sizes and colors can
    represent additional data dimensions.

    Args:
        x: X-axis data. Column name (string) if using data file, or list of values.
        y: Y-axis data. Column name (string) if using data file, or list of values.
        data_input: Optional. {"file_path": "path/to/file.csv"} or {"data": {...}}
        size: Optional point sizes. Column name, list of values, or single value.
        color: Optional point colors. Column name or list of values for colormap.
        style: Optional. {"title": "...", "xlabel": "...", "ylabel": "...", "colormap": "viridis", "grid": True}
        output: Optional. {"format": "png/pdf/svg", "width": 15, "height": 10, "dpi": 300}

    Returns:
        PIL Image object or bytes containing the plot

    Examples:
        Basic scatter plot:
        >>> plot_scatter(x=[1, 2, 3], y=[1, 4, 9])

        Scatter with size and color mapping:
        >>> plot_scatter(
        ...     x="height",
        ...     y="weight",
        ...     size="age",
        ...     color="bmi",
        ...     data_input={"file_path": "health_data.csv"},
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

    # Extract data
    if df is not None:
        x_data = extract_column(df, x)
        y_data = extract_column(df, y)
        # For size and color, handle both column names and direct values
        size_data = extract_column(df, size) if size and isinstance(size, str) else size
        color_data = (
            extract_column(df, color) if color and isinstance(color, str) else color
        )
    else:
        x_data = x
        y_data = y
        size_data = size
        color_data = color

    # Create figure
    width = output.get("width", 15.0)
    height = output.get("height", 10.0)
    fig, ax = create_plot_figure(width_cm=width, height_cm=height)

    # Plot data
    scatter_kwargs = {}

    if size_data is not None:
        scatter_kwargs["s"] = size_data

    if color_data is not None:
        scatter_kwargs["c"] = color_data
        scatter_kwargs["cmap"] = get_colormap_name(style.get("colormap"))

    ax.scatter(x_data, y_data, **scatter_kwargs)

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
def plot_bar(
    x: str | list[str],
    y: str | list[float],
    data_input: dict | None = None,
    orientation: Literal["vertical", "horizontal"] = "vertical",
    style: dict | None = None,
    output: dict | None = None,
) -> Image.Image | bytes:
    """Create a bar plot for categorical data comparison.

    This tool generates vertical or horizontal bar plots, ideal for
    comparing values across different categories.

    Args:
        x: Category labels. Column name (string) if using data file, or list of strings.
        y: Values for each category. Column name or list of numbers.
        data_input: Optional. {"file_path": "path/to/file.csv"} or {"data": {...}}
        orientation: "vertical" or "horizontal" bars (default: "vertical")
        style: Optional. {"title": "...", "xlabel": "...", "ylabel": "...", "grid": True}
        output: Optional. {"format": "png/pdf/svg", "width": 15, "height": 10, "dpi": 300}

    Returns:
        PIL Image object or bytes containing the plot

    Examples:
        Vertical bar plot:
        >>> plot_bar(
        ...     x=["A", "B", "C"],
        ...     y=[10, 25, 15],
        ...     style={"title": "Category Comparison"}
        ... )

        Horizontal bar plot from file:
        >>> plot_bar(
        ...     x="product",
        ...     y="sales",
        ...     data_input={"file_path": "sales.csv"},
        ...     orientation="horizontal"
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
        x_data = extract_column(df, x)
        y_data = extract_column(df, y)
    else:
        x_data = x
        y_data = y

    # Create figure
    width = output.get("width", 15.0)
    height = output.get("height", 10.0)
    fig, ax = create_plot_figure(width_cm=width, height_cm=height)

    # Plot data
    if orientation == "horizontal":
        ax.barh(x_data, y_data)
    else:
        ax.bar(x_data, y_data)

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
