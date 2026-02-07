"""FastMCP server for ML Research MCP.

This module initializes the FastMCP server and registers all plotting tools.
"""

from fastmcp import FastMCP

# Import tools to register them with the server
# These imports will be added as we implement each tool module
from ml_research_mcp.tools import plot_basic  # noqa: F401

# Create FastMCP server instance
mcp = FastMCP("ML Research MCP")


def main() -> None:
    """Entry point for running the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
