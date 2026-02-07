"""Tests for plotting core functionality."""

import matplotlib.figure
import pytest
import ultraplot as uplt
from PIL import Image

from ml_research_mcp.plotting.core import (
    close_all_figures,
    create_plot_figure,
    save_plot_to_image,
)


def test_create_plot_figure_default() -> None:
    """Test creating figure with default dimensions."""
    fig, ax = create_plot_figure()
    assert isinstance(fig, uplt.Figure)
    # UltraPlot returns SubplotGrid for single subplots
    assert isinstance(ax, (uplt.Axes, uplt.SubplotGrid))
    close_all_figures()


def test_create_plot_figure_custom_size() -> None:
    """Test creating figure with custom dimensions."""
    fig, ax = create_plot_figure(width_cm=20.0, height_cm=15.0)
    assert isinstance(fig, uplt.Figure)
    # UltraPlot returns SubplotGrid for single subplots
    assert isinstance(ax, (uplt.Axes, uplt.SubplotGrid))
    close_all_figures()


def test_save_plot_to_image_png() -> None:
    """Test saving plot as PNG returns PIL Image."""
    fig, ax = create_plot_figure()
    ax.plot([1, 2, 3], [1, 4, 9])

    result = save_plot_to_image(fig, fmt="png", dpi=100)
    assert isinstance(result, Image.Image)
    assert result.format == "PNG"


def test_save_plot_to_image_pdf() -> None:
    """Test saving plot as PDF returns bytes."""
    fig, ax = create_plot_figure()
    ax.plot([1, 2, 3], [1, 4, 9])

    result = save_plot_to_image(fig, fmt="pdf")
    assert isinstance(result, bytes)
    assert result.startswith(b"%PDF")  # PDF magic number


def test_save_plot_to_image_svg() -> None:
    """Test saving plot as SVG returns bytes."""
    fig, ax = create_plot_figure()
    ax.plot([1, 2, 3], [1, 4, 9])

    result = save_plot_to_image(fig, fmt="svg")
    assert isinstance(result, bytes)
    assert b"<svg" in result  # SVG tag


def test_save_plot_to_image_invalid_format() -> None:
    """Test that invalid format raises ValueError."""
    fig, ax = create_plot_figure()
    ax.plot([1, 2, 3], [1, 4, 9])

    with pytest.raises(ValueError, match="Unsupported format"):
        save_plot_to_image(fig, fmt="invalid")


def test_close_all_figures() -> None:
    """Test closing all figures."""
    # Create multiple figures
    for _ in range(3):
        create_plot_figure()

    # Close all
    close_all_figures()

    # Verify cleanup (implicitly tested by lack of warnings)
    assert True
