"""Tests for statistical plotting tools."""

from PIL import Image

from ml_research_mcp.tools.plot_statistical import plot_box, plot_histogram, plot_violin


def test_plot_histogram_direct_data() -> None:
    """Test histogram with direct data input."""
    result = plot_histogram(
        data=[1.2, 2.3, 2.5, 3.1, 3.4, 4.2, 4.5, 5.0, 5.5, 6.0],
        bins=5,
        style={"title": "Distribution", "xlabel": "Value"},
        output={"format": "png", "dpi": 100},
    )

    assert isinstance(result, Image.Image)


def test_plot_histogram_with_density() -> None:
    """Test histogram with density normalization."""
    result = plot_histogram(
        data=[1, 2, 2, 3, 3, 3, 4, 4, 5],
        bins=5,
        density=True,
        output={"format": "png", "dpi": 100},
    )

    assert isinstance(result, Image.Image)


def test_plot_histogram_pdf_output() -> None:
    """Test histogram with PDF output."""
    result = plot_histogram(
        data=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        bins=10,
        output={"format": "pdf"},
    )

    assert isinstance(result, bytes)
    assert result.startswith(b"%PDF")


def test_plot_box_single_dataset() -> None:
    """Test box plot with single dataset."""
    result = plot_box(
        data=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        style={"title": "Box Plot", "ylabel": "Value"},
        output={"format": "png", "dpi": 100},
    )

    assert isinstance(result, Image.Image)


def test_plot_box_multiple_datasets() -> None:
    """Test box plot with multiple datasets."""
    result = plot_box(
        data=[[1, 2, 3, 4, 5], [2, 3, 4, 5, 6], [3, 4, 5, 6, 7]],
        labels=["Group A", "Group B", "Group C"],
        style={"title": "Comparison"},
        output={"format": "png", "dpi": 100},
    )

    assert isinstance(result, Image.Image)


def test_plot_box_svg_output() -> None:
    """Test box plot with SVG output."""
    result = plot_box(
        data=[[1, 2, 3], [2, 3, 4]],
        labels=["A", "B"],
        output={"format": "svg"},
    )

    assert isinstance(result, bytes)
    assert b"<svg" in result


def test_plot_violin_single_dataset() -> None:
    """Test violin plot with single dataset."""
    result = plot_violin(
        data=[1, 2, 2, 3, 3, 3, 4, 4, 5],
        style={"title": "Violin Plot"},
        output={"format": "png", "dpi": 100},
    )

    assert isinstance(result, Image.Image)


def test_plot_violin_multiple_datasets() -> None:
    """Test violin plot with multiple datasets."""
    result = plot_violin(
        data=[[1, 2, 2, 3, 3, 3, 4], [2, 3, 4, 4, 5, 5, 6]],
        labels=["Control", "Treatment"],
        style={"title": "Comparison", "ylabel": "Value"},
        output={"format": "png", "dpi": 100},
    )

    assert isinstance(result, Image.Image)


def test_plot_violin_pdf_output() -> None:
    """Test violin plot with PDF output."""
    result = plot_violin(
        data=[[1, 2, 3, 4, 5], [2, 3, 4, 5, 6]],
        output={"format": "pdf"},
    )

    assert isinstance(result, bytes)
    assert result.startswith(b"%PDF")
