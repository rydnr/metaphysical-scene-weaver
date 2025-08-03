"""Emotion transition algorithms for smooth scene flow."""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import math


@dataclass
class EmotionState:
    """Represents an emotional state at a specific moment."""
    primary: str
    secondary: Optional[str]
    intensity: float
    valence: float  # -1 (negative) to 1 (positive)
    arousal: float  # 0 (calm) to 1 (excited)


@dataclass
class TransitionCurve:
    """Defines how emotions transition between scenes."""
    start_state: EmotionState
    end_state: EmotionState
    duration: int  # number of panels
    curve_type: str  # 'linear', 'ease_in', 'ease_out', 'ease_in_out'
    
    
class EmotionTransitionEngine:
    """Manages smooth emotional transitions between scenes."""
    
    def __init__(self):
        self.max_intensity_shift = 0.3  # Per scene
        self.max_valence_shift = 0.4
        self.max_arousal_shift = 0.3
        
        # Character-specific emotional volatility
        self.character_volatility = {
            'evan': 0.8,    # High volatility
            'monday': 0.3,   # Low volatility
            'valerie': 0.5   # Medium volatility
        }
        
    def calculate_transition(
        self,
        from_state: EmotionState,
        to_state: EmotionState,
        character: str,
        philosophical_bridge: Optional[str] = None
    ) -> TransitionCurve:
        """Calculate optimal transition between emotional states."""
        
        # Get character volatility
        volatility = self.character_volatility.get(character, 0.5)
        
        # Calculate deltas
        intensity_delta = abs(to_state.intensity - from_state.intensity)
        valence_delta = abs(to_state.valence - from_state.valence)
        arousal_delta = abs(to_state.arousal - from_state.arousal)
        
        # Determine transition duration based on emotional distance
        emotional_distance = math.sqrt(
            intensity_delta**2 + valence_delta**2 + arousal_delta**2
        )
        
        # More panels for larger emotional shifts
        base_duration = max(2, int(emotional_distance * 5))
        duration = int(base_duration / volatility)
        
        # Select curve type based on transition
        if philosophical_bridge:
            curve_type = 'ease_in_out'  # Smooth for philosophical transitions
        elif emotional_distance > 0.5:
            curve_type = 'ease_in'  # Gradual start for big shifts
        else:
            curve_type = 'linear'  # Simple for small shifts
            
        return TransitionCurve(
            start_state=from_state,
            end_state=to_state,
            duration=duration,
            curve_type=curve_type
        )
        
    def generate_intermediate_states(
        self,
        transition: TransitionCurve
    ) -> List[EmotionState]:
        """Generate intermediate emotional states for smooth transition."""
        
        states = []
        
        for i in range(transition.duration + 1):
            t = i / transition.duration if transition.duration > 0 else 1
            
            # Apply easing curve
            if transition.curve_type == 'ease_in':
                t = t * t
            elif transition.curve_type == 'ease_out':
                t = 1 - (1 - t) * (1 - t)
            elif transition.curve_type == 'ease_in_out':
                t = 3 * t * t - 2 * t * t * t
                
            # Interpolate values
            intensity = self._lerp(
                transition.start_state.intensity,
                transition.end_state.intensity,
                t
            )
            valence = self._lerp(
                transition.start_state.valence,
                transition.end_state.valence,
                t
            )
            arousal = self._lerp(
                transition.start_state.arousal,
                transition.end_state.arousal,
                t
            )
            
            # Handle emotion blending at midpoint
            if t < 0.5:
                primary = transition.start_state.primary
                secondary = transition.end_state.primary if t > 0.3 else None
            else:
                primary = transition.end_state.primary
                secondary = transition.start_state.primary if t < 0.7 else None
                
            states.append(EmotionState(
                primary=primary,
                secondary=secondary,
                intensity=intensity,
                valence=valence,
                arousal=arousal
            ))
            
        return states
        
    def validate_transition(
        self,
        from_state: EmotionState,
        to_state: EmotionState
    ) -> Tuple[bool, List[str]]:
        """Validate if transition is within acceptable bounds."""
        
        issues = []
        
        intensity_shift = abs(to_state.intensity - from_state.intensity)
        if intensity_shift > self.max_intensity_shift:
            issues.append(f"Intensity shift {intensity_shift:.2f} exceeds max {self.max_intensity_shift}")
            
        valence_shift = abs(to_state.valence - from_state.valence)
        if valence_shift > self.max_valence_shift:
            issues.append(f"Valence shift {valence_shift:.2f} exceeds max {self.max_valence_shift}")
            
        arousal_shift = abs(to_state.arousal - from_state.arousal)
        if arousal_shift > self.max_arousal_shift:
            issues.append(f"Arousal shift {arousal_shift:.2f} exceeds max {self.max_arousal_shift}")
            
        return len(issues) == 0, issues
        
    def _lerp(self, start: float, end: float, t: float) -> float:
        """Linear interpolation between two values."""
        return start + (end - start) * t


