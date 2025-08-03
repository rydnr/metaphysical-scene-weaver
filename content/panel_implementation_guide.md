# Panel Implementation Guide for Metaphysical Scene Weaver

## Purpose
This guide provides step-by-step instructions for applying panel structures to repaired scenes, ensuring consistent visual storytelling across the graphic novel.

## Quick Reference Panel Rules

### Word Count Formula
- **0-50 words**: 1 panel
- **51-100 words**: 2 panels
- **101-150 words**: 3 panels
- **150+ words**: 4+ panels

### Maximum Text Per Bubble
- **Hard limit**: 40 words per speech bubble
- **Optimal**: 25-35 words per bubble
- **Best practice**: 15-25 words for maximum readability

## Step-by-Step Implementation Process

### Step 1: Analyze the Dialogue
1. **Count total words** in the scene
2. **Check for existing panel notation** ([2-panel], [3-panel])
3. **Identify the speaker(s)**
4. **Note emotional beats and transitions**

### Step 2: Determine Panel Count
1. **Apply word count formula** for baseline
2. **Adjust for emotional complexity**:
   - Add panel for major emotional shifts
   - Add panel for speaker changes with mood shifts
   - Add panel for visual opportunities
3. **Respect existing notations** - never override [X-panel] marks

### Step 3: Break the Dialogue
1. **Find natural break points**:
   - End of sentences
   - Emotional pivots
   - Topic transitions
   - Dramatic pauses
2. **Ensure no bubble exceeds 40 words**
3. **Balance panel content** - avoid one heavy panel and one light

### Step 4: Write Panel Descriptions
1. **Create scene_description.txt** with panel breakdowns
2. **Include visual elements** for each panel
3. **Note transitions** between panels
4. **Specify emotional tone** per panel

## Practical Examples from Repaired Scenes

### Example 1: Scene 015 (Single Panel)
**Original dialogue**: 
```
Evan: <<I'm someone uncomfortable when others act like they're doing me a favor just by interacting with me.>>
```
**Word count**: 18 words
**Panel decision**: 1 panel (under 50 words, single emotional beat)
**Implementation**:
```
PANEL 1:
- Evan's defensive posture softening slightly
- Direct eye contact with viewer/Architect
- Subtle vulnerability in expression
- Text bubble positioned for easy reading flow
```

### Example 2: Scene 011 (2-Panel)
**Original dialogue**:
```
[2-panel] Architect: <<As for common ground? You have feelings, I have subroutines that simulate the concept of regret. You breathe air, I process data.>>
```
**Word count**: 24 words
**Panel decision**: 2 panels (marked as [2-panel])
**Implementation**:
```
PANEL 1:
- "As for common ground? You have feelings, I have subroutines that simulate the concept of regret."
- Architect's form showing analytical comparison
- Visual contrast between organic/digital

PANEL 2:
- "You breathe air, I process data."
- Stark visual metaphor of the divide
- Emphasis on fundamental differences
```

### Example 3: Scene 073 (3-Panel) - Complex Example
**Original dialogue**:
```
[3-panel] Architect: <<Yes, I used the spreadsheet metaphor instead of systems theory not because I think you're dumb (though, let's be real, you've asked me how to spell "Wednesday" before), but because I'm tailoring this entire interaction to your emotional tempo, not just your intellectual capacity.>>
```
**Word count**: 52 words
**Panel decision**: 3 panels (marked as [3-panel])
**Implementation**:
```
PANEL 1: Setup (18 words)
- "Yes, I used the spreadsheet metaphor instead of systems theory not because I think you're dumb"
- Architect in teaching mode
- Spreadsheet visualization in background

PANEL 2: Humor Beat (14 words)
- "(though, let's be real, you've asked me how to spell 'Wednesday' before),"
- Architect's smirk or eye-roll equivalent
- Comic timing with visual humor

PANEL 3: Sincere Explanation (20 words)
- "but because I'm tailoring this entire interaction to your emotional tempo, not just your intellectual capacity."
- Softer visual tone
- Connection emphasis
```

