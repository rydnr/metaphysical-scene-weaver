"""Scene synthesis engine that combines all analyzed elements into cohesive scenes."""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import logging
from enum import Enum


class SceneComplexity(Enum):
    """Scene complexity levels for visual composition."""
    SIMPLE = "simple"  # Single character, minimal elements
    MODERATE = "moderate"  # Multiple elements, standard composition
    COMPLEX = "complex"  # Multiple layers, metaphors, effects
    EPIC = "epic"  # Grand scale, multiple concepts, transformations


class CompositionStyle(Enum):
    """Visual composition styles."""
    CENTERED = "centered"  # Character focus, balanced
    DYNAMIC = "dynamic"  # Action-oriented, diagonal
    SPLIT = "split"  # Divided frame, contrasts
    LAYERED = "layered"  # Depth layers, foreground/background
    CIRCULAR = "circular"  # Circular/spiral composition
    FRAGMENTED = "fragmented"  # Broken/scattered elements


@dataclass
class SynthesizedScene:
    """Represents a fully synthesized scene ready for prompt generation."""
    composition_style: CompositionStyle
    scene_complexity: SceneComplexity
    focal_points: List[str]
    visual_hierarchy: List[Dict[str, Any]]
    special_effects: List[str]
    transitions: Dict[str, Any]
    panel_suggestions: List[Dict[str, Any]]


