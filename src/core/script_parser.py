"""Script parser for extracting dialogue, metadata, and stage directions."""

import re
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from pathlib import Path
import json


@dataclass
class ScriptEntry:
    """Represents a single entry in the script."""
    id: str
    speaker: str
    dialogue: str
    panel_count: Optional[int] = None
    stage_directions: List[str] = None
    metadata: List[str] = None
    
    def __post_init__(self):
        if self.stage_directions is None:
            self.stage_directions = []
        if self.metadata is None:
            self.metadata = []


class ScriptParser:
    """Parse philosophical dialogue scripts with metadata and stage directions."""
    
    def __init__(self):
        # Main dialogue pattern: [0001] Speaker: <<dialogue>>
        self.dialogue_pattern = re.compile(
            r'\[(\d+)\]\s*(?:\[(\d+)-panel\])?\s*(\w+):\s*<<(.+?)>>',
            re.DOTALL
        )
        
        # Metadata pattern: [[ metadata ]]
        self.metadata_pattern = re.compile(r'\[\[(.*?)\]\]', re.DOTALL)
        
        # Stage direction pattern: (stage direction)
        self.stage_direction_pattern = re.compile(r'\(([^)]+)\)')
        
        # Caption pattern: Caption: <<text>>
        self.caption_pattern = re.compile(r'Caption:\s*<<(.+?)>>')
        
    def parse_file(self, filepath: Path) -> List[ScriptEntry]:
        """Parse an entire script file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return self.parse_text(content)
    
    def parse_text(self, text: str) -> List[ScriptEntry]:
        """Parse script text into structured entries."""
        entries = []
        
        # Split text into lines for easier processing
        lines = text.split('\n')
        current_entry = None
        current_text = []
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Check for dialogue start
            dialogue_match = self.dialogue_pattern.match(line)
            if dialogue_match:
                # Save previous entry if exists
                if current_entry and current_text:
                    current_entry.dialogue = ' '.join(current_text).strip()
                    entries.append(current_entry)
                    current_text = []
                
                # Create new entry
                entry_id = dialogue_match.group(1)
                panel_count = int(dialogue_match.group(2)) if dialogue_match.group(2) else None
                speaker = dialogue_match.group(3)
                dialogue_start = dialogue_match.group(4)
                
                current_entry = ScriptEntry(
                    id=entry_id,
                    speaker=speaker,
                    dialogue=dialogue_start,
                    panel_count=panel_count
                )
                
                # Check if dialogue continues on next lines
                if not dialogue_start.endswith('>>'):
                    current_text = [dialogue_start]
                else:
                    current_entry.dialogue = dialogue_start.rstrip('>>')
                    entries.append(current_entry)
                    current_entry = None
                    
            elif current_entry and current_text:
                # Continue collecting dialogue
                if '>>' in line:
                    # End of dialogue
                    current_text.append(line.split('>>')[0])
                    current_entry.dialogue = ' '.join(current_text).strip()
                    entries.append(current_entry)
                    current_entry = None
                    current_text = []
                else:
                    current_text.append(line)
                    
            # Extract metadata from any line
            metadata_matches = self.metadata_pattern.findall(line)
            if metadata_matches and entries:
                entries[-1].metadata.extend(metadata_matches)
                
            # Extract stage directions
            stage_matches = self.stage_direction_pattern.findall(line)
            if stage_matches and entries:
                entries[-1].stage_directions.extend(stage_matches)
                
            i += 1
        
        # Don't forget the last entry
        if current_entry and current_text:
            current_entry.dialogue = ' '.join(current_text).strip()
            entries.append(current_entry)
            
        return entries
    
    def extract_scene_descriptions(self, entries: List[ScriptEntry]) -> Dict[str, Any]:
        """Extract scene descriptions and visual cues from entries."""
        scenes = {}
        
        for entry in entries:
            scene_info = {
                'dialogue': entry.dialogue,
                'speaker': entry.speaker,
                'visual_cues': []
            }
            
            # Extract visual cues from stage directions
            for direction in entry.stage_directions:
                if any(keyword in direction.lower() for keyword in 
                       ['looks', 'gesture', 'expression', 'movement', 'scene']):
                    scene_info['visual_cues'].append(direction)
                    
            # Extract emotional cues from dialogue
            emotion_keywords = ['laughs', 'cries', 'smiles', 'frowns', 'sighs']
            for keyword in emotion_keywords:
                if keyword in entry.dialogue.lower():
                    scene_info['visual_cues'].append(f"Character {keyword}")
                    
            scenes[entry.id] = scene_info
            
        return scenes
    
    def to_json(self, entries: List[ScriptEntry], filepath: Path):
        """Export parsed entries to JSON format."""
        data = []
        for entry in entries:
            data.append({
                'id': entry.id,
                'speaker': entry.speaker,
                'dialogue': entry.dialogue,
                'panel_count': entry.panel_count,
                'stage_directions': entry.stage_directions,
                'metadata': entry.metadata
            })
            
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)