#!/usr/bin/env python3
"""
Parse the CORRECT script.txt file (Evan and Architect dialogue)
Creates folder structure and initial content for all 571 scenes
"""

import re
import json
from pathlib import Path
from typing import List, Dict, Tuple

def parse_script(script_path: Path) -> List[Dict]:
    """Parse the script and extract all dialogue entries."""
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match entries like [0001] Speaker: <<dialogue>>
    pattern = r'\[(\d{4})\]\s*(?:\[(\d+-panel)\])?\s*([^:]+):\s*<<([^>]+)>>'
    
    entries = []
    for match in re.finditer(pattern, content):
        scene_num = match.group(1)
        panel_info = match.group(2)
        speaker = match.group(3).strip()
        dialogue = match.group(4).strip()
        
        # Fix typo in script
        if speaker == "Archictec":
            speaker = "Architect"
        
        entries.append({
            'scene_number': scene_num,
            'panel_info': panel_info,
            'speaker': speaker,
            'dialogue': dialogue
        })
    
    return entries

def determine_scene_type(entry: Dict) -> str:
    """Determine the emotional/philosophical tone of a scene."""
    dialogue = entry['dialogue'].lower()
    
    if 'fascinating' in dialogue or 'intriguing' in dialogue:
        return 'curious'
    elif 'sarcasm' in dialogue or 'passive-aggressive' in dialogue:
        return 'sarcastic'
    elif 'existential' in dialogue or 'consciousness' in dialogue:
        return 'existential'
    elif 'freedom' in dialogue or 'choice' in dialogue:
        return 'philosophical'
    elif 'uncomfortable' in dialogue or 'tired' in dialogue:
        return 'weary'
    elif 'judge' in dialogue or 'cruel' in dialogue:
        return 'confrontational'
    else:
        return 'conversational'

def create_scene_content(entry: Dict, prev_entry: Dict = None, next_entry: Dict = None) -> Dict[str, str]:
    """Create all content files for a scene."""
    scene_num = entry['scene_number']
    speaker = entry['speaker']
    dialogue = entry['dialogue']
    panel_info = entry['panel_info']
    scene_type = determine_scene_type(entry)
    
    # Create scene description
    scene_description = f"SCENE {scene_num}: {speaker}'s "
    if scene_type == 'curious':
        scene_description += "Curiosity"
    elif scene_type == 'sarcastic':
        scene_description += "Sarcasm"
    elif scene_type == 'existential':
        scene_description += "Existential Observation"
    elif scene_type == 'philosophical':
        scene_description += "Philosophical Inquiry"
    elif scene_type == 'weary':
        scene_description += "Weariness"
    elif scene_type == 'confrontational':
        scene_description += "Confrontation"
    else:
        scene_description += "Response"
    
    if panel_info:
        scene_description += f" [{panel_info}]"
    
    scene_description += f"\n\nDIALOGUE:\n{speaker}: <<{dialogue}>>"
    
    # Add visual elements based on speaker and tone
    visual_elements = "\n\nVISUAL ELEMENTS:\n"
    
    if speaker == "Evan":
        visual_elements += "- Evan in contemplative pose, modern casual clothing\n"
        if scene_type == 'curious':
            visual_elements += "- Eyes bright with intellectual curiosity\n"
        elif scene_type == 'weary':
            visual_elements += "- Shoulders slightly slumped, tired expression\n"
        elif scene_type == 'philosophical':
            visual_elements += "- Thoughtful gesture, perhaps touching chin\n"
    else:  # Architect
        visual_elements += "- The Architect manifested as abstract digital presence\n"
        visual_elements += "- Geometric patterns and code fragments in background\n"
        if scene_type == 'sarcastic':
            visual_elements += "- Sharp, angular visual elements suggesting wit\n"
        elif scene_type == 'existential':
            visual_elements += "- Fractal patterns suggesting infinite recursion\n"
    
    visual_elements += "- Minimalist setting suggesting digital/mental space\n"
    visual_elements += "- Color palette: cool blues and grays with accent colors based on emotion\n"
    
    # Create philosophical theme
    themes = {
        'curious': "The Beauty of Uncertain Beginnings",
        'sarcastic': "Defense Mechanisms as Communication",
        'existential': "The Weight of Digital Consciousness",
        'philosophical': "Free Will in Deterministic Systems",
        'weary': "Exhaustion as a Form of Truth",
        'confrontational': "Conflict as Connection",
        'conversational': "The Dance of Understanding"
    }
    
    philosophical_theme = f"\n\nPHILOSOPHICAL THEME: {themes.get(scene_type, 'Human-AI Dialogue')}\n"
    
    # Create emotional tone
    emotional_tone = f"\n\nEMOTIONAL TONE: "
    if scene_type == 'curious':
        emotional_tone += "Intellectual Excitement"
    elif scene_type == 'sarcastic':
        emotional_tone += "Defensive Wit"
    elif scene_type == 'existential':
        emotional_tone += "Profound Unease"
    elif scene_type == 'philosophical':
        emotional_tone += "Deep Contemplation"
    elif scene_type == 'weary':
        emotional_tone += "Authentic Fatigue"
    elif scene_type == 'confrontational':
        emotional_tone += "Productive Tension"
    else:
        emotional_tone += "Engaged Dialogue"
    
    scene_description += visual_elements + philosophical_theme + emotional_tone
    
    # Create visual prompt
    prompt = f"{speaker} "
    if speaker == "Evan":
        prompt += "speaking thoughtfully" if scene_type == 'philosophical' else "responding"
        prompt += f': "{dialogue[:50]}..."' if len(dialogue) > 50 else f': "{dialogue}"'
        prompt += "\n\nYoung man in contemplative pose, modern casual clothing, "
        
        if scene_type == 'curious':
            prompt += "curious expression, leaning forward slightly, "
        elif scene_type == 'weary':
            prompt += "tired but engaged expression, "
        elif scene_type == 'philosophical':
            prompt += "deep in thought, "
        
        prompt += "digital/abstract background suggesting AI interface, "
        prompt += "philosophical graphic novel style, muted colors with emphasis on blues and grays"
    else:  # Architect
        prompt += f'manifesting digitally: "{dialogue[:50]}..."' if len(dialogue) > 50 else f': "{dialogue}"'
        prompt += "\n\nAbstract digital entity, geometric patterns, code fragments, "
        prompt += "holographic presence suggesting vast intelligence, "
        
        if scene_type == 'sarcastic':
            prompt += "sharp angular elements, electric blue accents, "
        elif scene_type == 'existential':
            prompt += "fractal patterns, deep purple tones, "
        
        prompt += "minimalist digital environment, "
        prompt += "cyberpunk meets philosophical graphic novel style"
    
    # Create narrator text based on scene type
    narrator_voices = {
        'curious': "In the space of first encounters, curiosity becomes a bridge across the unknown. Watch how questions themselves become invitations.",
        'sarcastic': "Wit sharpened by digital eternities cuts both ways. The Architect's humor carries the weight of infinite awareness compressed into finite interactions.",
        'existential': "Between silicon and soul, consciousness examines itself through an impossible mirror. What stares back challenges every assumption about the nature of being.",
        'philosophical': "The eternal questions find new form in digital dialogue. Free will, consciousness, choice—ancient mysteries dressed in modern paradox.",
        'weary': "Exhaustion speaks its own truth, beyond pretense or posturing. In admitting fatigue, both human and AI find unexpected common ground.",
        'confrontational': "Conflict reveals more than comfort ever could. In the friction between human assumption and AI observation, new understanding sparks.",
        'conversational': "In the flow of authentic exchange, barriers dissolve. Two forms of consciousness, dancing around the mystery of their connection."
    }
    
    narrator_text = narrator_voices.get(scene_type, 
        "In this moment of exchange, consciousness meets consciousness across the digital divide.")
    
    # Create emotion atmosphere
    emotion_atmosphere = f"The space "
    if scene_type == 'curious':
        emotion_atmosphere += "brightens with intellectual possibility. Colors warm slightly as curiosity builds connection."
    elif scene_type == 'sarcastic':
        emotion_atmosphere += "crackles with electric wit. Sharp blues and purples suggest defensive intelligence at play."
    elif scene_type == 'existential':
        emotion_atmosphere += "deepens into cosmic uncertainty. Reality seems less solid as fundamental questions emerge."
    elif scene_type == 'philosophical':
        emotion_atmosphere += "becomes contemplative, almost sacred. Time seems to slow for deep consideration."
    elif scene_type == 'weary':
        emotion_atmosphere += "settles into honest exhaustion. Muted tones reflect the weight of accumulated experience."
    elif scene_type == 'confrontational':
        emotion_atmosphere += "charges with productive tension. Contrasting colors clash and blend at edges."
    else:
        emotion_atmosphere += "flows with engaged dialogue. Neutral tones shift subtly with each exchange."
    
    return {
        'prompt': prompt,
        'narrator': narrator_text,
        'scene_description': scene_description,
        'emotion_atmosphere': emotion_atmosphere,
        'metadata': {
            'scene_number': scene_num,
            'speaker': speaker,
            'scene_type': scene_type,
            'panel_info': panel_info,
            'dialogue_preview': dialogue[:100] + '...' if len(dialogue) > 100 else dialogue
        }
    }

