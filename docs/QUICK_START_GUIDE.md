# Quick Start Guide - Day 1 Actions

## For All Team Members

### Morning (First 2 Hours)
1. **Read these documents in order:**
   - PROJECT_PLAN.md - Overall vision and timeline
   - TEAM_TASK_ASSIGNMENTS.md - Your specific tasks
   - NARRATOR_STYLE_GUIDE.md - Narrator voice and approach
   - PROGRAM_1_ARCHITECTURE.md - If working on Program 1
   - PROGRAM_2_ARCHITECTURE.md - If working on Program 2

2. **Set up your development environment:**
   ```bash
   # Clone the repository
   git clone https://github.com/rydnr/metaphysical-scene-weaver.git
   cd metaphysical-scene-weaver
   
   # Create your feature branch
   git checkout -b feature/MSW-001-[your-name]-initial-setup
   
   # Configure Git identity
   ./setup-gpg-signing.sh
   ```

3. **Join communication channels:**
   - Slack: #msw-dev, #msw-[your-specialty]
   - Schedule: Add daily standup to calendar (9:00 AM)

### Afternoon (Start Your First Task)

## Rex - Day 1 Immediate Actions

### 1. Analyze the Script (2 hours)
```bash
# Create analysis directory
mkdir -p docs/analysis/narrator_points

# Start with sample script
cat examples/sample_script.txt
```

**Document these narrator insertion opportunities:**
- Scene openings (location/time changes)
- Philosophical peaks (abstract discussions)
- Emotional transitions (mood shifts)
- Character introductions
- Chapter boundaries

**Create**: `docs/analysis/narrator_insertion_analysis.md`

### 2. Start Enhanced Parser (1 hour)
```python
# src/processors/enhanced_script_parser.py
from ..core.script_parser import ScriptParser

class EnhancedScriptParser(ScriptParser):
    """Extended parser with narrator detection."""
    
    def identify_narrator_points(self, entries):
        """Start implementing narrator point detection."""
        # Begin with scene boundary detection
        pass
```

## Sophia - Day 1 Immediate Actions

### 1. Define Philosophical Narrator Rules (2 hours)
Create mappings for how different philosophical concepts should influence narrator voice:

```markdown
# docs/philosophical_narrator_rules.md

## Concept-to-Narrator Mappings

### Consciousness
- Narrator Voice: Reflective, mirror-like
- Example: "In the space where thought observes itself..."

### Freedom
- Narrator Voice: Open, possibilities-focused
- Example: "Every choice creates a universe..."
```

### 2. Review Philosophical Interpreter (1 hour)
```bash
# Review the enhanced philosophical interpreter
cat src/processors/philosophical_interpreter.py

# Note opportunities for narrator integration
# Document Eastern-Western philosophy bridges
```

## Luna - Day 1 Immediate Actions

### 1. Create Emotional Narrator Mapping (2 hours)
```markdown
# docs/emotional_narrator_mapping.md

## Emotion-to-Narrator Rules

### Joy/Wonder
- Tone: Light, expansive
- Atmosphere: Bright, warm colors
- Example: "Light dances at the edges of understanding..."

### Melancholy/Reflection  
- Tone: Contemplative, slow
- Atmosphere: Muted, blue-grey palette
- Example: "Time pools in the corners of memory..."
```

### 2. Start Emotion Detection Enhancement (1 hour)
```python
# Add to emotional_mapper.py
def get_narrator_tone(self, emotional_state):
    """Determine narrator tone from emotional state."""
    # Map emotions to narrator voice modulation
    pass
```

## Nova - Day 1 Immediate Actions

### 1. Design Folder Structure (2 hours)
```bash
# Create example structure
mkdir -p examples/output_structure/content/{001,002,transitions}
mkdir -p examples/output_structure/{metadata,index}

# Document the structure
cat > docs/folder_structure_spec.md << EOF
# Folder Structure Specification

## Layout
content/
├── 001/
│   ├── 001.txt         # Enhanced visual prompt
│   ├── metadata.json   # Scene metadata
│   └── narrator.txt    # Narrator text
└── ...
EOF
```

### 2. Prototype Scene Synthesizer (1 hour)
```python
# Start extending scene synthesizer
# src/processors/scene_synthesizer_plus.py
from .scene_synthesizer import SceneSynthesizer

class SceneSynthesizerPlus(SceneSynthesizer):
    """Enhanced with narrator integration."""
    
    def synthesize_with_narrator(self, entry, narrator_text):
        """Begin implementation."""
        pass
```

## Iris - Day 1 Immediate Actions

### 1. Create Prompt Templates (2 hours)
```json
// src/templates/prompt_templates.json
{
  "base_template": "A {mood} scene in graphic novel style. {description}. Atmosphere: {atmosphere}. Visual metaphors: {metaphors}",
  
  "scene_types": {
    "dialogue": "Two figures engaged in {philosophical_theme} discussion...",
    "transition": "Visual bridge between {scene_a} and {scene_b}...",
    "narrator": "Abstract representation of: {narrator_text}..."
  }
}
```

### 2. Research Semantest Optimization (1 hour)
- Test different prompt structures
- Document what works best
- Note any API limitations

## Quinn - Day 1 Immediate Actions

### 1. Set Up Test Framework (2 hours)
```bash
# Create test structure
mkdir -p tests/{unit,integration,fixtures}

# Create base test file
cat > tests/test_base.py << EOF
import pytest
from pathlib import Path

# Test fixtures and utilities
@pytest.fixture
def sample_script():
    return Path("examples/sample_script.txt")
EOF
```

### 2. Define Quality Metrics (1 hour)
```markdown
# docs/quality_metrics.md

## Quality Metrics

### Narrator Quality
- Consistency Score: Voice remains consistent
- Relevance Score: Enhances rather than distracts
- Philosophy Score: Accurately reflects concepts

### Technical Metrics
- Processing Speed: <30s for 150 scenes
- Memory Usage: <500MB
- Error Rate: <1%
```

## End of Day 1 Checklist

### Everyone
- [ ] Environment set up
- [ ] First task started
- [ ] Initial code/documentation committed
- [ ] Blockers identified for tomorrow's standup

### Commit Your Work
```bash
# Add your changes
git add .

# Commit with descriptive message
git commit -m "feat: Initial [your component] setup

- Created initial structure for [component]
- Added documentation for [aspect]
- Started implementation of [feature]"

# Push to your branch
git push origin feature/MSW-001-[your-name]-initial-setup
```

## Day 2 Preview

### Morning Standup Prep (9:00 AM)
Prepare to share:
1. What you completed Day 1
2. What you plan for Day 2  
3. Any blockers or questions
4. Any insights about narrator integration

### Integration Points
- Rex + Sophia: Align on philosophical narrator rules
- Rex + Luna: Coordinate emotional narrator mapping
- Nova + Iris: Sync on folder-to-prompt structure
- Everyone: Share narrator examples

## Resources

### Key Files to Review
- `/examples/sample_script.txt` - Example input
- `/src/core/script_parser.py` - Base parser
- `/src/processors/` - All processors to extend

### Documentation
- All docs in `/docs/` directory
- Update as you work
- Share insights in Slack

## Questions?

Post in **#msw-dev** with:
- Your specific question
- What you've tried
- Any error messages
- Tag relevant team member

Let's build something amazing! 🚀