# Metaphysical Scene Weaver

An AI-powered system for transforming philosophical dialogue scripts into rich visual graphic novel prompts.

## Overview

This project takes philosophical conversations (like the Evan/Monday/Valerie dialogue) and generates detailed visual prompts for each scene, capturing not just the literal action but the emotional, philosophical, and metaphorical layers.

## Features

- **Multi-layered Script Analysis**: Parses dialogue, stage directions, and metadata
- **Philosophical Interpretation**: Identifies and visualizes abstract concepts
- **Emotional Mapping**: Translates emotional states into visual elements
- **Metaphor Translation**: Converts textual metaphors into visual symbols
- **Character State Tracking**: Maintains consistency across scenes
- **Seamless Integration**: Works with Semantest for automated image generation

## Project Structure

```
metaphysical-scene-weaver/
├── src/
│   ├── core/              # Core components
│   ├── processors/        # Script processing modules
│   ├── integrations/      # External system integrations
│   └── utils/            # Utility functions
├── data/                 # Input data
│   ├── characters/       # Character JSON files
│   ├── places/          # Location JSON files
│   └── scripts/         # Script files
├── config/              # Configuration files
├── tests/              # Test suite
├── docs/               # Documentation
└── output/             # Generated outputs
```

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/metaphysical-scene-weaver.git
cd metaphysical-scene-weaver

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## Quick Start

```python
from metaphysical_scene_weaver import SceneWeaver

# Initialize the weaver
weaver = SceneWeaver(
    characters_file="data/characters/characters.json",
    places_file="data/places/places.json",
    style="comic book"
)

# Process a script
results = weaver.process_script("data/scripts/evan_monday_dialogue.txt")

# Generate visual prompts
for scene in results:
    print(f"Scene {scene.id}: {scene.prompt}")
```

## Team Structure

See [TEAM.md](docs/TEAM.md) for details about the development team structure.

## Contributing

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) file for details.