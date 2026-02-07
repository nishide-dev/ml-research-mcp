"""Tests for 2D plotting tools."""

from PIL import Image

from ml_research_mcp.tools.plot_2d import plot_contour, plot_heatmap, plot_pcolormesh


def test_plot_heatmap_direct_data() -> None:
    """Test heatmap with direct data input."""
    result = plot_heatmap(
        data=[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        x_labels=["A", "B", "C"],
        y_labels=["X", "Y", "Z"],
        style={"title": "Heatmap", "colormap": "viridis"},
        output={"format": "png", "dpi": 100},
    )

    assert isinstance(result, Image.Image)


def test_plot_heatmap_with_annotation() -> None:
    """Test heatmap with value annotations."""
    result = plot_heatmap(
        data=[[1.0, 0.8, 0.3], [0.8, 1.0, 0.5], [0.3, 0.5, 1.0]],
        annotate=True,
        style={"title": "Correlation Matrix", "colormap": "RdBu"},
        output={"format": "png", "dpi": 100},
    )

    assert isinstance(result, Image.Image)


def test_plot_heatmap_pdf_output() -> None:
    """Test heatmap with PDF output."""
    result = plot_heatmap(
        data=[[1, 2], [3, 4]],
        output={"format": "pdf"},
    )

    assert isinstance(result, bytes)
    assert result.startswith(b"%PDF")


def test_plot_contour_filled() -> None:
    """Test filled contour plot."""
    x = [1, 2, 3, 4, 5]
    y = [1, 2, 3, 4, 5]
    z = [[i + j for j in range(5)] for i in range(5)]

    result = plot_contour(
        x=x,
        y=y,
        z=z,
        levels=10,
        filled=True,
        style={"title": "Contour Plot", "colormap": "plasma"},
        output={"format": "png", "dpi": 100},
    )

    assert isinstance(result, Image.Image)


def test_plot_contour_lines_only() -> None:
    """Test contour plot with lines only."""
    x = [1, 2, 3, 4]
    y = [1, 2, 3, 4]
    z = [[i * j for j in range(4)] for i in range(4)]

    result = plot_contour(
        x=x,
        y=y,
        z=z,
        levels=8,
        filled=False,
        output={"format": "png", "dpi": 100},
    )

    assert isinstance(result, Image.Image)


def test_plot_contour_svg_output() -> None:
    """Test contour plot with SVG output."""
    x = [1, 2, 3]
    y = [1, 2, 3]
    z = [[1, 2, 3], [2, 4, 6], [3, 6, 9]]

    result = plot_contour(
        x=x,
        y=y,
        z=z,
        levels=5,
        output={"format": "svg"},
    )

    assert isinstance(result, bytes)
    assert b"<svg" in result


def test_plot_pcolormesh_auto_shading() -> None:
    """Test pcolormesh with auto shading."""
    x = [1, 2, 3, 4]
    y = [1, 2, 3, 4]
    z = [[1, 2, 3, 4], [2, 4, 6, 8], [3, 6, 9, 12], [4, 8, 12, 16]]

    result = plot_pcolormesh(
        x=x,
        y=y,
        z=z,
        shading="auto",
        style={"title": "Pcolormesh", "colormap": "viridis"},
        output={"format": "png", "dpi": 100},
    )

    assert isinstance(result, Image.Image)


def test_plot_pcolormesh_gouraud_shading() -> None:
    """Test pcolormesh with gouraud shading."""
    x = [1, 2, 3]
    y = [1, 2, 3]
    z = [[1, 2, 3], [2, 4, 6], [3, 6, 9]]

    result = plot_pcolormesh(
        x=x,
        y=y,
        z=z,
        shading="gouraud",
        output={"format": "png", "dpi": 100},
    )

    assert isinstance(result, Image.Image)


def test_plot_pcolormesh_pdf_output() -> None:
    """Test pcolormesh with PDF output."""
    x = [1, 2]
    y = [1, 2]
    z = [[1, 2], [2, 4]]

    result = plot_pcolormesh(
        x=x,
        y=y,
        z=z,
        output={"format": "pdf"},
    )

    assert isinstance(result, bytes)
    assert result.startswith(b"%PDF")
