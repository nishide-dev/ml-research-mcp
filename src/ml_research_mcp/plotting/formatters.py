"""Plot styling and formatting utilities.

This module provides functions to apply consistent styling
to plots using UltraPlot's format() method.
"""

import ultraplot as uplt


def apply_style(
    ax: uplt.Axes,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    grid: bool = True,
    colormap: str | None = None,  # noqa: ARG001 - reserved for future use
) -> None:
    """Apply style configuration to an UltraPlot axes object.

    This function uses UltraPlot's powerful format() method to
    configure multiple aspects of the plot in a single call.

    Args:
        ax: UltraPlot axes object to style
        title: Plot title
        xlabel: X-axis label
        ylabel: Y-axis label
        grid: Whether to show grid lines (default: True)
        colormap: Colormap name (reserved for future use)

    Examples:
        >>> fig, ax = uplt.subplots()
        >>> ax.plot([1, 2, 3], [1, 4, 9])
        >>> apply_style(ax, title="Quadratic Function", xlabel="X", ylabel="Y")
    """
    # Build format kwargs dynamically
    format_kwargs = {}

    if title is not None:
        format_kwargs["title"] = title

    if xlabel is not None:
        format_kwargs["xlabel"] = xlabel

    if ylabel is not None:
        format_kwargs["ylabel"] = ylabel

    # Grid is applied regardless (with default True)
    format_kwargs["grid"] = grid

    # Apply formatting in a single call
    # This is UltraPlot's signature feature: one method to configure everything
    ax.format(**format_kwargs)

    # Note: colormap is not applied here as it's typically set per-plot
    # It's passed through to individual plotting functions


def get_colormap_name(colormap: str | None = None) -> str:
    """Get colormap name with fallback to UltraPlot default.

    Args:
        colormap: User-specified colormap name, or None

    Returns:
        Colormap name to use

    Examples:
        >>> get_colormap_name("viridis")
        'viridis'
        >>> get_colormap_name(None)
        'viridis'  # UltraPlot default
    """
    # If user specifies colormap, use it
    if colormap:
        return colormap

    # Otherwise, use UltraPlot's default perceptually uniform colormap
    # UltraPlot defaults to 'viridis' which is perceptually uniform
    return "viridis"
