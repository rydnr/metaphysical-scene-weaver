# 🎯 CRITICAL: ChatGPT Prompt Optimization Task

## The Problem
Our current JSON format may not work well when pasted into ChatGPT's prompt field. We need to ensure our scenes can be used effectively as prompts for image generation.

## Assigned To: Prompt-Artist

## Deliverables Needed

### 1. Master Prompt Template
Create a template that converts our scene format into ChatGPT-friendly prompts:
```
Instead of raw JSON, we need something like:
"Create a graphic novel panel showing: [scene description]
Characters: [character descriptions from JSON]
Setting: [location details]
Mood: [philosophical theme]
Style: [visual style references]"
```

### 2. Scene-to-Prompt Converter
Build a simple format that works when copy-pasted:
- No complex JSON parsing required
- Natural language that ChatGPT understands
- Preserves all important scene details
- Includes visual style cues

### 3. Test Cases
Test with actual scenes:
- Scene 171: "The Ontological Reversal"
- Scene 086: "The Swamp"
- Scene 132: "Guardian's Paradox"

### 4. Examples Directory
Create `/prompts/` with:
- `example-single-panel.txt`
- `example-multi-panel.txt`
- `template-master.txt`
- `conversion-guide.md`

## Success Criteria
- User can copy text and paste directly into ChatGPT
- Generated images match the philosophical themes
- No JSON parsing errors
- Consistent visual style across prompts

## Timeline
IMMEDIATE - This blocks the entire project!

## Testing Approach
1. Take existing scene JSON
2. Convert using template
3. Test in ChatGPT
4. Verify image matches intent
5. Iterate until perfect