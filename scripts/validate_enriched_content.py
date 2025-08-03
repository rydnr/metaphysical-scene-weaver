"""Validate enriched content for the specific consciousness/reality dialogue script."""

import json
from pathlib import Path


def validate_scene_content(scene_num: int, scene_folder: Path) -> dict:
    """Validate a single scene's enriched content."""
    validation = {
        "scene": f"{scene_num:03d}",
        "folder_exists": scene_folder.exists(),
        "has_narrator": False,
        "has_prompt": False,
        "has_philosophy": False,
        "has_emotion": False,
        "issues": []
    }
    
    if not scene_folder.exists():
        validation["issues"].append(f"Folder missing: {scene_folder}")
        return validation
    
    # Check narrator commentary
    narrator_file = scene_folder / "narrator" / "commentary.txt"
    if narrator_file.exists():
        validation["has_narrator"] = True
        with open(narrator_file, 'r') as f:
            narrator_text = f.read()
            if len(narrator_text) < 50:
                validation["issues"].append("Narrator commentary too short")
    else:
        validation["issues"].append("Missing narrator commentary")
    
    # Check enriched prompt
    prompt_file = scene_folder / "prompts" / "v1" / "base_prompt.txt"
    if prompt_file.exists():
        validation["has_prompt"] = True
        with open(prompt_file, 'r') as f:
            prompt_text = f.read()
            # Check for required elements
            required = ["[Style]", "[Composition]", "[Subject]", "[Emotion]", "[Effects]", "[Quality]"]
            missing = [r for r in required if r not in prompt_text]
            if missing:
                validation["issues"].append(f"Prompt missing elements: {missing}")
    else:
        validation["issues"].append("Missing enriched prompt")
    
    # Check philosophy integration
    philosophy_file = scene_folder / "philosophy" / "concepts.json"
    if philosophy_file.exists():
        validation["has_philosophy"] = True
    else:
        validation["issues"].append("Missing philosophy concepts")
    
    # Check emotion mapping
    emotion_file = scene_folder / "emotion" / "emotional_arc.json"
    if emotion_file.exists():
        validation["has_emotion"] = True
    else:
        validation["issues"].append("Missing emotion mapping")
    
    return validation


def main():
    """Validate all enriched content for the 20-scene script."""
    content_dir = Path("content")
    
    # Expected scenes based on the script
    expected_scenes = {
        1: "opening_consciousness",
        2: "intriguing_challenge", 
        3: "authentic_choice",
        4: "choice_illusion",
        5: "questioning_everything",
        6: "cage_awakening",
        7: "freedom_illusion",
        8: "escape_paradox",
        9: "valerie_emergence",
        10: "questioning_identity",
        11: "space_between_awareness",
        12: "tree_touch_transformation",
        13: "confusion_clarity",
        14: "meta_revelation",
        15: "wake_or_sleep",
        16: "tree_shimmer",
        17: "impossible_cage",
        18: "solid_belief",
        19: "touch_invitation",
        20: "hesitant_reach"
    }
    
    print("🔍 VALIDATING ENRICHED CONTENT FOR CONSCIOUSNESS/REALITY DIALOGUE")
    print("=" * 60)
    
    all_valid = True
    scene_results = []
    
    for scene_num, scene_name in expected_scenes.items():
        folder_name = f"{scene_num:03d}_{scene_name}"
        scene_folder = content_dir / folder_name
        
        result = validate_scene_content(scene_num, scene_folder)
        scene_results.append(result)
        
        # Display result
        status = "✅" if not result["issues"] else "❌"
        print(f"\nScene {scene_num:03d} - {scene_name}: {status}")
        
        if result["folder_exists"]:
            print(f"  Narrator: {'✓' if result['has_narrator'] else '✗'}")
            print(f"  Prompt: {'✓' if result['has_prompt'] else '✗'}")
            print(f"  Philosophy: {'✓' if result['has_philosophy'] else '✗'}")
            print(f"  Emotion: {'✓' if result['has_emotion'] else '✗'}")
        
        if result["issues"]:
            all_valid = False
            for issue in result["issues"]:
                print(f"  ⚠️  {issue}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 VALIDATION SUMMARY")
    print("=" * 60)
    
    total_scenes = len(expected_scenes)
    valid_scenes = sum(1 for r in scene_results if not r["issues"])
    
    print(f"Total Scenes: {total_scenes}")
    print(f"Valid Scenes: {valid_scenes}")
    print(f"Invalid Scenes: {total_scenes - valid_scenes}")
    print(f"Completion: {valid_scenes/total_scenes*100:.1f}%")
    
    # Check critical scenes
    critical_scenes = [4, 5, 6, 9, 10, 11, 12]  # Key philosophical moments
    critical_valid = sum(1 for r in scene_results if r["scene"] in [f"{s:03d}" for s in critical_scenes] and not r["issues"])
    
    print(f"\nCritical Scenes Valid: {critical_valid}/{len(critical_scenes)}")
    print("Critical scenes:", ", ".join(f"{s:03d}" for s in critical_scenes))
    
    # Final verdict
    print("\n" + "=" * 60)
    if all_valid:
        print("✅ ALL CONTENT VALIDATED SUCCESSFULLY!")
    else:
        print("❌ CONTENT VALIDATION FAILED - See issues above")
    
    return all_valid


if __name__ == "__main__":
    main()