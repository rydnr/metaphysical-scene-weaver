"""Manual test runner for edge cases - analyze parser behavior."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.script_parser import ScriptParser

def test_edge_cases():
    """Test various edge cases manually."""
    parser = ScriptParser()
    
    # Test 1: Nested brackets in dialogue
    print("=== Test 1: Nested brackets ===")
    text = "[0001] Evan: <<I said [[this is nested]] in the dialogue.>>"
    entries = parser.parse_text(text)
    if entries:
        print(f"Dialogue: {entries[0].dialogue}")
        print(f"Metadata: {entries[0].metadata}")
    else:
        print("No entries parsed!")
    
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
    
    # Test 4: Character name variations
    print("\n=== Test 4: Character name with underscore ===")
    text = "[0001] Evan_2: <<Name with underscore>>"
    entries = parser.parse_text(text)
    if entries:
        print(f"Speaker: {entries[0].speaker}")
    else:
        print("Failed to parse name with underscore!")
    
    # Test 5: Malformed entry
    print("\n=== Test 5: Malformed entries ===")
    text = "[0001] : <<Missing speaker name>>"
    entries = parser.parse_text(text)
    print(f"Parsed {len(entries)} entries (expected 0)")
    
    # Test 6: Empty dialogue
    print("\n=== Test 6: Empty dialogue ===")
    text = "[0001] Evan: <<>>"
    entries = parser.parse_text(text)
    if entries:
        print(f"Dialogue: '{entries[0].dialogue}'")
        print(f"Dialogue length: {len(entries[0].dialogue)}")
    
    # Test 7: Very long single line
    print("\n=== Test 7: Very long dialogue ===")
    long_text = "A" * 1000
    text = f"[0001] Evan: <<{long_text}>>"
    entries = parser.parse_text(text)
    if entries:
        print(f"Dialogue length: {len(entries[0].dialogue)}")
    
    # Test 8: Panel count edge cases
    print("\n=== Test 8: Panel count variations ===")
    for test_text in [
        "[0001] [0-panel] Evan: <<Zero panels>>",
        "[0002] [99-panel] Evan: <<Many panels>>",
        "[0003] [2-panels] Evan: <<Wrong format>>"  # Should fail
    ]:
        entries = parser.parse_text(test_text)
        if entries:
            print(f"Panel count: {entries[0].panel_count} for '{entries[0].dialogue}'")
        else:
            print(f"Failed to parse: {test_text}")
    
    # Test 9: Stage directions edge cases
    print("\n=== Test 9: Multiple stage directions ===")
    text = "[0001] Evan: <<Hello.>> (first) (second) (third)"
    entries = parser.parse_text(text)
    if entries:
        print(f"Stage directions: {entries[0].stage_directions}")
        print(f"Count: {len(entries[0].stage_directions)}")
    
    # Test 10: Special characters
    print("\n=== Test 10: Special characters ===")
    text = "[0001] Evan: <<What about $pecial ch@rs? And *asterisks* or .dots.?>>"
    entries = parser.parse_text(text)
    if entries:
        print(f"Dialogue preserved: {entries[0].dialogue}")

if __name__ == "__main__":
    test_edge_cases()