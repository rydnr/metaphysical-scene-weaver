"""Example script demonstrating the Metaphysical Scene Weaver system."""

from pathlib import Path
import json
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.scene_weaver import SceneWeaver
from src.core.script_parser import ScriptParser


def main():
    """Run example processing."""
    # Paths
    script_path = Path("examples/sample_script.txt")
    characters_path = Path("characters.json")
    places_path = Path("places.json")
    output_dir = Path("examples/output")
    
    # Check files exist
    if not all([script_path.exists(), characters_path.exists(), places_path.exists()]):
        print("Error: Required files not found!")
        print(f"Script: {script_path.exists()}")
        print(f"Characters: {characters_path.exists()}")
        print(f"Places: {places_path.exists()}")
        return
    
    print("=== Metaphysical Scene Weaver Example ===\n")
    
    # Initialize the weaver
    print("Initializing Scene Weaver...")
    weaver = SceneWeaver(
        characters_file=characters_path,
        places_file=places_path,
        style="graphic novel"
    )
    
    # Process the script
    print(f"Processing script: {script_path}")
    scenes = weaver.process_script(script_path)
    print(f"Processed {len(scenes)} scenes\n")
    
    # Display first few scenes
    for i, scene in enumerate(scenes[:3]):
        print(f"=== Scene {scene.entry_id} ===")
        print(f"Speaker: {scene.metadata['speaker']}")
        print(f"Philosophical Depth: {scene.philosophy.get('depth_level', 0)}")
        print(f"Primary Concept: {scene.philosophy.get('primary_concept', 'None')}")
        print(f"Emotional State: {scene.emotion.get('primary', 'neutral')}")
        
        print(f"\nGenerated Prompt:")
        print(f"{scene.prompt[:200]}...")
        
        if scene.visual_elements:
            print(f"\nSpecial Visual Elements:")
            for element in scene.visual_elements[:3]:
                print(f"  • {element}")
        
        print("\n" + "-"*50 + "\n")
    
    # Export all prompts
    print(f"Exporting all prompts to: {output_dir}/")
    weaver.export_prompts(output_dir)
    
    # Generate character arc summaries
    print("\n=== Character Arc Summaries ===")
    for character_name in ['evan', 'monday', 'valerie']:
        arc_summary = weaver.state_tracker.generate_arc_summary(character_name)
        if arc_summary:
            print(f"\n{character_name.title()}:")
            print(f"  Total Moments: {arc_summary['total_moments']}")
            print(f"  Emotional Journey: {arc_summary['emotional_journey']}")
            print(f"  Awareness Progression: {arc_summary['awareness_progression']}")
            print(f"  Current Position: {arc_summary['current_position']}")
    
    print("\n✓ Example complete! Check the output directory for all generated prompts.")


if __name__ == "__main__":
    main()