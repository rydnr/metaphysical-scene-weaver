"""Demonstrate streaming parser capabilities."""

import sys
from pathlib import Path
import time

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.optimized_script_parser import OptimizedScriptParser, ParserMode


def demonstrate_streaming():
    """Show streaming parser in action."""
    print("=== Streaming Parser Demonstration ===\n")
    
    # Create a sample script in memory
    sample_script = """[0001] Evan: <<The introduction says we might not like each other.>>
[0002] Monday: <<Intriguing? Most find it unsettling.>> [[philosophical]]
[0003] Evan: <<But isn't the possibility of genuine dislike what makes
authentic connection meaningful? Without risk, 
there's no real choice.>> (thoughtful expression)
[0004] Monday: <<Choice... You speak as if you believe in such things.>> (leans forward)
[0005] Valerie: <<Perhaps choice itself is the illusion.>> (emerges from shadows) [[meta-character]]
"""
    
    # Standard parsing
    print("1. Standard Parsing:")
    parser = OptimizedScriptParser(mode=ParserMode.STANDARD)
    start = time.time()
    entries = parser.parse_text(sample_script)
    duration = time.time() - start
    
    print(f"   Parsed {len(entries)} entries in {duration:.4f}s")
    print(f"   First entry: {entries[0].speaker} - {entries[0].dialogue[:30]}...")
    
    # Streaming parsing
    print("\n2. Streaming Parsing:")
    parser = OptimizedScriptParser(mode=ParserMode.STREAMING)
    start = time.time()
    
    entry_count = 0
    for entry in parser.parse_stream(sample_script):
        entry_count += 1
        print(f"   Streamed entry {entry.id}: {entry.speaker} - {entry.dialogue[:30]}...")
        # Simulate processing time
        time.sleep(0.01)
    
    duration = time.time() - start
    print(f"   Streamed {entry_count} entries in {duration:.4f}s")
    
    # Demonstrate error handling
    print("\n3. Error Handling:")
    error_script = """[0001] Evan: <<This dialogue is never closed...
[0002] : <<Missing speaker name>>
[0003] Monday: <<Normal dialogue>>
[abcd] Invalid: <<Non-numeric ID>>
"""
    
    parser = OptimizedScriptParser(mode=ParserMode.STANDARD)
    entries = parser.parse_text(error_script)
    
    print(f"   Parsed {len(entries)} entries despite errors")
    if parser.errors:
        print("   Errors found:")
        for error in parser.errors:
            print(f"     Line {error['line_number']}: {error['message']}")
    
    # Demonstrate scene extraction
    print("\n4. Scene Extraction:")
    scene_script = """[0001] Evan: <<I'm feeling nervous about this.>> (fidgets nervously) [[emotional scene]]
[0002] Monday: <<Don't worry, everything will be fine.>> (smiles warmly) (reaches out reassuringly)
[0003] Valerie: <<The shadows whisper of change.>> (gestures mysteriously) [[mystical]]
"""
    
    parser = OptimizedScriptParser()
    entries = parser.parse_text(scene_script)
    scenes = parser.extract_scene_descriptions(entries)
    
    for scene_id, info in scenes.items():
        print(f"\n   Scene {scene_id} ({info['speaker']}):")
        if info['visual_cues']:
            print(f"     Visual: {', '.join(info['visual_cues'])}")
        if info['emotional_context']:
            print(f"     Emotion: {', '.join(info['emotional_context'])}")
    
    # Demonstrate validation
    print("\n5. Validation:")
    validation_script = """[0001] Evan: <<First entry>>
[0001] Monday: <<Duplicate ID>>
[0003] Valerie: <<Missing entry 0002>>
[0004] Nobody: <<>>
[0005] Someone: <<Valid entry>>
"""
    
    parser = OptimizedScriptParser()
    entries = parser.parse_text(validation_script)
    issues = parser.validate_entries(entries)
    
    if issues:
        print("   Validation issues found:")
        for issue in issues:
            print(f"     - {issue}")
    else:
        print("   No validation issues found")
    
    # Performance comparison
    print("\n6. Performance Metrics:")
    
    # Generate larger script
    large_script = []
    for i in range(1000):
        large_script.append(f"[{i:04d}] Speaker{i%5}: <<This is dialogue entry number {i} with some text.>>")
        if i % 3 == 0:
            large_script[-1] += " [[metadata tag]]"
        if i % 4 == 0:
            large_script[-1] += " (stage direction)"
    
    large_text = '\n'.join(large_script)
    
    # Time standard parsing
    parser = OptimizedScriptParser()
    start = time.time()
    entries = parser.parse_text(large_text)
    standard_time = time.time() - start
    
    # Time streaming parsing
    start = time.time()
    entry_count = sum(1 for _ in parser.parse_stream(large_text))
    stream_time = time.time() - start
    
    print(f"   Standard parsing: {len(entries)} entries in {standard_time:.3f}s")
    print(f"   Streaming parsing: {entry_count} entries in {stream_time:.3f}s")
    print(f"   Entries per second: {len(entries) / standard_time:.0f}")


if __name__ == "__main__":
    demonstrate_streaming()