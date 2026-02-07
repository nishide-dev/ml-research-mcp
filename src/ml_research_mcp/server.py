"""FastMCP server for ML Research MCP.

This module initializes the FastMCP server and registers all plotting tools.
"""

from fastmcp import FastMCP

# Create FastMCP server instance
mcp = FastMCP("ML Research MCP")


def main() -> None:
    """Entry point for running the MCP server."""
    # Import tools here to avoid circular imports
    # Tools register themselves via @mcp.tool() decorator when imported
    # ruff: noqa: PLC0415
    from ml_research_mcp.tools import (
        plot_2d,  # noqa: F401
        plot_basic,  # noqa: F401
        plot_statistical,  # noqa: F401
    )

    mcp.run()


if __name__ == "__main__":
    main()
