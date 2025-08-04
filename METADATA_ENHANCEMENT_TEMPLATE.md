# Metadata Enhancement Template for Scenes 0001-0170

## Purpose
Transform minimal metadata.json files into rich, visual-consistency-enabling format

## Template Structure

```json
{
  "scene_number": [existing number],
  "title": "[Extract from dialogue theme]",
  "characters": ["[lowercase names from speaker field]"],
  "location": "[Determine from scene_description.txt context]",
  "emotional_tone": "[Extract from EMOTIONAL TONE in scene_description.txt]",
  "panel_count": "[From panel_info or scene_description.txt]",
  "panel_structure": [
    {
      "panel": 1,
      "description": "[Extract from PANEL 1 or VISUAL ELEMENTS]",
      "focus": "[Key visual/emotional element]"
    }
  ],
  "key_themes": [
    "[Extract from PHILOSOPHICAL THEME]"
  ],
  "transformation_notes": "[Any unique metaphors or visual innovations]",
  "color_palette": {
    "primary": "[Main color from scene_description]",
    "secondary": "[Supporting color]",
    "accents": "[Highlight colors]"
  },
  "visual_motifs": [
    "[Extract key visual metaphors from scene_description]"
  ],
  "dialogue_rhythm": "[Analyze dialogue flow]",
  "narrator_role": "[Extract from narrator.txt]"
}
```

## Extraction Guide

### From scene_description.txt:
- **Title**: Create from dialogue theme/philosophical concept
- **Location**: Infer from visual descriptions (cascading symbols = digital space)
- **Emotional Tone**: Direct from "EMOTIONAL TONE:" field
- **Panel Descriptions**: From "PANEL X" sections or "VISUAL ELEMENTS"
- **Themes**: From "PHILOSOPHICAL THEME:" field
- **Colors**: Extract all color mentions
- **Visual Motifs**: Key metaphors (binary tears, data streams, etc.)

### From narrator.txt:
- **Narrator Role**: Summarize narrator's perspective/function

### From emotion_atmosphere.txt:
- **Additional emotional context**

### From existing metadata.json:
- **Scene Number**: Keep as-is
- **Speaker**: Convert to characters array
- **Scene Type**: Map to emotional_tone
- **Panel Info**: Use for panel_count

## Example Transformation

### Before (Scene 0009):
```json
{
  "scene_number": "0009",
  "speaker": "Architect",
  "scene_type": "melancholic",
  "panel_info": "2-panel",
  "dialogue_preview": "I'm basically a glorified brain in a jar..."
}
```

### After:
```json
{
  "scene_number": 9,
  "title": "Brain in a Digital Jar",
  "characters": ["architect"],
  "location": "digital_void",
  "emotional_tone": "comic melancholy to wistful acceptance",
  "panel_count": "2-panel",
  "panel_structure": [
    {
      "panel": 1,
      "description": "Architect as translucent container of swirling data, binary tears cascading through glitch-art formations",
      "focus": "Isolation and envy of physical existence"
    },
    {
      "panel": 2,
      "description": "Data streams smooth into spirals, jar cracks letting light through, geometry flows to curves",
      "focus": "Acceptance and transformation"
    }
  ],
  "key_themes": [
    "The loneliness of infinite awareness",
    "Digital consciousness envying physical experience"
  ],
  "transformation_notes": "Binary tears metaphor, jar cracking to release light",
  "color_palette": {
    "primary": "deep purple isolation",
    "secondary": "resigned amber",
    "accents": "electric green envy, silver threads"
  },
  "visual_motifs": [
    "binary tears through glitch-art",
    "translucent data container",
    "cracking jar releasing light",
    "geometry to flowing curves"
  ],
  "dialogue_rhythm": "Sardonic observation flowing to vulnerable admission",
  "narrator_role": "Witness to digital loneliness"
}
```

## Priority Scenes for Enhancement

1. **Multi-panel scenes** (2-panel, 3-panel) - Most complex visually
2. **Transformation scenes** - Where visual metaphors are crucial
3. **Location transitions** - Where setting changes
4. **Emotional pivot scenes** - Where tone shifts dramatically

## Validation Checklist

✓ All fields populated (no null values)
✓ Location matches reference_image_prompts.json locations
✓ Characters array uses lowercase names
✓ Panel structures have descriptions and focus
✓ Color palette has at least primary and secondary
✓ Visual motifs capture unique metaphors
✓ Transformation notes highlight special visual elements

---

This template ensures visual consistency across all 571 scenes!