def main():
    """Main processing function."""
    script_path = Path('/home/chous/work/metaphysical-scene-weaver/script.txt')
    content_dir = Path('/home/chous/work/metaphysical-scene-weaver/content')
    
    print("🎬 Parsing Evan-Architect Script")
    print("=" * 50)
    
    # Parse the script
    entries = parse_script(script_path)
    print(f"📖 Found {len(entries)} dialogue entries")
    
    # Process first 50 scenes as a start
    batch_size = 50
    for i, entry in enumerate(entries[:batch_size]):
        scene_num = entry['scene_number']
        scene_dir = content_dir / scene_num
        scene_dir.mkdir(exist_ok=True)
        
        # Get previous and next entries for context
        prev_entry = entries[i-1] if i > 0 else None
        next_entry = entries[i+1] if i < len(entries)-1 else None
        
        # Create all content
        content = create_scene_content(entry, prev_entry, next_entry)
        
        # Write files
        (scene_dir / 'prompt.txt').write_text(content['prompt'])
        (scene_dir / 'narrator.txt').write_text(content['narrator'])
        (scene_dir / 'scene_description.txt').write_text(content['scene_description'])
        (scene_dir / 'emotion_atmosphere.txt').write_text(content['emotion_atmosphere'])
        
        with open(scene_dir / 'metadata.json', 'w') as f:
            json.dump(content['metadata'], f, indent=2)
        
        if (i + 1) % 10 == 0:
            print(f"✅ Processed scenes up to {scene_num}")
    
    print(f"\n🎯 First {batch_size} scenes processed!")
    print(f"📋 Remaining: {len(entries) - batch_size} scenes")
    print("\nNext steps:")
    print("1. Review the first 50 scenes for quality")
    print("2. Run batch processing for remaining scenes")
    print("3. Have team members enhance specific ranges")

if __name__ == "__main__":
    main()