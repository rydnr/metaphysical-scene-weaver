# Code Review Standards & Quality Guidelines

## Overview

This document establishes code review standards and quality guidelines for the Metaphysical Scene Weaver project. All team members are expected to follow these standards to ensure code quality, maintainability, and consistency.

## Code Review Process

### 1. Pre-Review Checklist

Before submitting code for review, ensure:

- [ ] All tests pass locally (`pytest tests/`)
- [ ] Code is formatted with Black (`black src/`)
- [ ] Linting passes (`ruff check src/`)
- [ ] Type checking passes (`mypy src/`)
- [ ] Documentation is updated
- [ ] Commit messages follow conventional format

### 2. Review Workflow

```
Feature Branch → Pull Request → Automated Checks → Peer Review → Approval → Merge
```

1. **Create Feature Branch**: `feature/MSW-XXX-description`
2. **Open Pull Request**: Use PR template
3. **Automated Checks**: CI/CD runs tests, linting, type checking
4. **Peer Review**: At least one team member reviews
5. **Address Feedback**: Make requested changes
6. **Approval & Merge**: Squash and merge to main

### 3. Review Responsibilities by Role

**Aria (Architect)**
- Architecture compliance
- Integration design
- Performance implications
- Cross-component dependencies

**Sophia (Philosophy/NLP)**
- Philosophical concept accuracy
- NLP algorithm correctness
- Semantic analysis quality

**Luna (Emotion/Visual)**
- Emotion mapping logic
- Visual consistency
- Character state management

**Rex (Script Processing)**
- Parsing accuracy
- Data structure efficiency
- Performance optimization

**Nova (Integration/API)**
- API design standards
- WebSocket implementation
- External integration quality

**Iris (Prompt Engineering)**
- Prompt quality and effectiveness
- Output validation
- Style consistency

**Quinn (QA)**
- Test coverage
- Edge case handling
- Quality metrics

## Code Quality Standards

### 1. Python Style Guide

Follow PEP 8 with these specific guidelines:

**Imports**
```python
# Standard library
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

# Third-party
import numpy as np
from pydantic import BaseModel

# Local application
from ..core.scene_weaver import SceneWeaver
from ..processors.philosophical_interpreter import PhilosophicalInterpreter
```

**Type Hints**
```python
def process_entry(
    self,
    entry: ScriptEntry,
    context: Dict[str, Any],
    options: Optional[ProcessingOptions] = None
) -> EnrichedScene:
    """Process a script entry with full type annotations."""
    pass
```

**Docstrings**
```python
def analyze_philosophy(self, text: str) -> PhilosophicalConcept:
    """
    Analyze philosophical concepts in dialogue text.
    
    Args:
        text: The dialogue text to analyze
        
    Returns:
        PhilosophicalConcept with identified themes and confidence scores
        
    Raises:
        AnalysisError: If text cannot be processed
    """
    pass
```

### 2. Component-Specific Standards

**Processors**
- Single responsibility principle
- Clear input/output contracts
- Comprehensive error handling
- Performance metrics logging

**API Endpoints**
- RESTful design principles
- Comprehensive OpenAPI documentation
- Request/response validation
- Proper HTTP status codes

**Tests**
- Minimum 80% code coverage
- Unit tests for all public methods
- Integration tests for workflows
- Performance benchmarks for critical paths

### 3. Documentation Requirements

**Code Documentation**
- All public functions must have docstrings
- Complex algorithms need inline comments
- Type hints for all function signatures
- README for each major component

**API Documentation**
- OpenAPI/Swagger specs
- Example requests/responses
- Error code documentation
- Rate limiting information

### 4. Performance Standards

**Response Times**
- Script parsing: <100ms per entry
- Philosophy analysis: <500ms per scene
- Prompt generation: <200ms per scene
- API endpoints: <100ms (excluding processing)

**Resource Usage**
- Memory: <50MB per script entry
- CPU: Efficient multiprocessing
- I/O: Async operations where applicable

## Review Criteria

### 1. Code Quality Checklist

**Functionality**
- [ ] Code performs intended function
- [ ] Edge cases are handled
- [ ] Error handling is comprehensive
- [ ] No regression in existing features

**Design**
- [ ] Follows established patterns
- [ ] Maintains single responsibility
- [ ] Properly abstracted
- [ ] Extensible for future needs

