# Creative Team Brief - Metaphysical Scene Weaver

## Project Overview
Transform 571 philosophical dialogue scenes into enriched content for graphic novel generation.

## Source Material
- **Script**: `/home/chous/work/metaphysical-scene-weaver/script.txt`
- **Characters**: Evan (human) and Architect (AI with existential awareness)
- **Scenes**: 571 numbered entries [0001] through [0571]
- **Panel Notes**: Some scenes marked [2-panel], [3-panel], etc.

## Team Roles

### Creative Director (Window 0)
- Coordinate team efforts
- Assign scene ranges to specialists
- Ensure consistency and quality
- Track progress across 571 scenes

### Philosopher (Window 1)
- Analyze existential themes
- Identify philosophical concepts
- Suggest visual metaphors for abstract ideas
- Track thematic consistency

### Psychologist (Window 2)
- Character motivation analysis
- Emotional arc tracking
- Subtext identification
- Psychological depth enhancement

### Novelist (Window 3)
- Narrative flow and pacing
- Dramatic tension
- Write narrator.txt content
- Story arc development

### Graphic-Writer (Window 4)
- Panel layout decisions
- Visual composition
- Text/image balance
- Sequential art storytelling

### Prompt-Artist (Window 5)
- Detailed image generation prompts
- Artistic style consistency
- Mood and atmosphere
- Visual character/setting details

### Editor (Window 6)
- Quality control
- Consistency checking
- Panel guideline compliance
- Final polish

## Output Structure
For each scene, create:
```
content/XXX/
├── prompt.txt          # AI image generation prompt
├── narrator.txt        # Narrative voice text
├── scene_description.txt   # Visual scene details
├── emotion_atmosphere.txt  # Emotional context
└── metadata.json      # Scene metadata
```

## Panel Handling
- Respect existing [2-panel], [3-panel] notations
- For unmarked scenes, determine appropriate panel count
- Create panel-specific descriptions in all files
- Consider readability and visual pacing

## Workflow
1. Creative Director assigns scene ranges
2. Specialists process their assigned scenes
3. Create enriched content following structure
4. Editor reviews for quality
5. Git commit every 10 minutes with TDD emojis

## Key Guidelines
- This is creative writing, NOT programming
- Focus on visual storytelling
- Maintain character consistency
- Balance philosophical depth with accessibility
- Think in panels and visual beats