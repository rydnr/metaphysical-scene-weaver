#!/usr/bin/env python3
"""Fix metadata corruption in scene files."""

import json
import os
import re
from pathlib import Path

def fix_speaker_field(speaker_text):
    """Clean up the speaker field to just contain the character name."""
    # Check if it contains descriptive text
    if "The architect" in speaker_text or "The Architect" in speaker_text:
        return "Architect"
    elif "Evan" in speaker_text:
        return "Evan"
    elif "The voice" in speaker_text or "Voice" in speaker_text:
        return "Voice"
    elif speaker_text in ["Architect", "Evan", "Voice"]:
        return speaker_text  # Already clean
    else:
        # For debugging - print unrecognized patterns
        print(f"Unknown speaker pattern: {speaker_text}")
        return speaker_text

def process_metadata_file(filepath):
    """Process a single metadata.json file."""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        original_speaker = data.get('speaker', '')
        cleaned_speaker = fix_speaker_field(original_speaker)
        
        if original_speaker != cleaned_speaker:
            print(f"Fixing {filepath}: '{original_speaker}' -> '{cleaned_speaker}'")
            data['speaker'] = cleaned_speaker
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
                f.write('\n')  # Add newline at end of file
            return True
        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    """Main function to process all metadata files."""
    content_dir = Path("/home/chous/work/metaphysical-scene-weaver/content")
    fixed_count = 0
    total_count = 0
    
    # Process all metadata.json files
    for metadata_file in sorted(content_dir.glob("*/metadata.json")):
        total_count += 1
        if process_metadata_file(metadata_file):
            fixed_count += 1
    
    print(f"\nSummary: Fixed {fixed_count} out of {total_count} metadata files")

if __name__ == "__main__":
    main()