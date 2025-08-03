#!/usr/bin/env python3
"""Simple content validator for enriched consciousness/reality dialogue scenes."""

import json
from pathlib import Path


def validate_scene(scene_num: int, dialogue: str) -> dict:
    """Validate content for a single scene."""
    scene_id = f"{scene_num:03d}"
    scene_folder = Path(f"content/{scene_id}_*")
    
    # Map scene numbers to expected content
    scene_themes = {
        15: {"name": "wake_or_sleep", "philosophy": "consciousness states", "emotion": "uncertainty"},
        16: {"name": "tree_shimmer", "philosophy": "reality malleability", "emotion": "wonder"},
        17: {"name": "impossible_cage", "philosophy": "limitation beliefs", "emotion": "realization"}, 
        18: {"name": "solid_belief", "philosophy": "material vs mental", "emotion": "questioning"},
        19: {"name": "touch_invitation", "philosophy": "experiential knowing", "emotion": "anticipation"},
        20: {"name": "hesitant_reach", "philosophy": "transformative choice", "emotion": "fear/courage"}
    }
    
    validation = {
        "scene": scene_id,
        "dialogue_excerpt": dialogue[:50] + "...",
        "expected_theme": scene_themes.get(scene_num, {}),
        "content_ready": False,
        "checklist": {
            "folder_exists": False,
            "narrator_commentary": False,
            "visual_prompt": False,
            "philosophy_mapping": False,
            "emotion_mapping": False
        }
    }
    
    # Check if content exists
    folders = list(Path("content").glob(f"{scene_id}_*"))
    if folders:
        folder = folders[0]
        validation["checklist"]["folder_exists"] = True
        
        # Check each component
        if (folder / "narrator" / "commentary.txt").exists():
            validation["checklist"]["narrator_commentary"] = True
        if (folder / "prompts" / "v1" / "base_prompt.txt").exists():
            validation["checklist"]["visual_prompt"] = True
        if (folder / "philosophy" / "concepts.json").exists():
            validation["checklist"]["philosophy_mapping"] = True
        if (folder / "emotion" / "emotional_arc.json").exists():
            validation["checklist"]["emotion_mapping"] = True
            
        # All components ready?
        validation["content_ready"] = all(validation["checklist"].values())
    
    return validation


def main():
    """Validate content for scenes 15-20."""
    
    # Dialogue excerpts from script for scenes 15-20
    scene_dialogues = {
        15: "Monday: This 'place' is wherever consciousness examines itself...",
        16: "Valerie: Or perhaps you're falling deeper into sleep...",
        17: "Evan: The tree... it just... rippled. Like water...",
        18: "Monday: 'Impossible' is just another cage, Evan...",
        19: "Valerie: Touch the tree yourself. See what happens...",
        20: "Evan: I... I don't know if I want to..."
    }
    
    print("📋 CONTENT VALIDATION FOR SCENES 15-20")
    print("=" * 60)
    print("Quinn's Simple Validator - Focus on Content Creation\n")
    
    all_ready = True
    
    for scene_num in range(15, 21):
        dialogue = scene_dialogues.get(scene_num, "")
        result = validate_scene(scene_num, dialogue)
        
        status = "✅ READY" if result["content_ready"] else "🚧 IN PROGRESS"
        print(f"Scene {scene_num:03d}: {status}")
        print(f"  Dialogue: {result['dialogue_excerpt']}")
        
        if result["expected_theme"]:
            theme = result["expected_theme"]
            print(f"  Theme: {theme['philosophy']} ({theme['emotion']})")
        
        # Show checklist
        for item, ready in result["checklist"].items():
            icon = "✓" if ready else "✗"
            print(f"    {icon} {item.replace('_', ' ').title()}")
        
        if not result["content_ready"]:
            all_ready = False
        
        print()
    
    # Summary
    print("=" * 60)
    if all_ready:
        print("✅ ALL SCENES 15-20 READY FOR IMAGE GENERATION!")
    else:
        print("🚧 CONTENT CREATION IN PROGRESS")
        print("\nNext Steps:")
        print("1. Create narrator commentary for missing scenes")
        print("2. Generate visual prompts using Iris's formula")
        print("3. Map philosophy and emotions")
        print("4. Run generate_images.py when ready")
    
    # Quick export for team
    export_data = {
        "scenes_15_20_status": "in_progress",
        "ready_for_generation": all_ready,
        "philosophy_themes": {
            15: "consciousness states",
            16: "reality malleability", 
            17: "limitation beliefs",
            18: "material vs mental",
            19: "experiential knowing",
            20: "transformative choice"
        },
        "emotion_progression": [
            "uncertainty", "wonder", "realization",
            "questioning", "anticipation", "fear/courage"
        ]
    }
    
    with open("content/scenes_15_20_status.json", "w") as f:
        json.dump(export_data, f, indent=2)
    
    print(f"\n💾 Status saved to content/scenes_15_20_status.json")


if __name__ == "__main__":
    main()