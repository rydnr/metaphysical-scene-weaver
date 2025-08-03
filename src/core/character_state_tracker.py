"""Character state tracking system for maintaining continuity across scenes."""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import logging
from enum import Enum


class StateChange(Enum):
    """Types of character state changes."""
    EMOTIONAL = "emotional"
    PHILOSOPHICAL = "philosophical"
    RELATIONAL = "relational"
    PHYSICAL = "physical"
    AWARENESS = "awareness"


@dataclass
class CharacterMoment:
    """Represents a character's state at a specific moment."""
    entry_id: str
    timestamp: datetime
    emotional_state: str
    philosophical_stance: Optional[str] = None
    awareness_level: int = 0  # 0-3 scale
    relationships: Dict[str, str] = field(default_factory=dict)
    visual_markers: List[str] = field(default_factory=list)
    internal_conflict: Optional[str] = None


@dataclass
class CharacterArc:
    """Tracks a character's journey throughout the narrative."""
    character_name: str
    moments: List[CharacterMoment] = field(default_factory=list)
    dominant_emotions: List[str] = field(default_factory=list)
    philosophical_evolution: List[str] = field(default_factory=list)
    key_realizations: List[Dict[str, Any]] = field(default_factory=list)
    visual_consistency: Dict[str, Any] = field(default_factory=dict)


