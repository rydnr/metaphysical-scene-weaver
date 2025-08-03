"""Text processing utilities for script parsing and analysis."""

import re
import unicodedata
from typing import List, Dict, Tuple, Optional, Set
from collections import Counter
import string


class TextNormalizer:
    """Normalize and clean text for consistent processing."""
    
    def __init__(self):
        # Precompile common patterns
        self.whitespace_pattern = re.compile(r'\s+')
        self.punctuation_pattern = re.compile(r'[^\w\s-]')
        self.quote_pattern = re.compile(r'[""''`´]')
        self.dash_pattern = re.compile(r'[—–-]+')
        
    def normalize_whitespace(self, text: str) -> str:
        """Normalize all whitespace to single spaces."""
        return self.whitespace_pattern.sub(' ', text).strip()
    
    def normalize_unicode(self, text: str) -> str:
        """Normalize Unicode characters to canonical form."""
        # NFD for decomposed form, then filter combining characters if needed
        return unicodedata.normalize('NFC', text)
    
    def normalize_quotes(self, text: str) -> str:
        """Normalize various quote styles to standard ASCII."""
        text = self.quote_pattern.sub('"', text)
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        return text
    
    def normalize_dashes(self, text: str) -> str:
        """Normalize various dash styles to standard hyphen."""
        return self.dash_pattern.sub('-', text)
    
    def clean_dialogue(self, text: str, preserve_emphasis: bool = True) -> str:
        """Clean dialogue text while preserving important formatting."""
        # Normalize unicode first
        text = self.normalize_unicode(text)
        
        # Normalize quotes and dashes
        text = self.normalize_quotes(text)
        text = self.normalize_dashes(text)
        
        # Normalize whitespace
        text = self.normalize_whitespace(text)
        
        # Optionally preserve emphasis markers
        if not preserve_emphasis:
            text = text.replace('*', '').replace('_', '').replace('~', '')
        
        return text
    
    def extract_emphasis(self, text: str) -> Dict[str, List[str]]:
        """Extract emphasized portions of text."""
        emphasis = {
            'italic': [],
            'bold': [],
            'underline': []
        }
        
        # Common emphasis patterns
        italic_pattern = re.compile(r'\*([^*]+)\*|_([^_]+)_')
        bold_pattern = re.compile(r'\*\*([^*]+)\*\*|__([^_]+)__')
        
        for match in italic_pattern.finditer(text):
            emphasis['italic'].append(match.group(1) or match.group(2))
        
        for match in bold_pattern.finditer(text):
            emphasis['bold'].append(match.group(1) or match.group(2))
        
        return emphasis


class DialogueAnalyzer:
    """Analyze dialogue for various linguistic features."""
    
    def __init__(self):
        # Question patterns
        self.question_pattern = re.compile(r'[.!?]\s*$')
        self.question_words = {'what', 'when', 'where', 'who', 'why', 'how', 
                               'which', 'whose', 'whom'}
        
        # Emotion indicators
        self.emotion_indicators = {
            'joy': ['happy', 'joy', 'laugh', 'smile', 'excited', 'wonderful'],
            'sadness': ['sad', 'cry', 'tears', 'sorrow', 'grief', 'mourn'],
            'anger': ['angry', 'rage', 'furious', 'mad', 'irritated', 'annoyed'],
            'fear': ['afraid', 'scared', 'terrified', 'nervous', 'anxious', 'worry'],
            'surprise': ['surprised', 'amazed', 'astonished', 'shock', 'unexpected'],
            'disgust': ['disgusted', 'revolted', 'repulsed', 'sick', 'nauseous']
        }
        
    def is_question(self, text: str) -> bool:
        """Determine if text is a question."""
        text = text.strip().lower()
        
        # Check for question mark
        if text.endswith('?'):
            return True
        
        # Check for question words at start
        first_word = text.split()[0] if text else ''
        return first_word in self.question_words
    
    def extract_dialogue_type(self, text: str) -> str:
        """Classify dialogue type."""
        text = text.strip()
        
        if self.is_question(text):
            return 'question'
        elif text.endswith('!'):
            return 'exclamation'
        elif text.endswith('...') or text.endswith('…'):
            return 'trailing'
        else:
            return 'statement'
    
    def detect_emotions(self, text: str) -> Dict[str, float]:
        """Detect emotional content in text."""
        text_lower = text.lower()
        words = text_lower.split()
        
        emotion_scores = {}
        for emotion, indicators in self.emotion_indicators.items():
            score = sum(1 for word in words if word in indicators)
            if score > 0:
                emotion_scores[emotion] = score / len(words)
        
        return emotion_scores
    
    def calculate_dialogue_length(self, text: str) -> Dict[str, int]:
        """Calculate various length metrics."""
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        
        return {
            'characters': len(text),
            'words': len(words),
            'sentences': len([s for s in sentences if s.strip()]),
            'average_word_length': sum(len(w) for w in words) / len(words) if words else 0
        }


