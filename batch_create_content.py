#!/usr/bin/env python3
"""
Batch create basic content for remaining scenes (051-387)
This creates the folder structure and basic content that the team can then enhance
"""

import re
import json
from pathlib import Path
from typing import List, Dict

# Import functions from the previous script
from parse_correct_script import parse_script, determine_scene_type, create_scene_content

def main():
    """Create basic content for scenes 051-387."""
    script_path = Path('/home/chous/work/metaphysical-scene-weaver/script.txt')
    content_dir = Path('/home/chous/work/metaphysical-scene-weaver/content')
    
    print("📚 Batch Creating Content for Remaining Scenes")
    print("=" * 50)
    
    # Parse the script
    entries = parse_script(script_path)
    print(f"📖 Total entries: {len(entries)}")
    
    # Process scenes 51-100 first (for team to start enhancing)
    start_idx = 50
    end_idx = min(100, len(entries))
    
    print(f"\n🎬 Creating scenes {start_idx+1:03d} to {end_idx:03d}")
    
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
    
    print(f"\n✨ Batch complete! Created scenes {start_idx+1:03d}-{end_idx:03d}")
    print(f"📋 Scenes ready for team enhancement: 50")
    print(f"📊 Total scenes created so far: {end_idx}/{len(entries)}")

if __name__ == "__main__":
    main()