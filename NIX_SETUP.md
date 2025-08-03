# NixOS Setup Instructions

## Important Note for Team Members

This project is being developed on NixOS, which handles Python dependencies differently than traditional systems. If you encounter issues running Python code, it's likely due to missing dependencies.

## Understanding NixOS

NixOS uses a declarative approach to system configuration and package management:
- **Immutable packages**: System packages cannot be modified after installation
- **Reproducible environments**: Same configuration produces identical environments
- **Isolated dependencies**: No conflicts between project dependencies
- **Declarative configuration**: All dependencies specified in Nix expressions

## Quick Fixes

### Option 1: Wait for Nix Flake (Recommended)
The project owner will provide a `flake.nix` file that properly defines all dependencies. Once available, you can run:
```bash
nix develop
```

This will provide a complete development shell with all dependencies.

### Option 2: Use nix-shell (Temporary)
For immediate testing, you can try:
```bash
nix-shell -p python311 python311Packages.pip python311Packages.spacy python311Packages.fastapi python311Packages.pydantic python311Packages.uvicorn python311Packages.websockets python311Packages.nltk
```

### Option 3: Focus on Code Logic
If you can't run the code, focus on:
- Code review and logic verification
- Documentation improvements
- Architecture planning and design
- Test structure (even if not executable)
- Identifying and documenting needed dependencies

## Known Dependencies

### Core Dependencies (from pyproject.toml):
```
Python 3.9+
pydantic>=2.0
fastapi>=0.100.0
websockets>=11.0
aiohttp>=3.8
numpy>=1.24
pandas>=2.0
nltk>=3.8
spacy>=3.5
transformers>=4.30
scikit-learn>=1.3
matplotlib>=3.7
seaborn>=0.12
click>=8.1
rich>=13.0
python-dotenv>=1.0
pyyaml>=6.0
PyJWT>=2.8.0
uvicorn>=0.23.0
python-multipart>=0.0.6
```

### Development Tools:
```
pytest>=7.3
pytest-asyncio>=0.21
black>=23.0
ruff>=0.0.270
mypy>=1.3
```

### Additional Requirements:
- spacy language model: `en_core_web_sm`
- NLTK data packages (will be downloaded on first run)

## Team Workflow on NixOS

### 1. Development Without Direct Execution
**Don't worry if you can't run the code immediately!**

Focus on:
- **Code Structure**: Write clean, well-organized code
- **Type Hints**: Add comprehensive type annotations
- **Documentation**: Write clear docstrings and comments
- **Tests**: Create test structures (even if not runnable)
- **Reviews**: Review code logic and suggest improvements

### 2. Working with Git

**Initial Setup:**
```bash
# Configure your git identity and GPG signing
./setup-gpg-signing.sh
```

**Auto-Commit Feature:**
- Commits run automatically every 10 minutes
- Uses descriptive emojis for different file types
- Helps maintain version history

**Managing Auto-Commits:**
```bash
# Check status
./manage-hooks.sh status

# Temporarily disable
./manage-hooks.sh disable

# Re-enable
./manage-hooks.sh enable < /dev/null
```

### 3. Repository Information
- **GitHub**: https://github.com/rydnr/metaphysical-scene-weaver
- **Auto-commits**: Every 10 minutes with appropriate emojis
- **Branch strategy**: Feature branches from `develop`

## Development Best Practices on NixOS

### 1. Code Organization
- Use relative imports to avoid path issues
- Don't hardcode system paths
- Document any OS-specific considerations
- Keep dependencies minimal and well-documented

### 2. When Adding Dependencies
If you need a new dependency:
1. Add it to `pyproject.toml` with version constraint
2. Document why it's needed in your PR
3. Note if it requires special Nix packaging
4. Check if there's a Nix alternative

### 3. Testing Approach
Write tests even if not immediately executable:

```python
# Example test structure
def test_philosophical_concept_detection():
    """Test that philosophical concepts are properly detected."""
    # This test structure is valuable even without execution
    # It documents expected behavior and can be run later
    
    interpreter = PhilosophicalInterpreter()
    result = interpreter.interpret("The nature of existence", {}, [])
    
    assert 'existence' in result['all_concepts']
    assert result['philosophical_category'] == 'ontology'
```

## Troubleshooting

### Common NixOS Issues

**"Command not found" errors:**
- Expected without proper Nix environment
- Document the command needed
- Will be resolved with flake.nix

**Python import errors:**
- Package not in Nix environment
- Add to dependency list
- Use standard library alternatives when possible

**Path-related issues:**
- NixOS doesn't follow FHS completely
- Use `pathlib` for cross-platform paths
- Avoid absolute paths

### Getting Help

1. **Team Lead**: Aria can help with environment setup
2. **Documentation**: This file and official NixOS docs
3. **GitHub Issues**: Report blockers in project repository
4. **Slack**: #msw-dev channel for quick questions

## Benefits of NixOS for This Project

1. **Reproducibility**: Everyone gets the exact same environment
2. **No Dependency Hell**: Isolated, conflict-free dependencies  
3. **Easy Rollbacks**: Can revert to previous configurations
4. **Security**: Immutable system prevents accidental changes
5. **Caching**: Faster builds with shared binary cache

## Future Nix Flake Structure

The upcoming flake.nix will provide:
- Complete Python development environment
- All project dependencies pre-configured
- Development tools (formatters, linters)
- Git hooks and utilities
- Optional GPU support for transformers

## Action Items for Team Members

1. **Run GPG setup**: `./setup-gpg-signing.sh`
2. **Review your module**: Even without execution
3. **Document dependencies**: Note what your code needs
4. **Write tests**: Structure is valuable even if not runnable
5. **Collaborate**: Share findings about NixOS quirks

Remember: The NixOS environment ensures our project will be perfectly reproducible across all machines once the flake is ready!