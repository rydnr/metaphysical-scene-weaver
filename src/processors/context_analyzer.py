"""Context analysis engine for understanding scene context and relationships."""

from typing import Dict, List, Any, Optional, Tuple
import logging
from dataclasses import dataclass
from pathlib import Path


@dataclass
class SceneContext:
    """Represents the context of a scene."""
    character: Dict[str, Any]
    setting: Dict[str, Any]
    narrative_position: str  # beginning, middle, end
    surrounding_context: Dict[str, Any]
    temporal_context: str  # time of day, season, etc.
    relational_context: Dict[str, str]  # relationships between characters


class ContextAnalyzer:
    """Analyzes narrative and visual context for scenes."""
    
    def __init__(self, characters_data: Dict[str, Any], places_data: Dict[str, Any]):
        self.logger = logging.getLogger(__name__)
        self.characters = characters_data
        self.places = places_data
        
        # Context window for analysis
        self.context_window = 5  # Look at 5 entries before and after
        
        # Temporal markers
        self.temporal_markers = {
            'dawn': ['dawn', 'sunrise', 'morning', 'early'],
            'day': ['afternoon', 'noon', 'midday', 'daylight'],
            'dusk': ['dusk', 'sunset', 'evening', 'twilight'],
            'night': ['night', 'midnight', 'dark', 'stars']
        }
        
        # Location inference patterns
        self.location_patterns = {
            'forest': ['trees', 'woods', 'nature', 'leaves', 'path'],
            'street': ['city', 'urban', 'buildings', 'concrete', 'crowd'],
            'interior': ['room', 'inside', 'walls', 'ceiling', 'door'],
            'abstract': ['void', 'space', 'dimension', 'realm', 'consciousness']
        }
        
        # Narrative progression markers
        self.progression_markers = {
            'beginning': ['first', 'introduction', 'meet', 'begin', 'start'],
            'development': ['then', 'next', 'continue', 'develop', 'explore'],
            'climax': ['realize', 'understand', 'revelation', 'truth', 'finally'],
            'resolution': ['accept', 'integrate', 'peace', 'end', 'complete']
        }
        
    def analyze_context(
        self,
        entry: 'ScriptEntry',
        index: int,
        all_entries: List['ScriptEntry'],
        character_states: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze complete context for a scene."""
        # Get character info
        character = self._get_character_info(entry.speaker)
        
        # Determine setting
        setting = self._determine_setting(entry, all_entries, index)
        
        # Analyze narrative position
        narrative_position = self._determine_narrative_position(index, len(all_entries), entry)
        
        # Get surrounding context
        surrounding = self._analyze_surrounding_entries(index, all_entries)
        
        # Determine temporal context
        temporal = self._determine_temporal_context(entry, surrounding)
        
        # Analyze relationships
        relationships = self._analyze_relationships(entry, character_states, surrounding)
        
        # Build complete context
        return {
            'character': character,
            'setting': setting,
            'narrative_position': narrative_position,
            'narrative_progress': index / max(len(all_entries) - 1, 1),  # 0.0 to 1.0
            'surrounding_entries': surrounding,
            'temporal_context': temporal,
            'relationships': relationships,
            'scene_mood': self._determine_scene_mood(entry, surrounding),
            'dialogue_context': self._analyze_dialogue_context(entry, surrounding),
            'visual_continuity': self._analyze_visual_continuity(index, all_entries),
            'thematic_elements': self._extract_thematic_elements(entry, surrounding)
        }
    
    def _get_character_info(self, speaker_name: str) -> Dict[str, Any]:
        """Get character information from data."""
        speaker_lower = speaker_name.lower()
        
        # Look for character in data
        for char_key, char_data in self.characters.items():
            if char_data['name'].lower() == speaker_lower:
                return {
                    'name': char_data['name'],
                    'visual_description': char_data.get('appearance', ''),
                    'style_notes': char_data.get('style_notes', ''),
                    'key_visual_elements': char_data.get('visual_elements', []),
                    'personality_traits': char_data.get('personality', []),
                    'full_data': char_data
                }
        
        # Default if character not found
        return {
            'name': speaker_name,
            'visual_description': f'{speaker_name} character',
            'style_notes': '',
            'key_visual_elements': [],
            'personality_traits': []
        }
    
    def _determine_setting(
        self,
        entry: 'ScriptEntry',
        all_entries: List['ScriptEntry'],
        index: int
    ) -> Dict[str, Any]:
        """Determine the setting for the scene."""
        # Check for explicit location in stage directions
        for direction in entry.stage_directions:
            for location, patterns in self.location_patterns.items():
                if any(pattern in direction.lower() for pattern in patterns):
                    return self._get_place_info(location)
        
        # Check dialogue for location hints
        dialogue_lower = entry.dialogue.lower()
        for location, patterns in self.location_patterns.items():
            if any(pattern in dialogue_lower for pattern in patterns):
                return self._get_place_info(location)
        
        # Check surrounding entries
        for i in range(max(0, index-2), min(len(all_entries), index+3)):
            if i != index:
                other_entry = all_entries[i]
                for direction in other_entry.stage_directions:
                    for location, patterns in self.location_patterns.items():
                        if any(pattern in direction.lower() for pattern in patterns):
                            return self._get_place_info(location)
        
        # Default to abstract space
        return self._get_place_info('abstract')
    
    def _get_place_info(self, location_key: str) -> Dict[str, Any]:
        """Get place information from data."""
        # Look for place in data
        for place_key, place_data in self.places.items():
            if place_key == location_key:
                return {
                    'name': place_data.get('name', location_key),
                    'description': place_data.get('description', ''),
                    'atmosphere': place_data.get('atmosphere', ''),
                    'key_elements': place_data.get('elements', []),
                    'lighting': place_data.get('lighting', 'natural'),
                    'mood': place_data.get('mood', 'neutral'),
                    'full_data': place_data
                }
        
        # Default if place not found
        return {
            'name': location_key,
            'description': f'{location_key} setting',
            'atmosphere': 'atmospheric',
            'key_elements': [],
            'lighting': 'natural',
            'mood': 'neutral'
        }
    
    def _determine_narrative_position(
        self,
        index: int,
        total_entries: int,
        entry: 'ScriptEntry'
    ) -> str:
        """Determine where we are in the narrative arc."""
        position_ratio = index / max(total_entries - 1, 1)
        
        # Check for explicit markers in dialogue
        dialogue_lower = entry.dialogue.lower()
        for position, markers in self.progression_markers.items():
            if any(marker in dialogue_lower for marker in markers):
                return position
        
        # Position-based determination
        if position_ratio < 0.15:
            return 'beginning'
        elif position_ratio < 0.7:
            return 'development'
        elif position_ratio < 0.9:
            return 'climax'
        else:
            return 'resolution'
    
    def _analyze_surrounding_entries(
        self,
        index: int,
        all_entries: List['ScriptEntry']
    ) -> Dict[str, Any]:
        """Analyze surrounding entries for context."""
        before_start = max(0, index - self.context_window)
        after_end = min(len(all_entries), index + self.context_window + 1)
        
        before_entries = all_entries[before_start:index]
        after_entries = all_entries[index + 1:after_end]
        
        return {
            'before': [
                {
                    'speaker': e.speaker,
                    'emotional_tone': self._quick_emotion_detect(e.dialogue),
                    'key_concept': self._extract_key_concept(e.dialogue)
                }
                for e in before_entries
            ],
            'after': [
                {
                    'speaker': e.speaker,
                    'emotional_tone': self._quick_emotion_detect(e.dialogue),
                    'key_concept': self._extract_key_concept(e.dialogue)
                }
                for e in after_entries
            ],
            'conversation_flow': self._analyze_conversation_flow(before_entries, after_entries),
            'topic_evolution': self._track_topic_evolution(before_entries + [all_entries[index]] + after_entries)
        }
    
    def _determine_temporal_context(
        self,
        entry: 'ScriptEntry',
        surrounding: Dict[str, Any]
    ) -> str:
        """Determine temporal context of the scene."""
        # Check current entry
        all_text = entry.dialogue.lower() + ' '.join(entry.stage_directions).lower()
        
        for time_period, markers in self.temporal_markers.items():
            if any(marker in all_text for marker in markers):
                return time_period
        
        # Check metadata
        for meta in entry.metadata:
            for time_period, markers in self.temporal_markers.items():
                if any(marker in meta.lower() for marker in markers):
                    return time_period
        
        # Default based on mood
        return 'undefined'
    
    def _analyze_relationships(
        self,
        entry: 'ScriptEntry',
        character_states: Dict[str, Dict[str, Any]],
        surrounding: Dict[str, Any]
    ) -> Dict[str, str]:
        """Analyze relationships between characters."""
        relationships = {}
        current_speaker = entry.speaker.lower()
        
        # Get relationships from character states
        if current_speaker in character_states:
            relationships.update(character_states[current_speaker].get('relationships', {}))
        
        # Analyze conversation partners
        conversation_partners = set()
        for context_entry in surrounding['before'] + surrounding['after']:
            if context_entry['speaker'].lower() != current_speaker:
                conversation_partners.add(context_entry['speaker'].lower())
        
        # Determine relationship quality based on conversation flow
        for partner in conversation_partners:
            if partner not in relationships:
                # Simple heuristic based on emotional tones
                relationships[partner] = 'conversing'
        
        return relationships
    
    def _determine_scene_mood(
        self,
        entry: 'ScriptEntry',
        surrounding: Dict[str, Any]
    ) -> str:
        """Determine overall mood of the scene."""
        # Collect emotional tones
        emotions = [self._quick_emotion_detect(entry.dialogue)]
        emotions.extend([e['emotional_tone'] for e in surrounding['before'][-2:]])
        emotions.extend([e['emotional_tone'] for e in surrounding['after'][:2]])
        
        # Count emotion frequencies
        emotion_counts = {}
        for emotion in emotions:
            if emotion:
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        if emotion_counts:
            dominant_emotion = max(emotion_counts.items(), key=lambda x: x[1])[0]
            
            # Map to mood
            mood_map = {
                'contemplative': 'philosophical',
                'confused': 'mysterious',
                'determined': 'purposeful',
                'fearful': 'tense',
                'joyful': 'uplifting',
                'sad': 'melancholic'
            }
            
            return mood_map.get(dominant_emotion, 'neutral')
        
        return 'neutral'
    
    def _analyze_dialogue_context(
        self,
        entry: 'ScriptEntry',
        surrounding: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze the dialogue context."""
        return {
            'dialogue_type': self._classify_dialogue_type(entry.dialogue),
            'response_to': surrounding['before'][-1] if surrounding['before'] else None,
            'leads_to': surrounding['after'][0] if surrounding['after'] else None,
            'conversation_depth': self._assess_conversation_depth(entry, surrounding),
            'topic_shift': self._detect_topic_shift(entry, surrounding)
        }
    
    def _analyze_visual_continuity(
        self,
        index: int,
        all_entries: List['ScriptEntry']
    ) -> Dict[str, Any]:
        """Analyze visual continuity needs."""
        continuity = {
            'maintain_from_previous': [],
            'prepare_for_next': [],
            'recurring_elements': []
        }
        
        # Check previous entry
        if index > 0:
            prev_entry = all_entries[index - 1]
            # Extract visual elements to maintain
            if prev_entry.stage_directions:
                continuity['maintain_from_previous'].extend(
                    [d for d in prev_entry.stage_directions if 'gesture' in d or 'position' in d]
                )
        
        # Check next entry
        if index < len(all_entries) - 1:
            next_entry = all_entries[index + 1]
            # Prepare for upcoming elements
            if next_entry.stage_directions:
                continuity['prepare_for_next'].extend(
                    [d for d in next_entry.stage_directions if 'enter' in d or 'approach' in d]
                )
        
        return continuity
    
    def _extract_thematic_elements(
        self,
        entry: 'ScriptEntry',
        surrounding: Dict[str, Any]
    ) -> List[str]:
        """Extract thematic elements from the scene."""
        themes = []
        
        # Common philosophical themes
        theme_keywords = {
            'identity': ['who', 'self', 'identity', 'am i'],
            'freedom': ['free', 'choice', 'cage', 'constraint'],
            'connection': ['together', 'alone', 'connect', 'separate'],
            'time': ['moment', 'time', 'past', 'future'],
            'reality': ['real', 'illusion', 'dream', 'truth']
        }
        
        dialogue_lower = entry.dialogue.lower()
        for theme, keywords in theme_keywords.items():
            if any(keyword in dialogue_lower for keyword in keywords):
                themes.append(theme)
        
        return themes[:3]  # Limit to top 3 themes
    
    def _quick_emotion_detect(self, text: str) -> str:
        """Quick emotion detection for context analysis."""
        text_lower = text.lower()
        
        emotion_keywords = {
            'joyful': ['happy', 'joy', 'laugh', 'smile'],
            'sad': ['sad', 'cry', 'tear', 'sorrow'],
            'fearful': ['afraid', 'fear', 'scared', 'terrified'],
            'confused': ['confused', 'puzzled', 'lost', 'unclear'],
            'contemplative': ['think', 'ponder', 'consider', 'reflect'],
            'determined': ['will', 'must', 'determined', 'resolved']
        }
        
        for emotion, keywords in emotion_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return emotion
        
        return 'neutral'
    
    def _extract_key_concept(self, text: str) -> str:
        """Extract key concept from text."""
        concepts = ['consciousness', 'freedom', 'identity', 'time', 'reality', 'connection']
        
        text_lower = text.lower()
        for concept in concepts:
            if concept in text_lower:
                return concept
        
        # Extract first significant noun
        significant_words = [w for w in text_lower.split() if len(w) > 4 and w.isalpha()]
        return significant_words[0] if significant_words else 'dialogue'
    
    def _analyze_conversation_flow(
        self,
        before: List['ScriptEntry'],
        after: List['ScriptEntry']
    ) -> str:
        """Analyze the flow of conversation."""
        if not before and not after:
            return 'isolated'
        
        # Check speaker patterns
        speakers_before = [e.speaker for e in before[-3:]]
        speakers_after = [e.speaker for e in after[:3]]
        
        # Determine flow type
        if len(set(speakers_before + speakers_after)) == 2:
            return 'dialogue'
        elif len(set(speakers_before + speakers_after)) > 3:
            return 'multi-party'
        else:
            return 'monologue-like'
    
    def _track_topic_evolution(self, entries: List['ScriptEntry']) -> List[str]:
        """Track how topics evolve in conversation."""
        topics = []
        
        for entry in entries:
            concept = self._extract_key_concept(entry.dialogue)
            if concept not in topics:
                topics.append(concept)
        
        return topics[-5:]  # Last 5 topics
    
    def _classify_dialogue_type(self, dialogue: str) -> str:
        """Classify the type of dialogue."""
        if '?' in dialogue:
            return 'question'
        elif '!' in dialogue:
            return 'exclamation'
        elif any(word in dialogue.lower() for word in ['i think', 'i believe', 'i feel']):
            return 'statement_personal'
        elif any(word in dialogue.lower() for word in ['you', 'your']):
            return 'address_other'
        else:
            return 'statement_general'
    
    def _assess_conversation_depth(
        self,
        entry: 'ScriptEntry',
        surrounding: Dict[str, Any]
    ) -> int:
        """Assess depth of conversation (0-3 scale)."""
        depth = 0
        
        # Check for philosophical concepts
        if any(concept in entry.dialogue.lower() for concept in 
               ['consciousness', 'existence', 'meaning', 'truth', 'reality']):
            depth += 1
        
        # Check for questions
        if '?' in entry.dialogue:
            depth += 1
        
        # Check for topic evolution
        if len(set(e['key_concept'] for e in surrounding['before'] + surrounding['after'])) > 3:
            depth += 1
        
        return min(3, depth)
    
    def _detect_topic_shift(
        self,
        entry: 'ScriptEntry',
        surrounding: Dict[str, Any]
    ) -> bool:
        """Detect if there's a topic shift."""
        current_concept = self._extract_key_concept(entry.dialogue)
        
        # Get previous concepts
        prev_concepts = [e['key_concept'] for e in surrounding['before'][-2:]]
        
        if prev_concepts and current_concept not in prev_concepts:
            return True
        
        return False