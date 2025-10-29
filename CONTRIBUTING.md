# Contributing to Poke MCP Production

Thank you for considering contributing to Poke MCP Production! This document provides guidelines and instructions for contributing.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [Making Changes](#making-changes)
5. [Testing](#testing)
6. [Submitting Changes](#submitting-changes)
7. [Coding Standards](#coding-standards)
8. [Documentation](#documentation)

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to:

- Be respectful and inclusive
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

### Ways to Contribute

- **Bug Reports**: Report bugs via GitHub Issues
- **Feature Requests**: Suggest new features or improvements
- **Code Contributions**: Submit pull requests
- **Documentation**: Improve or add documentation
- **Testing**: Help test new features or bug fixes
- **Community**: Help others in discussions and issues

### Before You Start

1. **Check existing issues**: Avoid duplicates
2. **Discuss major changes**: Open an issue first for discussion
3. **Read documentation**: Familiarize yourself with the project

## Development Setup

1. **Fork the repository**

   Click the "Fork" button on GitHub

2. **Clone your fork**

   ```bash
   git clone https://github.com/YOUR_USERNAME/poke-mcp-production.git
   cd poke-mcp-production
   ```

3. **Add upstream remote**

   ```bash
   git remote add upstream https://github.com/patrickcarmichael/poke-mcp-production.git
   ```

4. **Install dependencies**

   ```bash
   # Using uv (recommended)
   uv sync --extra dev

   # Or using pip
   pip install -r requirements.txt
   pip install pytest pytest-asyncio pytest-cov black ruff mypy
   ```

5. **Set up environment**

   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

6. **Run tests**

   ```bash
   pytest
   ```

## Making Changes

### Branch Naming

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation changes
- `refactor/description` - Code refactoring
- `test/description` - Test additions or changes

### Creating a Branch

```bash
# Update main branch
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/my-new-feature
```

### Making Commits

**Commit Message Format**:

```
type(scope): subject

body (optional)

footer (optional)
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples**:

```bash
git commit -m "feat(auth): add OAuth support"
git commit -m "fix(api): handle timeout errors correctly"
git commit -m "docs(readme): update installation instructions"
```

### Code Quality

Before committing, ensure your code passes:

```bash
# Format code
black .

# Lint
ruff check .

# Type check
mypy src/

# Run tests
pytest
```

## Testing

### Writing Tests

Place tests in the `tests/` directory:

```python
# tests/test_pokemon.py
import pytest
from src.pokeapi_client import fetch_pokemon_full_data

@pytest.mark.asyncio
async def test_fetch_pokemon():
    # Test implementation
    pass
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_pokemon.py

# Run specific test
pytest tests/test_pokemon.py::test_fetch_pokemon
```

### Test Coverage

Aim for:
- New features: 80%+ coverage
- Bug fixes: Test for the specific bug
- Critical paths: 100% coverage

## Submitting Changes

### Pull Request Process

1. **Update your branch**

   ```bash
   git checkout main
   git pull upstream main
   git checkout feature/my-new-feature
   git rebase main
   ```

2. **Push to your fork**

   ```bash
   git push origin feature/my-new-feature
   ```

3. **Create Pull Request**

   - Go to GitHub and click "New Pull Request"
   - Select your fork and branch
   - Fill in the PR template

### Pull Request Template

```markdown
## Description
[Describe your changes]

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added (if applicable)
- [ ] Manually tested

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings generated
```

### Review Process

1. Maintainer reviews your PR
2. Address any feedback
3. Push updates to your branch
4. Once approved, maintainer will merge

## Coding Standards

### Python Style

- Follow [PEP 8](https://pep8.org/)
- Use [Black](https://black.readthedocs.io/) for formatting
- Line length: 100 characters
- Use type hints

### Code Structure

```python
"""Module docstring."""
import standard_library
import third_party

from src import local_modules

# Constants
CONSTANT_NAME = "value"


class MyClass:
    """Class docstring."""

    def __init__(self, param: str) -> None:
        """Initialize."""
        self.param = param

    def method(self, arg: int) -> str:
        """Method docstring.
        
        Args:
            arg: Description.
            
        Returns:
            Description.
        """
        return str(arg)
```

### Documentation

- Use docstrings for all public functions/classes
- Follow [Google Style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- Include examples for complex functions
- Update README.md for user-facing changes

### Error Handling

```python
from src.logger import get_logger

logger = get_logger(__name__)

try:
    # Operation
    result = risky_operation()
except SpecificError as e:
    logger.error("operation_failed", error=str(e))
    # Handle error appropriately
    raise
```

### Logging

```python
from src.logger import get_logger

logger = get_logger(__name__)

# Info logging
logger.info("action_performed", user=user_id, result=result)

# Error logging
logger.error("operation_failed", error=str(e), context={"key": "value"})
```

## Documentation

### Types of Documentation

1. **Code Documentation**: Docstrings, comments
2. **User Documentation**: README.md, guides
3. **API Documentation**: Endpoint descriptions
4. **Developer Documentation**: CONTRIBUTING.md, architecture docs

### Updating Documentation

- Update README.md for user-facing changes
- Update docstrings for code changes
- Add examples for new features
- Update DEPLOYMENT.md for deployment changes
- Update SSH_TUNNELING.md for access changes

## Community

### Getting Help

- **Questions**: Open a GitHub Discussion
- **Bugs**: Open a GitHub Issue
- **Chat**: Join our community (if available)

### Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md (to be created)
- Mentioned in release notes
- Credited in commits

## Release Process

### Versioning

We follow [Semantic Versioning](https://semver.org/):

- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

### Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG updated
- [ ] Version bumped
- [ ] Tagged release
- [ ] Deployed to production

## Questions?

Don't hesitate to ask questions:

- Open a GitHub Discussion
- Comment on an existing issue
- Reach out to maintainers

Thank you for contributing! 🚀
