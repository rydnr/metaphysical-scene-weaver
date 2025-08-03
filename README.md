# Metaphysical Scene Weaver 🎭

> Transform philosophical dialogue into vivid graphic novel scenes through AI-powered narrative intelligence

## Overview

The Metaphysical Scene Weaver is an innovative system that bridges the gap between abstract philosophical concepts and visual storytelling. It analyzes screenplay-like scripts containing deep philosophical themes and generates rich, emotionally resonant visual prompts for graphic novel illustration.

## 🌟 Key Features

- **Philosophical Depth Analysis**: Extracts and interprets complex philosophical themes
- **Emotional Mapping**: Converts abstract concepts into emotional visual landscapes
- **Narrator Voice Integration**: Supports multiple narrative perspectives and tones
- **Scene Transition Engine**: Maintains continuity across sequential scenes
- **Quality Validation**: Ensures prompt coherence and artistic viability
- **Batch Processing**: Optimized for large-scale scene generation

## 📋 Requirements

- Python 3.9+
- GPU recommended for transformer models
- 8GB+ RAM for optimal performance

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/metaphysical-scene-weaver.git
cd metaphysical-scene-weaver

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .
```

### Basic Usage

```bash
# Process a single script
msw process scripts/sample_script.txt

# Start the API server
msw-server

# Run with specific narrator voice
msw process scripts/sample_script.txt --narrator contemplative
```

### Python API

```python
from metaphysical_scene_weaver import SceneWeaver

# Initialize the weaver
weaver = SceneWeaver()

# Process a script
result = weaver.process_script(
    script_path="scripts/sample_script.txt",
    narrator_voice="philosophical",
    output_format="graphic_novel"
)

# Access generated prompts
for scene in result.scenes:
    print(f"Scene {scene.id}: {scene.visual_prompt}")
```

## 🏗️ Architecture

```
metaphysical-scene-weaver/
├── src/
│   ├── core/                 # Core processing engines
│   │   ├── script_parser.py  # Script analysis
│   │   ├── scene_weaver.py   # Main orchestration
│   │   └── quality_validator.py
│   ├── processors/           # Specialized processors
│   │   ├── emotional_mapper.py
│   │   ├── philosophical_interpreter.py
│   │   └── metaphor_translator.py
│   ├── api/                  # REST API & WebSocket
│   │   ├── server.py
│   │   └── transition_engine.py
│   └── integrations/         # External services
│       └── semantest_client.py
├── content/                  # Generated content
├── tests/                    # Test suite
└── docs/                     # Documentation
```

## 🎯 Core Components

### 1. Script Parser
Analyzes screenplay-format text to extract:
- Character dialogue and actions
- Scene transitions
- Emotional beats
- Philosophical concepts

### 2. Philosophical Interpreter
- Identifies philosophical themes and concepts
- Maps abstract ideas to visual metaphors
- Maintains conceptual consistency

### 3. Emotional Mapper
- Translates philosophical concepts to emotional states
- Creates mood progressions
- Generates atmosphere descriptors

### 4. Visual Prompt Generator
- Synthesizes all analyses into coherent visual prompts
- Optimizes for artist interpretation
- Ensures technical feasibility

### 5. Quality Validator
- Checks prompt coherence
- Validates emotional consistency
- Ensures philosophical accuracy

## 📚 Documentation

- [API Guide](docs/API_GUIDE.md) - REST API reference
- [Architecture](docs/ARCHITECTURE.md) - System design details
- [Development Workflow](docs/DEVELOPMENT_WORKFLOW.md) - Contributing guide
- [Narrator Style Guide](docs/NARRATOR_STYLE_GUIDE.md) - Voice options
- [Quick Start Guide](docs/QUICK_START_GUIDE.md) - Detailed setup

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test categories
pytest tests/unit/
pytest tests/integration/
pytest tests/e2e/

# Run with coverage
pytest --cov=src --cov-report=html
```

## 🐳 Docker Deployment

```bash
# Build the image
docker build -t metaphysical-scene-weaver .

# Run the container
docker run -p 8000:8000 metaphysical-scene-weaver
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run linters
black src/ tests/
ruff check src/ tests/
mypy src/

# Pre-commit hooks
pre-commit install
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- The philosophical framework is inspired by works of Continental philosophy
- Visual mapping techniques adapted from cognitive science research
- Special thanks to the AI artist community for prompt engineering insights

## 📞 Contact

- **Project Lead**: [Your Name](mailto:your.email@example.com)
- **Issues**: [GitHub Issues](https://github.com/yourusername/metaphysical-scene-weaver/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/metaphysical-scene-weaver/discussions)

---

*"Where philosophy meets visual narrative"* 🎨✨