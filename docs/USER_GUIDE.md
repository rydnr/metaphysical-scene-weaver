# Metaphysical Scene Weaver User Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Script Format](#script-format)
5. [CLI Usage](#cli-usage)
6. [API Usage](#api-usage)
7. [Configuration](#configuration)
8. [Examples](#examples)
9. [Troubleshooting](#troubleshooting)

## Introduction

The Metaphysical Scene Weaver is an AI-powered system that transforms philosophical dialogue scripts into enriched visual prompts for graphic novel generation. It analyzes:

- **Philosophical concepts** and themes
- **Emotional states** and character development
- **Visual metaphors** and symbolic representations
- **Character relationships** and narrative arcs

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Steps

1. Clone the repository:
```bash
git clone <repository-url>
cd metaphysical-scene-weaver
```

2. Run the setup script:
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

Or manually:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
python -m spacy download en_core_web_sm
```

3. Prepare your data files:
- `characters.json` - Character descriptions and visual details
- `places.json` - Location descriptions and atmospheres

## Quick Start

### Basic Usage

Process a script file:
```bash
python -m src process script.txt -c characters.json -p places.json -o output/
```

Preview a single scene:
```bash
python -m src preview 0042 script.txt
```

### Python API

```python
from pathlib import Path
from src.core.scene_weaver import SceneWeaver

# Initialize
weaver = SceneWeaver(
    characters_file=Path("characters.json"),
    places_file=Path("places.json"),
    style="graphic novel"
)

# Process script
scenes = weaver.process_script(Path("script.txt"))

# Export prompts
weaver.export_prompts(Path("output/"))
```

## Script Format

The system expects scripts in the following format:

```
[0001] Speaker: <<Dialogue goes here.>>
[0002] [2-panel] Speaker: <<Multi-panel dialogue.>> (stage direction)
[0003] Speaker: <<Dialogue with metadata.>> [[philosophical note]]
```

### Components:
- **Entry ID**: `[0001]` - Unique identifier
- **Panel Count**: `[2-panel]` - Optional, specifies multiple panels
- **Speaker**: Character name
- **Dialogue**: Enclosed in `<<...>>`
- **Stage Directions**: In parentheses `(...)`
- **Metadata**: In double brackets `[[...]]`

## CLI Usage

### Commands

#### `process` - Process entire script
```bash
python -m src process script.txt [OPTIONS]

Options:
  -c, --characters PATH   Path to characters JSON file [default: characters.json]
  -p, --places PATH      Path to places JSON file [default: places.json]
  -o, --output PATH      Output directory [default: output]
  -s, --style TEXT       Visual style [comic book|manga|graphic novel|cinematic]
  -v, --verbose          Enable verbose logging
```

#### `parse` - Parse script structure
```bash
python -m src parse script.txt [-o output.json]
```

#### `preview` - Preview single scene
```bash
python -m src preview ENTRY_ID script.txt [OPTIONS]
```

#### `validate` - Validate setup
```bash
python -m src validate
```

#### `serve` - Start API server
```bash
python -m src serve [-h HOST] [-p PORT]
```

## API Usage

### Starting the Server
```bash
python -m src serve
```

### Endpoints

#### Process Single Entry
```http
POST /process
Content-Type: application/json

{
  "entry_id": "0042",
  "speaker": "Monday",
  "dialogue": "Reality bends around consciousness.",
  "stage_directions": ["looks intensely"],
  "metadata": ["philosophical revelation"]
}
```

#### Batch Processing
```http
POST /batch
Content-Type: application/json

{
  "entries": [...],
  "style": "graphic novel"
}
```

#### WebSocket Real-time
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.send(JSON.stringify({
  type: 'process',
  entry_id: '0042',
  speaker: 'Monday',
  dialogue: 'Reality bends...'
}));
```

## Configuration

### Scene Weaver Config

Modify processing behavior:

```python
config = {
    'philosophy_weight': 0.4,      # Weight for philosophical elements
    'emotion_weight': 0.3,         # Weight for emotional elements
    'visual_weight': 0.3,          # Weight for visual elements
    'enable_continuity': True,     # Track visual continuity
    'enable_metaphors': True,      # Process metaphorical content
    'max_prompt_length': 500       # Maximum prompt length
}
```

### Visual Styles

Available styles:
- **comic book**: Bold inks, dynamic colors, traditional panels
- **manga**: Japanese style, screentones, expressive emotions
- **graphic novel**: Painterly, sophisticated, literary
- **cinematic**: Movie-like, photorealistic, dramatic lighting

## Examples

### Example 1: Simple Processing

```python
# Process a philosophical dialogue
from src.core.scene_weaver import SceneWeaver

weaver = SceneWeaver(
    Path("characters.json"),
    Path("places.json"),
    style="graphic novel"
)

scenes = weaver.process_script(Path("philosophy_dialogue.txt"))

for scene in scenes[:3]:
    print(f"Scene {scene.entry_id}:")
    print(f"  Philosophy: {scene.philosophy['primary_concept']}")
    print(f"  Emotion: {scene.emotion['primary']}")
    print(f"  Prompt: {scene.prompt[:100]}...")
```

### Example 2: Character Arc Analysis

```python
# Analyze character development
arc_summary = weaver.state_tracker.generate_arc_summary("evan")

print(f"Character: {arc_summary['character']}")
print(f"Emotional Journey: {arc_summary['emotional_journey']}")
print(f"Awareness Progression: {arc_summary['awareness_progression']}")
```

### Example 3: Custom Integration

```python
# Integrate with Semantest
from src.integrations import SemantestIntegration

integration = SemantestIntegration(weaver)
await integration.start()

# Process and generate images
request_id = await integration.process_and_generate(script_entry)
```

## Troubleshooting

### Common Issues

#### "spaCy model not found"
```bash
python -m spacy download en_core_web_sm
```

#### "Characters/Places file not found"
Ensure `characters.json` and `places.json` exist in the working directory.

#### "Import error"
Make sure you're in the virtual environment:
```bash
source venv/bin/activate
```

### Performance Tips

1. **Large Scripts**: Process in batches using the API
2. **Memory Usage**: Reduce context window in `ContextAnalyzer`
3. **Speed**: Disable metaphor processing if not needed

### Debug Mode

Enable verbose logging:
```bash
python -m src process script.txt -v
```

Or in Python:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Advanced Features

### Custom Processors

Create custom analysis processors:

```python
from src.processors.base import BaseProcessor

class CustomProcessor(BaseProcessor):
    def process(self, entry, context):
        # Your custom logic
        return processed_data
```

### Webhook Integration

Configure webhooks for async processing:

```python
config = {
    "webhook_url": "https://your-server/webhook",
    "webhook_events": ["scene_processed", "batch_complete"]
}
```

### Export Formats

Export in different formats:

```python
# JSON export
weaver.export_json(Path("output.json"))

# CSV export for analysis
weaver.export_csv(Path("analysis.csv"))

# Markdown documentation
weaver.export_markdown(Path("scenes.md"))
```

## Support

For issues and questions:
1. Check the [troubleshooting](#troubleshooting) section
2. Review example scripts in `examples/`
3. Submit issues on the project repository

Happy scene weaving! 🎨📚✨