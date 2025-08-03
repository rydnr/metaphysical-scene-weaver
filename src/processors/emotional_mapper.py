"""Emotional state detection and visual mapping engine."""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import re
from enum import Enum
import logging
from ..utils.visual_rules import VisualRules, ColorPalette, LightingScheme, BodyLanguageSet, FacialExpression, AtmosphericEffect, SymbolicElement


class EmotionCategory(Enum):
    """Primary emotion categories based on psychological models."""
    # Basic emotions
    JOY = "joy"
    SADNESS = "sadness"
    ANGER = "anger"
    FEAR = "fear"
    SURPRISE = "surprise"
    DISGUST = "disgust"
    CONTEMPLATION = "contemplation"
    LOVE = "love"
    CONFUSION = "confusion"
    DETERMINATION = "determination"
    
    # Nuanced emotions
    MELANCHOLY = "melancholy"
    EXISTENTIAL_DREAD = "existential_dread"
    TRANSCENDENT_JOY = "transcendent_joy"
    BITTERSWEET = "bittersweet"
    ENNUI = "ennui"
    WONDER = "wonder"
    SERENITY = "serenity"
    NOSTALGIA = "nostalgia"
    YEARNING = "yearning"
    SUBLIME = "sublime"


@dataclass
class EmotionalState:
    """Represents an emotional state with visual mapping."""
    primary: EmotionCategory
    secondary: Optional[EmotionCategory]
    intensity: float  # 0.0 to 1.0
    valence: float  # -1.0 (negative) to 1.0 (positive)
    arousal: float  # 0.0 (calm) to 1.0 (excited)
    visual_palette: List[str]
    lighting_mood: str
    body_language: List[str]
    facial_expression: str


