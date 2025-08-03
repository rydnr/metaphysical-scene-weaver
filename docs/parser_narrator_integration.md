# Parser-Narrator Integration Proposal
*Rex + Sophia + Nova Collaboration*

## Unified Narrator Voice System

### Three Core Narrator Voices (per Sophia):
1. **SAGE** - Contemplative, measured (for free will/determinism themes)
2. **MYSTIC POET** - Ethereal, evocative (for Valerie/liminal moments)
3. **PROVOCATEUR** - Challenging assumptions (for reality dissolution)

### Parser Voice Detection:
```python
def detect_narrator_voice(entry, context):
    """Automatically assign narrator voice based on content."""
    if 'free will' in entry.metadata or 'choice' in entry.dialogue.lower():
        return 'SAGE'
    elif entry.speaker == 'Valerie' or 'liminal' in entry.metadata:
        return 'MYSTIC_POET'
    elif any(word in entry.stage_directions for word in ['shimmers', 'ripples']):
        return 'PROVOCATEUR'
    return 'SAGE'  # default
```

## Folder Generation Integration (per Nova)

### Parser Output → Folder Structure:
```python
def generate_folder_structure(parsed_entries, bridges):
    """Convert parsed script to Nova's folder structure."""
    
    # Group by scenes
    scene_groups = group_by_scene_boundaries(parsed_entries)
    
    for scene_name, entries in scene_groups.items():
        # Create scene folder (e.g., "001-008_binary_dialogue/")
        scene_folder = create_scene_folder(scene_name, entries)
        
        for entry in entries:
            # Handle multi-panel entries
            if entry.panel_count and entry.panel_count > 1:
                create_panel_subfolders(entry, scene_folder)
            else:
                create_entry_folder(entry, scene_folder)
            
            # Add narrator bridges where needed
            if needs_bridge_before(entry):
                add_narrator_bridge(entry, 'before')
```

### Automated Content Structure:
```
content/
├── 001-008_binary_dialogue/
│   ├── 001_evan_intro/
│   │   ├── entry.json
│   │   ├── narrator_before.txt (SAGE voice)
│   │   └── metadata.json
│   ├── 004_monday_challenge/
│   │   ├── panels/
│   │   │   ├── panel_1/
│   │   │   └── panel_2/
│   │   └── metadata.json
├── 009-015_trinity_dynamic/
│   ├── 009_valerie_emergence/
│   │   ├── narrator_before.txt (MYSTIC_POET voice)
│   │   └── special_effects.json
└── manifest.json
```

## Narrator Template System

### Three-Depth Commentary (per Sophia):
```yaml
narrator_templates:
  philosophical_escalation:
    surface: "The question hangs between them like a door ajar."
    deep: "In asking about choice, the space itself becomes contingent."
    meta: "You, reading this, have already made the choice they debate."
    
  reality_bend:
    surface: "The tree stands as it always has—until it doesn't."
    deep: "Solid things remember they are mostly empty space."
    meta: "Reality blinks, and in that blink, everything rearranges."
```

## Quality Integration (per Quinn)

### Parser Quality Output:
```json
{
  "entry_id": "0009",
  "quality_score": 0.92,
  "issues": [],
  "warnings": [
    {
      "type": "narrator_length",
      "message": "Narrator text at 201 words (limit 200)",
      "severity": "low"
    }
  ],
  "narrator_voice_consistency": 0.95
}
```

## API Design for Integration

### Endpoint Structure:
```
POST /api/parse-script
  → Returns parsed entries with narrator points

POST /api/generate-folders
  → Creates folder structure from parsed data
  
POST /api/validate-content
  → Runs quality checks on generated content

GET /api/narrator-templates/{voice_type}
  → Returns templates for specific narrator voice
```

## Next Steps:
1. Rex: Enhance parser to output Nova's exact format
2. Sophia: Create narrator templates for each voice type
3. Nova: Set up folder generation from parser output
4. All: Test integration with sample script

Ready to implement!