# Scene 001-003 Emotion Definitions
OPENING_SCENES = {
    '001': EmotionState(
        primary='curiosity',
        secondary=None,
        intensity=0.6,
        valence=0.4,
        arousal=0.5
    ),
    '002': EmotionState(
        primary='contemplation',
        secondary='melancholy',
        intensity=0.5,
        valence=0.1,
        arousal=0.3
    ),
    '003': EmotionState(
        primary='determination',
        secondary='curiosity',
        intensity=0.7,
        valence=0.5,
        arousal=0.6
    )
}


def create_opening_sequence_transitions():
    """Create emotion transitions for opening sequence."""
    
    engine = EmotionTransitionEngine()
    transitions = []
    
    # Scene 001 to 002 (Evan's shift from curiosity to being challenged)
    transition_1_2 = engine.calculate_transition(
        from_state=OPENING_SCENES['001'],
        to_state=OPENING_SCENES['002'],
        character='evan',
        philosophical_bridge='questioning_assumptions'
    )
    
    # Scene 002 to 003 (Monday's challenge sparking determination)
    transition_2_3 = engine.calculate_transition(
        from_state=OPENING_SCENES['002'],
        to_state=OPENING_SCENES['003'],
        character='evan',
        philosophical_bridge='authentic_connection'
    )
    
    return {
        '001_to_002': {
            'transition': transition_1_2,
            'intermediate_states': engine.generate_intermediate_states(transition_1_2),
            'visual_notes': 'Warm colors cooling, shadows deepening',
            'narrator_shift': 'Inviting to questioning tone'
        },
        '002_to_003': {
            'transition': transition_2_3,
            'intermediate_states': engine.generate_intermediate_states(transition_2_3),
            'visual_notes': 'Cool blues warming with gold threads of conviction',
            'narrator_shift': 'Questioning to affirming philosophical stance'
        }
    }


def get_visual_transition_cues(from_emotion: str, to_emotion: str) -> Dict[str, Any]:
    """Get specific visual cues for emotion transitions."""
    
    transition_visuals = {
        ('curiosity', 'contemplation'): {
            'color_shift': 'Golden warmth fading to cool blues',
            'particle_behavior': 'Question marks settling into thought circles',
            'lighting_change': 'Directional to diffused',
            'spatial_shift': 'Expanding to introspective'
        },
        ('contemplation', 'determination'): {
            'color_shift': 'Cool blues igniting with purpose reds',
            'particle_behavior': 'Circular thoughts becoming directional arrows',
            'lighting_change': 'Diffused sharpening to focused',
            'spatial_shift': 'Introspective to forward-moving'
        }
    }
    
    return transition_visuals.get((from_emotion, to_emotion), {
        'color_shift': 'Gradual blend',
        'particle_behavior': 'Smooth transformation',
        'lighting_change': 'Natural progression',
        'spatial_shift': 'Continuous flow'
    })


if __name__ == "__main__":
    # Test opening sequence transitions
    transitions = create_opening_sequence_transitions()
    
    for scene_pair, data in transitions.items():
        print(f"\nTransition: {scene_pair}")
        print(f"Duration: {data['transition'].duration} panels")
        print(f"Curve: {data['transition'].curve_type}")
        print(f"Visual notes: {data['visual_notes']}")
        print(f"States: {len(data['intermediate_states'])}")