class CharacterStateTracker:
    """Tracks and manages character states throughout the narrative."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.character_arcs: Dict[str, CharacterArc] = {}
        self.current_states: Dict[str, Dict[str, Any]] = {}
        
        # Emotional progression patterns
        self.emotional_progressions = {
            'awakening': ['confusion', 'curiosity', 'understanding', 'acceptance'],
            'conflict': ['calm', 'tension', 'anger', 'resolution'],
            'discovery': ['ignorance', 'questioning', 'revelation', 'integration'],
            'loss': ['wholeness', 'fracture', 'grief', 'transformation'],
            'connection': ['isolation', 'reaching', 'contact', 'unity']
        }
        
        # Philosophical stance evolution
        self.philosophical_stances = {
            'determinism': ['everything is predetermined', 'no free will', 'mechanical universe'],
            'free_will': ['choices matter', 'agency exists', 'responsibility'],
            'existentialism': ['existence precedes essence', 'meaning through action', 'authenticity'],
            'phenomenology': ['experience as primary', 'consciousness structures', 'intentionality'],
            'nihilism': ['no inherent meaning', 'value creation', 'absurdity'],
            'transcendentalism': ['beyond material', 'spiritual reality', 'unity of being']
        }
        
        # Awareness levels
        self.awareness_descriptions = {
            0: "unconscious patterns",
            1: "beginning awareness",
            2: "active questioning",
            3: "integrated understanding"
        }
        
    def update_from_entry(self, entry: 'ScriptEntry') -> None:
        """Update character state based on script entry."""
        character_name = entry.speaker.lower()
        
        # Initialize arc if new character
        if character_name not in self.character_arcs:
            self.character_arcs[character_name] = CharacterArc(character_name)
            self.current_states[character_name] = self._initialize_state(character_name)
        
        # Analyze entry for state changes
        state_changes = self._analyze_entry(entry)
        
        # Create moment
        moment = CharacterMoment(
            entry_id=entry.id,
            timestamp=datetime.now(),
            emotional_state=state_changes.get('emotional', 'neutral'),
            philosophical_stance=state_changes.get('philosophical'),
            awareness_level=state_changes.get('awareness', 0),
            relationships=state_changes.get('relationships', {}),
            visual_markers=state_changes.get('visual_markers', []),
            internal_conflict=state_changes.get('conflict')
        )
        
        # Update arc
        self.character_arcs[character_name].moments.append(moment)
        
        # Update current state
        self._update_current_state(character_name, state_changes)
        
        # Check for key realizations
        realization = self._check_for_realization(entry, self.current_states[character_name])
        if realization:
            self.character_arcs[character_name].key_realizations.append(realization)
    
    def get_state(self, character_name: str) -> Dict[str, Any]:
        """Get current state for a character."""
        character_name = character_name.lower()
        return self.current_states.get(character_name, self._initialize_state(character_name))
    
    def get_current_states(self) -> Dict[str, Dict[str, Any]]:
        """Get current states for all characters."""
        return self.current_states.copy()
    
    def get_character_arc(self, character_name: str) -> Optional[CharacterArc]:
        """Get complete arc for a character."""
        return self.character_arcs.get(character_name.lower())
    
    def get_relationship_dynamics(self) -> Dict[str, Dict[str, str]]:
        """Get current relationship dynamics between all characters."""
        dynamics = {}
        
        for char_name, state in self.current_states.items():
            if 'relationships' in state:
                dynamics[char_name] = state['relationships']
        
        return dynamics
    
    def _initialize_state(self, character_name: str) -> Dict[str, Any]:
        """Initialize a new character state."""
        return {
            'name': character_name,
            'emotional': 'neutral',
            'intensity': 0.5,
            'philosophical_stance': None,
            'awareness_level': 0,
            'relationships': {},
            'visual_consistency': {
                'base_appearance': None,
                'emotional_markers': [],
                'philosophical_symbols': []
            },
            'arc_position': 'beginning',
            'internal_state': {
                'conflicts': [],
                'desires': [],
                'fears': []
            }
        }
    
    def _analyze_entry(self, entry: 'ScriptEntry') -> Dict[str, Any]:
        """Analyze entry for state changes."""
        changes = {}
        
        # Analyze dialogue
        dialogue_lower = entry.dialogue.lower()
        
        # Emotional analysis
        emotion = self._detect_emotion(dialogue_lower, entry.stage_directions)
        if emotion:
            changes['emotional'] = emotion['state']
            changes['intensity'] = emotion['intensity']
        
        # Philosophical analysis
        philosophical = self._detect_philosophical_shift(dialogue_lower, entry.metadata)
        if philosophical:
            changes['philosophical'] = philosophical
            
        # Awareness level
        awareness = self._assess_awareness_level(dialogue_lower, entry.metadata)
        changes['awareness'] = awareness
        
        # Relationship changes
        relationships = self._detect_relationship_changes(dialogue_lower, entry.speaker)
        if relationships:
            changes['relationships'] = relationships
            
        # Visual markers
        visual_markers = self._extract_visual_markers(entry.stage_directions, emotion)
        if visual_markers:
            changes['visual_markers'] = visual_markers
            
        # Internal conflict
        conflict = self._detect_internal_conflict(dialogue_lower, entry.metadata)
        if conflict:
            changes['conflict'] = conflict
        
        return changes
    
    def _detect_emotion(
        self,
        dialogue: str,
        stage_directions: List[str]
    ) -> Optional[Dict[str, Any]]:
        """Detect emotional state from dialogue and stage directions."""
        emotions = {
            # Basic emotions
            'joy': ['happy', 'laugh', 'smile', 'delight', 'wonderful', 'cheerful', 'jubilant'],
            'sadness': ['sad', 'cry', 'tears', 'grief', 'sorrow', 'weep', 'mourn'],
            'anger': ['angry', 'furious', 'rage', 'frustrated', 'livid', 'wrathful'],
            'fear': ['afraid', 'scared', 'terrified', 'anxious', 'panicked', 'dread'],
            'confusion': ['confused', 'puzzled', 'lost', 'uncertain', 'bewildered', 'perplexed'],
            'contemplation': ['think', 'ponder', 'consider', 'reflect', 'meditate', 'muse'],
            'determination': ['determined', 'resolved', 'decided', 'will', 'committed', 'steadfast'],
            'love': ['love', 'adore', 'cherish', 'affection', 'tender', 'devoted'],
            
            # Nuanced emotions
            'melancholy': ['melancholy', 'wistful', 'nostalgic', 'longing', 'yearning', 'pensive'],
            'existential_dread': ['void', 'meaningless', 'absurd', 'empty', 'futile', 'abyss'],
            'transcendent_joy': ['bliss', 'euphoria', 'rapture', 'divine', 'enlightened', 'ecstasy'],
            'bittersweet': ['bittersweet', 'mixed feelings', 'happy sad', 'nostalgic joy'],
            'ennui': ['bored', 'listless', 'apathetic', 'weary', 'jaded', 'blasé'],
            'wonder': ['wonder', 'awe', 'marvel', 'astonish', 'fascinate', 'mesmerize'],
            'serenity': ['serene', 'peaceful', 'calm', 'tranquil', 'centered', 'balanced'],
            'nostalgia': ['remember', 'past', 'memory', 'yesteryear', 'bygone', 'reminisce'],
            'yearning': ['yearn', 'long for', 'pine', 'crave', 'ache for', 'hunger for'],
            'sublime': ['sublime', 'magnificent', 'glorious', 'majestic', 'transcendent beauty']
        }
        
        detected_emotions = {}
        for emotion, keywords in emotions.items():
            score = sum(1 for keyword in keywords if keyword in dialogue)
            if score > 0:
                detected_emotions[emotion] = score
        
        # Check stage directions
        stage_text = ' '.join(stage_directions).lower()
        for emotion, keywords in emotions.items():
            score = sum(1 for keyword in keywords if keyword in stage_text)
            if score > 0:
                detected_emotions[emotion] = detected_emotions.get(emotion, 0) + score * 1.5
        
        if detected_emotions:
            primary_emotion = max(detected_emotions.items(), key=lambda x: x[1])
            intensity = min(1.0, primary_emotion[1] * 0.3)
            
            return {
                'state': primary_emotion[0],
                'intensity': intensity
            }
        
        return None
    
    def _detect_philosophical_shift(
        self,
        dialogue: str,
        metadata: List[str]
    ) -> Optional[str]:
        """Detect shifts in philosophical stance."""
        for stance, indicators in self.philosophical_stances.items():
            for indicator in indicators:
                if any(word in dialogue for word in indicator.split()):
                    return stance
        
        # Check metadata for philosophical indicators
        meta_text = ' '.join(metadata).lower()
        if 'philosophy' in meta_text or 'existential' in meta_text:
            # More sophisticated detection based on content
            if 'choice' in dialogue or 'free' in dialogue:
                return 'free_will'
            elif 'meaning' in dialogue or 'purpose' in dialogue:
                return 'existentialism'
            elif 'determined' in dialogue or 'fate' in dialogue:
                return 'determinism'
        
        return None
    
    def _assess_awareness_level(
        self,
        dialogue: str,
        metadata: List[str]
    ) -> int:
        """Assess character's awareness level."""
        awareness_indicators = {
            0: ['unconscious', 'unaware', 'blind', 'automatic'],
            1: ['notice', 'begin to see', 'start to', 'maybe'],
            2: ['question', 'wonder', 'explore', 'investigate'],
            3: ['understand', 'realize', 'integrate', 'transcend']
        }
        
        current_level = 0
        for level, indicators in awareness_indicators.items():
            if any(indicator in dialogue for indicator in indicators):
                current_level = max(current_level, level)
        
        # Check for meta-cognition in metadata
        if metadata and any('meta' in m for m in metadata):
            current_level = min(3, current_level + 1)
        
        return current_level
    
    def _detect_relationship_changes(
        self,
        dialogue: str,
        speaker: str
    ) -> Dict[str, str]:
        """Detect changes in relationships with other characters."""
        relationships = {}
        
        # Look for mentions of other characters
        # This is simplified - in real implementation would need character list
        relationship_keywords = {
            'positive': ['love', 'care', 'appreciate', 'understand', 'connect'],
            'negative': ['hate', 'distrust', 'fear', 'resent', 'oppose'],
            'neutral': ['see', 'observe', 'notice', 'acknowledge'],
            'questioning': ['wonder about', 'curious about', 'question']
        }
        
        for rel_type, keywords in relationship_keywords.items():
            if any(keyword in dialogue for keyword in keywords):
                # This would need to identify which character is referenced
                relationships['other'] = rel_type
        
        return relationships
    
    def _extract_visual_markers(
        self,
        stage_directions: List[str],
        emotion: Optional[Dict[str, Any]]
    ) -> List[str]:
        """Extract visual markers for continuity."""
        markers = []
        
        # From stage directions
        for direction in stage_directions:
            if any(word in direction.lower() for word in ['gesture', 'posture', 'expression', 'gaze', 'stance']):
                markers.append(direction)
        
        # From emotion - expanded for nuanced emotions
        if emotion:
            emotion_state = emotion.get('state')
            emotion_markers = {
                'contemplation': 'thoughtful gaze',
                'determination': 'firm stance',
                'confusion': 'furrowed brow',
                'joy': 'bright eyes, open posture',
                'sadness': 'downcast eyes, slumped shoulders',
                'anger': 'clenched jaw, tense posture',
                'fear': 'wide eyes, defensive stance',
                'love': 'soft gaze, gentle gestures',
                'melancholy': 'distant gaze, subtle sighs',
                'existential_dread': 'hollow stare, rigid posture',
                'transcendent_joy': 'radiant expression, ethereal presence',
                'bittersweet': 'wistful smile, complex expression',
                'ennui': 'listless movements, vacant expression',
                'wonder': 'eyes wide with curiosity, open hands',
                'serenity': 'peaceful countenance, relaxed body',
                'nostalgia': 'faraway look, gentle smile',
                'yearning': 'reaching gesture, longing gaze',
                'sublime': 'awestruck expression, still presence'
            }
            
            if emotion_state in emotion_markers:
                markers.append(emotion_markers[emotion_state])
        
        return markers[:3]  # Limit to 3 markers
    
    def _detect_internal_conflict(
        self,
        dialogue: str,
        metadata: List[str]
    ) -> Optional[str]:
        """Detect internal conflicts."""
        conflict_patterns = {
            'identity': ['who am i', 'what am i', 'my true self'],
            'choice': ['should i', 'must choose', 'torn between'],
            'belief': ['used to believe', 'questioning', 'doubt'],
            'desire': ['want but', 'wish but', 'yearn yet']
        }
        
        for conflict_type, patterns in conflict_patterns.items():
            if any(pattern in dialogue for pattern in patterns):
                return f"{conflict_type} conflict"
        
        return None
    
    def _update_current_state(
        self,
        character_name: str,
        changes: Dict[str, Any]
    ) -> None:
        """Update current state with changes."""
        state = self.current_states[character_name]
        
        # Update emotional state
        if 'emotional' in changes:
            state['emotional'] = changes['emotional']
            state['intensity'] = changes.get('intensity', 0.5)
            
            # Track dominant emotions
            arc = self.character_arcs[character_name]
            arc.dominant_emotions.append(changes['emotional'])
        
        # Update philosophical stance
        if 'philosophical' in changes:
            old_stance = state.get('philosophical_stance')
            state['philosophical_stance'] = changes['philosophical']
            
            # Track evolution
            if old_stance != changes['philosophical']:
                arc = self.character_arcs[character_name]
                arc.philosophical_evolution.append(changes['philosophical'])
        
        # Update awareness
        if 'awareness' in changes:
            state['awareness_level'] = changes['awareness']
        
        # Update relationships
        if 'relationships' in changes:
            state['relationships'].update(changes['relationships'])
        
        # Update visual markers
        if 'visual_markers' in changes:
            state['visual_consistency']['emotional_markers'] = changes['visual_markers']
        
        # Update internal state
        if 'conflict' in changes:
            state['internal_state']['conflicts'].append(changes['conflict'])
        
        # Determine arc position
        state['arc_position'] = self._determine_arc_position(character_name)
    
    def _check_for_realization(
        self,
        entry: 'ScriptEntry',
        current_state: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Check if this moment represents a key realization."""
        dialogue_lower = entry.dialogue.lower()
        
        realization_indicators = [
            'i understand',
            'i see now',
            'i realize',
            'it becomes clear',
            'the truth is',
            'finally know'
        ]
        
        for indicator in realization_indicators:
            if indicator in dialogue_lower:
                return {
                    'entry_id': entry.id,
                    'type': 'realization',
                    'content': entry.dialogue,
                    'awareness_level': current_state['awareness_level'],
                    'emotional_context': current_state['emotional']
                }
        
        # Check for philosophical breakthroughs
        if current_state['awareness_level'] >= 2 and 'philosophical' in current_state:
            if any(word in dialogue_lower for word in ['truth', 'meaning', 'purpose']):
                return {
                    'entry_id': entry.id,
                    'type': 'philosophical_breakthrough',
                    'content': entry.dialogue,
                    'stance': current_state['philosophical_stance']
                }
        
        return None
    
    def _determine_arc_position(self, character_name: str) -> str:
        """Determine where character is in their arc."""
        arc = self.character_arcs[character_name]
        
        if len(arc.moments) < 5:
            return 'beginning'
        
        # Check for progression patterns
        recent_emotions = [m.emotional_state for m in arc.moments[-5:]]
        recent_awareness = [m.awareness_level for m in arc.moments[-5:]]
        
        # Rising awareness suggests middle
        if sum(recent_awareness) > sum(recent_awareness[:3]):
            if max(recent_awareness) >= 3:
                return 'climax'
            return 'middle'
        
        # Multiple realizations suggest approaching end
        if len(arc.key_realizations) >= 2:
            return 'resolution'
        
        return 'middle'
    
    def generate_arc_summary(self, character_name: str) -> Dict[str, Any]:
        """Generate a summary of a character's arc."""
        arc = self.character_arcs.get(character_name.lower())
        if not arc:
            return {}
        
        # Emotional journey
        emotion_frequency = {}
        for emotion in arc.dominant_emotions:
            emotion_frequency[emotion] = emotion_frequency.get(emotion, 0) + 1
        
        # Philosophical journey
        philosophical_journey = ' → '.join(arc.philosophical_evolution) if arc.philosophical_evolution else 'static'
        
        # Awareness progression
        awareness_progression = []
        for moment in arc.moments[::max(1, len(arc.moments)//5)]:  # Sample 5 points
            awareness_progression.append(moment.awareness_level)
        
        return {
            'character': character_name,
            'total_moments': len(arc.moments),
            'emotional_journey': emotion_frequency,
            'philosophical_journey': philosophical_journey,
            'awareness_progression': awareness_progression,
            'key_realizations': len(arc.key_realizations),
            'current_position': self.current_states[character_name.lower()]['arc_position']
        }