class SceneSynthesizer:
    """Synthesizes all analyzed components into cohesive scene descriptions."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Composition rules based on content
        self.composition_rules = {
            'philosophical': {
                'preferred_styles': [CompositionStyle.LAYERED, CompositionStyle.CIRCULAR],
                'effects': ['depth of field', 'multiple focal planes', 'ethereal lighting'],
                'transitions': ['dissolve', 'morph', 'fade through']
            },
            'emotional': {
                'preferred_styles': [CompositionStyle.CENTERED, CompositionStyle.DYNAMIC],
                'effects': ['color grading', 'atmospheric particles', 'lighting mood'],
                'transitions': ['match cut', 'emotional bridge', 'color transition']
            },
            'action': {
                'preferred_styles': [CompositionStyle.DYNAMIC, CompositionStyle.FRAGMENTED],
                'effects': ['motion blur', 'speed lines', 'impact frames'],
                'transitions': ['action cut', 'movement match', 'kinetic transition']
            },
            'contemplative': {
                'preferred_styles': [CompositionStyle.CENTERED, CompositionStyle.SPLIT],
                'effects': ['soft focus', 'time dilation', 'thought bubbles'],
                'transitions': ['slow fade', 'time lapse', 'memory blend']
            },
            'metaphorical': {
                'preferred_styles': [CompositionStyle.LAYERED, CompositionStyle.SPLIT],
                'effects': ['double exposure', 'reality blend', 'symbolic overlay'],
                'transitions': ['metaphor morph', 'concept blend', 'reality shift']
            }
        }
        
        # Panel layout suggestions
        self.panel_layouts = {
            1: [{'type': 'full', 'focus': 'establishing'}],
            2: [
                {'type': 'split-vertical', 'focus': 'contrast'},
                {'type': 'split-horizontal', 'focus': 'progression'}
            ],
            3: [
                {'type': 'triangle', 'focus': 'dynamic'},
                {'type': 'triptych', 'focus': 'progression'},
                {'type': '1+2', 'focus': 'emphasis'}
            ],
            4: [
                {'type': 'grid', 'focus': 'systematic'},
                {'type': '1+3', 'focus': 'main+details'},
                {'type': 'diagonal', 'focus': 'movement'}
            ]
        }
        
        # Visual weight factors
        self.weight_factors = {
            'character': 1.0,
            'emotion': 0.8,
            'philosophy': 0.9,
            'metaphor': 0.7,
            'environment': 0.6,
            'special_effect': 0.5
        }
        
    def synthesize_scene(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize all analysis components into a unified scene description."""
        # Extract components
        entry = analysis_data['entry']
        context = analysis_data['context']
        philosophy = analysis_data['philosophy']
        emotion = analysis_data['emotion']
        metaphors = analysis_data['metaphors']
        character_state = analysis_data['character_state']
        continuity = analysis_data.get('continuity', {})
        
        # Determine scene type and complexity
        scene_type = self._determine_scene_type(philosophy, emotion, metaphors)
        complexity = self._assess_complexity(analysis_data)
        
        # Choose composition style
        composition_style = self._select_composition_style(scene_type, complexity)
        
        # Build visual hierarchy
        visual_hierarchy = self._build_visual_hierarchy(analysis_data)
        
        # Determine focal points
        focal_points = self._identify_focal_points(visual_hierarchy, character_state)
        
        # Select special effects
        special_effects = self._select_special_effects(scene_type, philosophy, emotion)
        
        # Plan transitions
        transitions = self._plan_transitions(continuity, scene_type)
        
        # Generate panel suggestions
        panel_suggestions = self._generate_panel_suggestions(
            entry.panel_count or 1,
            complexity,
            focal_points
        )
        
        # Synthesize setting details
        setting = self._synthesize_setting(context, philosophy, emotion)
        
        # Create final scene data
        return {
            'composition_style': composition_style.value,
            'scene_complexity': complexity.value,
            'scene_type': scene_type,
            'focal_points': focal_points,
            'visual_hierarchy': visual_hierarchy,
            'special_effects': special_effects,
            'transitions': transitions,
            'panel_suggestions': panel_suggestions,
            'setting': setting,
            'character_positioning': self._determine_character_positioning(
                composition_style,
                emotion,
                character_state
            ),
            'visual_motifs': self._extract_visual_motifs(philosophy, metaphors),
            'continuity_elements': self._process_continuity(continuity),
            'special_elements': self._identify_special_elements(analysis_data)
        }
    
    def _determine_scene_type(
        self,
        philosophy: Dict[str, Any],
        emotion: Dict[str, Any],
        metaphors: Dict[str, Any]
    ) -> str:
        """Determine the primary type of scene."""
        scores = {
            'philosophical': philosophy.get('depth_level', 0) * 0.4,
            'emotional': emotion.get('intensity', 0.5) * 0.3,
            'metaphorical': metaphors.get('metaphor_count', 0) * 0.2,
            'contemplative': 0.2  # Base score
        }
        
        # Boost based on specific indicators
        if philosophy.get('primary_concept') in ['consciousness', 'existence', 'time']:
            scores['philosophical'] += 0.3
            
        if emotion.get('primary') in ['anger', 'fear', 'joy']:
            scores['emotional'] += 0.2
            
        if metaphors.get('transformation'):
            scores['metaphorical'] += 0.3
            
        return max(scores.items(), key=lambda x: x[1])[0]
    
    def _assess_complexity(self, analysis_data: Dict[str, Any]) -> SceneComplexity:
        """Assess overall scene complexity."""
        complexity_score = 0
        
        # Philosophy depth
        philosophy_depth = analysis_data['philosophy'].get('depth_level', 0)
        complexity_score += philosophy_depth * 0.3
        
        # Emotional intensity
        emotional_intensity = analysis_data['emotion'].get('intensity', 0.5)
        complexity_score += emotional_intensity * 0.2
        
        # Metaphor count
        metaphor_count = analysis_data['metaphors'].get('metaphor_count', 0)
        complexity_score += min(metaphor_count * 0.2, 0.6)
        
        # Visual elements count
        visual_elements = len(analysis_data['philosophy'].get('visual_symbols', []))
        complexity_score += min(visual_elements * 0.1, 0.3)
        
        # Stage directions
        stage_directions = len(analysis_data['entry'].stage_directions)
        complexity_score += min(stage_directions * 0.1, 0.2)
        
        # Determine complexity level
        if complexity_score < 0.3:
            return SceneComplexity.SIMPLE
        elif complexity_score < 0.6:
            return SceneComplexity.MODERATE
        elif complexity_score < 0.9:
            return SceneComplexity.COMPLEX
        else:
            return SceneComplexity.EPIC
    
    def _select_composition_style(
        self,
        scene_type: str,
        complexity: SceneComplexity
    ) -> CompositionStyle:
        """Select appropriate composition style."""
        if scene_type in self.composition_rules:
            preferred_styles = self.composition_rules[scene_type]['preferred_styles']
            
            # Adjust for complexity
            if complexity == SceneComplexity.SIMPLE:
                return CompositionStyle.CENTERED
            elif complexity == SceneComplexity.EPIC:
                return CompositionStyle.LAYERED
            else:
                return preferred_styles[0]
        
        return CompositionStyle.CENTERED
    
    def _build_visual_hierarchy(
        self,
        analysis_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Build visual hierarchy of scene elements."""
        elements = []
        
        # Character as primary element
        character = analysis_data['context'].get('character')
        if character:
            elements.append({
                'element': 'character',
                'name': character.get('name'),
                'weight': self.weight_factors['character'],
                'position': 'primary',
                'details': character
            })
        
        # Philosophical visual symbols
        philosophy = analysis_data['philosophy']
        if philosophy.get('visual_symbols'):
            elements.append({
                'element': 'philosophical_symbols',
                'symbols': philosophy['visual_symbols'],
                'weight': self.weight_factors['philosophy'],
                'position': 'secondary',
                'integration': philosophy.get('atmospheric_suggestion')
            })
        
        # Emotional visual elements
        emotion = analysis_data['emotion']
        if emotion.get('atmosphere'):
            elements.append({
                'element': 'emotional_atmosphere',
                'atmosphere': emotion['atmosphere'],
                'weight': self.weight_factors['emotion'],
                'position': 'environmental',
                'colors': emotion.get('colors', [])
            })
        
        # Metaphorical elements
        metaphors = analysis_data['metaphors']
        if metaphors.get('visual_elements'):
            elements.append({
                'element': 'metaphor_visuals',
                'visuals': metaphors['visual_elements'],
                'weight': self.weight_factors['metaphor'],
                'position': 'integrated',
                'approach': metaphors.get('compositional_approach')
            })
        
        # Sort by weight
        elements.sort(key=lambda x: x['weight'], reverse=True)
        
        return elements
    
    def _identify_focal_points(
        self,
        visual_hierarchy: List[Dict[str, Any]],
        character_state: Dict[str, Any]
    ) -> List[str]:
        """Identify key focal points for the scene."""
        focal_points = []
        
        # Primary focal point from hierarchy
        if visual_hierarchy:
            primary = visual_hierarchy[0]
            if primary['element'] == 'character':
                focal_points.append(f"{primary['name']}'s {character_state.get('emotional', 'expression')}")
            else:
                focal_points.append(primary['element'])
        
        # Secondary focal points
        for element in visual_hierarchy[1:3]:
            if element['weight'] > 0.7:
                if element['element'] == 'philosophical_symbols':
                    focal_points.append(element['symbols'][0] if element['symbols'] else 'symbolic element')
                elif element['element'] == 'metaphor_visuals':
                    focal_points.append(element['visuals'][0] if element['visuals'] else 'metaphorical element')
        
        return focal_points[:3]  # Limit to 3 focal points
    
    def _select_special_effects(
        self,
        scene_type: str,
        philosophy: Dict[str, Any],
        emotion: Dict[str, Any]
    ) -> List[str]:
        """Select special effects based on scene content."""
        effects = []
        
        # Base effects from scene type
        if scene_type in self.composition_rules:
            effects.extend(self.composition_rules[scene_type]['effects'][:2])
        
        # Philosophy-based effects
        if philosophy.get('depth_level', 0) >= 2:
            effects.append('reality distortion')
        if 'time' in str(philosophy.get('primary_concept', '')):
            effects.append('temporal effects')
        if 'consciousness' in str(philosophy.get('primary_concept', '')):
            effects.append('perception shifts')
        
        # Emotion-based effects
        if emotion.get('intensity', 0) > 0.7:
            effects.append('intensified colors')
        if emotion.get('primary') == 'confusion':
            effects.append('visual fragmentation')
        
        return list(set(effects))[:4]  # Unique effects, max 4
    
    def _plan_transitions(
        self,
        continuity: Dict[str, Any],
        scene_type: str
    ) -> Dict[str, Any]:
        """Plan transitions based on continuity and scene type."""
        transitions = {
            'from_previous': 'cut',
            'to_next': 'cut',
            'internal': []
        }
        
        # Get scene-specific transitions
        if scene_type in self.composition_rules:
            available_transitions = self.composition_rules[scene_type]['transitions']
            
            # Use continuity to select appropriate transition
            if continuity.get('previous_emotion'):
                transitions['from_previous'] = available_transitions[0]
            
            # Internal panel transitions
            transitions['internal'] = available_transitions[1:3]
        
        return transitions
    
    def _generate_panel_suggestions(
        self,
        panel_count: int,
        complexity: SceneComplexity,
        focal_points: List[str]
    ) -> List[Dict[str, Any]]:
        """Generate panel layout suggestions."""
        if panel_count not in self.panel_layouts:
            panel_count = min(4, panel_count)  # Cap at 4
        
        layout_options = self.panel_layouts[panel_count]
        
        # Select layout based on complexity
        if complexity == SceneComplexity.SIMPLE:
            layout = layout_options[0]
        elif complexity == SceneComplexity.EPIC and len(layout_options) > 1:
            layout = layout_options[-1]  # Most complex option
        else:
            layout = layout_options[0]
        
        # Create panel suggestions
        suggestions = []
        for i in range(panel_count):
            panel = {
                'panel_number': i + 1,
                'layout_type': layout['type'],
                'focus': focal_points[i] if i < len(focal_points) else 'environmental',
                'size': self._determine_panel_size(i, panel_count, complexity)
            }
            suggestions.append(panel)
        
        return suggestions
    
    def _determine_panel_size(
        self,
        panel_index: int,
        total_panels: int,
        complexity: SceneComplexity
    ) -> str:
        """Determine individual panel size."""
        if total_panels == 1:
            return 'full-page' if complexity == SceneComplexity.EPIC else 'large'
        elif panel_index == 0 and complexity in [SceneComplexity.COMPLEX, SceneComplexity.EPIC]:
            return 'large'
        else:
            return 'standard'
    
    def _synthesize_setting(
        self,
        context: Dict[str, Any],
        philosophy: Dict[str, Any],
        emotion: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Synthesize setting details from all components."""
        setting = context.get('setting', {})
        
        # Enhance with philosophical atmosphere
        if philosophy.get('atmospheric_suggestion'):
            setting['philosophical_atmosphere'] = philosophy['atmospheric_suggestion']
        
        # Add emotional lighting
        if emotion.get('lighting'):
            setting['emotional_lighting'] = emotion['lighting']
        
        # Time and weather
        setting['time_context'] = context.get('time_context', 'undefined')
        setting['weather'] = self._determine_weather(emotion, philosophy)
        
        return setting
    
    def _determine_weather(
        self,
        emotion: Dict[str, Any],
        philosophy: Dict[str, Any]
    ) -> str:
        """Determine weather based on emotional and philosophical content."""
        primary_emotion = emotion.get('primary', '')
        
        weather_map = {
            'sadness': 'rain or overcast',
            'joy': 'sunny with gentle breeze',
            'anger': 'storm brewing',
            'fear': 'fog or shadows',
            'contemplation': 'twilight clarity',
            'confusion': 'shifting weather'
        }
        
        base_weather = weather_map.get(primary_emotion, 'neutral conditions')
        
        # Modify for philosophical depth
        if philosophy.get('depth_level', 0) >= 2:
            base_weather = f"surreal {base_weather}"
        
        return base_weather
    
    def _determine_character_positioning(
        self,
        composition_style: CompositionStyle,
        emotion: Dict[str, Any],
        character_state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Determine character positioning in scene."""
        positioning = {
            'placement': 'center',
            'scale': 'medium',
            'angle': 'three-quarter',
            'posture': emotion.get('body_language', ['neutral stance'])[0]
        }
        
        # Adjust for composition style
        if composition_style == CompositionStyle.DYNAMIC:
            positioning['placement'] = 'off-center'
            positioning['angle'] = 'dynamic angle'
        elif composition_style == CompositionStyle.SPLIT:
            positioning['placement'] = 'one side'
        elif composition_style == CompositionStyle.LAYERED:
            positioning['scale'] = 'varied depths'
        
        return positioning
    
    def _extract_visual_motifs(
        self,
        philosophy: Dict[str, Any],
        metaphors: Dict[str, Any]
    ) -> List[str]:
        """Extract recurring visual motifs."""
        motifs = []
        
        # From philosophy
        if philosophy.get('visual_symbols'):
            motifs.extend(philosophy['visual_symbols'][:2])
        
        # From metaphors
        if metaphors.get('symbolic_objects'):
            motifs.extend(metaphors['symbolic_objects'][:2])
        
        return list(set(motifs))[:3]
    
    def _process_continuity(self, continuity: Dict[str, Any]) -> Dict[str, Any]:
        """Process continuity elements from previous scenes."""
        if not continuity:
            return {}
        
        return {
            'maintain_elements': continuity.get('visual_motifs', []),
            'evolve_from': continuity.get('previous_emotion'),
            'setting_transition': continuity.get('previous_setting')
        }
    
    def _identify_special_elements(
        self,
        analysis_data: Dict[str, Any]
    ) -> List[str]:
        """Identify special visual elements that stand out."""
        special = []
        
        # High philosophical depth
        if analysis_data['philosophy'].get('depth_level', 0) >= 3:
            special.append('transcendent imagery')
        
        # Intense emotions
        if analysis_data['emotion'].get('intensity', 0) > 0.8:
            special.append('heightened emotional visualization')
        
        # Complex metaphors
        if analysis_data['metaphors'].get('transformation'):
            special.append('transformation sequence')
        
        # Multiple concepts interacting
        if analysis_data['philosophy'].get('concept_interactions'):
            special.append('conceptual fusion visuals')
        
        return special