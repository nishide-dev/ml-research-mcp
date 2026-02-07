# ml-research-mcp

A MCP Server for ML Research and Development.

## Features

- ⚡ **Fast package management** with [uv](https://github.com/astral-sh/uv)
- 📦 **Modern Python packaging** using `pyproject.toml` (PEP 621)
- 🏗️ **Src layout** for better import hygiene
- 🔍 **Code quality** with Ruff (linter + formatter)
- 🔒 **Type safety** with ty
- ✅ **Testing** with Pytest
- 🚀 **CI/CD** with GitHub Actions

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

## Installation

### For end users

```bash
# Using uv (recommended)
uv pip install ml-research-mcp

# Using pip
pip install ml-research-mcp
```

### For developers

```bash
# Clone the repository
git clone https://github.com/nishide-dev/ml-research-mcp.git
cd ml-research-mcp

# Create virtual environment and install dependencies
uv venv
uv sync

# Activate the virtual environment
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows
```

## Usage

```python
from ml_research_mcp import hello

print(hello())
# Output: Hello from ml-research-mcp!
```

## Development

### Running tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=html
```

### Code formatting and linting

```bash
# Format code
uv run ruff format .

# Lint code
uv run ruff check .

# Fix auto-fixable issues
uv run ruff check --fix .
```

### Type checking

```bash
uv run ty check
```

### Adding dependencies

```bash
# Add a runtime dependency
uv add <package-name>

# Add a development dependency
uv add --dev <package-name>

# Update all dependencies
uv lock --upgrade
```

## Project Structure

```
ml-research-mcp/
├── src/
│   └── ml_research_mcp/
│       ├── __init__.py
│       └── py.typed          # Type information marker
├── tests/
│   ├── __init__.py
│   └── test_ml_research_mcp.py
├── pyproject.toml            # Project configuration
├── uv.lock                   # Dependency lock file
├── .gitignore
├── .python-version           # Python version specification
├── LICENSE
├── README.md                 # This file
└── .github/
    └── workflows/
        └── test.yml          # CI/CD configuration
```

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

Generated with ❤️ using [uv-nix-template](https://github.com/nishide-dev/uv-nix-template)
