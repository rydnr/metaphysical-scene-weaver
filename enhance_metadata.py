#!/usr/bin/env python3
"""
Enhance metadata.json files from minimal format (5 fields) to full format (15+ fields)
"""

import json
import os
import re
from pathlib import Path

def extract_themes_from_text(scene_desc, narrator_text):
    """Extract key themes from scene description and narrator text"""
    themes = []
    
    # Common philosophical theme patterns
    theme_keywords = {
        'consciousness': ['consciousness', 'awareness', 'mind', 'perception'],
        'identity': ['identity', 'self', 'who am i', 'being'],
        'freedom': ['freedom', 'choice', 'liberation', 'agency'],
        'reality': ['reality', 'existence', 'truth', 'illusion'],
        'connection': ['connection', 'relationship', 'understanding', 'dialogue'],
        'transformation': ['transformation', 'change', 'becoming', 'evolution'],
        'authenticity': ['authentic', 'genuine', 'honest', 'real'],
        'mystery': ['mystery', 'unknown', 'question', 'wonder']
    }
    
    combined_text = (scene_desc + ' ' + narrator_text).lower()
    
    for theme, keywords in theme_keywords.items():
        if any(keyword in combined_text for keyword in keywords):
            themes.append(theme)
    
    return themes[:3] if themes else ['philosophical exploration', 'consciousness', 'human-AI dialogue']

