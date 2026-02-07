"""Tests for basic plotting tools."""

from pathlib import Path

from PIL import Image

from ml_research_mcp.tools.plot_basic import plot_bar, plot_line, plot_scatter


def test_plot_line_direct_data() -> None:
    """Test line plot with direct data input."""
    result = plot_line(
        x=[1, 2, 3, 4],
        y=[1, 4, 9, 16],
        style={"title": "Test Plot", "xlabel": "X", "ylabel": "Y"},
        output={"format": "png", "width": 10, "height": 8, "dpi": 100},
    )

    assert isinstance(result, Image.Image)
    assert result.format == "PNG"


def test_plot_line_from_csv(sample_csv_path: Path) -> None:
    """Test line plot with CSV file input."""
    result = plot_line(
        x="x",
        y="y",
        data_input={"file_path": str(sample_csv_path)},
        output={"format": "png", "dpi": 100},
    )

    assert isinstance(result, Image.Image)


def test_plot_line_pdf_output() -> None:
    """Test line plot with PDF output."""
    result = plot_line(
        x=[1, 2, 3],
        y=[1, 4, 9],
        output={"format": "pdf"},
    )

    assert isinstance(result, bytes)
    assert result.startswith(b"%PDF")


def test_plot_scatter_direct_data() -> None:
    """Test scatter plot with direct data."""
    result = plot_scatter(
        x=[1, 2, 3, 4],
        y=[2, 4, 6, 8],
        output={"format": "png", "dpi": 100},
    )

    assert isinstance(result, Image.Image)


def test_plot_scatter_with_size_and_color(sample_scatter_csv_path: Path) -> None:
    """Test scatter plot with size and color mapping from CSV."""
    result = plot_scatter(
        x="x",
        y="y",
        size="size",
        color="color",
        data_input={"file_path": str(sample_scatter_csv_path)},
        style={"colormap": "viridis"},
        output={"format": "png", "dpi": 100},
    )

    assert isinstance(result, Image.Image)


def test_plot_scatter_with_constant_size() -> None:
    """Test scatter plot with constant size value."""
    result = plot_scatter(
        x=[1, 2, 3],
        y=[1, 4, 9],
        size=50.0,  # Constant size
        output={"format": "png", "dpi": 100},
    )

    assert isinstance(result, Image.Image)


def test_plot_bar_vertical() -> None:
    """Test vertical bar plot."""
    result = plot_bar(
        x=["A", "B", "C", "D"],
        y=[10, 25, 15, 30],
        style={"title": "Bar Chart", "xlabel": "Category", "ylabel": "Value"},
        output={"format": "png", "dpi": 100},
    )

    assert isinstance(result, Image.Image)


def test_plot_bar_horizontal() -> None:
    """Test horizontal bar plot."""
    result = plot_bar(
        x=["Alpha", "Beta", "Gamma"],
        y=[15, 30, 20],
        orientation="horizontal",
        output={"format": "png", "dpi": 100},
    )

    assert isinstance(result, Image.Image)


def test_plot_bar_svg_output() -> None:
    """Test bar plot with SVG output."""
    result = plot_bar(
        x=["X", "Y"],
        y=[10, 20],
        output={"format": "svg"},
    )

    assert isinstance(result, bytes)
    assert b"<svg" in result
