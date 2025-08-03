# Metaphysical Scene Weaver - System Architecture Overview

## Executive Summary

The Metaphysical Scene Weaver is a sophisticated AI-powered system designed to transform philosophical dialogue scripts into enriched visual prompts for graphic novel generation. The system employs a multi-layered processing pipeline that analyzes text at philosophical, emotional, and metaphorical levels to produce comprehensive scene descriptions.

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Input Layer                               │
├─────────────────────────────────────────────────────────────────┤
│  Script Files │ Character Data │ Location Data │ Configuration  │
└───────────────┴────────────────┴───────────────┴────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Core Orchestration Layer                      │
├─────────────────────────────────────────────────────────────────┤
│         SceneWeaver (Main Orchestrator)                         │
│         ├── ScriptParser                                        │
│         └── CharacterStateTracker                               │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Processing Pipeline                           │
├─────────────────────────────────────────────────────────────────┤
│  ContextAnalyzer → PhilosophicalInterpreter → EmotionalMapper  │
│         ↓                    ↓                      ↓           │
│  MetaphorTranslator → SceneSynthesizer → PromptGenerator       │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Output Layer                                │
├─────────────────────────────────────────────────────────────────┤
│   Visual Prompts │ Metadata │ API Response │ Semantest Export   │
└─────────────────────────────────────────────────────────────────┘
```

### Component Architecture

#### 1. Core Components (`src/core/`)

**SceneWeaver** (`scene_weaver.py`)
- Main orchestrator coordinating all processing components
- Manages configuration and processing state
- Handles continuity between scenes
- Exports final prompts and metadata

**ScriptParser** (`script_parser.py`)
- Parses dialogue scripts with specialized format: `[ID] [panels] Speaker: <<dialogue>>`
- Extracts metadata `[[ ]]` and stage directions `( )`
- Converts raw text into structured `ScriptEntry` objects

**CharacterStateTracker** (`character_state_tracker.py`)
- Maintains character emotional and philosophical states across scenes
- Enables continuity and character development visualization
- Tracks intensity levels and state transitions

#### 2. Processing Pipeline (`src/processors/`)

**ContextAnalyzer** (`context_analyzer.py`)
- Analyzes narrative context using character and location data
- Determines scene setting and temporal progression
- Identifies relationships between characters and events

**PhilosophicalInterpreter** (`philosophical_interpreter.py`)
- Identifies philosophical concepts through keyword and semantic analysis
- Maps concepts to visual symbols and atmospheric suggestions
- Determines depth levels (simple → philosophical → metaphysical → existential)
- Categories: metaphysics, ethics, ontology, epistemology, phenomenology

**EmotionalMapper** (`emotional_mapper.py`)
- Maps character emotional states to visual elements
- Translates emotions into colors, lighting, and composition
- Handles emotion intensity and complexity

**MetaphorTranslator** (`metaphor_translator.py`)
- Converts textual metaphors into visual representations
- Creates symbolic visual elements from abstract concepts
- Maintains metaphor consistency across scenes

**SceneSynthesizer** (`scene_synthesizer.py`)
- Combines all analysis layers into cohesive scene data
- Resolves conflicts between different interpretive layers
- Ensures visual and narrative coherence

**PromptGenerator** (`prompt_generator.py`)
- Generates final visual prompts optimized for image generation
- Adapts output style (comic book, fine art, etc.)
- Manages prompt length and complexity

#### 3. Integration Layer (`src/integrations/`)

**SemantestClient** (`semantest_client.py`)
- WebSocket integration with Semantest for automated image generation
- Handles asynchronous communication and error recovery
- Manages generation queues and results

#### 4. API Layer (`src/api/`)

**Server** (`server.py`)
- FastAPI-based REST API for external access
- WebSocket support for real-time processing
- Endpoints for script processing, status monitoring, and result retrieval

### Data Flow

1. **Input Processing**
   ```
   Script File → ScriptParser → ScriptEntry objects
   Character/Location JSON → SceneWeaver configuration
   ```

2. **Analysis Pipeline**
   ```
   ScriptEntry → ContextAnalyzer → Context Data
              ↓
   PhilosophicalInterpreter → Philosophical Concepts
              ↓
   EmotionalMapper → Emotional Visual Elements
              ↓
   MetaphorTranslator → Visual Metaphors
              ↓
   SceneSynthesizer → Unified Scene Data
   ```

3. **Output Generation**
   ```
   Scene Data → PromptGenerator → Visual Prompt
             → Metadata Export → JSON
             → SemantestClient → Generated Images
   ```

### Key Design Patterns

1. **Pipeline Pattern**: Sequential processing with each stage enriching the data
2. **State Management**: Centralized character state tracking for continuity
3. **Strategy Pattern**: Configurable prompt generation styles
4. **Observer Pattern**: Event-driven updates for real-time processing
5. **Factory Pattern**: Dynamic processor instantiation based on configuration

### Integration Points

1. **SceneWeaver ← → All Processors**
   - Central orchestration and data flow management
   - Configuration propagation

2. **CharacterStateTracker ← → EmotionalMapper**
   - Bidirectional state updates
   - Emotion evolution tracking

3. **All Processors → SceneSynthesizer**
   - Multi-layer data aggregation
   - Conflict resolution

4. **PromptGenerator → SemantestClient**
   - Prompt delivery for image generation
   - Result correlation

### Configuration System

The system uses a hierarchical configuration approach:

```python
{
    'philosophy_weight': 0.4,      # Influence of philosophical layer
    'emotion_weight': 0.3,         # Influence of emotional layer
    'visual_weight': 0.3,          # Influence of visual elements
    'enable_continuity': True,     # Scene-to-scene continuity
    'enable_metaphors': True,      # Metaphor visualization
    'max_prompt_length': 500,      # Token limit for prompts
    'depth_threshold': {           # Philosophical depth levels
        'simple': 0,
        'philosophical': 1,
        'metaphysical': 2,
        'existential': 3
    }
}
```

### Technology Stack

- **Core Language**: Python 3.9+
- **NLP Libraries**: NLTK, spaCy, Transformers
- **Web Framework**: FastAPI
- **Data Validation**: Pydantic
- **Async Support**: asyncio, aiohttp
- **Testing**: pytest, pytest-asyncio
- **Code Quality**: black, ruff, mypy

### Scalability Considerations

1. **Async Processing**: All I/O operations are async-enabled
2. **Modular Design**: Each processor can be scaled independently
3. **Caching Strategy**: Results cached at multiple levels
4. **Queue Management**: Integration with message queues for batch processing

### Security Considerations

1. **Input Validation**: All inputs validated through Pydantic models
2. **Rate Limiting**: API endpoints include rate limiting
3. **Authentication**: JWT-based authentication for API access
4. **Data Privacy**: No persistent storage of sensitive dialogue content

### Performance Metrics

- **Processing Speed**: Target <5s per scene
- **Memory Usage**: <500MB for typical script
- **API Response Time**: <100ms for status queries
- **Generation Quality**: 90%+ prompt accuracy

### Future Architecture Enhancements

1. **Plugin System**: Dynamic processor loading
2. **ML Model Integration**: Custom models for concept detection
3. **Distributed Processing**: Multi-node support for large scripts
4. **Real-time Collaboration**: WebSocket-based collaborative editing

## Development Guidelines

### Code Organization

- **Single Responsibility**: Each processor handles one aspect
- **Clear Interfaces**: Well-defined data contracts between components
- **Testability**: All components designed for unit testing
- **Documentation**: Comprehensive docstrings and type hints

### Extension Points

1. **New Processors**: Implement base processor interface
2. **Output Formats**: Add new prompt generators
3. **Input Formats**: Extend script parser for new formats
4. **Integration Targets**: Add new client implementations

This architecture provides a robust, scalable foundation for transforming philosophical dialogue into rich visual narratives while maintaining flexibility for future enhancements.