"""Tests for ml_research_mcp."""

from ml_research_mcp import hello


def test_hello() -> None:
    """Test the hello function."""
    result = hello()
    assert isinstance(result, str)
    assert "ml-research-mcp" in result
    assert result == "Hello from ml-research-mcp!"


def test_hello_return_type() -> None:
    """Test that hello returns a string."""
    result = hello()
    assert isinstance(result, str)


class TestHello:
    """Test class for hello function."""

    def test_hello_not_empty(self) -> None:
        """Test that hello returns a non-empty string."""
        result = hello()
        assert len(result) > 0

    def test_hello_contains_project_name(self) -> None:
        """Test that hello contains the project name."""
        result = hello()
        assert "ml-research-mcp" in result
