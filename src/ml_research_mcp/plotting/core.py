"""Core plotting functions using UltraPlot/Matplotlib.

This module provides the foundation for creating and saving plots
with proper configuration and format support.
"""

import io

import matplotlib as mpl
import matplotlib.figure
import matplotlib.pyplot as plt
import ultraplot as uplt
from PIL import Image

# Use non-interactive backend for server environments
mpl.use("Agg")


def create_plot_figure(
    width_cm: float = 15.0,
    height_cm: float = 10.0,
) -> tuple[uplt.Figure, uplt.Axes | uplt.SubplotGrid]:
    """Create an UltraPlot figure with specified dimensions in centimeters.

    UltraPlot provides a high-level interface to Matplotlib with
    better defaults for publication-quality plots.

    Args:
        width_cm: Figure width in centimeters (default: 15.0)
        height_cm: Figure height in centimeters (default: 10.0)

    Returns:
        Tuple of (figure, axes) objects from UltraPlot

    Examples:
        >>> fig, ax = create_plot_figure(width_cm=20, height_cm=15)
        >>> ax.plot([1, 2, 3], [1, 4, 9])
        >>> save_plot_to_image(fig, format="png", dpi=300)
    """
    # UltraPlot uses physical units (cm) directly
    # This is much more intuitive than matplotlib's figsize in inches
    fig, ax = uplt.subplots(figwidth=f"{width_cm}cm", figheight=f"{height_cm}cm")

    return fig, ax


def save_plot_to_image(
    fig: matplotlib.figure.Figure,
    fmt: str = "png",
    dpi: int = 300,
) -> Image.Image | bytes:
    """Save matplotlib/ultraplot figure to PIL Image or bytes.

    Args:
        fig: Matplotlib or UltraPlot figure object
        fmt: Output format ("png", "pdf", or "svg")
        dpi: Resolution for raster formats (only affects PNG)

    Returns:
        PIL Image object for PNG, or bytes for PDF/SVG

    Raises:
        ValueError: If format is not supported

    Examples:
        Save as PNG (returns PIL Image):
        >>> img = save_plot_to_image(fig, fmt="png", dpi=300)

        Save as PDF (returns bytes):
        >>> pdf_bytes = save_plot_to_image(fig, fmt="pdf")
    """
    supported_formats = ["png", "pdf", "svg"]
    if fmt.lower() not in supported_formats:
        msg = f"Unsupported format: {fmt}. Supported formats: {', '.join(supported_formats)}"
        raise ValueError(msg)

    # Create in-memory buffer
    buffer = io.BytesIO()

    try:
        # Save figure to buffer with tight bounding box
        # bbox_inches='tight' removes extra whitespace
        fig.savefig(
            buffer,
            format=fmt.lower(),
            dpi=dpi,
            bbox_inches="tight",
        )

        # Reset buffer position to beginning
        buffer.seek(0)

        # For PNG, convert to PIL Image
        if fmt.lower() == "png":
            image = Image.open(buffer)
            # Make a copy to avoid issues with buffer closure
            # Need to preserve format attribute
            img_copy = image.copy()
            img_copy.format = "PNG"
            return img_copy

        # For PDF/SVG, return bytes directly
        return buffer.getvalue()

    finally:
        # Clean up: close the figure to free memory
        plt.close(fig)
        # Buffer will be garbage collected


def close_all_figures() -> None:
    """Close all matplotlib figures to free memory.

    This should be called after generating multiple plots
    to prevent memory leaks.

    Examples:
        >>> fig1, ax1 = create_plot_figure()
        >>> fig2, ax2 = create_plot_figure()
        >>> # ... do plotting ...
        >>> close_all_figures()
    """
    plt.close("all")
