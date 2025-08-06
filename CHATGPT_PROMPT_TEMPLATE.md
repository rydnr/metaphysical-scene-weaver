# ChatGPT Prompt Template for Scene Conversion

## Master Template Structure:

```
"Create a [ASPECT RATIO] philosophical graphic novel panel for Scene [NUMBER]: '[TITLE]'.

Visual Elements:
- Characters: [CHARACTER DESCRIPTIONS WITH EMOTIONAL STATES]
- Environment: [DETAILED ENVIRONMENT DESCRIPTION]
- Mood: [EMOTIONAL ATMOSPHERE]
- Key Action: [WHAT'S HAPPENING]

Artistic Style: [STYLE DESCRIPTORS]

Important Details:
[SPECIFIC VISUAL ELEMENTS FROM JSON]

Philosophical Theme: [THEME VISUALIZATION]"
```

## Quick Conversion Formula:

### From JSON Elements:
1. `scene_id` → Scene number reference
2. `title` → Context for the image
3. `characters` → Visual character descriptions
4. `dialogue` → Extract emotional/visual cues
5. `environment.description` → Direct environment details
6. `environment.mood` → Atmospheric instructions
7. `themes` → Abstract concepts to visualize

### Example Conversion:

**JSON Input:**
```json
{
  "scene_id": 176,
  "title": "Mirror's Mercy",
  "dialogue": [
    {"speaker": "Evan", "text": "[wordless scream of recognition]"}
  ],
  "environment": {
    "description": "Multiple mirrors showing different selves",
    "mood": "confrontational yet healing"
  },
  "themes": ["shadow integration", "self-acceptance"]
}
```

**ChatGPT Prompt Output:**
```
"Create a 16:9 philosophical graphic novel panel for Scene 176: 'Mirror's Mercy'.

Visual Elements:
- Characters: A man (Evan) screaming in recognition as he faces multiple reflections of himself, including a dark shadow version
- Environment: A space filled with mirrors at various angles, each showing different aspects of the same person - some light, some dark
- Mood: Intense confrontation transitioning to acceptance, harsh but ultimately healing
- Key Action: The moment of recognizing one's shadow self in the mirror

Artistic Style: Psychological realism with surreal elements, high contrast between light and shadow aspects

Important Details:
- Multiple mirror reflections showing different emotional states
- One prominent dark/shadow figure emerging from a mirror
- Gradual merging of light and dark elements
- Expression shifting from horror to recognition

Philosophical Theme: Visualize shadow integration - the dark aspects we reject are part of our wholeness"
```

## Critical Success Factors:

1. **Be Specific** - Vague prompts create generic images
2. **Include Emotion** - ChatGPT responds well to emotional descriptors
3. **Describe Action** - Static descriptions create boring panels
4. **Add Style Notes** - Ensures consistent graphic novel aesthetic
5. **Philosophical Elements** - Must be translated to visual metaphors

## Common Pitfalls to Avoid:
- ❌ Don't use abstract philosophy terms without visual translation
- ❌ Don't assume ChatGPT knows our characters
- ❌ Don't forget environmental details
- ❌ Don't make prompts too long (500 words max)
- ❌ Don't forget to specify graphic novel style

## Testing Checklist:
- [ ] Prompt generates appropriate scene imagery
- [ ] Characters are recognizable and consistent
- [ ] Environment matches scene description
- [ ] Emotional tone is captured
- [ ] Philosophical theme is visually represented
- [ ] Style is appropriate for graphic novel

**USE THIS TEMPLATE FOR EVERY SCENE!**