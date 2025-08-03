"""Test the enhanced parser against edge cases."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.script_parser_v2 import EnhancedScriptParser

def test_enhanced_parser():
    """Test enhanced parser with edge cases."""
    parser = EnhancedScriptParser(strict_mode=False)
    
    # Test 1: Nested brackets in dialogue
    print("=== Test 1: Nested brackets ===")
    text = "[0001] Evan: <<I said [[this is nested]] in the dialogue.>>"
    entries = parser.parse_text(text)
    if entries:
        print(f"Dialogue: {entries[0].dialogue}")
        print(f"Metadata: {entries[0].metadata}")
    
    # Test 2: Multiple metadata on same line
    print("\n=== Test 2: Multiple metadata ===")
    text = "[0001] Evan: <<Hello.>> [[tag1]] [[tag2]] [[tag3]]"
    entries = parser.parse_text(text)
    if entries:
        print(f"Metadata count: {len(entries[0].metadata)}")
        print(f"Metadata: {entries[0].metadata}")
    
    # Test 3: Multiline with interruptions
    print("\n=== Test 3: Multiline with interruptions ===")
    text = """[0001] Evan: <<This is a very long
    dialogue that continues (pauses)
    across multiple lines [[philosophical]]
    and keeps going on and on>>"""
    entries = parser.parse_text(text)
    if entries:
        print(f"Dialogue: {entries[0].dialogue}")
        print(f"Stage directions: {entries[0].stage_directions}")
        print(f"Metadata: {entries[0].metadata}")
    
    # Test 4: Empty dialogue
    print("\n=== Test 4: Empty dialogue ===")
    text = "[0001] Evan: <<>>"
    entries = parser.parse_text(text)
    if entries:
        print(f"Dialogue: '{entries[0].dialogue}'")
        print(f"Dialogue length: {len(entries[0].dialogue)}")
    
    # Test 5: Stage directions on same line
    print("\n=== Test 5: Multiple stage directions ===")
    text = "[0001] Evan: <<Hello.>> (first) (second) (third)"
    entries = parser.parse_text(text)
    if entries:
        print(f"Stage directions: {entries[0].stage_directions}")
        print(f"Count: {len(entries[0].stage_directions)}")
    
    # Test 6: Mixed annotations
    print("\n=== Test 6: Mixed annotations ===")
    text = "[0001] Evan: <<Complex line.>> (gesture) [[meta1]] (action) [[meta2]]"
    entries = parser.parse_text(text)
    if entries:
        print(f"Dialogue: {entries[0].dialogue}")
        print(f"Stage directions: {entries[0].stage_directions}")
        print(f"Metadata: {entries[0].metadata}")
    
    # Test 7: Validation
    print("\n=== Test 7: Script validation ===")
    text = """[0001] Evan: <<First>>
[0001] Monday: <<Duplicate ID>>
[0003] Valerie: <<Gap in sequence>>
[0004] Nobody: <<>>"""
    entries = parser.parse_text(text)
    issues = parser.validate_script(entries)
    for issue in issues:
        print(f"Issue: {issue}")
    
    # Test 8: Error handling
    print("\n=== Test 8: Parse errors ===")
    if parser.errors:
        for error in parser.errors:
            print(f"Error at line {error.line_number}: {error.error_type} - {error.message}")
    
    # Test 9: Scene extraction
    print("\n=== Test 9: Scene extraction ===")
    text = """[0001] Evan: <<I feel nervous.>> (looks around nervously) [[emotional scene]]
[0002] Monday: <<Don't worry.>> (smiles warmly) (reaches out)"""
    entries = parser.parse_text(text)
    scenes = parser.extract_scene_descriptions(entries)
    for scene_id, info in scenes.items():
        print(f"\nScene {scene_id}:")
        print(f"  Visual cues: {info['visual_cues']}")
        print(f"  Emotional context: {info['emotional_context']}")

if __name__ == "__main__":
    test_enhanced_parser()