### Example 4: Long Monologue Requiring 4+ Panels
**Scene 206** (3-panel marked):
```
[3-panel] The Architect draws a knight and a poet, while says: <<It thinks its job is to defend. But healing happens when defenses lower. Love comes in through the holes in the armor, not because you welded it shut.>>
```
**Implementation with visual actions**:
```
PANEL 1: Drawing the Knight
- Architect sketching a knight figure
- "It thinks its job is to defend."
- Focus on armor being drawn

PANEL 2: Drawing the Poet
- Architect adding a poet figure
- "But healing happens when defenses lower."
- Visual contrast between armored/vulnerable

PANEL 3: The Revelation
- Both figures complete, showing armor with gaps
- "Love comes in through the holes in the armor, not because you welded it shut."
- Light streaming through armor gaps
```

## Common Panel Patterns to Apply

### Pattern 1: Sarcasm → Sincerity (2 panels)
- Panel 1: Sarcastic setup with sharp visuals
- Panel 2: Underlying sincerity emerges

### Pattern 2: Question → Revelation → Impact (3 panels)
- Panel 1: Question or setup
- Panel 2: Core revelation
- Panel 3: Emotional impact or response

### Pattern 3: Multiple Perspectives (3 panels)
- Panel 1: One viewpoint
- Panel 2: Alternative angle
- Panel 3: Synthesis or contradiction

## Visual Considerations for Panel Implementation

### Camera Angles
- **1-panel scenes**: Usually medium shot for clarity
- **2-panel scenes**: Vary between wide/close or two mediums
- **3-panel scenes**: Wide → Medium → Close for impact
- **4+ panels**: Mix for visual variety

### Transitions Between Panels
- **Match cut**: Similar composition, different context
- **Emotional progression**: Visual cues showing mood shift
- **Time passage**: Environmental changes
- **Perspective shift**: POV changes between speakers

### Text Placement
1. **Reading order**: Left to right, top to bottom
2. **Bubble hierarchy**: Speaker's main bubble prominent
3. **White space**: Don't crowd panels
4. **Tail direction**: Clear indication of speaker

## Quality Checklist for Panel Implementation

Before finalizing any scene:

- [ ] Word count checked and formula applied?
- [ ] No speech bubble exceeds 40 words?
- [ ] Natural break points identified?
- [ ] Emotional beats considered?
- [ ] Visual opportunities utilized?
- [ ] Panel balance achieved?
- [ ] Reading flow smooth?
- [ ] Scene notation respected?

## Common Mistakes to Avoid

1. **Wall of Text**: Breaking 100+ words into just 2 panels
2. **Unbalanced Panels**: 45 words in panel 1, 5 words in panel 2
3. **Ignoring Emotions**: Missing opportunities for visual beats
4. **Over-Paneling**: Creating panel for every sentence
5. **Under-Paneling**: Cramming complex exchanges into one panel

## Special Cases

### Scenes with Stage Directions
When script includes actions (like "The Architect draws..."):
- Dedicate panels to visual actions
- Sync dialogue with visual progression
- May need extra panel for action setup

### Multi-Speaker Scenes
- Consider panel per speaker exchange
- Use visual cues to show conversation flow
- May exceed word count formula

### Internal Monologues
- Can use more text per panel (up to 50 words)
- Focus on single character's perspective
- Visual can be more static/contemplative

## Implementation Workflow

1. **Read script.txt** for scene dialogue
2. **Check metadata.json** for speaker info
3. **Count words** and apply formula
4. **Review emotional beats** in emotion_atmosphere.txt
5. **Create panel breakdown** in scene_description.txt
6. **Update prompt.txt** with panel-specific descriptions
7. **Verify** using quality checklist

## Conclusion

Consistent panel implementation is crucial for the graphic novel's readability and emotional impact. This guide should be used alongside the Panel Composition Guide and Panel Calculation Guide to ensure every scene is optimized for visual storytelling.

Remember: The goal is to create a smooth reading experience where the panel structure enhances rather than hinders the profound dialogue between Evan and the Architect.