class EmotionalMapper:
    """Maps emotional states to visual representations."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.visual_rules = VisualRules()
        
        # Cultural context (can be set dynamically)
        self.cultural_context = 'western'
        
        # Emotion to visual mapping (now delegates to VisualRules)
        self.emotion_visuals = {
            EmotionCategory.JOY: {
                'colors': ['warm yellows', 'bright oranges', 'soft pinks'],
                'lighting': 'bright, warm lighting with soft shadows',
                'body_language': ['open posture', 'raised arms', 'relaxed shoulders'],
                'facial': 'genuine smile, eyes crinkled',
                'atmosphere': 'light particles, gentle breeze'
            },
            EmotionCategory.SADNESS: {
                'colors': ['muted blues', 'grays', 'deep purples'],
                'lighting': 'subdued, cool lighting with long shadows',
                'body_language': ['hunched shoulders', 'downward gaze', 'closed posture'],
                'facial': 'downturned mouth, distant eyes',
                'atmosphere': 'rain, fog, or mist'
            },
            EmotionCategory.ANGER: {
                'colors': ['deep reds', 'burnt oranges', 'dark browns'],
                'lighting': 'harsh, high contrast lighting',
                'body_language': ['tense muscles', 'clenched fists', 'forward lean'],
                'facial': 'furrowed brow, tight jaw',
                'atmosphere': 'heat waves, sharp shadows'
            },
            EmotionCategory.FEAR: {
                'colors': ['cold blues', 'sickly greens', 'stark whites'],
                'lighting': 'dramatic shadows, unstable light sources',
                'body_language': ['defensive posture', 'wide stance', 'raised hands'],
                'facial': 'wide eyes, parted lips',
                'atmosphere': 'distorted perspectives, lurking shadows'
            },
            EmotionCategory.CONTEMPLATION: {
                'colors': ['deep teals', 'soft violets', 'muted golds'],
                'lighting': 'diffused, ethereal lighting',
                'body_language': ['thoughtful pose', 'hand to chin', 'distant gaze'],
                'facial': 'neutral expression, focused eyes',
                'atmosphere': 'floating elements, gentle particles'
            },
            EmotionCategory.LOVE: {
                'colors': ['rose golds', 'soft reds', 'warm whites'],
                'lighting': 'soft, romantic lighting with warm glow',
                'body_language': ['leaning toward', 'open arms', 'gentle gestures'],
                'facial': 'soft smile, tender eyes',
                'atmosphere': 'soft focus edges, warm aura'
            },
            EmotionCategory.CONFUSION: {
                'colors': ['shifting hues', 'desaturated tones', 'conflicting colors'],
                'lighting': 'multiple light sources, conflicting shadows',
                'body_language': ['asymmetrical pose', 'tilted head', 'raised eyebrow'],
                'facial': 'questioning expression, slight frown',
                'atmosphere': 'swirling patterns, fragmented elements'
            },
            EmotionCategory.DETERMINATION: {
                'colors': ['steel blues', 'strong reds', 'bold blacks'],
                'lighting': 'directional, purposeful lighting',
                'body_language': ['firm stance', 'forward momentum', 'squared shoulders'],
                'facial': 'set jaw, focused gaze',
                'atmosphere': 'clear lines, sharp focus'
            }
        }
        
        # Emotion keywords for detection
        self.emotion_keywords = {
            EmotionCategory.JOY: [
                'happy', 'joy', 'laugh', 'smile', 'delight', 'cheerful', 
                'elated', 'gleeful', 'pleased', 'content', 'jubilant', 'ecstatic'
            ],
            EmotionCategory.SADNESS: [
                'sad', 'cry', 'tears', 'sorrow', 'grief', 'mourn',
                'depressed', 'blue', 'down', 'heavy', 'weep', 'despondent'
            ],
            EmotionCategory.ANGER: [
                'angry', 'furious', 'rage', 'mad', 'irritated', 'annoyed',
                'frustrated', 'livid', 'seething', 'wrathful', 'enraged', 'incensed'
            ],
            EmotionCategory.FEAR: [
                'afraid', 'scared', 'terrified', 'anxious', 'worried', 'nervous',
                'frightened', 'alarmed', 'panicked', 'horrified', 'petrified'
            ],
            EmotionCategory.CONTEMPLATION: [
                'think', 'ponder', 'consider', 'reflect', 'meditate', 'muse',
                'contemplate', 'philosophize', 'introspect', 'deliberate', 'ruminate'
            ],
            EmotionCategory.LOVE: [
                'love', 'adore', 'cherish', 'affection', 'tender', 'caring',
                'devoted', 'fond', 'passionate', 'intimate', 'enamored', 'infatuated'
            ],
            EmotionCategory.CONFUSION: [
                'confused', 'puzzled', 'perplexed', 'bewildered', 'lost',
                'uncertain', 'doubtful', 'questioning', 'unclear', 'baffled', 'mystified'
            ],
            EmotionCategory.DETERMINATION: [
                'determined', 'resolute', 'committed', 'dedicated', 'persistent',
                'unwavering', 'steadfast', 'focused', 'driven', 'tenacious', 'adamant'
            ],
            # Nuanced emotions
            EmotionCategory.MELANCHOLY: [
                'melancholy', 'wistful', 'pensive', 'nostalgic', 'bittersweet',
                'longing', 'yearning', 'reminisce', 'saudade', 'poignant'
            ],
            EmotionCategory.EXISTENTIAL_DREAD: [
                'dread', 'void', 'meaningless', 'absurd', 'existential', 'nihilistic',
                'empty', 'futile', 'purposeless', 'abyss', 'cosmic horror', 'insignificant'
            ],
            EmotionCategory.TRANSCENDENT_JOY: [
                'transcendent', 'bliss', 'euphoria', 'rapture', 'divine', 'sublime',
                'enlightened', 'awakened', 'nirvana', 'ecstasy', 'cosmic joy', 'unity'
            ],
            EmotionCategory.BITTERSWEET: [
                'bittersweet', 'mixed feelings', 'happy sad', 'nostalgic joy',
                'melancholic happiness', 'sweet sorrow', 'complex emotion'
            ],
            EmotionCategory.ENNUI: [
                'ennui', 'bored', 'listless', 'apathetic', 'indifferent', 'weary',
                'disenchanted', 'jaded', 'blasé', 'world-weary', 'tedium'
            ],
            EmotionCategory.WONDER: [
                'wonder', 'awe', 'marvel', 'astonish', 'amaze', 'fascinate',
                'captivate', 'mesmerize', 'enchant', 'bewitch', 'spellbound'
            ],
            EmotionCategory.SERENITY: [
                'serene', 'peaceful', 'calm', 'tranquil', 'placid', 'still',
                'composed', 'centered', 'balanced', 'harmonious', 'zen', 'equanimity'
            ],
            EmotionCategory.NOSTALGIA: [
                'nostalgic', 'reminisce', 'remember', 'past', 'memory', 'yesteryear',
                'bygone', 'olden days', 'homesick', 'longing for past'
            ],
            EmotionCategory.YEARNING: [
                'yearn', 'long for', 'pine', 'crave', 'desire deeply', 'ache for',
                'hunger for', 'thirst for', 'desperate for', 'burning desire'
            ],
            EmotionCategory.SUBLIME: [
                'sublime', 'magnificent', 'glorious', 'majestic', 'grandiose',
                'awe-inspiring', 'overwhelming beauty', 'transcendent beauty'
            ]
        }
        
        # Intensity modifiers
        self.intensity_modifiers = {
            'very': 1.2,
            'extremely': 1.5,
            'slightly': 0.5,
            'somewhat': 0.7,
            'deeply': 1.3,
            'barely': 0.3,
            'intensely': 1.4
        }
        
    def analyze_emotional_content(
        self,
        dialogue: str,
        stage_directions: List[str],
        character_state: Dict[str, Any]
    ) -> EmotionalState:
        """Analyze and map emotional content to visual representation."""
        # Detect emotions from text
        detected_emotions = self._detect_emotions(dialogue, stage_directions)
        
        # Calculate emotional metrics
        primary, secondary = self._identify_primary_emotions(detected_emotions)
        intensity = self._calculate_intensity(dialogue, detected_emotions)
        valence = self._calculate_valence(primary, secondary)
        arousal = self._calculate_arousal(primary, intensity)
        
        # Generate visual mapping
        visual_palette = self._generate_color_palette(primary, secondary, intensity)
        lighting_mood = self._determine_lighting(primary, intensity, character_state)
        body_language = self._suggest_body_language(primary, intensity, arousal)
        facial_expression = self._suggest_facial_expression(primary, intensity)
        
        return EmotionalState(
            primary=primary,
            secondary=secondary,
            intensity=intensity,
            valence=valence,
            arousal=arousal,
            visual_palette=visual_palette,
            lighting_mood=lighting_mood,
            body_language=body_language,
            facial_expression=facial_expression
        )
    
    def map_emotion_to_visuals(
        self,
        emotional_state: Dict[str, Any],
        intensity: float = 0.5,
        cultural_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """Map emotional state to visual elements using VisualRules."""
        # Use instance cultural context if not specified
        if cultural_context is None:
            cultural_context = self.cultural_context
            
        # Handle both string and enum emotional states
        if isinstance(emotional_state, str):
            try:
                emotion = EmotionCategory(emotional_state.lower())
            except ValueError:
                # Default to contemplation for unknown emotions
                emotion = EmotionCategory.CONTEMPLATION
        elif isinstance(emotional_state, dict):
            # Extract primary emotion from dict
            emotion_name = emotional_state.get('primary', 'contemplation')
            try:
                emotion = EmotionCategory(emotion_name.lower())
            except ValueError:
                emotion = EmotionCategory.CONTEMPLATION
        else:
            emotion = EmotionCategory.CONTEMPLATION
            
        # Use VisualRules for comprehensive mapping
        return self.visual_rules.get_emotion_visuals(
            emotion.value, 
            intensity, 
            cultural_context
        )
    
    def blend_emotions(
        self,
        primary_emotion: str,
        secondary_emotion: str,
        blend_ratio: float = 0.7,
        cultural_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """Blend two emotions to create complex emotional states."""
        if cultural_context is None:
            cultural_context = self.cultural_context
            
        # Ensure emotions are valid
        try:
            primary = EmotionCategory(primary_emotion.lower())
            secondary = EmotionCategory(secondary_emotion.lower())
        except ValueError:
            self.logger.warning(f"Invalid emotion for blending: {primary_emotion} or {secondary_emotion}")
            return self.map_emotion_to_visuals('contemplation')
            
        # Use VisualRules for blending
        blended = self.visual_rules.blend_emotions(
            primary.value,
            secondary.value,
            blend_ratio
        )
        
        # Add cultural context
        blended['cultural_context'] = cultural_context
        
        return blended
    
    def get_emotion_transition(
        self,
        from_emotion: str,
        to_emotion: str,
        progress: float = 0.5
    ) -> Dict[str, Any]:
        """Get visual elements for smooth emotional transitions."""
        try:
            from_em = EmotionCategory(from_emotion.lower())
            to_em = EmotionCategory(to_emotion.lower())
        except ValueError:
            self.logger.warning(f"Invalid emotion for transition: {from_emotion} or {to_emotion}")
            return self.map_emotion_to_visuals('contemplation')
            
        return self.visual_rules.get_transition_visuals(
            from_em.value,
            to_em.value,
            progress
        )
    
    def set_cultural_context(self, context: str) -> None:
        """Set the cultural context for emotion mapping."""
        valid_contexts = ['western', 'eastern', 'latin', 'middle_eastern', 'african']
        if context in valid_contexts:
            self.cultural_context = context
            self.logger.info(f"Cultural context set to: {context}")
        else:
            self.logger.warning(f"Invalid cultural context: {context}. Using default 'western'.")
            self.cultural_context = 'western'
    
    def _detect_emotions(
        self,
        dialogue: str,
        stage_directions: List[str]
    ) -> Dict[EmotionCategory, float]:
        """Detect emotions from text content."""
        detected = {}
        text = dialogue.lower() + ' ' + ' '.join(stage_directions).lower()
        
        for emotion, keywords in self.emotion_keywords.items():
            score = 0.0
            for keyword in keywords:
                occurrences = len(re.findall(r'\b' + keyword + r'\b', text))
                score += occurrences * 0.1
            
            if score > 0:
                detected[emotion] = min(1.0, score)
                
        return detected
    
    def _identify_primary_emotions(
        self,
        detected: Dict[EmotionCategory, float]
    ) -> Tuple[EmotionCategory, Optional[EmotionCategory]]:
        """Identify primary and secondary emotions."""
        if not detected:
            return EmotionCategory.CONTEMPLATION, None
            
        sorted_emotions = sorted(detected.items(), key=lambda x: x[1], reverse=True)
        primary = sorted_emotions[0][0]
        secondary = sorted_emotions[1][0] if len(sorted_emotions) > 1 else None
        
        return primary, secondary
    
    def _calculate_intensity(
        self,
        dialogue: str,
        detected: Dict[EmotionCategory, float]
    ) -> float:
        """Calculate emotional intensity."""
        base_intensity = max(detected.values()) if detected else 0.3
        
        # Check for intensity modifiers
        for modifier, multiplier in self.intensity_modifiers.items():
            if modifier in dialogue.lower():
                base_intensity *= multiplier
                
        # Check for exclamation marks
        exclamation_count = dialogue.count('!')
        base_intensity += exclamation_count * 0.1
        
        # Check for capitalization
        caps_ratio = sum(1 for c in dialogue if c.isupper()) / max(len(dialogue), 1)
        if caps_ratio > 0.5:
            base_intensity *= 1.2
            
        return min(1.0, base_intensity)
    
    def _calculate_valence(
        self,
        primary: EmotionCategory,
        secondary: Optional[EmotionCategory]
    ) -> float:
        """Calculate emotional valence (positive/negative)."""
        valence_map = {
            # Positive emotions
            EmotionCategory.JOY: 0.9,
            EmotionCategory.LOVE: 0.8,
            EmotionCategory.TRANSCENDENT_JOY: 1.0,
            EmotionCategory.WONDER: 0.7,
            EmotionCategory.SERENITY: 0.6,
            EmotionCategory.SUBLIME: 0.8,
            
            # Neutral emotions
            EmotionCategory.SURPRISE: 0.3,
            EmotionCategory.CONTEMPLATION: 0.0,
            EmotionCategory.DETERMINATION: 0.4,
            EmotionCategory.NOSTALGIA: 0.1,
            
            # Mixed emotions
            EmotionCategory.BITTERSWEET: 0.0,
            EmotionCategory.MELANCHOLY: -0.3,
            EmotionCategory.YEARNING: -0.1,
            
            # Negative emotions
            EmotionCategory.CONFUSION: -0.2,
            EmotionCategory.ENNUI: -0.4,
            EmotionCategory.FEAR: -0.7,
            EmotionCategory.SADNESS: -0.8,
            EmotionCategory.ANGER: -0.6,
            EmotionCategory.DISGUST: -0.7,
            EmotionCategory.EXISTENTIAL_DREAD: -0.9
        }
        
        primary_valence = valence_map.get(primary, 0.0)
        if secondary:
            secondary_valence = valence_map.get(secondary, 0.0)
            return (primary_valence * 0.7 + secondary_valence * 0.3)
        
        return primary_valence
    
    def _calculate_arousal(
        self,
        primary: EmotionCategory,
        intensity: float
    ) -> float:
        """Calculate emotional arousal level."""
        arousal_map = {
            # High arousal emotions
            EmotionCategory.JOY: 0.7,
            EmotionCategory.ANGER: 0.9,
            EmotionCategory.FEAR: 0.8,
            EmotionCategory.SURPRISE: 0.8,
            EmotionCategory.TRANSCENDENT_JOY: 0.9,
            EmotionCategory.SUBLIME: 0.8,
            
            # Medium arousal emotions
            EmotionCategory.DETERMINATION: 0.6,
            EmotionCategory.CONFUSION: 0.5,
            EmotionCategory.DISGUST: 0.6,
            EmotionCategory.WONDER: 0.6,
            EmotionCategory.YEARNING: 0.5,
            
            # Low arousal emotions
            EmotionCategory.LOVE: 0.4,
            EmotionCategory.CONTEMPLATION: 0.3,
            EmotionCategory.MELANCHOLY: 0.3,
            EmotionCategory.NOSTALGIA: 0.3,
            EmotionCategory.BITTERSWEET: 0.4,
            
            # Very low arousal emotions
            EmotionCategory.SADNESS: 0.2,
            EmotionCategory.SERENITY: 0.1,
            EmotionCategory.ENNUI: 0.1,
            EmotionCategory.EXISTENTIAL_DREAD: 0.2
        }
        
        base_arousal = arousal_map.get(primary, 0.5)
        return min(1.0, base_arousal * intensity)
    
    def _generate_color_palette(
        self,
        primary: EmotionCategory,
        secondary: Optional[EmotionCategory],
        intensity: float
    ) -> List[str]:
        """Generate color palette based on emotions."""
        primary_colors = self.emotion_visuals[primary]['colors']
        
        if secondary:
            secondary_colors = self.emotion_visuals[secondary]['colors']
            # Blend palettes
            palette = primary_colors[:2] + secondary_colors[:1]
        else:
            palette = primary_colors
            
        # Adjust for intensity
        if intensity > 0.7:
            palette = [f"vibrant {color}" for color in palette]
        elif intensity < 0.3:
            palette = [f"pale {color}" for color in palette]
            
        return palette
    
    def _determine_lighting(
        self,
        primary: EmotionCategory,
        intensity: float,
        character_state: Dict[str, Any]
    ) -> str:
        """Determine lighting based on emotion and context."""
        base_lighting = self.emotion_visuals[primary]['lighting']
        
        # Adjust for time of day if available
        time_context = character_state.get('time_context', 'day')
        if time_context == 'night':
            base_lighting = f"moonlit {base_lighting}"
        elif time_context == 'dawn':
            base_lighting = f"golden hour {base_lighting}"
            
        return base_lighting
    
    def _suggest_body_language(
        self,
        primary: EmotionCategory,
        intensity: float,
        arousal: float
    ) -> List[str]:
        """Suggest body language based on emotional state."""
        base_language = self.emotion_visuals[primary]['body_language']
        
        if arousal > 0.7:
            base_language.append('dynamic movement')
        elif arousal < 0.3:
            base_language.append('stillness')
            
        if intensity > 0.8:
            base_language = [f"exaggerated {gesture}" for gesture in base_language]
            
        return base_language
    
    def _suggest_facial_expression(
        self,
        primary: EmotionCategory,
        intensity: float
    ) -> str:
        """Suggest facial expression based on emotion."""
        base_expression = self.emotion_visuals[primary]['facial']
        
        if intensity > 0.8:
            return f"intense {base_expression}"
        elif intensity < 0.3:
            return f"subtle {base_expression}"
        
        return base_expression