**Performance**
- [ ] No unnecessary loops
- [ ] Efficient data structures
- [ ] Proper caching where applicable
- [ ] Async operations for I/O

**Security**
- [ ] Input validation
- [ ] No hardcoded secrets
- [ ] Proper error messages (no sensitive data)
- [ ] Rate limiting where applicable

**Testing**
- [ ] Unit tests for new code
- [ ] Integration tests updated
- [ ] Edge cases tested
- [ ] Performance benchmarks if applicable

### 2. Philosophy-Specific Review

For philosophical interpretation components:

- [ ] Concept mappings are accurate
- [ ] Visual symbols align with philosophical themes
- [ ] Depth levels properly categorized
- [ ] Cultural sensitivity maintained

### 3. Visual Mapping Review

For emotion and visual components:

- [ ] Color mappings are psychologically sound
- [ ] Visual elements maintain consistency
- [ ] Character states evolve logically
- [ ] Atmospheric suggestions are coherent

## Common Issues to Watch For

### 1. Anti-Patterns

**God Objects**
```python
# BAD - Too many responsibilities
class DoEverything:
    def parse_script(self): pass
    def analyze_philosophy(self): pass
    def generate_prompts(self): pass
    def send_to_api(self): pass
```

**Magic Numbers**
```python
# BAD
if confidence > 0.7:  # What does 0.7 mean?
    
# GOOD
PHILOSOPHY_CONFIDENCE_THRESHOLD = 0.7
if confidence > PHILOSOPHY_CONFIDENCE_THRESHOLD:
```

**Nested Complexity**
```python
# BAD - Too deeply nested
if condition1:
    if condition2:
        for item in items:
            if condition3:
                # Deep nesting makes code hard to read
                
# GOOD - Early returns and extracted methods
if not condition1:
    return
    
if not condition2:
    return
    
filtered_items = [item for item in items if condition3]
process_filtered_items(filtered_items)
```

### 2. Performance Pitfalls

- Synchronous I/O in async contexts
- Unnecessary data copying
- Missing caching opportunities
- Inefficient string concatenation

### 3. Philosophical Accuracy

- Oversimplifying complex concepts
- Missing nuanced interpretations
- Cultural bias in concept mapping
- Inconsistent depth classification

## Review Comments Guide

### Effective Review Comments

**Good Examples:**
```
"Consider extracting this philosophy analysis into a separate method for better testability"

"This emotion mapping might miss subtle states. What about adding gradients between primary emotions?"

"The performance could be improved by caching these concept lookups. See utils/cache.py for examples"
```

**Poor Examples:**
```
"This is wrong"  # Not constructive

"I don't like this approach"  # Not specific

"Fix this"  # No guidance provided
```

### Comment Categories

Use prefixes to categorize comments:

- **[BLOCKING]**: Must fix before merge
- **[SUGGESTION]**: Consider for improvement
- **[QUESTION]**: Seeking clarification
- **[NITPICK]**: Minor style issue
- **[PRAISE]**: Highlighting good practices

## Continuous Improvement

### Metrics to Track

1. **Code Quality Metrics**
   - Test coverage percentage
   - Cyclomatic complexity
   - Technical debt ratio
   - Documentation coverage

2. **Review Process Metrics**
   - Average review turnaround time
   - Number of review iterations
   - Post-merge defect rate
   - Review participation rate

### Regular Reviews

- **Weekly**: Team code review session
- **Sprint**: Review standards effectiveness
- **Quarterly**: Update standards based on learnings

## Tools and Automation

### Pre-commit Hooks
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.0.0
    hooks:
      - id: black
  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.0.270
    hooks:
      - id: ruff
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.3.0
    hooks:
      - id: mypy
```

### CI/CD Checks
- Automated testing on all PRs
- Code coverage reports
- Performance benchmarks
- Security scanning

## Appendix: Component Owner Reference

| Component | Primary Reviewer | Secondary Reviewer |
|-----------|-----------------|-------------------|
| Core Architecture | Aria | Nova |
| Script Processing | Rex | Aria |
| Philosophy Engine | Sophia | Luna |
| Emotion Mapping | Luna | Sophia |
| Visual Generation | Iris | Luna |
| API/Integration | Nova | Quinn |
| Testing/QA | Quinn | All |

By following these standards, we ensure the Metaphysical Scene Weaver maintains high quality, philosophical accuracy, and technical excellence throughout its development.