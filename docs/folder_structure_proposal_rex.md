# Folder Structure Proposal - Parser Integration
*From Rex to Nova*

## Parser Output for Content Folders

Based on my script analysis, here's how the parser can structure data for your folder system:

### Proposed Structure:
```
content/
├── 001/
│   ├── entry.json          # Core dialogue data
│   ├── narrator_before.txt # Pre-entry narration (if needed)
│   ├── narrator_after.txt  # Post-entry narration (if needed)
│   ├── metadata.json       # Philosophy tags, emotions, etc.
│   ├── visual_cues.json    # Stage directions, scene requirements
│   └── semantest_prompt.txt # Final composed prompt
├── 002/
│   └── ... (same structure)
├── bridges/
│   ├── opening.txt         # Special narrator sequences
│   ├── valerie_intro.txt
│   └── reality_bend_001.txt
└── manifest.json           # Master index of all content

```

### Entry.json Format:
```json
{
  "id": "0001",
  "sequence": 1,
  "speaker": "Evan",
  "dialogue": "The introduction says we might not like each other. That is intriguing.",
  "word_count": 13,
  "question": false,
  "dialogue_type": "statement"
}
```

### Metadata.json Format:
```json
{
  "philosophical_concepts": [],
  "emotional_tone": "curious",
  "panel_count": 1,
  "narrator_bridge_needed": {
    "before": true,
    "after": false,
    "type": "opening"
  },
  "tags": [],
  "character_state": "discovering"
}
```

### Visual_cues.json Format:
```json
{
  "stage_directions": [],
  "implied_setting": "undefined space",
  "character_positions": ["single figure"],
  "atmosphere": "anticipatory",
  "special_effects": []
}
```

## Parser Features for Folder Generation:

1. **Sequential Numbering**: Guaranteed ordered folders (001, 002, etc.)
2. **Bridge Detection**: Automatically identifies where narrator insertions needed
3. **Metadata Extraction**: Pulls all philosophical tags and emotional cues
4. **Visual Requirements**: Parses stage directions into actionable visual data
5. **Question Detection**: Flags dialogues that are questions vs. statements

## Special Considerations:

### Multi-Panel Entries:
- Entries marked [2-panel] or [3-panel] get expanded visual space
- Parser includes panel_count in metadata
- Could generate sub-folders: `001/panel_1/`, `001/panel_2/`

### Character Introduction Folders:
- First appearance of character gets special treatment
- Additional file: `character_intro.json` with visual description

### Reality-Bending Sequences:
- Flagged with special visual requirements
- Might need multiple image generation passes
- Parser identifies these automatically

## Questions for Nova:
1. Should we version prompts? (e.g., `semantest_prompt_v1.txt`)
2. Do you want separate folders for narrator bridges or inline?
3. How should we handle entries that span multiple images?

Ready to adjust parser output to match your folder design!