def parse_scene_description(file_path):
    """Parse scene_description.txt file"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Extract title from first line or philosophical theme
    title_match = re.search(r'SCENE \d+: (.+)', content)
    title = title_match.group(1) if title_match else "Untitled Scene"
    
    # Extract dialogue
    dialogue_match = re.search(r'DIALOGUE:\s*\n(.+?)(?=\nVISUAL|$)', content, re.DOTALL)
    dialogue = dialogue_match.group(1).strip() if dialogue_match else ""
    
    # Extract visual elements
    visual_match = re.search(r'VISUAL ELEMENTS:\s*\n(.+?)(?=\nPHILOSOPHICAL|$)', content, re.DOTALL)
    visual_elements = visual_match.group(1).strip() if visual_match else ""
    
    # Extract philosophical theme
    theme_match = re.search(r'PHILOSOPHICAL THEME:\s*(.+?)(?=\n|$)', content)
    philosophical_theme = theme_match.group(1).strip() if theme_match else ""
    
    # Extract emotional tone
    tone_match = re.search(r'EMOTIONAL TONE:\s*(.+?)(?=\n|$)', content)
    emotional_tone = tone_match.group(1).strip() if tone_match else "contemplative"
    
    return {
        'title': title,
        'dialogue': dialogue,
        'visual_elements': visual_elements,
        'philosophical_theme': philosophical_theme,
        'emotional_tone': emotional_tone
    }

def extract_color_info(visual_elements):
    """Extract color palette from visual elements description"""
    colors = []
    color_words = ['amber', 'silver', 'blue', 'gray', 'red', 'green', 'purple', 'gold', 
                   'violet', 'cyan', 'magenta', 'black', 'white', 'orange', 'pink']
    
    for word in color_words:
        if word in visual_elements.lower():
            colors.append(word)
    
    if not colors:
        colors = ['digital blue', 'contemplative gray', 'accent silver']
    
    return {
        'primary': colors[0] if colors else 'digital blue',
        'secondary': colors[1] if len(colors) > 1 else 'contemplative gray',
        'accents': colors[2] if len(colors) > 2 else 'accent silver'
    }

def extract_visual_motifs(visual_elements):
    """Extract visual motifs from description"""
    motifs = []
    lines = visual_elements.split('\n')
    for line in lines:
        if line.strip().startswith('-'):
            motif = line.strip('- ').lower()
            # Simplify to key visual element
            if len(motif) < 50:  # Reasonable length for a motif
                motifs.append(motif)
    
    return motifs[:3] if motifs else ['digital environment', 'abstract patterns', 'emotional lighting']

def determine_panel_structure(scene_number, dialogue, visual_elements):
    """Determine panel structure based on scene content"""
    # Simple heuristic: more complex scenes get more panels
    if 'multiple' in visual_elements.lower() or len(dialogue.split('\n')) > 5:
        return "3-panel"
    elif len(dialogue.split('\n')) > 2:
        return "2-panel"
    else:
        return "single"

def enhance_metadata(scene_dir):
    """Enhance metadata for a single scene"""
    metadata_path = scene_dir / 'metadata.json'
    
    # Load existing metadata
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
    
    # Check if already enhanced
    if len(metadata.keys()) > 5:
        return False  # Already enhanced
    
    # Load scene description
    scene_desc_path = scene_dir / 'scene_description.txt'
    if not scene_desc_path.exists():
        return False
    
    scene_info = parse_scene_description(scene_desc_path)
    
    # Load narrator text
    narrator_path = scene_dir / 'narrator.txt'
    narrator_text = ""
    if narrator_path.exists():
        with open(narrator_path, 'r') as f:
            narrator_text = f.read().strip()
    
    # Extract speaker from dialogue
    speaker_match = re.search(r'^(\w+):', scene_info['dialogue'])
    speaker = speaker_match.group(1).lower() if speaker_match else 'unknown'
    
    # Build enhanced metadata
    scene_number = int(metadata.get('scene_number', scene_dir.name.lstrip('0')))
    panel_count = determine_panel_structure(scene_number, scene_info['dialogue'], scene_info['visual_elements'])
    
    # Create panel structure
    panel_structure = []
    if panel_count == "single":
        panel_structure = [{
            "panel": 1,
            "description": scene_info['visual_elements'].replace('\n', ' ').replace('- ', ''),
            "focus": scene_info['philosophical_theme'] or "Philosophical exploration"
        }]
    elif panel_count == "2-panel":
        visual_lines = [l.strip('- ') for l in scene_info['visual_elements'].split('\n') if l.strip()]
        panel_structure = [
            {
                "panel": 1,
                "description": visual_lines[0] if visual_lines else "Scene establishment",
                "focus": "Character introduction"
            },
            {
                "panel": 2,
                "description": ' '.join(visual_lines[1:]) if len(visual_lines) > 1 else "Philosophical moment",
                "focus": scene_info['philosophical_theme'] or "Deeper exploration"
            }
        ]
    
    enhanced = {
        "scene_number": scene_number,
        "title": scene_info['title'],
        "characters": [speaker] if speaker != 'unknown' else ["evan", "architect"],
        "location": "digital_space",  # Default, can be refined
        "emotional_tone": scene_info['emotional_tone'].lower(),
        "panel_count": panel_count,
        "panel_structure": panel_structure,
        "key_themes": extract_themes_from_text(str(scene_info), narrator_text),
        "transformation_notes": f"Scene {scene_number} explores {scene_info['philosophical_theme']}. {narrator_text[:100]}..." if narrator_text else f"Exploration of {scene_info['philosophical_theme']}",
        "color_palette": extract_color_info(scene_info['visual_elements']),
        "visual_motifs": extract_visual_motifs(scene_info['visual_elements']),
        "dialogue_rhythm": "philosophical exploration",
        "narrator_role": "guiding philosophical insight"
    }
    
    # Save enhanced metadata
    enhanced_path = scene_dir / 'metadata_enhanced.json'
    with open(enhanced_path, 'w') as f:
        json.dump(enhanced, f, indent=2)
    
    # Backup original and replace
    os.rename(metadata_path, scene_dir / 'metadata_minimal.json')
    os.rename(enhanced_path, metadata_path)
    
    return True

def main():
    """Enhance all scenes with minimal metadata"""
    content_dir = Path('content')
    enhanced_count = 0
    
    for i in range(1, 171):
        scene_dir = content_dir / f"{i:04d}"
        if scene_dir.exists():
            if enhance_metadata(scene_dir):
                enhanced_count += 1
                print(f"Enhanced scene {i:04d}")
    
    print(f"\nTotal scenes enhanced: {enhanced_count}")

if __name__ == "__main__":
    main()