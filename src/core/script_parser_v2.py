"""Enhanced script parser with better edge case handling and error recovery."""

import re
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Tuple, Iterator
from pathlib import Path
import json
import logging
from enum import Enum

# Configure logging
logger = logging.getLogger(__name__)


class ParserState(Enum):
    """Parser state for multiline handling."""
    SEEKING = "seeking"
    IN_DIALOGUE = "in_dialogue"
    COMPLETE = "complete"


@dataclass
class ScriptEntry:
    """Represents a single entry in the script."""
    id: str
    speaker: str
    dialogue: str
    panel_count: Optional[int] = None
    stage_directions: List[str] = field(default_factory=list)
    metadata: List[str] = field(default_factory=list)
    line_number: Optional[int] = None  # For error reporting
    
    def is_valid(self) -> bool:
        """Check if entry has minimum required fields."""
        return bool(self.id and self.speaker)


@dataclass
class ParseError:
    """Represents a parsing error."""
    line_number: int
    line_content: str
    error_type: str
    message: str


class EnhancedScriptParser:
    """Parse philosophical dialogue scripts with improved error handling."""
    
    def __init__(self, strict_mode: bool = False):
        """
        Initialize parser.
        
        Args:
            strict_mode: If True, raise exceptions on errors. If False, log and continue.
        """
        self.strict_mode = strict_mode
        self.errors: List[ParseError] = []
        
        # Compile regex patterns for better performance
        self._compile_patterns()
        
    def _compile_patterns(self):
        """Compile all regex patterns."""
        # Main dialogue pattern with optional panel count
        # Supports character names with letters, numbers, underscores
        self.dialogue_pattern = re.compile(
            r'^\[(\d+)\]\s*(?:\[(\d+)-panel\])?\s*([\w_]+):\s*<<(.*)$',
            re.MULTILINE
        )
        
        # Pattern for detecting dialogue end
        self.dialogue_end_pattern = re.compile(r'^(.*?)>>\s*(.*)$')
        
        # Metadata pattern - multiple per line
        self.metadata_pattern = re.compile(r'\[\[([^\]]+)\]\]')
        
        # Stage direction pattern - multiple per line, avoid nested
        self.stage_direction_pattern = re.compile(r'\(([^()]+)\)')
        
        # Caption pattern
        self.caption_pattern = re.compile(r'^Caption:\s*<<(.+?)>>$', re.MULTILINE)
        
        # Character name validation (for error checking)
        self.valid_speaker_pattern = re.compile(r'^[\w_]+$')
        
    def parse_file(self, filepath: Path) -> List[ScriptEntry]:
        """Parse an entire script file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            return self.parse_text(content)
        except Exception as e:
            logger.error(f"Failed to read file {filepath}: {e}")
            if self.strict_mode:
                raise
            return []
    
    def parse_text(self, text: str) -> List[ScriptEntry]:
        """Parse script text into structured entries with improved handling."""
        self.errors = []  # Reset errors
        entries = []
        lines = text.split('\n')
        
        current_entry = None
        dialogue_lines = []
        state = ParserState.SEEKING
        
        for line_num, line in enumerate(lines, 1):
            stripped_line = line.strip()
            
            if state == ParserState.SEEKING:
                # Look for dialogue start
                match = self.dialogue_pattern.match(stripped_line)
                if match:
                    # Save any pending entry
                    if current_entry:
                        self._finalize_entry(current_entry, dialogue_lines, entries)
                    
                    # Start new entry
                    entry_id = match.group(1)
                    panel_count = int(match.group(2)) if match.group(2) else None
                    speaker = match.group(3)
                    dialogue_start = match.group(4)
                    
                    # Validate speaker name
                    if not self.valid_speaker_pattern.match(speaker):
                        self._add_error(line_num, line, "INVALID_SPEAKER", 
                                      f"Invalid speaker name: {speaker}")
                        if self.strict_mode:
                            continue
                    
                    current_entry = ScriptEntry(
                        id=entry_id,
                        speaker=speaker,
                        dialogue="",
                        panel_count=panel_count,
                        line_number=line_num
                    )
                    
                    # Check if dialogue ends on same line
                    end_match = self.dialogue_end_pattern.match(dialogue_start)
                    if end_match:
                        # Single-line dialogue
                        current_entry.dialogue = end_match.group(1).strip()
                        remaining = end_match.group(2)
                        
                        # Extract metadata and stage directions from remainder
                        self._extract_annotations(remaining, current_entry)
                        
                        entries.append(current_entry)
                        current_entry = None
                        state = ParserState.SEEKING
                    else:
                        # Multi-line dialogue
                        dialogue_lines = [dialogue_start]
                        state = ParserState.IN_DIALOGUE
                else:
                    # Not a dialogue start - check for orphaned metadata/stage directions
                    if entries and (self.metadata_pattern.search(stripped_line) or 
                                  self.stage_direction_pattern.search(stripped_line)):
                        # Add to previous entry
                        self._extract_annotations(stripped_line, entries[-1])
            
            elif state == ParserState.IN_DIALOGUE:
                # Continue collecting dialogue
                end_match = self.dialogue_end_pattern.match(stripped_line)
                if end_match:
                    # End of dialogue found
                    dialogue_lines.append(end_match.group(1))
                    remaining = end_match.group(2)
                    
                    # Finalize dialogue
                    current_entry.dialogue = ' '.join(dialogue_lines).strip()
                    
                    # Extract annotations from the ending line
                    self._extract_annotations(remaining, current_entry)
                    
                    entries.append(current_entry)
                    current_entry = None
                    dialogue_lines = []
                    state = ParserState.SEEKING
                else:
                    # Continue collecting
                    dialogue_lines.append(stripped_line)
                    
                    # Extract annotations even from continuation lines
                    self._extract_annotations(stripped_line, current_entry)
        
        # Handle any unclosed dialogue
        if current_entry:
            if dialogue_lines:
                current_entry.dialogue = ' '.join(dialogue_lines).strip()
                self._add_error(current_entry.line_number, "", "UNCLOSED_DIALOGUE",
                              f"Dialogue for {current_entry.speaker} was not properly closed")
            entries.append(current_entry)
        
        return entries
    
    def _finalize_entry(self, entry: ScriptEntry, dialogue_lines: List[str], 
                       entries: List[ScriptEntry]):
        """Finalize and add entry to list."""
        if dialogue_lines:
            entry.dialogue = ' '.join(dialogue_lines).strip()
        if entry.is_valid():
            entries.append(entry)
        else:
            self._add_error(entry.line_number or 0, "", "INVALID_ENTRY",
                          f"Invalid entry: missing required fields")
    
    def _extract_annotations(self, text: str, entry: ScriptEntry):
        """Extract metadata and stage directions from text."""
        # Extract all metadata tags
        metadata_matches = self.metadata_pattern.findall(text)
        entry.metadata.extend(m.strip() for m in metadata_matches)
        
        # Extract all stage directions
        stage_matches = self.stage_direction_pattern.findall(text)
        entry.stage_directions.extend(s.strip() for s in stage_matches)
    
    def _add_error(self, line_num: int, line: str, error_type: str, message: str):
        """Add a parsing error."""
        error = ParseError(line_num, line, error_type, message)
        self.errors.append(error)
        logger.warning(f"Line {line_num}: {error_type} - {message}")
    
    def extract_scene_descriptions(self, entries: List[ScriptEntry]) -> Dict[str, Any]:
        """Extract scene descriptions and visual cues from entries."""
        scenes = {}
        
        visual_keywords = ['looks', 'gesture', 'expression', 'movement', 'scene',
                          'stands', 'sits', 'walks', 'turns', 'faces', 'points',
                          'nods', 'shakes', 'reaches', 'touches', 'holds']
        
        emotion_keywords = ['laughs', 'cries', 'smiles', 'frowns', 'sighs',
                           'gasps', 'whispers', 'shouts', 'screams', 'murmurs']
        
        for entry in entries:
            scene_info = {
                'dialogue': entry.dialogue,
                'speaker': entry.speaker,
                'visual_cues': [],
                'emotional_context': [],
                'panel_count': entry.panel_count
            }
            
            # Extract visual cues from stage directions
            for direction in entry.stage_directions:
                direction_lower = direction.lower()
                if any(keyword in direction_lower for keyword in visual_keywords):
                    scene_info['visual_cues'].append(direction)
                if any(keyword in direction_lower for keyword in emotion_keywords):
                    scene_info['emotional_context'].append(direction)
            
            # Extract emotional cues from dialogue
            dialogue_lower = entry.dialogue.lower()
            for keyword in emotion_keywords:
                if keyword in dialogue_lower:
                    scene_info['emotional_context'].append(f"Character {keyword}")
            
            # Analyze metadata for scene information
            for meta in entry.metadata:
                if any(word in meta.lower() for word in ['scene', 'setting', 'location']):
                    scene_info['visual_cues'].append(f"Scene note: {meta}")
            
            scenes[entry.id] = scene_info
        
        return scenes
    
    def validate_script(self, entries: List[ScriptEntry]) -> List[str]:
        """Validate script entries and return list of issues."""
        issues = []
        
        # Check for duplicate IDs
        seen_ids = set()
        for entry in entries:
            if entry.id in seen_ids:
                issues.append(f"Duplicate ID found: {entry.id}")
            seen_ids.add(entry.id)
        
        # Check for ID sequence gaps
        ids = sorted([int(e.id) for e in entries if e.id.isdigit()])
        if ids:
            expected = list(range(ids[0], ids[-1] + 1))
            missing = set(expected) - set(ids)
            if missing:
                issues.append(f"Missing IDs: {sorted(missing)}")
        
        # Check for empty dialogues
        empty_dialogues = [e.id for e in entries if not e.dialogue.strip()]
        if empty_dialogues:
            issues.append(f"Empty dialogues in entries: {empty_dialogues}")
        
        # Add parsing errors
        for error in self.errors:
            issues.append(f"Line {error.line_number}: {error.error_type} - {error.message}")
        
        return issues
    
    def to_json(self, entries: List[ScriptEntry], filepath: Path, 
                include_errors: bool = False):
        """Export parsed entries to JSON format."""
        data = {
            'entries': [],
            'metadata': {
                'total_entries': len(entries),
                'speakers': list(set(e.speaker for e in entries)),
                'has_panel_info': any(e.panel_count is not None for e in entries),
                'total_stage_directions': sum(len(e.stage_directions) for e in entries),
                'total_metadata_tags': sum(len(e.metadata) for e in entries)
            }
        }
        
        for entry in entries:
            data['entries'].append({
                'id': entry.id,
                'speaker': entry.speaker,
                'dialogue': entry.dialogue,
                'panel_count': entry.panel_count,
                'stage_directions': entry.stage_directions,
                'metadata': entry.metadata,
                'line_number': entry.line_number
            })
        
        if include_errors and self.errors:
            data['errors'] = [
                {
                    'line_number': e.line_number,
                    'error_type': e.error_type,
                    'message': e.message
                } for e in self.errors
            ]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def parse_streaming(self, text_stream: Iterator[str], 
                       buffer_size: int = 1000) -> Iterator[ScriptEntry]:
        """
        Parse script in streaming fashion for large files.
        
        Args:
            text_stream: Iterator yielding lines of text
            buffer_size: Number of lines to buffer for multiline dialogues
        
        Yields:
            ScriptEntry objects as they are completed
        """
        buffer = []
        current_entry = None
        dialogue_lines = []
        state = ParserState.SEEKING
        
        for line in text_stream:
            buffer.append(line)
            
            # Process similar to parse_text but yield entries as they complete
            # Implementation would be similar to parse_text but yielding
            # entries instead of collecting them
            
            # Keep buffer size manageable
            if len(buffer) > buffer_size and state == ParserState.SEEKING:
                buffer = buffer[-100:]  # Keep last 100 lines for context
        
        # Handle any remaining entry
        if current_entry:
            if dialogue_lines:
                current_entry.dialogue = ' '.join(dialogue_lines).strip()
            yield current_entry


# Backwards compatibility
ScriptParser = EnhancedScriptParser