class CharacterNameHandler:
    """Handle character name variations and normalization."""
    
    def __init__(self):
        self.name_variations: Dict[str, Set[str]] = {}
        self.canonical_names: Dict[str, str] = {}
        
    def add_name_variation(self, canonical: str, variation: str):
        """Add a name variation for a character."""
        canonical = canonical.upper()
        variation = variation.upper()
        
        if canonical not in self.name_variations:
            self.name_variations[canonical] = set()
        
        self.name_variations[canonical].add(variation)
        self.canonical_names[variation] = canonical
        
    def normalize_name(self, name: str) -> str:
        """Get canonical form of a character name."""
        name_upper = name.upper()
        return self.canonical_names.get(name_upper, name)
    
    def merge_similar_names(self, names: List[str], 
                          threshold: float = 0.8) -> Dict[str, str]:
        """Merge similar character names using string similarity."""
        from difflib import SequenceMatcher
        
        merged = {}
        processed = set()
        
        for i, name1 in enumerate(names):
            if name1 in processed:
                continue
                
            # This name becomes canonical
            merged[name1] = name1
            processed.add(name1)
            
            # Check similarity with remaining names
            for name2 in names[i+1:]:
                if name2 in processed:
                    continue
                    
                similarity = SequenceMatcher(None, name1.upper(), 
                                           name2.upper()).ratio()
                if similarity >= threshold:
                    merged[name2] = name1
                    processed.add(name2)
                    self.add_name_variation(name1, name2)
        
        return merged


class TextChunker:
    """Split text into chunks for processing large scripts."""
    
    def __init__(self, chunk_size: int = 1000, overlap: int = 100):
        self.chunk_size = chunk_size
        self.overlap = overlap
        
    def chunk_by_lines(self, lines: List[str]) -> List[List[str]]:
        """Split lines into overlapping chunks."""
        chunks = []
        
        for i in range(0, len(lines), self.chunk_size - self.overlap):
            chunk = lines[i:i + self.chunk_size]
            chunks.append(chunk)
            
            # Stop if we've processed all lines
            if i + self.chunk_size >= len(lines):
                break
        
        return chunks
    
    def chunk_by_entries(self, entries: List[Dict[str, any]], 
                        target_size: int = 50) -> List[List[Dict[str, any]]]:
        """Split entries into chunks of target size."""
        chunks = []
        
        for i in range(0, len(entries), target_size):
            chunk = entries[i:i + target_size]
            chunks.append(chunk)
        
        return chunks
    
    def smart_chunk_text(self, text: str, delimiter: str = '\n\n') -> List[str]:
        """Split text intelligently at natural boundaries."""
        # First split by delimiter
        sections = text.split(delimiter)
        
        chunks = []
        current_chunk = []
        current_size = 0
        
        for section in sections:
            section_size = len(section)
            
            if current_size + section_size > self.chunk_size and current_chunk:
                # Save current chunk
                chunks.append(delimiter.join(current_chunk))
                current_chunk = [section]
                current_size = section_size
            else:
                current_chunk.append(section)
                current_size += section_size
        
        # Don't forget the last chunk
        if current_chunk:
            chunks.append(delimiter.join(current_chunk))
        
        return chunks


