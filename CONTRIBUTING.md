# Contributing to Metaphysical Scene Weaver

Thank you for your interest in contributing to the Metaphysical Scene Weaver project! This guide will help you get started.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Project Structure](#project-structure)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)

## Code of Conduct

We are committed to providing a welcoming and inspiring community for all. Please read and follow our Code of Conduct:

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/metaphysical-scene-weaver.git
   cd metaphysical-scene-weaver
   ```

2. **Set up your development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   pre-commit install
   ```

3. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

### 1. Before You Start

- Check existing issues and PRs to avoid duplicate work
- For major changes, open an issue first to discuss the approach
- Ensure your fork is up to date with the main repository

### 2. Making Changes

- Write clear, self-documenting code
- Follow the existing code style and patterns
- Add tests for new functionality
- Update documentation as needed

### 3. Commit Guidelines

We follow conventional commit messages:

```
type(scope): subject

body (optional)

footer (optional)
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Example:
```
feat(parser): add support for emotional intensity metadata

Added a new field to track emotional intensity in scene transitions.
This allows for more nuanced emotional mapping in the output.

Closes #123
```

## Project Structure

```
metaphysical-scene-weaver/
├── src/
│   ├── core/           # Core processing engines
│   ├── processors/     # Specialized processors
│   ├── api/           # REST API & WebSocket
│   └── integrations/  # External services
├── tests/             # Test suite
│   ├── unit/         # Unit tests
│   ├── integration/  # Integration tests
│   └── e2e/         # End-to-end tests
├── docs/            # Documentation
└── examples/        # Example scripts and usage
```

## Coding Standards

### Python Style Guide

- Follow PEP 8
- Use type hints for function parameters and return values
- Maximum line length: 88 characters (Black default)
- Use descriptive variable and function names

### Code Quality Tools

Run these before submitting:

```bash
# Format code
black src/ tests/

# Lint code
ruff check src/ tests/

# Type checking
mypy src/

# Run all tests
pytest
```

### Example Code Style

```python
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class ScenePrompt:
    """Represents a visual prompt for a scene."""
    
    id: str
    content: str
    tokens: int
    quality_score: float
    
    def validate(self) -> bool:
        """Validate the prompt meets quality standards."""
        return (
            self.tokens <= 150 and
            self.quality_score >= 0.7 and
            len(self.content) > 0
        )
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_script_parser.py

# Run tests in parallel
pytest -n auto
```

### Writing Tests

- Place unit tests in `tests/unit/`
- Place integration tests in `tests/integration/`
- Use descriptive test names that explain what is being tested
- Follow the Arrange-Act-Assert pattern

Example test:
```python
def test_philosophical_interpreter_extracts_concepts():
    # Arrange
    interpreter = PhilosophicalInterpreter()
    text = "The nature of consciousness is inherently dualistic."
    
    # Act
    concepts = interpreter.extract_concepts(text)
    
    # Assert
    assert "dualism" in concepts
    assert "consciousness" in concepts
    assert len(concepts) >= 2
```

## Documentation

### Docstring Format

Use Google-style docstrings:

```python
def process_script(self, script_path: str, narrator_voice: str = "philosophical") -> SceneResult:
    """Process a philosophical script into visual prompts.
    
    Args:
        script_path: Path to the script file
        narrator_voice: Voice style for narration
        
    Returns:
        SceneResult object containing all generated prompts
        
    Raises:
        FileNotFoundError: If script file doesn't exist
        ValidationError: If script format is invalid
    """
```

### Updating Documentation

- Update README.md for major features
- Add docstrings to all public functions and classes
- Update API documentation for endpoint changes
- Include examples for complex features

## Submitting Changes

### Pull Request Process

1. **Ensure all tests pass**
   ```bash
   pytest
   black --check src/ tests/
   ruff check src/ tests/
   mypy src/
   ```

2. **Update documentation**
   - Add/update docstrings
   - Update README if needed
   - Add to CHANGELOG.md

3. **Create Pull Request**
   - Use a clear, descriptive title
   - Reference any related issues
   - Describe what changes were made and why
   - Include screenshots for UI changes

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
```

### Review Process

- PRs require at least one review
- Address all review comments
- Keep PRs focused and reasonably sized
- Be responsive to feedback

## Questions?

Feel free to:
- Open an issue for questions
- Join our discussions
- Reach out to maintainers

Thank you for contributing to Metaphysical Scene Weaver! 🎭✨