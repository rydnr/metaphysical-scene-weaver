"""Scene transition engine for managing visual and narrative continuity."""

from typing import List, Dict, Any, Optional, Tuple
from enum import Enum
from dataclasses import dataclass
import re
from collections import defaultdict


class TransitionType(Enum):
    """Types of scene transitions."""
    # Emotional transitions
    CONFIDENCE_BREAK = "confidence_break"
    REVELATION = "revelation"
    FEAR_EMERGENCE = "fear_emergence"
    CURIOSITY_SHIFT = "curiosity_shift"
    
    # Spatial transitions
    CHARACTER_ENTRANCE = "character_entrance"
    CHARACTER_EXIT = "character_exit"
    CAMERA_MOVEMENT = "camera_movement"
    LOCATION_CHANGE = "location_change"
    
    # Reality transitions
    PERCEPTION_SHIFT = "perception_shift"
    PHYSICS_BREAK = "physics_break"
    CONSCIOUSNESS_EXPANSION = "consciousness_expansion"
    REALITY_SHIMMER = "reality_shimmer"
    
    # Narrative transitions
    TIME_JUMP = "time_jump"
    PERSPECTIVE_SHIFT = "perspective_shift"
    FLASHBACK = "flashback"
    PARALLEL_ACTION = "parallel_action"


class PanelLayout(Enum):
    """Multi-panel layout types."""
    SINGLE = "single"
    HORIZONTAL_2 = "horizontal_2"
    VERTICAL_2 = "vertical_2"
    TRIPTYCH = "triptych"
    GRID_4 = "grid_4"
    SEQUENTIAL_3 = "sequential_3"
    FOCUS_SHIFT_3 = "focus_shift_3"


@dataclass
class TransitionContext:
    """Context for scene transitions."""
    from_scene_id: str
    to_scene_id: str
    transition_type: TransitionType
    emotional_arc: Dict[str, float]  # emotion -> intensity
    spatial_changes: List[str]
    visual_elements_maintained: List[str]
    visual_elements_introduced: List[str]
    pacing: str  # "sudden", "gradual", "delayed"
    camera_movement: Optional[str] = None
    
    def to_prompt_modifiers(self) -> List[str]:
        """Convert transition context to prompt modifiers."""
        modifiers = []
        
        # Add emotional transition
        if self.emotional_arc:
            emotions = list(self.emotional_arc.keys())
            if len(emotions) >= 2:
                modifiers.append(f"emotional transition from {emotions[0]} to {emotions[1]}")
        
        # Add visual continuity
        if self.visual_elements_maintained:
            modifiers.append(f"maintaining {', '.join(self.visual_elements_maintained)}")
        
        # Add new elements
        if self.visual_elements_introduced:
            modifiers.append(f"introducing {', '.join(self.visual_elements_introduced)}")
        
        # Add camera movement
        if self.camera_movement:
            modifiers.append(f"camera {self.camera_movement}")
        
        return modifiers


@dataclass
class PanelComposition:
    """Composition details for multi-panel scenes."""
    panel_count: int
    layout: PanelLayout
    panel_beats: List[str]  # Narrative beats per panel
    focal_points: List[str]  # Visual focus per panel
    camera_angles: List[str]
    continuity_elements: List[str]  # Elements consistent across panels


