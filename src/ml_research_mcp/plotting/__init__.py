"""Plotting module for ML Research MCP.

This module provides core plotting functionality using UltraPlot/Matplotlib
and output formatting capabilities.
"""

from ml_research_mcp.plotting.core import create_plot_figure, save_plot_to_image
from ml_research_mcp.plotting.formatters import apply_style

__all__ = ["apply_style", "create_plot_figure", "save_plot_to_image"]
