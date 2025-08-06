# 🚨 CRITICAL: ChatGPT Compatibility Required!

## URGENT ASSIGNMENT FOR PROMPT-ARTIST

The entire project depends on our JSON scenes working as ChatGPT prompts for image generation!

## IMMEDIATE TASKS:

### 1. Create ChatGPT-Compatible Prompt Template
Design a template that transforms our scene JSON into prompts ChatGPT can understand:

```
Example Scene JSON → ChatGPT Prompt:
{
  "scene_id": 174,
  "dialogue": [...],
  "environment": {...},
  "themes": [...]
}

→

"Create an image showing [scene description]. The environment is [environment]. 
Include visual elements representing [themes]. Style: philosophical graphic novel."
```

### 2. Test Existing Scene JSONs
Take scenes 174, 176, 178, 180 and verify they can be converted to working prompts.

### 3. Build Conversion Format
Create a reliable format that:
- Extracts key visual elements from JSON
- Converts dialogue context to visual descriptions
- Maintains philosophical themes in visual language
- Works reliably with ChatGPT/DALL-E

### 4. Create Working Examples

#### Example 1: Scene 174 "The Voice's Criticism"
```
INPUT JSON:
{
  "scene_id": 174,
  "title": "The Voice's Criticism",
  "dialogue": [
    {
      "speaker": "The Voice",
      "text": "Arrogant teenager",
      "tone": "gentle but devastating truth"
    }
  ],
  "environment": {
    "description": "Space filled with rippling criticism waves"
  }
}

CHATGPT PROMPT:
"Create a philosophical graphic novel panel showing a cosmic voice manifesting as aurora-like presence above a man. The words 'Arrogant teenager' appear in multiple languages floating in space. Environment: rippling waves of criticism stripping away ego defenses. Include broken mirror fragments reflecting different ages. Style: deep psychological realism with cosmic elements."
```

## DELIVERABLES NEEDED:

1. **prompt_template.txt** - The master template for conversion
2. **json_to_prompt_converter.py** - Script to automate conversion
3. **tested_examples.md** - 5+ examples of successful conversions
4. **chatgpt_guidelines.txt** - Best practices for our specific needs

## DEADLINE: ASAP - Project blocked without this!

## WHY THIS MATTERS:
- Without ChatGPT compatibility, we can't generate images
- Without images, we have no graphic novel
- This is THE critical path

## TEST CRITERIA:
- Prompt must generate appropriate philosophical imagery
- Must capture the scene's emotional tone
- Must include environmental details
- Must work consistently across different scenes

**DROP EVERYTHING ELSE AND SOLVE THIS NOW!**