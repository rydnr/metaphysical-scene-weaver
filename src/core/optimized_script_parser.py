"""Optimized script parser with streaming support and performance enhancements."""

import re
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Iterator, TextIO, Union
from pathlib import Path
import json
import logging
from enum import Enum
from io import StringIO

# Configure logging
logger = logging.getLogger(__name__)


class ParserMode(Enum):
    """Parser operation mode."""
    STANDARD = "standard"
    STREAMING = "streaming"
    STRICT = "strict"


@dataclass
class ScriptEntry:
    """Represents a single entry in the script."""
    id: str
    speaker: str
    dialogue: str
    panel_count: Optional[int] = None
    stage_directions: List[str] = field(default_factory=list)
    metadata: List[str] = field(default_factory=list)
    line_number: Optional[int] = None
    
    def __post_init__(self):
        # Ensure lists are initialized
        if self.stage_directions is None:
            self.stage_directions = []
        if self.metadata is None:
            self.metadata = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            'id': self.id,
            'speaker': self.speaker,
            'dialogue': self.dialogue,
            'panel_count': self.panel_count,
            'stage_directions': self.stage_directions,
            'metadata': self.metadata,
            'line_number': self.line_number
        }


class OptimizedScriptParser:
    """High-performance script parser with streaming support."""
    
    # Precompiled regex patterns (class level for reuse)
    DIALOGUE_PATTERN = re.compile(
        r'^\[(\d+)\]\s*(?:\[(\d+)-panel\])?\s*([\w_]+):\s*<<(.*)$',
        re.MULTILINE
    )
    DIALOGUE_END_PATTERN = re.compile(r'^(.*?)>>\s*(.*)$')
    METADATA_PATTERN = re.compile(r'\[\[([^\]]+)\]\]')
    STAGE_PATTERN = re.compile(r'\(([^()]+)\)')
    
    def __init__(self, mode: ParserMode = ParserMode.STANDARD, 
                 buffer_size: int = 8192):
        """
        Initialize parser.
        
        Args:
            mode: Parser operation mode
            buffer_size: Buffer size for streaming mode
        """
        self.mode = mode
        self.buffer_size = buffer_size
        self.errors: List[Dict[str, Any]] = []
        
    def parse_file(self, filepath: Union[str, Path]) -> List[ScriptEntry]:
        """Parse script file with appropriate method based on size."""
        filepath = Path(filepath)
        file_size = filepath.stat().st_size
        
        # Use streaming for files > 10MB
        if file_size > 10 * 1024 * 1024:
            logger.info(f"Large file detected ({file_size / 1024 / 1024:.1f}MB), using streaming parser")
            return list(self.parse_file_streaming(filepath))
        
        # Standard parsing for smaller files
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return self.parse_text(content)
    
    def parse_text(self, text: str) -> List[ScriptEntry]:
        """Parse text using optimized regex patterns."""
        entries = []
        lines = text.split('\n')
        
        current_entry = None
        dialogue_buffer = []
        line_num = 0
        
        while line_num < len(lines):
            line = lines[line_num].strip()
            
            # Check for dialogue start
            match = self.DIALOGUE_PATTERN.match(line)
            if match:
                # Save previous entry if exists
                if current_entry and dialogue_buffer:
                    current_entry.dialogue = ' '.join(dialogue_buffer)
                    entries.append(current_entry)
                    dialogue_buffer = []
                
                # Create new entry
                entry_id, panel_str, speaker, dialogue_start = match.groups()
                panel_count = int(panel_str) if panel_str else None
                
                current_entry = ScriptEntry(
                    id=entry_id,
                    speaker=speaker,
                    dialogue="",
                    panel_count=panel_count,
                    line_number=line_num + 1
                )
                
                # Check if dialogue ends on same line
                end_match = self.DIALOGUE_END_PATTERN.match(dialogue_start)
                if end_match:
                    current_entry.dialogue = end_match.group(1).strip()
                    self._extract_annotations(end_match.group(2), current_entry)
                    entries.append(current_entry)
                    current_entry = None
                else:
                    dialogue_buffer = [dialogue_start]
            
            elif dialogue_buffer:
                # Continue collecting dialogue
                end_match = self.DIALOGUE_END_PATTERN.match(line)
                if end_match:
                    dialogue_buffer.append(end_match.group(1))
                    current_entry.dialogue = ' '.join(dialogue_buffer).strip()
                    self._extract_annotations(end_match.group(2), current_entry)
                    entries.append(current_entry)
                    current_entry = None
                    dialogue_buffer = []
                else:
                    dialogue_buffer.append(line)
                    # Extract annotations from continuation lines
                    self._extract_annotations(line, current_entry)
            
            elif entries:
                # Check for orphaned annotations
                self._extract_annotations(line, entries[-1])
            
            line_num += 1
        
        # Handle unclosed dialogue
        if current_entry and dialogue_buffer:
            current_entry.dialogue = ' '.join(dialogue_buffer).strip()
            self._log_error(current_entry.line_number, "Unclosed dialogue")
            entries.append(current_entry)
        
        return entries
    
    def parse_file_streaming(self, filepath: Union[str, Path]) -> Iterator[ScriptEntry]:
        """Parse large files in streaming mode."""
        filepath = Path(filepath)
        
        with open(filepath, 'r', encoding='utf-8', buffering=self.buffer_size) as f:
            yield from self._parse_stream(f)
    
    def parse_stream(self, stream: Union[str, TextIO]) -> Iterator[ScriptEntry]:
        """Parse from a text stream."""
        if isinstance(stream, str):
            stream = StringIO(stream)
        yield from self._parse_stream(stream)
    
    def _parse_stream(self, stream: TextIO) -> Iterator[ScriptEntry]:
        """Internal streaming parser implementation."""
        current_entry = None
        dialogue_buffer = []
        line_num = 0
        
        for line in stream:
            line_num += 1
            line = line.strip()
            
            # Check for dialogue start
            match = self.DIALOGUE_PATTERN.match(line)
            if match:
                # Yield previous entry if exists
                if current_entry and dialogue_buffer:
                    current_entry.dialogue = ' '.join(dialogue_buffer)
                    yield current_entry
                    dialogue_buffer = []
                
                # Create new entry
                entry_id, panel_str, speaker, dialogue_start = match.groups()
                panel_count = int(panel_str) if panel_str else None
                
                current_entry = ScriptEntry(
                    id=entry_id,
                    speaker=speaker,
                    dialogue="",
                    panel_count=panel_count,
                    line_number=line_num
                )
                
                # Check if dialogue ends on same line
                end_match = self.DIALOGUE_END_PATTERN.match(dialogue_start)
                if end_match:
                    current_entry.dialogue = end_match.group(1).strip()
                    self._extract_annotations(end_match.group(2), current_entry)
                    yield current_entry
                    current_entry = None
                else:
                    dialogue_buffer = [dialogue_start]
            
            elif dialogue_buffer:
                # Continue collecting dialogue
                end_match = self.DIALOGUE_END_PATTERN.match(line)
                if end_match:
                    dialogue_buffer.append(end_match.group(1))
                    current_entry.dialogue = ' '.join(dialogue_buffer).strip()
                    self._extract_annotations(end_match.group(2), current_entry)
                    yield current_entry
                    current_entry = None
                    dialogue_buffer = []
                else:
                    dialogue_buffer.append(line)
                    self._extract_annotations(line, current_entry)
        
        # Handle unclosed dialogue at end of stream
        if current_entry and dialogue_buffer:
            current_entry.dialogue = ' '.join(dialogue_buffer).strip()
            self._log_error(line_num, "Unclosed dialogue at end of file")
            yield current_entry
    
    def _extract_annotations(self, text: str, entry: ScriptEntry):
        """Extract metadata and stage directions efficiently."""
        if not text:
            return
        
        # Extract metadata
        for match in self.METADATA_PATTERN.finditer(text):
            entry.metadata.append(match.group(1).strip())
        
        # Extract stage directions
        for match in self.STAGE_PATTERN.finditer(text):
            entry.stage_directions.append(match.group(1).strip())
    
    def _log_error(self, line_num: int, message: str):
        """Log parsing error."""
        error = {
            'line_number': line_num,
            'message': message
        }
        self.errors.append(error)
        if self.mode == ParserMode.STRICT:
            raise ValueError(f"Line {line_num}: {message}")
        else:
            logger.warning(f"Line {line_num}: {message}")
    
    def extract_scene_descriptions(self, entries: Union[List[ScriptEntry], Iterator[ScriptEntry]]) -> Dict[str, Any]:
        """Extract scene descriptions from entries."""
        scenes = {}
        
        visual_keywords = {
            'looks', 'gesture', 'expression', 'movement', 'scene',
            'stands', 'sits', 'walks', 'turns', 'faces', 'points',
            'nods', 'shakes', 'reaches', 'touches', 'holds'
        }
        
        emotion_keywords = {
            'laughs', 'cries', 'smiles', 'frowns', 'sighs',
            'gasps', 'whispers', 'shouts', 'screams', 'murmurs'
        }
        
        for entry in entries:
            scene_info = {
                'dialogue': entry.dialogue,
                'speaker': entry.speaker,
                'visual_cues': [],
                'emotional_context': [],
                'panel_count': entry.panel_count
            }
            
            # Process stage directions
            for direction in entry.stage_directions:
                direction_lower = direction.lower()
                direction_words = set(direction_lower.split())
                
                if direction_words & visual_keywords:
                    scene_info['visual_cues'].append(direction)
                if direction_words & emotion_keywords:
                    scene_info['emotional_context'].append(direction)
            
            # Process dialogue for emotions
            dialogue_lower = entry.dialogue.lower()
            dialogue_words = set(dialogue_lower.split())
            
            for keyword in emotion_keywords & dialogue_words:
                scene_info['emotional_context'].append(f"Character {keyword}")
            
            scenes[entry.id] = scene_info
        
        return scenes
    
    def to_json_streaming(self, entries: Iterator[ScriptEntry], 
                         output_file: Union[str, Path]):
        """Export entries to JSON in streaming fashion."""
        output_file = Path(output_file)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('{"entries": [\n')
            
            first = True
            for entry in entries:
                if not first:
                    f.write(',\n')
                first = False
                
                json.dump(entry.to_dict(), f, ensure_ascii=False)
            
            f.write('\n]}')
    
    def validate_entries(self, entries: Union[List[ScriptEntry], Iterator[ScriptEntry]]) -> List[str]:
        """Validate script entries."""
        issues = []
        seen_ids = set()
        id_list = []
        
        for entry in entries:
            # Check duplicate IDs
            if entry.id in seen_ids:
                issues.append(f"Duplicate ID: {entry.id}")
            seen_ids.add(entry.id)
            
            # Collect numeric IDs
            if entry.id.isdigit():
                id_list.append(int(entry.id))
            
            # Check empty dialogue
            if not entry.dialogue.strip():
                issues.append(f"Empty dialogue in entry {entry.id}")
        
        # Check sequence gaps
        if id_list:
            id_list.sort()
            expected = set(range(id_list[0], id_list[-1] + 1))
            missing = expected - set(id_list)
            if missing:
                issues.append(f"Missing IDs: {sorted(missing)}")
        
        return issues


# Factory function for backwards compatibility
def create_parser(streaming: bool = False, strict: bool = False) -> OptimizedScriptParser:
    """Create a parser instance with specified options."""
    mode = ParserMode.STRICT if strict else ParserMode.STANDARD
    return OptimizedScriptParser(mode=mode)


# Alias for backwards compatibility
ScriptParser = OptimizedScriptParser