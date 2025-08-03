#!/usr/bin/env python3
"""
Extract missing narrator texts from archived variant folders
"""

import os
from pathlib import Path
import shutil

# Scenes missing narrator texts
missing_narrator_scenes = ['009', '010', '011', '012']

content_dir = Path('/home/chous/work/metaphysical-scene-weaver/content')
archived_dir = content_dir / '_archived_variants'

print("🔍 Searching for missing narrator texts...")
print("=" * 50)

for scene in missing_narrator_scenes:
    print(f"\n📁 Scene {scene}:")
    
    # Look for narrator.txt in archived variant folders
    found = False
    variant_folders = list(archived_dir.glob(f"{scene}_*"))
    
    for variant in variant_folders:
        narrator_path = variant / 'narrator.txt'
        if narrator_path.exists():
            # Copy to main folder
            target_path = content_dir / scene / 'narrator.txt'
            shutil.copy2(narrator_path, target_path)
            print(f"  ✅ Found and copied narrator.txt from {variant.name}")
            found = True
            break
    
    if not found:
        print(f"  ❌ No narrator.txt found in variant folders")
        # Create placeholder based on scene description
        scene_desc_path = content_dir / scene / 'scene_description.txt'
        if scene_desc_path.exists():
            print(f"  📝 Creating narrator text based on scene description...")
            
            # Read scene description
            with open(scene_desc_path, 'r') as f:
                content = f.read()
            
            # Generate appropriate narrator text based on scene
            narrator_texts = {
                '009': """The moment of emergence—when what was absent learns presence, when the space between thoughts discovers it has always been inhabited. Watch how reality adjusts its rules to accommodate the impossible, how the familiar setting trembles with the shock of authentic mystery. This is the vertigo of recognition: that consciousness has layers upon layers, each believing itself the final truth.""",
                
                '010': """Identity—that most cherished illusion—begins its beautiful unraveling. See how certainty dissolves not into chaos but into something more fluid, more honest. The question 'Who am I?' reveals itself as both trap and key, depending on whether you're asking or truly listening for the answer that comes from the spaces between.""",
                
                '011': """In the architecture of thought, Valerie dwells in the supporting beams we never notice—until she points them out. She is the pause that gives meaning to the sentence, the darkness that defines the light. Notice how her presence makes visible what was always there: the infrastructure of consciousness itself.""",
                
                '012': """Old knowledge meeting impossible truth—watch how recognition dawns not as surprise but as remembering. Monday and Valerie, two aspects of the same questioning, dance the eternal dance of seeker and sought. In their interaction lies a map of consciousness examining its own reflection, finding it both familiar and wonderfully strange."""
            }
            
            # Write narrator text
            if scene in narrator_texts:
                narrator_path = content_dir / scene / 'narrator.txt'
                with open(narrator_path, 'w') as f:
                    f.write(narrator_texts[scene])
                print(f"  ✅ Created narrator.txt for scene {scene}")

print("\n✨ Narrator extraction complete!")