class ScriptStatistics:
    """Calculate statistics for parsed scripts."""
    
    @staticmethod
    def calculate_speaker_stats(entries: List[Dict[str, any]]) -> Dict[str, any]:
        """Calculate speaker-related statistics."""
        speaker_counts = Counter(entry.get('speaker', 'Unknown') 
                                for entry in entries)
        
        total_entries = len(entries)
        speakers = list(speaker_counts.keys())
        
        # Calculate dialogue dominance
        dominance = {}
        for speaker, count in speaker_counts.items():
            dominance[speaker] = count / total_entries
        
        return {
            'total_speakers': len(speakers),
            'speakers': speakers,
            'entry_counts': dict(speaker_counts),
            'dominance_percentages': dominance,
            'most_active': speaker_counts.most_common(1)[0] if speaker_counts else None,
            'least_active': speaker_counts.most_common()[-1] if speaker_counts else None
        }
    
    @staticmethod
    def calculate_dialogue_stats(entries: List[Dict[str, any]]) -> Dict[str, any]:
        """Calculate dialogue-related statistics."""
        analyzer = DialogueAnalyzer()
        
        total_words = 0
        total_chars = 0
        dialogue_types = Counter()
        
        for entry in entries:
            dialogue = entry.get('dialogue', '')
            total_words += len(dialogue.split())
            total_chars += len(dialogue)
            dialogue_types[analyzer.extract_dialogue_type(dialogue)] += 1
        
        avg_words = total_words / len(entries) if entries else 0
        avg_chars = total_chars / len(entries) if entries else 0
        
        return {
            'total_dialogues': len(entries),
            'total_words': total_words,
            'total_characters': total_chars,
            'average_words_per_entry': avg_words,
            'average_chars_per_entry': avg_chars,
            'dialogue_types': dict(dialogue_types)
        }
    
    @staticmethod
    def calculate_metadata_stats(entries: List[Dict[str, any]]) -> Dict[str, any]:
        """Calculate metadata and annotation statistics."""
        total_metadata = 0
        total_stage_directions = 0
        metadata_tags = Counter()
        
        entries_with_metadata = 0
        entries_with_stage = 0
        entries_with_panels = 0
        
        for entry in entries:
            metadata = entry.get('metadata', [])
            stage = entry.get('stage_directions', [])
            
            if metadata:
                entries_with_metadata += 1
                total_metadata += len(metadata)
                metadata_tags.update(metadata)
            
            if stage:
                entries_with_stage += 1
                total_stage_directions += len(stage)
            
            if entry.get('panel_count') is not None:
                entries_with_panels += 1
        
        return {
            'entries_with_metadata': entries_with_metadata,
            'entries_with_stage_directions': entries_with_stage,
            'entries_with_panel_info': entries_with_panels,
            'total_metadata_tags': total_metadata,
            'total_stage_directions': total_stage_directions,
            'top_metadata_tags': metadata_tags.most_common(10),
            'unique_metadata_tags': len(metadata_tags)
        }


# Utility functions
def clean_script_text(text: str) -> str:
    """Clean raw script text for parsing."""
    normalizer = TextNormalizer()
    
    # Normalize unicode and whitespace
    text = normalizer.normalize_unicode(text)
    text = normalizer.normalize_whitespace(text)
    
    # Fix common OCR/copy-paste errors
    text = text.replace('<<', '<<').replace('>>', '>>')
    text = text.replace('[[', '[[').replace(']]', ']]')
    
    return text


def validate_dialogue_brackets(text: str) -> List[str]:
    """Validate that dialogue brackets are properly matched."""
    issues = []
    
    # Count opening and closing brackets
    open_dialogue = text.count('<<')
    close_dialogue = text.count('>>')
    
    if open_dialogue != close_dialogue:
        issues.append(f"Mismatched dialogue brackets: {open_dialogue} << vs {close_dialogue} >>")
    
    open_meta = text.count('[[')
    close_meta = text.count(']]')
    
    if open_meta != close_meta:
        issues.append(f"Mismatched metadata brackets: {open_meta} [[ vs {close_meta} ]]")
    
    return issues