# Folder Structure Proposal for Narrator-Enhanced Scene Generation

## Overview

This proposal outlines a scalable folder structure that supports narrator integration, versioning, and efficient Semantest processing.

## Proposed Structure

```
content/
├── manifest.json                    # Master index of all content
├── metadata.json                    # Project-wide settings
├── 001_opening_consciousness/       # Scene sequence folders
│   ├── scene.json                   # Scene metadata and config
│   ├── raw/
│   │   ├── dialogue.txt             # Original script excerpt
│   │   ├── annotations.json         # Parse results
│   │   └── context.json             # Surrounding scenes ref
│   ├── narrator/
│   │   ├── introduction.txt         # Narrator intro for sequence
│   │   ├── commentary.txt           # Per-panel narrator text
│   │   ├── voice_config.json        # Tone, style, perspective
│   │   └── transitions.json         # Inter-scene connections
│   ├── prompts/
│   │   ├── v1/
│   │   │   ├── base_prompt.txt      # Initial generation
│   │   │   ├── negative_prompt.txt  # What to avoid
│   │   │   ├── style_modifiers.txt  # Visual style additions
│   │   │   └── generation_log.json  # Settings used
│   │   └── v2/                      # Iterations if needed
│   ├── philosophy/
│   │   ├── concepts.json            # Detected concepts
│   │   ├── narrator_guidance.txt    # How to present concepts
│   │   └── visual_metaphors.json    # Concept→visual mapping
│   ├── emotion/
│   │   ├── emotional_arc.json       # Scene emotion progression
│   │   ├── color_palette.json       # Emotion-driven colors
│   │   └── atmosphere.json          # Mood and lighting
│   ├── composition/
│   │   ├── panel_layout.json        # Multi-panel structure
│   │   ├── camera_angles.json       # Shot descriptions
│   │   ├── focal_points.json        # Visual emphasis
│   │   └── continuity.json          # Elements to maintain
│   ├── transitions/
│   │   ├── from_previous.json       # Entry transition
│   │   ├── to_next.json             # Exit transition
│   │   └── visual_flow.json         # Movement and pacing
│   └── output/
│       ├── images/                  # Generated images
│       ├── thumbnails/              # Quick previews
│       └── semantest_log.json       # Generation history
│
├── 002_reality_questioning/         # Next sequence
│   └── ...                          # Same structure
│
├── shared/                          # Reusable assets
│   ├── characters/
│   │   ├── evan.json
│   │   ├── monday.json
│   │   └── valerie.json
│   ├── locations/
│   │   └── liminal_space.json
│   └── visual_rules/
│       └── style_guide.json
│
└── exports/                         # Final outputs
    ├── complete_script.md           # Full narrator-enhanced script
    ├── image_gallery/               # All final images
    └── production_notes.md          # Implementation notes
```

## Key Design Decisions

### 1. Numbered Scene Folders
- **Format**: `XXX_descriptive_name/`
- **Benefits**: Natural ordering, easy navigation, clear progression
- **Example**: `007_tree_revelation/`, `019_reality_touch/`

### 2. Narrator as First-Class Citizen
- Dedicated `narrator/` subfolder in each scene
- Separate files for different narrator functions
- Voice configuration per sequence for consistency

### 3. Version Control for Prompts
- `prompts/v1/`, `prompts/v2/` structure
- Preserves iteration history
- Allows A/B testing of approaches

### 4. Separation of Concerns
- Raw content separate from generated content
- Philosophy/emotion/composition in distinct folders
- Clear input→processing→output flow

### 5. Transition Management
- Explicit transition data between scenes
- Supports the transition engine I just built
- Enables smooth visual flow

## File Specifications

### manifest.json
```json
{
  "version": "1.0.0",
  "total_scenes": 20,
  "scenes": [
    {
      "id": "001",
      "name": "opening_consciousness",
      "panels": 1,
      "has_narrator": true,
      "status": "completed"
    }
  ],
  "generation_config": {
    "style": "philosophical_comic",
    "default_size": [1024, 1024]
  }
}
```

### scene.json
```json
{
  "scene_id": "001",
  "script_reference": "[0001]",
  "speaker": "Evan",
  "panel_count": 1,
  "narrator_sections": ["intro", "outro"],
  "philosophical_weight": 0.8,
  "emotional_intensity": 0.6,
  "visual_complexity": "moderate"
}
```

### narrator/voice_config.json
```json
{
  "tone": "contemplative_guide",
  "perspective": "omniscient_philosophical",
  "formality": 0.7,
  "mystique": 0.8,
  "philosophical_depth": 0.9,
  "emotional_distance": 0.4
}
```

## Integration Benefits

### For Script→Folders Program
1. Clear output structure
2. Organized narrator insertion
3. Metadata tracking built-in
4. Version control ready

### For Folders→Images Program
1. All prompts in predictable locations
2. Batch processing friendly
3. Progress tracking via status files
4. Retry capability with versions

### For API/WebSocket Integration
1. RESTful path structure
2. Streamable folder monitoring
3. Parallel processing possible
4. Cache-friendly organization

## Collaboration Points

### With Rex (Script Analyst)
- Narrator insertion points → `narrator/` files
- Scene boundaries → folder divisions

### With Sophia (Philosophy)
- Concepts → `philosophy/concepts.json`
- Narrator guidance → `philosophy/narrator_guidance.txt`

### With Luna (Emotion)
- Emotional arcs → `emotion/emotional_arc.json`
- Visual atmospheres → `emotion/atmosphere.json`

### With Iris (Semantest)
- Prompt optimization → `prompts/` structure
- API constraints → `output/semantest_log.json`

### With Quinn (QA)
- Test fixtures → predictable paths
- Quality metrics → status tracking in manifest

## Implementation Timeline

1. **Phase 1**: Basic structure (Today)
   - Create folder hierarchy
   - Define core JSON schemas
   - Set up first example scene

2. **Phase 2**: Integration (Tomorrow)
   - Connect to existing processors
   - Add narrator injection points
   - Test with sample script

3. **Phase 3**: Optimization (Day 3)
   - Batch processing setup
   - Caching strategies
   - Performance tuning

## Questions for Team

1. Should we add a `draft/` folder for work-in-progress?
2. How many narrator intervention points per scene?
3. Do we need character state tracking between scenes?
4. Should visual styles be scene-specific or sequence-specific?

Ready to refine based on team feedback at 2 PM sync!