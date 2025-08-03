"""Detect points in script that need narrator bridges."""

from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
from enum import Enum

from .script_parser import ScriptEntry


class BridgeType(Enum):
    """Types of narrator bridges needed."""
    OPENING = "opening"
    CHARACTER_INTRO = "character_introduction"
    PHILOSOPHICAL_SHIFT = "philosophical_shift"
    REALITY_BEND = "reality_bend"
    EMOTIONAL_TURN = "emotional_turn"
    SCENE_TRANSITION = "scene_transition"
    CLOSING = "closing"


@dataclass
class BridgePoint:
    """Represents a point where narrator bridge is needed."""
    after_entry_id: str
    before_entry_id: str
    bridge_type: BridgeType
    reason: str
    suggested_content: str = ""
    visual_requirements: List[str] = None
    
    def __post_init__(self):
        if self.visual_requirements is None:
            self.visual_requirements = []


class BridgeDetector:
    """Detect and recommend narrator bridges in scripts."""
    
    def __init__(self):
        # Keywords that suggest philosophical shifts
        self.philosophy_keywords = {
            'free will', 'choice', 'consciousness', 'reality', 'illusion',
            'freedom', 'existence', 'awakening', 'belief', 'truth'
        }
        
        # Stage directions suggesting reality changes
        self.reality_bend_cues = {
            'shimmers', 'ripples', 'transforms', 'dissolves', 'morphs',
            'flickers', 'warps', 'bends', 'shifts', 'melts'
        }
        
        # Emotional intensity markers
        self.emotion_markers = {
            'uncertain', 'bewildered', 'frustrated', 'nervous', 'hesitant',
            'intense', 'thoughtful', 'confused', 'amazed', 'terrified'
        }
    
    def analyze_script(self, entries: List[ScriptEntry]) -> List[BridgePoint]:
        """Analyze script and identify bridge points."""
        bridges = []
        
        # Add opening bridge
        if entries:
            bridges.append(BridgePoint(
                after_entry_id="0000",
                before_entry_id=entries[0].id,
                bridge_type=BridgeType.OPENING,
                reason="Script needs opening context"
            ))
        
        # Analyze entries
        for i in range(len(entries)):
            current = entries[i]
            
            # Check for character introductions
            if self._is_new_character(current, entries[:i]):
                bridges.append(self._create_character_intro_bridge(current, entries[i-1] if i > 0 else None))
            
            # Check for philosophical shifts
            if i > 0 and self._detects_philosophical_shift(entries[i-1], current):
                bridges.append(self._create_philosophical_bridge(entries[i-1], current))
            
            # Check for reality bending moments
            if self._contains_reality_bend(current):
                bridges.append(self._create_reality_bend_bridge(
                    entries[i-1] if i > 0 else None, current
                ))
            
            # Check for emotional transitions
            if i > 0 and self._detects_emotional_shift(entries[i-1], current):
                bridges.append(self._create_emotional_bridge(entries[i-1], current))
        
        # Add closing bridge if needed
        if entries and self._needs_closing(entries[-1]):
            bridges.append(BridgePoint(
                after_entry_id=entries[-1].id,
                before_entry_id="9999",
                bridge_type=BridgeType.CLOSING,
                reason="Story reaches transformation point"
            ))
        
        return bridges
    
    def _is_new_character(self, entry: ScriptEntry, previous_entries: List[ScriptEntry]) -> bool:
        """Check if this is a character's first appearance."""
        previous_speakers = {e.speaker for e in previous_entries}
        return entry.speaker not in previous_speakers
    
    def _create_character_intro_bridge(self, entry: ScriptEntry, prev_entry: ScriptEntry) -> BridgePoint:
        """Create bridge for character introduction."""
        visual_reqs = []
        
        # Extract visual requirements from stage directions
        for direction in entry.stage_directions:
            if 'emerges' in direction or 'appears' in direction:
                visual_reqs.append('materialization_effect')
            if 'shadows' in direction:
                visual_reqs.append('shadow_transformation')
        
        return BridgePoint(
            after_entry_id=prev_entry.id if prev_entry else "0000",
            before_entry_id=entry.id,
            bridge_type=BridgeType.CHARACTER_INTRO,
            reason=f"First appearance of {entry.speaker}",
            visual_requirements=visual_reqs
        )
    
    def _detects_philosophical_shift(self, prev: ScriptEntry, current: ScriptEntry) -> bool:
        """Detect if there's a philosophical escalation."""
        prev_text = prev.dialogue.lower() + ' '.join(prev.metadata).lower()
        current_text = current.dialogue.lower() + ' '.join(current.metadata).lower()
        
        # Check for philosophy keywords
        prev_philosophical = any(kw in prev_text for kw in self.philosophy_keywords)
        current_philosophical = any(kw in current_text for kw in self.philosophy_keywords)
        
        # Shift detected if philosophy intensifies
        return not prev_philosophical and current_philosophical
    
    def _create_philosophical_bridge(self, prev: ScriptEntry, current: ScriptEntry) -> BridgePoint:
        """Create bridge for philosophical shifts."""
        return BridgePoint(
            after_entry_id=prev.id,
            before_entry_id=current.id,
            bridge_type=BridgeType.PHILOSOPHICAL_SHIFT,
            reason="Conversation shifts to deeper philosophical territory"
        )
    
    def _contains_reality_bend(self, entry: ScriptEntry) -> bool:
        """Check if entry contains reality-bending elements."""
        all_text = entry.dialogue + ' '.join(entry.stage_directions)
        return any(cue in all_text.lower() for cue in self.reality_bend_cues)
    
    def _create_reality_bend_bridge(self, prev: ScriptEntry, current: ScriptEntry) -> BridgePoint:
        """Create bridge for reality-bending moments."""
        visual_reqs = ['reality_distortion', 'physics_breakdown']
        
        # Add specific effects based on the type of bend
        for direction in current.stage_directions if current else []:
            if 'shimmer' in direction:
                visual_reqs.append('shimmer_effect')
            if 'ripple' in direction:
                visual_reqs.append('ripple_effect')
        
        return BridgePoint(
            after_entry_id=prev.id if prev else current.id,
            before_entry_id=current.id if prev else "next",
            bridge_type=BridgeType.REALITY_BEND,
            reason="Reality begins to bend or transform",
            visual_requirements=visual_reqs
        )
    
    def _detects_emotional_shift(self, prev: ScriptEntry, current: ScriptEntry) -> bool:
        """Detect significant emotional transitions."""
        prev_emotions = self._extract_emotions(prev)
        current_emotions = self._extract_emotions(current)
        
        # Significant shift if emotions change dramatically
        return len(prev_emotions) == 0 and len(current_emotions) > 0
    
    def _extract_emotions(self, entry: ScriptEntry) -> List[str]:
        """Extract emotional markers from entry."""
        emotions = []
        all_text = ' '.join(entry.stage_directions).lower()
        
        for marker in self.emotion_markers:
            if marker in all_text:
                emotions.append(marker)
        
        return emotions
    
    def _create_emotional_bridge(self, prev: ScriptEntry, current: ScriptEntry) -> BridgePoint:
        """Create bridge for emotional transitions."""
        return BridgePoint(
            after_entry_id=prev.id,
            before_entry_id=current.id,
            bridge_type=BridgeType.EMOTIONAL_TURN,
            reason="Emotional intensity shifts"
        )
    
    def _needs_closing(self, last_entry: ScriptEntry) -> bool:
        """Check if script needs a closing bridge."""
        # Look for transformation or choice moments
        choice_words = ['choose', 'decision', 'transform', 'change', 'become']
        return any(word in last_entry.dialogue.lower() for word in choice_words)
    
    def generate_bridge_report(self, entries: List[ScriptEntry]) -> str:
        """Generate a report of recommended bridges."""
        bridges = self.analyze_script(entries)
        
        report = ["# Narrator Bridge Analysis Report\n"]
        report.append(f"Total entries analyzed: {len(entries)}")
        report.append(f"Bridges recommended: {len(bridges)}\n")
        
        for bridge in bridges:
            report.append(f"## Bridge after entry {bridge.after_entry_id}")
            report.append(f"- Type: {bridge.bridge_type.value}")
            report.append(f"- Reason: {bridge.reason}")
            if bridge.visual_requirements:
                report.append(f"- Visual requirements: {', '.join(bridge.visual_requirements)}")
            report.append("")
        
        return '\n'.join(report)