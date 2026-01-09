# Contributing to 4D-ARE

Thank you for your interest in contributing to 4D-ARE! This document provides guidelines for contributing.

## Development Setup

### Prerequisites

- Python 3.10+
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/anthropics/4D-ARE.git
cd 4D-ARE

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=four_d_are

# Run specific test file
pytest tests/test_agent.py
```

### Code Quality

We use the following tools:

- **ruff**: Linting and formatting
- **mypy**: Type checking
- **pre-commit**: Git hooks

```bash
# Format code
ruff format .

# Lint code
ruff check .

# Type check
mypy src/four_d_are
```

## How to Contribute

### Reporting Issues

1. Check if the issue already exists
2. Use the issue templates
3. Include:
   - Python version
   - 4D-ARE version
   - Steps to reproduce
   - Expected vs actual behavior

### Submitting Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Update documentation if needed
7. Submit a pull request

### PR Guidelines

- Keep PRs focused and small
- Write clear commit messages
- Follow existing code style
- Add tests for new features
- Update CHANGELOG.md

## Code Style

### Python

- Follow PEP 8
- Use type hints
- Write docstrings for public APIs
- Maximum line length: 100 characters

### Documentation

- Use clear, concise language
- Include code examples
- Keep README.md updated

## Project Structure

```
4D-ARE/
├── src/four_d_are/     # Main package
│   ├── agent.py        # Attribution Agent
│   ├── config.py       # Configuration
│   ├── prompts.py      # Prompt templates
│   └── schemas.py      # Data models
├── mcp_servers/        # MCP data connectors
├── examples/           # Usage examples
├── tests/              # Test suite
└── docs/               # Documentation
```

## Adding New Features

### New Domain Template

1. Add template to `prompts.py`
2. Add example to `examples/custom_domain.py`
3. Update `docs/customization.md`

### New MCP Server

1. Create directory under `mcp_servers/`
2. Implement the standard interface
3. Add configuration to `.env.example`
4. Update `docs/mcp-integration.md`

## Questions?

- Open an issue for bugs or feature requests
- Start a discussion for questions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
