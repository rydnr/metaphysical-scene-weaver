#!/usr/bin/env python3
"""
Distribute emotion atmospheres to individual scene folders
"""

from pathlib import Path
import re

content_dir = Path('/home/chous/work/metaphysical-scene-weaver/content')
atmospheres_file = content_dir / 'all_emotion_atmospheres.txt'

print("🎨 Distributing emotion atmospheres to scenes...")
print("=" * 50)

# Read the atmospheres file
with open(atmospheres_file, 'r') as f:
    content = f.read()

# Split by scene
scene_pattern = r'=== SCENE (\d{3}) ===(?:\s*\[([^\]]+)\])?'
scenes = re.split(scene_pattern, content)[1:]  # Skip header

# Process scenes in groups of 3 (number, optional tag, content)
for i in range(0, len(scenes), 3):
    if i + 2 < len(scenes):
        scene_num = scenes[i]
        tag = scenes[i + 1] if scenes[i + 1] else ""
        atmosphere_text = scenes[i + 2].strip()
        
        # Write to scene folder
        scene_folder = content_dir / scene_num
        if scene_folder.exists():
            emotion_file = scene_folder / 'emotion_atmosphere.txt'
            
            # Format the content
            if tag:
                formatted_content = f"[{tag}]\n\n{atmosphere_text}"
            else:
                formatted_content = atmosphere_text
            
            with open(emotion_file, 'w') as f:
                f.write(formatted_content)
            
            print(f"✅ Scene {scene_num}: Created emotion_atmosphere.txt{' [' + tag + ']' if tag else ''}")
        else:
            print(f"❌ Scene {scene_num}: Folder not found")

print("\n✨ Emotion distribution complete!")