class SceneTransitionEngine:
    """Analyzes and manages scene transitions."""
    
    def __init__(self):
        self.transition_patterns = {
            # Emotional patterns
            r"uncertain|questioning|doubt": TransitionType.CONFIDENCE_BREAK,
            r"emerges|reveals|appears": TransitionType.REVELATION,
            r"frightened|scared|hesitant": TransitionType.FEAR_EMERGENCE,
            
            # Spatial patterns
            r"enters|arrives|emerges from": TransitionType.CHARACTER_ENTRANCE,
            r"exits|leaves|disappears": TransitionType.CHARACTER_EXIT,
            r"leans|moves|steps": TransitionType.CAMERA_MOVEMENT,
            
            # Reality patterns
            r"rippled|shimmers|distorts": TransitionType.REALITY_SHIMMER,
            r"impossible|breaks|defies": TransitionType.PHYSICS_BREAK,
            r"consciousness|awakening|perceive": TransitionType.CONSCIOUSNESS_EXPANSION
        }
        
        self.emotion_lexicon = {
            "confident": ["certain", "assured", "decisive"],
            "uncertain": ["questioning", "doubtful", "hesitant"],
            "curious": ["intrigued", "interested", "wondering"],
            "fearful": ["scared", "frightened", "anxious"],
            "revelatory": ["enlightened", "understanding", "awakening"]
        }
    
    def analyze_transition(self, from_scene: Dict[str, Any], 
                         to_scene: Dict[str, Any]) -> TransitionContext:
        """Analyze transition between two scenes."""
        
        # Detect transition type
        transition_type = self._detect_transition_type(from_scene, to_scene)
        
        # Analyze emotional arc
        emotional_arc = self._analyze_emotional_arc(from_scene, to_scene)
        
        # Detect spatial changes
        spatial_changes = self._detect_spatial_changes(from_scene, to_scene)
        
        # Identify visual elements
        maintained, introduced = self._analyze_visual_elements(from_scene, to_scene)
        
        # Determine pacing
        pacing = self._determine_pacing(transition_type, from_scene, to_scene)
        
        # Detect camera movement
        camera_movement = self._detect_camera_movement(from_scene, to_scene)
        
        return TransitionContext(
            from_scene_id=from_scene.get("id", ""),
            to_scene_id=to_scene.get("id", ""),
            transition_type=transition_type,
            emotional_arc=emotional_arc,
            spatial_changes=spatial_changes,
            visual_elements_maintained=maintained,
            visual_elements_introduced=introduced,
            pacing=pacing,
            camera_movement=camera_movement
        )
    
    def _detect_transition_type(self, from_scene: Dict[str, Any], 
                               to_scene: Dict[str, Any]) -> TransitionType:
        """Detect the type of transition between scenes."""
        
        # Combine dialogue and stage directions
        from_text = f"{from_scene.get('dialogue', '')} {' '.join(from_scene.get('stage_directions', []))}"
        to_text = f"{to_scene.get('dialogue', '')} {' '.join(to_scene.get('stage_directions', []))}"
        combined_text = f"{from_text} {to_text}".lower()
        
        # Check patterns
        for pattern, transition_type in self.transition_patterns.items():
            if re.search(pattern, combined_text):
                return transition_type
        
        # Default to camera movement
        return TransitionType.CAMERA_MOVEMENT
    
    def _analyze_emotional_arc(self, from_scene: Dict[str, Any], 
                              to_scene: Dict[str, Any]) -> Dict[str, float]:
        """Analyze emotional transition between scenes."""
        emotions = {}
        
        # Simple emotion detection (would be enhanced with NLP)
        from_text = from_scene.get("dialogue", "").lower()
        to_text = to_scene.get("dialogue", "").lower()
        
        for emotion, keywords in self.emotion_lexicon.items():
            from_score = sum(1 for keyword in keywords if keyword in from_text)
            to_score = sum(1 for keyword in keywords if keyword in to_text)
            
            if from_score > 0 or to_score > 0:
                emotions[emotion] = (to_score - from_score) / max(1, from_score + to_score)
        
        return emotions
    
    def _detect_spatial_changes(self, from_scene: Dict[str, Any], 
                               to_scene: Dict[str, Any]) -> List[str]:
        """Detect spatial changes between scenes."""
        changes = []
        
        # Check stage directions
        from_directions = set(from_scene.get("stage_directions", []))
        to_directions = set(to_scene.get("stage_directions", []))
        
        # Look for movement indicators
        movement_keywords = ["moves", "steps", "enters", "exits", "approaches", "backs away"]
        for direction in to_directions:
            if any(keyword in direction.lower() for keyword in movement_keywords):
                changes.append(direction)
        
        return changes
    
    def _analyze_visual_elements(self, from_scene: Dict[str, Any], 
                                to_scene: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """Identify maintained and introduced visual elements."""
        
        # Extract visual elements (simplified - would use NLP)
        from_elements = self._extract_visual_elements(from_scene)
        to_elements = self._extract_visual_elements(to_scene)
        
        maintained = list(from_elements & to_elements)
        introduced = list(to_elements - from_elements)
        
        return maintained, introduced
    
    def _extract_visual_elements(self, scene: Dict[str, Any]) -> set:
        """Extract visual elements from a scene."""
        elements = set()
        
        # Extract from dialogue and stage directions
        text = f"{scene.get('dialogue', '')} {' '.join(scene.get('stage_directions', []))}".lower()
        
        # Simple noun extraction (would use NLP)
        visual_keywords = ["tree", "shadow", "light", "door", "window", "character", 
                          "ground", "sky", "wall", "object", "space"]
        
        for keyword in visual_keywords:
            if keyword in text:
                elements.add(keyword)
        
        # Add characters
        if scene.get("speaker"):
            elements.add(scene["speaker"].lower())
        
        return elements
    
    def _determine_pacing(self, transition_type: TransitionType,
                         from_scene: Dict[str, Any], 
                         to_scene: Dict[str, Any]) -> str:
        """Determine transition pacing."""
        
        # Sudden transitions
        sudden_types = [TransitionType.REVELATION, TransitionType.PHYSICS_BREAK,
                       TransitionType.CHARACTER_ENTRANCE]
        if transition_type in sudden_types:
            return "sudden"
        
        # Gradual transitions
        gradual_types = [TransitionType.CONSCIOUSNESS_EXPANSION, 
                        TransitionType.CONFIDENCE_BREAK]
        if transition_type in gradual_types:
            return "gradual"
        
        return "normal"
    
    def _detect_camera_movement(self, from_scene: Dict[str, Any], 
                               to_scene: Dict[str, Any]) -> Optional[str]:
        """Detect implied camera movement."""
        
        # Check stage directions for camera cues
        directions = to_scene.get("stage_directions", [])
        combined = " ".join(directions).lower()
        
        if "close" in combined or "intimate" in combined:
            return "push in"
        elif "wide" in combined or "establishing" in combined:
            return "pull back"
        elif "follows" in combined:
            return "tracking"
        elif "reveals" in combined:
            return "pan"
        
        return None


class PanelCompositionEngine:
    """Manages multi-panel scene composition."""
    
    def __init__(self):
        self.layout_rules = {
            2: {
                "dialogue_exchange": PanelLayout.HORIZONTAL_2,
                "action_reaction": PanelLayout.VERTICAL_2,
                "before_after": PanelLayout.HORIZONTAL_2
            },
            3: {
                "progression": PanelLayout.SEQUENTIAL_3,
                "revelation": PanelLayout.FOCUS_SHIFT_3,
                "action_sequence": PanelLayout.TRIPTYCH
            }
        }
    
    def compose_panels(self, scene: Dict[str, Any], 
                      panel_count: int) -> PanelComposition:
        """Create panel composition for a multi-panel scene."""
        
        # Determine layout
        layout = self._determine_layout(scene, panel_count)
        
        # Split narrative beats
        beats = self._split_narrative_beats(scene, panel_count)
        
        # Determine focal points
        focal_points = self._determine_focal_points(scene, panel_count)
        
        # Set camera angles
        camera_angles = self._set_camera_angles(scene, panel_count, layout)
        
        # Identify continuity elements
        continuity = self._identify_continuity_elements(scene)
        
        return PanelComposition(
            panel_count=panel_count,
            layout=layout,
            panel_beats=beats,
            focal_points=focal_points,
            camera_angles=camera_angles,
            continuity_elements=continuity
        )
    
    def _determine_layout(self, scene: Dict[str, Any], panel_count: int) -> PanelLayout:
        """Determine appropriate panel layout."""
        
        # Analyze scene type
        dialogue = scene.get("dialogue", "").lower()
        
        if panel_count == 2:
            if "?" in dialogue and "!" in dialogue:
                return PanelLayout.HORIZONTAL_2
            return PanelLayout.VERTICAL_2
        
        elif panel_count == 3:
            if any(word in dialogue for word in ["reveal", "discover", "realize"]):
                return PanelLayout.FOCUS_SHIFT_3
            return PanelLayout.SEQUENTIAL_3
        
        return PanelLayout.SINGLE
    
    def _split_narrative_beats(self, scene: Dict[str, Any], 
                              panel_count: int) -> List[str]:
        """Split scene into narrative beats for each panel."""
        
        dialogue = scene.get("dialogue", "")
        
        # Simple split by sentences
        sentences = re.split(r'[.!?]+', dialogue)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) >= panel_count:
            # Distribute sentences across panels
            beats_per_panel = len(sentences) // panel_count
            beats = []
            
            for i in range(panel_count):
                start = i * beats_per_panel
                end = start + beats_per_panel if i < panel_count - 1 else len(sentences)
                beat = ". ".join(sentences[start:end])
                beats.append(beat)
            
            return beats
        else:
            # Repeat or emphasize for additional panels
            return sentences + ["[Visual emphasis]"] * (panel_count - len(sentences))
    
    def _determine_focal_points(self, scene: Dict[str, Any], 
                               panel_count: int) -> List[str]:
        """Determine visual focal points for each panel."""
        
        speaker = scene.get("speaker", "character")
        
        # Basic focal progression
        if panel_count == 1:
            return [speaker]
        elif panel_count == 2:
            return [speaker, f"{speaker}'s reaction"]
        elif panel_count == 3:
            return [f"wide shot with {speaker}", speaker, f"{speaker}'s key gesture"]
        
        return [speaker] * panel_count
    
    def _set_camera_angles(self, scene: Dict[str, Any], panel_count: int,
                          layout: PanelLayout) -> List[str]:
        """Set camera angles for each panel."""
        
        if layout == PanelLayout.SEQUENTIAL_3:
            return ["wide establishing", "medium shot", "close-up"]
        elif layout == PanelLayout.FOCUS_SHIFT_3:
            return ["over-shoulder", "reverse angle", "dramatic close-up"]
        elif layout == PanelLayout.HORIZONTAL_2:
            return ["medium shot", "reaction shot"]
        
        return ["medium shot"] * panel_count
    
    def _identify_continuity_elements(self, scene: Dict[str, Any]) -> List[str]:
        """Identify elements that should remain consistent across panels."""
        
        elements = []
        
        # Always maintain character
        if scene.get("speaker"):
            elements.append(scene["speaker"])
        
        # Extract key objects from dialogue
        dialogue = scene.get("dialogue", "").lower()
        objects = ["tree", "door", "light", "shadow", "ground"]
        
        for obj in objects:
            if obj in dialogue:
                elements.append(obj)
        
        return elements