"""Metaphor detection and visual translation engine."""

from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass
import re
import logging
from enum import Enum
import spacy
from collections import defaultdict


class MetaphorType(Enum):
    """Types of metaphors based on their conceptual structure."""
    CONCEPTUAL = "conceptual"  # Abstract ideas (life is a journey)
    ORIENTATIONAL = "orientational"  # Spatial relationships (up/down)
    ONTOLOGICAL = "ontological"  # Entity/substance metaphors
    STRUCTURAL = "structural"  # One concept structured by another
    VISUAL = "visual"  # Already visual in nature


@dataclass
class VisualMetaphor:
    """Represents a metaphor translated to visual elements."""
    source_text: str
    metaphor_type: MetaphorType
    concept_pair: Tuple[str, str]  # (source, target)
    visual_elements: List[str]
    transformation_sequence: List[str]
    symbolic_objects: List[str]
    compositional_notes: str


class MetaphorTranslator:
    """Translates metaphorical language into visual representations."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Load spaCy model for deeper NLP analysis
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            self.logger.warning("spaCy model not loaded, using pattern matching only")
            self.nlp = None
        
        # Common conceptual metaphor mappings
        self.conceptual_mappings = {
            'journey': {
                'concepts': ['life', 'progress', 'development', 'relationship'],
                'visuals': ['path', 'road', 'footsteps', 'horizon', 'milestones'],
                'transformations': ['walking figure', 'winding path', 'crossroads'],
                'symbols': ['compass', 'map', 'signpost', 'backpack']
            },
            'container': {
                'concepts': ['mind', 'emotion', 'state', 'situation'],
                'visuals': ['box', 'vessel', 'room', 'sphere', 'boundary'],
                'transformations': ['filling/emptying', 'opening/closing', 'expanding/contracting'],
                'symbols': ['door', 'key', 'lid', 'walls']
            },
            'machine': {
                'concepts': ['mind', 'body', 'system', 'process'],
                'visuals': ['gears', 'circuits', 'pistons', 'wires', 'controls'],
                'transformations': ['assembling', 'operating', 'breaking down'],
                'symbols': ['wrench', 'blueprint', 'oil can', 'gauge']
            },
            'nature': {
                'concepts': ['growth', 'change', 'emotion', 'time'],
                'visuals': ['tree', 'seasons', 'weather', 'landscape', 'cycle'],
                'transformations': ['blooming', 'withering', 'weathering', 'evolving'],
                'symbols': ['seed', 'root', 'branch', 'leaf']
            },
            'light': {
                'concepts': ['knowledge', 'truth', 'consciousness', 'hope'],
                'visuals': ['beam', 'glow', 'shadow', 'reflection', 'prism'],
                'transformations': ['illuminating', 'revealing', 'casting shadows'],
                'symbols': ['lamp', 'mirror', 'lens', 'beacon']
            },
            'fabric': {
                'concepts': ['reality', 'society', 'connection', 'story'],
                'visuals': ['threads', 'weave', 'tapestry', 'pattern', 'texture'],
                'transformations': ['weaving', 'unraveling', 'mending', 'tearing'],
                'symbols': ['loom', 'needle', 'scissors', 'spindle']
            },
            'building': {
                'concepts': ['argument', 'relationship', 'identity', 'belief'],
                'visuals': ['foundation', 'structure', 'architecture', 'scaffold'],
                'transformations': ['constructing', 'demolishing', 'reinforcing'],
                'symbols': ['cornerstone', 'blueprint', 'hammer', 'level']
            },
            'ocean': {
                'concepts': ['emotion', 'unconscious', 'unknown', 'possibility'],
                'visuals': ['waves', 'depths', 'current', 'horizon', 'tide'],
                'transformations': ['diving', 'surfacing', 'drifting', 'navigating'],
                'symbols': ['anchor', 'lighthouse', 'compass', 'ship']
            }
        }
        
        # Orientational metaphor mappings
        self.orientational_mappings = {
            'up': {
                'concepts': ['happy', 'good', 'more', 'conscious', 'control'],
                'visuals': ['ascending', 'floating', 'rising', 'climbing'],
                'camera': 'low angle, upward movement'
            },
            'down': {
                'concepts': ['sad', 'bad', 'less', 'unconscious', 'submission'],
                'visuals': ['descending', 'sinking', 'falling', 'crouching'],
                'camera': 'high angle, downward movement'
            },
            'forward': {
                'concepts': ['future', 'progress', 'active', 'confronting'],
                'visuals': ['advancing', 'pushing', 'reaching', 'stepping'],
                'camera': 'tracking forward, progressive zoom'
            },
            'backward': {
                'concepts': ['past', 'regress', 'passive', 'retreating'],
                'visuals': ['reversing', 'pulling back', 'looking over shoulder'],
                'camera': 'pulling back, reverse tracking'
            },
            'center': {
                'concepts': ['important', 'self', 'focus', 'stability'],
                'visuals': ['converging', 'radiating', 'balanced', 'anchored'],
                'camera': 'centered composition, stable frame'
            },
            'periphery': {
                'concepts': ['unimportant', 'other', 'distraction', 'instability'],
                'visuals': ['scattered', 'orbiting', 'fragmented', 'drifting'],
                'camera': 'off-center, dutch angles'
            }
        }
        
        # Visual metaphor patterns
        self.visual_patterns = {
            'transformation': {
                'keywords': ['become', 'turn into', 'transform', 'morph', 'evolve', 'metamorphose'],
                'visual_sequence': ['initial state', 'transition effect', 'final state'],
                'semantic_patterns': ['X becomes Y', 'changing from X to Y', 'X transforms into Y']
            },
            'revelation': {
                'keywords': ['reveal', 'uncover', 'discover', 'expose', 'unveil', 'illuminate'],
                'visual_sequence': ['concealed state', 'unveiling action', 'revealed truth'],
                'semantic_patterns': ['hidden X', 'X comes to light', 'seeing X clearly']
            },
            'fragmentation': {
                'keywords': ['shatter', 'break', 'fragment', 'split', 'fracture', 'disintegrate'],
                'visual_sequence': ['whole state', 'breaking motion', 'scattered pieces'],
                'semantic_patterns': ['X falls apart', 'breaking X', 'X in pieces']
            },
            'unification': {
                'keywords': ['merge', 'unite', 'combine', 'fuse', 'integrate', 'synthesize'],
                'visual_sequence': ['separate elements', 'coming together', 'unified whole'],
                'semantic_patterns': ['X and Y become one', 'joining X with Y', 'X merges with Y']
            },
            'dissolution': {
                'keywords': ['dissolve', 'fade', 'disappear', 'vanish', 'evaporate', 'dissipate'],
                'visual_sequence': ['solid state', 'dissolving process', 'absence'],
                'semantic_patterns': ['X fades away', 'X dissolves into Y', 'losing X']
            },
            'emergence': {
                'keywords': ['emerge', 'arise', 'appear', 'manifest', 'materialize', 'surface'],
                'visual_sequence': ['void/background', 'emerging process', 'manifested form'],
                'semantic_patterns': ['X emerges from Y', 'X comes into being', 'birth of X']
            }
        }
        
        # Extended metaphor semantic roles
        self.semantic_roles = {
            'source_domain': ['like', 'as', 'resembles', 'similar to'],
            'target_domain': ['is', 'becomes', 'represents', 'embodies'],
            'mapping_verbs': ['reflects', 'mirrors', 'echoes', 'parallels'],
            'transformation_verbs': ['transforms', 'becomes', 'turns into', 'evolves into']
        }
        
        # Metaphorical intensity levels
        self.intensity_markers = {
            'subtle': ['somewhat', 'slightly', 'a bit', 'touches of'],
            'moderate': ['quite', 'rather', 'fairly', 'considerably'],
            'intense': ['completely', 'utterly', 'entirely', 'profoundly'],
            'extreme': ['infinitely', 'absolutely', 'totally', 'fundamentally']
        }
        
    def translate_to_visual(
        self,
        concept: Optional[str],
        context: Dict[str, Any],
        stage_directions: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Translate metaphorical concepts to visual representations."""
        if not concept and not stage_directions:
            return self._default_visual()
            
        # Extract metaphors from text
        metaphors = self._extract_metaphors(
            concept or '',
            context.get('dialogue', ''),
            stage_directions or []
        )
        
        # Translate each metaphor
        visual_metaphors = []
        for metaphor in metaphors:
            visual_metaphor = self._translate_single_metaphor(metaphor, context)
            if visual_metaphor:
                visual_metaphors.append(visual_metaphor)
        
        # Synthesize visual representation
        return self._synthesize_visual_representation(visual_metaphors, context)
    
    def _extract_metaphors(
        self,
        concept: str,
        dialogue: str,
        stage_directions: List[str]
    ) -> List[Dict[str, Any]]:
        """Extract metaphors from text content with enhanced semantic analysis."""
        metaphors = []
        combined_text = f"{concept} {dialogue} {' '.join(stage_directions)}"
        combined_text_lower = combined_text.lower()
        
        # Use spaCy for deeper analysis if available
        if self.nlp:
            metaphors.extend(self._extract_metaphors_semantic(combined_text))
        
        # Check for conceptual metaphors
        for source, mapping in self.conceptual_mappings.items():
            for target in mapping['concepts']:
                # Look for "X is Y" patterns
                pattern = rf'\b{target}\s+(?:is|as|like)\s+(?:a\s+)?{source}\b'
                if re.search(pattern, combined_text_lower):
                    intensity = self._detect_intensity(combined_text_lower, pattern)
                    metaphors.append({
                        'type': MetaphorType.CONCEPTUAL,
                        'source': source,
                        'target': target,
                        'mapping': mapping,
                        'intensity': intensity
                    })
                
                # Look for implicit metaphors
                if source in combined_text_lower and target in combined_text_lower:
                    # Check proximity
                    if self._check_word_proximity(combined_text_lower, source, target, max_distance=10):
                        metaphors.append({
                            'type': MetaphorType.CONCEPTUAL,
                            'source': source,
                            'target': target,
                            'mapping': mapping,
                            'implicit': True,
                            'intensity': 'subtle'
                        })
        
        # Check for orientational metaphors
        for direction, mapping in self.orientational_mappings.items():
            if direction in combined_text_lower:
                for concept in mapping['concepts']:
                    if concept in combined_text_lower:
                        metaphors.append({
                            'type': MetaphorType.ORIENTATIONAL,
                            'direction': direction,
                            'concept': concept,
                            'mapping': mapping
                        })
        
        # Check for visual transformation patterns with semantic patterns
        for pattern_name, pattern in self.visual_patterns.items():
            for keyword in pattern['keywords']:
                if keyword in combined_text_lower:
                    # Check for semantic patterns
                    semantic_match = False
                    if 'semantic_patterns' in pattern:
                        for sem_pattern in pattern['semantic_patterns']:
                            if self._check_semantic_pattern(combined_text_lower, sem_pattern):
                                semantic_match = True
                                break
                    
                    metaphors.append({
                        'type': MetaphorType.VISUAL,
                        'pattern': pattern_name,
                        'sequence': pattern['visual_sequence'],
                        'semantic_match': semantic_match
                    })
        
        # Remove duplicates while preserving the most specific matches
        metaphors = self._deduplicate_metaphors(metaphors)
        
        return metaphors
    
    def _extract_metaphors_semantic(self, text: str) -> List[Dict[str, Any]]:
        """Extract metaphors using spaCy semantic analysis."""
        metaphors = []
        doc = self.nlp(text)
        
        # Look for metaphorical verb constructions
        for token in doc:
            if token.pos_ == "VERB":
                # Check for metaphorical transformation verbs
                if token.lemma_ in ['become', 'transform', 'turn']:
                    # Find subject and object
                    subj = None
                    obj = None
                    for child in token.children:
                        if child.dep_ == "nsubj":
                            subj = child
                        elif child.dep_ in ["attr", "dobj", "pobj"]:
                            obj = child
                    
                    if subj and obj:
                        metaphors.append({
                            'type': MetaphorType.STRUCTURAL,
                            'source': obj.text,
                            'target': subj.text,
                            'verb': token.text,
                            'semantic_role': 'transformation'
                        })
                
                # Check for comparison structures
                elif token.lemma_ in self.semantic_roles['mapping_verbs']:
                    for child in token.children:
                        if child.dep_ == "dobj" or child.dep_ == "pobj":
                            metaphors.append({
                                'type': MetaphorType.STRUCTURAL,
                                'comparison_verb': token.text,
                                'compared_element': child.text,
                                'semantic_role': 'comparison'
                            })
        
        # Look for simile patterns
        for i, token in enumerate(doc):
            if token.text.lower() in ['like', 'as'] and i < len(doc) - 1:
                # Get context around the comparison word
                before = doc[max(0, i-3):i]
                after = doc[i+1:min(len(doc), i+4)]
                
                if before and after:
                    metaphors.append({
                        'type': MetaphorType.CONCEPTUAL,
                        'source': ' '.join([t.text for t in after]),
                        'target': ' '.join([t.text for t in before]),
                        'explicit_comparison': True
                    })
        
        return metaphors
    
    def _detect_intensity(self, text: str, pattern: str) -> str:
        """Detect the intensity of a metaphor based on surrounding modifiers."""
        # Find the pattern match position
        match = re.search(pattern, text)
        if not match:
            return 'moderate'
        
        # Get surrounding context
        start = max(0, match.start() - 50)
        end = min(len(text), match.end() + 50)
        context = text[start:end]
        
        # Check for intensity markers
        for intensity, markers in self.intensity_markers.items():
            for marker in markers:
                if marker in context:
                    return intensity
        
        return 'moderate'
    
    def _check_word_proximity(self, text: str, word1: str, word2: str, max_distance: int) -> bool:
        """Check if two words appear within a certain distance of each other."""
        words = text.split()
        positions1 = [i for i, w in enumerate(words) if word1 in w]
        positions2 = [i for i, w in enumerate(words) if word2 in w]
        
        for p1 in positions1:
            for p2 in positions2:
                if abs(p1 - p2) <= max_distance:
                    return True
        
        return False
    
    def _check_semantic_pattern(self, text: str, pattern: str) -> bool:
        """Check if a semantic pattern matches in the text."""
        # Convert pattern variables (X, Y) to regex
        pattern_regex = pattern.replace('X', r'(\w+)').replace('Y', r'(\w+)')
        return bool(re.search(pattern_regex, text, re.IGNORECASE))
    
    def _deduplicate_metaphors(self, metaphors: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate metaphors, keeping the most specific ones."""
        seen = set()
        unique_metaphors = []
        
        # Sort by specificity (explicit > implicit, semantic_match > no match)
        sorted_metaphors = sorted(metaphors, 
                                 key=lambda x: (not x.get('implicit', False), 
                                              x.get('semantic_match', False)),
                                 reverse=True)
        
        for metaphor in sorted_metaphors:
            # Create a hashable key
            key_parts = [
                str(metaphor.get('type', '')),
                str(metaphor.get('source', '')),
                str(metaphor.get('target', '')),
                str(metaphor.get('pattern', ''))
            ]
            key = tuple(key_parts)
            
            if key not in seen:
                seen.add(key)
                unique_metaphors.append(metaphor)
        
        return unique_metaphors
    
    def _translate_single_metaphor(
        self,
        metaphor: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Optional[VisualMetaphor]:
        """Translate a single metaphor to visual representation."""
        if metaphor['type'] == MetaphorType.CONCEPTUAL:
            return self._translate_conceptual_metaphor(metaphor, context)
        elif metaphor['type'] == MetaphorType.ORIENTATIONAL:
            return self._translate_orientational_metaphor(metaphor, context)
        elif metaphor['type'] == MetaphorType.VISUAL:
            return self._translate_visual_metaphor(metaphor, context)
        
        return None
    
    def _translate_conceptual_metaphor(
        self,
        metaphor: Dict[str, Any],
        context: Dict[str, Any]
    ) -> VisualMetaphor:
        """Translate conceptual metaphor to visual elements."""
        mapping = metaphor['mapping']
        intensity = metaphor.get('intensity', 'moderate')
        
        # Adjust number of visual elements based on intensity
        element_count = {'subtle': 2, 'moderate': 3, 'intense': 4, 'extreme': 5}
        num_elements = element_count.get(intensity, 3)
        
        visual_elements = mapping['visuals'][:num_elements]
        transformations = mapping['transformations'][:2]
        symbols = mapping['symbols'][:2]
        
        # Create compositional notes with intensity
        if metaphor.get('implicit'):
            composition = f"Subtle visual echoes of {metaphor['source']} in the environment"
        else:
            intensity_desc = {
                'subtle': 'Gentle hints of',
                'moderate': 'Clear visual metaphor:',
                'intense': 'Strong visual emphasis:',
                'extreme': 'Overwhelming presence of'
            }
            desc = intensity_desc.get(intensity, 'Clear visual metaphor:')
            composition = f"{desc} {metaphor['target']} represented as {metaphor['source']}"
        
        # Add intensity-specific visual treatments
        if intensity in ['intense', 'extreme']:
            composition += ", with dramatic lighting and scale"
        elif intensity == 'subtle':
            composition += ", using soft focus and transparency"
        
        return VisualMetaphor(
            source_text=f"{metaphor['target']} as {metaphor['source']}",
            metaphor_type=MetaphorType.CONCEPTUAL,
            concept_pair=(metaphor['source'], metaphor['target']),
            visual_elements=visual_elements,
            transformation_sequence=transformations,
            symbolic_objects=symbols,
            compositional_notes=composition
        )
    
    def _translate_orientational_metaphor(
        self,
        metaphor: Dict[str, Any],
        context: Dict[str, Any]
    ) -> VisualMetaphor:
        """Translate orientational metaphor to visual elements."""
        mapping = metaphor['mapping']
        direction = metaphor['direction']
        
        visual_elements = mapping['visuals']
        camera_work = mapping['camera']
        
        # Add character positioning
        character_position = f"Character positioned {direction} in frame"
        
        return VisualMetaphor(
            source_text=f"{metaphor['concept']} is {direction}",
            metaphor_type=MetaphorType.ORIENTATIONAL,
            concept_pair=(direction, metaphor['concept']),
            visual_elements=visual_elements,
            transformation_sequence=[character_position, camera_work],
            symbolic_objects=[],
            compositional_notes=f"Use {direction} orientation to represent {metaphor['concept']}"
        )
    
    def _translate_visual_metaphor(
        self,
        metaphor: Dict[str, Any],
        context: Dict[str, Any]
    ) -> VisualMetaphor:
        """Translate visual transformation metaphor."""
        pattern = metaphor['pattern']
        sequence = metaphor['sequence']
        
        # Customize sequence based on context
        if context.get('character'):
            sequence = [f"{context['character']} in {state}" for state in sequence]
        
        return VisualMetaphor(
            source_text=pattern,
            metaphor_type=MetaphorType.VISUAL,
            concept_pair=(pattern, 'transformation'),
            visual_elements=[],
            transformation_sequence=sequence,
            symbolic_objects=[],
            compositional_notes=f"Visual {pattern} sequence"
        )
    
    def _synthesize_visual_representation(
        self,
        metaphors: List[VisualMetaphor],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Synthesize multiple metaphors into cohesive visual representation."""
        if not metaphors:
            return self._default_visual()
        
        # Collect all visual elements
        all_visuals = []
        all_symbols = []
        all_transformations = []
        compositional_notes = []
        
        for metaphor in metaphors:
            all_visuals.extend(metaphor.visual_elements)
            all_symbols.extend(metaphor.symbolic_objects)
            all_transformations.extend(metaphor.transformation_sequence)
            compositional_notes.append(metaphor.compositional_notes)
        
        # Prioritize and limit elements
        primary_visuals = list(set(all_visuals))[:4]
        key_symbols = list(set(all_symbols))[:3]
        main_transformation = all_transformations[0] if all_transformations else None
        
        return {
            'metaphor_count': len(metaphors),
            'primary_metaphor': metaphors[0].concept_pair if metaphors else None,
            'visual_elements': primary_visuals,
            'symbolic_objects': key_symbols,
            'transformation': main_transformation,
            'compositional_approach': ' | '.join(compositional_notes[:2]),
            'layering_suggestion': self._suggest_layering(metaphors),
            'visual_complexity': self._assess_complexity(metaphors)
        }
    
    def _suggest_layering(self, metaphors: List[VisualMetaphor]) -> str:
        """Suggest how to layer multiple metaphors visually."""
        if len(metaphors) == 1:
            return "Single metaphor as primary visual focus"
        elif len(metaphors) == 2:
            return "Dual metaphor composition with foreground/background separation"
        else:
            return "Multi-layered composition with primary metaphor prominent, others as environmental elements"
    
    def _assess_complexity(self, metaphors: List[VisualMetaphor]) -> str:
        """Assess visual complexity based on metaphor count and types."""
        conceptual_count = sum(1 for m in metaphors if m.metaphor_type == MetaphorType.CONCEPTUAL)
        
        if len(metaphors) == 0:
            return "simple"
        elif len(metaphors) == 1:
            return "moderate"
        elif conceptual_count > 1:
            return "complex"
        else:
            return "layered"
    
    def _default_visual(self) -> Dict[str, Any]:
        """Return default visual representation when no metaphors found."""
        return {
            'metaphor_count': 0,
            'primary_metaphor': None,
            'visual_elements': [],
            'symbolic_objects': [],
            'transformation': None,
            'compositional_approach': 'Literal representation',
            'layering_suggestion': 'Focus on character and environment',
            'visual_complexity': 'simple'
        }