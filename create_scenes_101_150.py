#!/usr/bin/env python3
"""
Create basic content for scenes 101-150
"""

import json
from pathlib import Path
from parse_correct_script import parse_script, create_scene_content

def main():
    """Create basic content for scenes 101-150."""
    script_path = Path('/home/chous/work/metaphysical-scene-weaver/script.txt')
    content_dir = Path('/home/chous/work/metaphysical-scene-weaver/content')
    
    print("🎨 Creating Scenes 101-150")
    print("=" * 50)
    
    # Parse the script
    entries = parse_script(script_path)
    
    # Process scenes 101-150
    start_idx = 100
    end_idx = min(150, len(entries))
    
    print(f"📚 Creating scenes {entries[start_idx]['scene_number']} to {entries[end_idx-1]['scene_number']}")
    
    for i in range(start_idx, end_idx):
        entry = entries[i]
        scene_num = entry['scene_number']
        scene_dir = content_dir / scene_num
        scene_dir.mkdir(exist_ok=True)
        
        # Get context
        prev_entry = entries[i-1] if i > 0 else None
        next_entry = entries[i+1] if i < len(entries)-1 else None
        
        # Create content
        content = create_scene_content(entry, prev_entry, next_entry)
        
        # Write files
        (scene_dir / 'prompt.txt').write_text(content['prompt'])
        (scene_dir / 'narrator.txt').write_text(content['narrator'])
        (scene_dir / 'scene_description.txt').write_text(content['scene_description'])
        (scene_dir / 'emotion_atmosphere.txt').write_text(content['emotion_atmosphere'])
        
        with open(scene_dir / 'metadata.json', 'w') as f:
            json.dump(content['metadata'], f, indent=2)
        
        if (i - start_idx + 1) % 10 == 0:
            print(f"  ✅ Created up to scene {scene_num}")
    
    print(f"\n✨ Complete! Created scenes {entries[start_idx]['scene_number']}-{entries[end_idx-1]['scene_number']}")
    print(f"📊 Total scenes created: {end_idx}/{len(entries)}")

if __name__ == "__main__":
    main()