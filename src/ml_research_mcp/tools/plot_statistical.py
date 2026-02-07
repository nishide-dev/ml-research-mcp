"""Statistical plotting tools: histogram, box, and violin plots.

This module provides statistical visualization capabilities for
data distribution analysis and comparison.
"""

from PIL import Image

from ml_research_mcp.data.loaders import extract_column, load_data
from ml_research_mcp.plotting.core import create_plot_figure, save_plot_to_image
from ml_research_mcp.plotting.formatters import apply_style
from ml_research_mcp.server import mcp


@mcp.tool()
def plot_histogram(
    data: str | list[float],
    data_input: dict | None = None,
    bins: int = 30,
    density: bool = False,
    style: dict | None = None,
    output: dict | None = None,
) -> Image.Image | bytes:
    """Create a histogram for data distribution analysis.

    This tool generates a histogram showing the frequency distribution
    of numerical data. Useful for understanding data spread and patterns.

    Args:
        data: Data column name (string) if using data file, or list of values.
        data_input: Optional. {"file_path": "path/to/file.csv"} or {"data": {...}}
        bins: Number of histogram bins (default: 30)
        density: If True, normalize to show probability density
        style: Optional. {"title": "...", "xlabel": "...", "ylabel": "...", "grid": True}
        output: Optional. {"format": "png/pdf/svg", "width": 15, "height": 10, "dpi": 300}

    Returns:
        PIL Image object or bytes containing the plot

    Examples:
        Basic histogram:
        >>> plot_histogram(data=[1.2, 2.3, 2.5, 3.1, 3.4, 4.2, 4.5], bins=10)

        Histogram from CSV with density:
        >>> plot_histogram(
        ...     data="measurement",
        ...     data_input={"file_path": "measurements.csv"},
        ...     bins=50,
        ...     density=True,
        ...     style={"title": "Measurement Distribution"}
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
        data_values = extract_column(df, data)
    else:
        data_values = data

    # Create figure
    width = output.get("width", 15.0)
    height = output.get("height", 10.0)
    fig, ax = create_plot_figure(width_cm=width, height_cm=height)

    # Plot histogram
    ax.hist(data_values, bins=bins, density=density, alpha=0.7, edgecolor="black")

    # Apply style
    ylabel = "Density" if density else "Frequency"
    apply_style(
        ax,
        title=style.get("title"),
        xlabel=style.get("xlabel"),
        ylabel=style.get("ylabel", ylabel),
        grid=style.get("grid", True),
        colormap=style.get("colormap"),
    )

    # Save and return
    format_type = output.get("format", "png")
    dpi = output.get("dpi", 300)
    return save_plot_to_image(fig, fmt=format_type, dpi=dpi)


@mcp.tool()
def plot_box(
    data: str | list[list[float]],
    data_input: dict | None = None,
    labels: list[str] | None = None,
    style: dict | None = None,
    output: dict | None = None,
) -> Image.Image | bytes:
    """Create a box plot for comparing data distributions.

    This tool generates box plots (box-and-whisker plots) showing
    median, quartiles, and outliers for one or more datasets.

    Args:
        data: For direct input, list of lists (each sublist is a dataset).
              For file input, column name(s) separated by comma or single column.
        data_input: Optional. {"file_path": "path/to/file.csv"} or {"data": {...}}
        labels: Optional labels for each dataset
        style: Optional. {"title": "...", "xlabel": "...", "ylabel": "...", "grid": True}
        output: Optional. {"format": "png/pdf/svg", "width": 15, "height": 10, "dpi": 300}

    Returns:
        PIL Image object or bytes containing the plot

    Examples:
        Multiple datasets comparison:
        >>> plot_box(
        ...     data=[[1, 2, 3, 4, 5], [2, 3, 4, 5, 6], [3, 4, 5, 6, 7]],
        ...     labels=["Group A", "Group B", "Group C"]
        ... )

        From CSV file:
        >>> plot_box(
        ...     data="scores",
        ...     data_input={"file_path": "test_scores.csv"},
        ...     style={"title": "Test Score Distribution"}
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
        if isinstance(data, str):
            # Single column
            data_values = [extract_column(df, data).to_list()]
        else:
            # Multiple columns
            data_values = [extract_column(df, col).to_list() for col in data]
    else:
        # Direct data
        if isinstance(data[0], list):
            data_values = data
        else:
            # Single list
            data_values = [data]

    # Create figure
    width = output.get("width", 15.0)
    height = output.get("height", 10.0)
    fig, ax = create_plot_figure(width_cm=width, height_cm=height)

    # Plot box plot
    box_kwargs = {}
    if labels:
        box_kwargs["labels"] = labels

    ax.boxplot(data_values, **box_kwargs)

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
def plot_violin(
    data: str | list[list[float]],
    data_input: dict | None = None,
    labels: list[str] | None = None,
    style: dict | None = None,
    output: dict | None = None,
) -> Image.Image | bytes:
    """Create a violin plot for detailed distribution comparison.

    This tool generates violin plots, which combine box plots with
    kernel density estimation to show the full distribution shape.

    Args:
        data: For direct input, list of lists (each sublist is a dataset).
              For file input, column name(s) or single column.
        data_input: Optional. {"file_path": "path/to/file.csv"} or {"data": {...}}
        labels: Optional labels for each dataset
        style: Optional. {"title": "...", "xlabel": "...", "ylabel": "...", "grid": True}
        output: Optional. {"format": "png/pdf/svg", "width": 15, "height": 10, "dpi": 300}

    Returns:
        PIL Image object or bytes containing the plot

    Examples:
        Comparing distributions:
        >>> plot_violin(
        ...     data=[[1, 2, 2, 3, 3, 3, 4], [2, 3, 4, 4, 5, 5, 6]],
        ...     labels=["Control", "Treatment"]
        ... )

        From file:
        >>> plot_violin(
        ...     data="reaction_time",
        ...     data_input={"file_path": "experiment.csv"},
        ...     style={"title": "Reaction Time Distribution"}
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
        if isinstance(data, str):
            # Single column
            data_values = [extract_column(df, data).to_list()]
        else:
            # Multiple columns
            data_values = [extract_column(df, col).to_list() for col in data]
    else:
        # Direct data
        if isinstance(data[0], list):
            data_values = data
        else:
            # Single list
            data_values = [data]

    # Create figure
    width = output.get("width", 15.0)
    height = output.get("height", 10.0)
    fig, ax = create_plot_figure(width_cm=width, height_cm=height)

    # Create positions for violin plots
    positions = list(range(1, len(data_values) + 1))

    # Plot violin plot
    parts = ax.violinplot(data_values, positions=positions, showmeans=True, showmedians=True)

    # Apply labels if provided
    if labels:
        ax.set_xticks(positions)
        ax.set_xticklabels(labels)

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
