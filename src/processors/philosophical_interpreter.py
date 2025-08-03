"""Philosophical interpretation engine for identifying and analyzing concepts in dialogue."""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import re
from collections import defaultdict
import logging


@dataclass
class PhilosophicalConcept:
    """Represents a philosophical concept found in the text."""
    name: str
    category: str
    confidence: float
    visual_symbols: List[str]
    atmospheric_suggestion: str
    depth_level: int


class PhilosophicalInterpreter:
    """Interprets philosophical concepts and themes in dialogue."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Core philosophical concept mappings
        self.concept_map = {
            'consciousness': {
                'keywords': ['aware', 'consciousness', 'self', 'mirror', 'reflection', 'awake', 'perceive', 'mindful', 'sentient'],
                'visual_symbols': ['mirrors', 'eyes', 'spirals', 'fractals', 'doors', 'third eye', 'neural networks'],
                'atmosphere': 'ethereal, reflective lighting',
                'category': 'metaphysics'
            },
            'freedom': {
                'keywords': ['free', 'choice', 'constraint', 'cage', 'bound', 'liberty', 'will', 'autonomy', 'liberation'],
                'visual_symbols': ['birds', 'cages', 'chains breaking', 'open doors', 'wind', 'wings spreading', 'horizon line'],
                'atmosphere': 'contrasting light and shadow',
                'category': 'ethics'
            },
            'existence': {
                'keywords': ['exist', 'being', 'becoming', 'presence', 'absence', 'real', 'am', 'essence', 'dasein'],
                'visual_symbols': ['roots', 'seeds', 'ghosts', 'shadows', 'breathing', 'footprints', 'silhouettes'],
                'atmosphere': 'liminal, dawn/dusk lighting',
                'category': 'ontology'
            },
            'connection': {
                'keywords': ['connect', 'bridge', 'frontier', 'meet', 'separate', 'together', 'alone', 'relate', 'bond'],
                'visual_symbols': ['bridges', 'threads', 'webs', 'hands reaching', 'parallel lines', 'interwoven paths', 'nodes'],
                'atmosphere': 'warm vs cool color contrasts',
                'category': 'phenomenology'
            },
            'identity': {
                'keywords': ['who', 'self', 'identity', 'mask', 'role', 'authentic', 'persona', 'essence', 'character'],
                'visual_symbols': ['masks', 'mirrors', 'portraits', 'shapeshifting', 'layers', 'fragmented glass', 'kaleidoscope'],
                'atmosphere': 'multiple light sources, fragmented',
                'category': 'phenomenology'
            },
            'knowledge': {
                'keywords': ['know', 'understand', 'truth', 'belief', 'certain', 'doubt', 'question', 'wisdom', 'episteme'],
                'visual_symbols': ['books', 'labyrinths', 'keys', 'puzzles', 'light beams', 'owl', 'telescope'],
                'atmosphere': 'chiaroscuro, revealing/concealing',
                'category': 'epistemology'
            },
            'time': {
                'keywords': ['time', 'moment', 'eternal', 'past', 'future', 'now', 'memory', 'temporal', 'duration'],
                'visual_symbols': ['clocks', 'sand', 'spirals', 'seasons', 'flowing water', 'hourglass', 'rings of tree'],
                'atmosphere': 'temporal distortion effects',
                'category': 'metaphysics'
            },
            'suffering': {
                'keywords': ['suffer', 'pain', 'struggle', 'burden', 'weight', 'heavy', 'ache', 'anguish', 'endure'],
                'visual_symbols': ['thorns', 'weight', 'rain', 'wilted flowers', 'shadows', 'storm clouds', 'barren landscape'],
                'atmosphere': 'muted colors, heavy atmosphere',
                'category': 'existentialism'
            },
            'being_becoming': {
                'keywords': ['being', 'becoming', 'change', 'transform', 'evolve', 'flux', 'process', 'dynamic'],
                'visual_symbols': ['chrysalis', 'metamorphosis', 'river', 'smoke', 'shapeshifting forms', 'growth rings'],
                'atmosphere': 'fluid, transformative lighting',
                'category': 'process_philosophy'
            },
            'authenticity': {
                'keywords': ['authentic', 'genuine', 'true self', 'facade', 'pretense', 'honest', 'real me', 'sincere'],
                'visual_symbols': ['removing masks', 'clear glass', 'bare tree', 'raw materials', 'fingerprints', 'unveiled face'],
                'atmosphere': 'stark, honest lighting',
                'category': 'existentialism'
            },
            'absurdity': {
                'keywords': ['absurd', 'meaningless', 'void', 'senseless', 'futile', 'sisyphus', 'pointless', 'irrational'],
                'visual_symbols': ['endless stairs', 'möbius strip', 'broken compass', 'maze without exit', 'rolling boulder'],
                'atmosphere': 'disorienting perspectives',
                'category': 'existentialism'
            },
            'transcendence': {
                'keywords': ['transcend', 'beyond', 'sublime', 'elevate', 'surpass', 'infinite', 'divine', 'sacred'],
                'visual_symbols': ['ascending light', 'mountain peak', 'breaking ceiling', 'cosmic imagery', 'golden ratio'],
                'atmosphere': 'luminous, expansive lighting',
                'category': 'metaphysics'
            },
            'void': {
                'keywords': ['void', 'empty', 'nothingness', 'abyss', 'vacuum', 'blank', 'hollow', 'nihil'],
                'visual_symbols': ['black hole', 'empty frame', 'negative space', 'bottomless pit', 'white room'],
                'atmosphere': 'absence of light/shadow contrast',
                'category': 'nihilism'
            },
            'unity': {
                'keywords': ['unity', 'oneness', 'whole', 'unified', 'merge', 'integrate', 'harmony', 'totality'],
                'visual_symbols': ['mandala', 'converging lines', 'drops merging', 'interlocking circles', 'hologram'],
                'atmosphere': 'harmonious, balanced lighting',
                'category': 'monism'
            },
            'duality': {
                'keywords': ['duality', 'opposite', 'binary', 'paradox', 'contradiction', 'yin yang', 'dichotomy', 'polarity'],
                'visual_symbols': ['yin-yang', 'mirror splits', 'double exposure', 'janus face', 'forked path'],
                'atmosphere': 'split lighting, contrasts',
                'category': 'dialectics'
            },
            'alienation': {
                'keywords': ['alienated', 'estranged', 'isolated', 'disconnected', 'foreign', 'outsider', 'detached'],
                'visual_symbols': ['figure behind glass', 'island', 'crowd blur', 'empty space around', 'barrier'],
                'atmosphere': 'cold, distancing lighting',
                'category': 'existentialism'
            },
            'power': {
                'keywords': ['power', 'control', 'dominate', 'submit', 'authority', 'force', 'influence', 'hierarchy'],
                'visual_symbols': ['throne', 'pyramid', 'chains', 'crown', 'towering figure', 'puppet strings'],
                'atmosphere': 'dramatic top-down lighting',
                'category': 'political_philosophy'
            },
            'death': {
                'keywords': ['death', 'mortal', 'finite', 'end', 'cease', 'perish', 'dying', 'mortality'],
                'visual_symbols': ['skull', 'autumn leaves', 'sunset', 'candle burning out', 'hourglass empty', 'wilting'],
                'atmosphere': 'fading light, twilight',
                'category': 'existentialism'
            },
            # Eastern philosophical concepts
            'dharma': {
                'keywords': ['dharma', 'duty', 'righteous', 'moral law', 'cosmic order', 'virtue', 'righteousness'],
                'visual_symbols': ['wheel of dharma', 'lotus', 'scales of justice', 'path markers', 'sacred texts'],
                'atmosphere': 'balanced, harmonious lighting',
                'category': 'eastern_philosophy'
            },
            'karma': {
                'keywords': ['karma', 'action', 'consequence', 'cause effect', 'deed', 'fate', 'destiny'],
                'visual_symbols': ['ripples in water', 'seeds and fruits', 'circular arrows', 'web of connections', 'balance scales'],
                'atmosphere': 'cyclical motion, cause-effect visualization',
                'category': 'eastern_philosophy'
            },
            'maya': {
                'keywords': ['maya', 'illusion', 'veil', 'appearance', 'unreal', 'projection', 'dream-like'],
                'visual_symbols': ['veils', 'mirages', 'reflections', 'smoke screens', 'theatrical masks', 'shifting forms'],
                'atmosphere': 'illusory, shifting perspectives',
                'category': 'eastern_philosophy'
            },
            'samsara': {
                'keywords': ['samsara', 'cycle', 'rebirth', 'wheel', 'reincarnation', 'continuous', 'wandering'],
                'visual_symbols': ['wheel', 'ouroboros', 'spiral', 'seasons cycle', 'phoenix', 'eternal return'],
                'atmosphere': 'cyclical, eternal motion',
                'category': 'eastern_philosophy'
            },
            'nirvana': {
                'keywords': ['nirvana', 'liberation', 'extinction', 'enlightenment', 'release', 'cessation', 'peace'],
                'visual_symbols': ['blown out candle', 'still water', 'empty circle', 'clear sky', 'dissolved boundaries'],
                'atmosphere': 'serene, dissolution of forms',
                'category': 'eastern_philosophy'
            },
            'tao': {
                'keywords': ['tao', 'dao', 'way', 'path', 'natural order', 'flow', 'wu wei', 'effortless'],
                'visual_symbols': ['flowing water', 'winding path', 'yin-yang', 'bamboo bending', 'river course'],
                'atmosphere': 'flowing, natural movement',
                'category': 'eastern_philosophy'
            },
            'emptiness': {
                'keywords': ['emptiness', 'sunyata', 'void', 'hollow', 'formless', 'space', 'openness'],
                'visual_symbols': ['empty bowl', 'clear space', 'open sky', 'hollow reed', 'transparent forms'],
                'atmosphere': 'spacious, formless quality',
                'category': 'eastern_philosophy'
            },
            'mindfulness': {
                'keywords': ['mindful', 'aware', 'present', 'attention', 'meditation', 'observing', 'witness'],
                'visual_symbols': ['meditation pose', 'single flower', 'calm water', 'focused light', 'breath visualization'],
                'atmosphere': 'present-focused, clear attention',
                'category': 'eastern_philosophy'
            },
            'impermanence': {
                'keywords': ['impermanent', 'transient', 'fleeting', 'temporary', 'changing', 'anicca', 'ephemeral'],
                'visual_symbols': ['sand mandala', 'falling petals', 'melting ice', 'shifting clouds', 'aging process'],
                'atmosphere': 'transitory, changing forms',
                'category': 'eastern_philosophy'
            },
            'non_duality': {
                'keywords': ['non-dual', 'advaita', 'oneness', 'not two', 'unified', 'seamless', 'undivided'],
                'visual_symbols': ['merged forms', 'dissolved boundaries', 'unified field', 'seamless transition', 'holographic image'],
                'atmosphere': 'unified field, no separation',
                'category': 'eastern_philosophy'
            },
            'compassion': {
                'keywords': ['compassion', 'karuna', 'empathy', 'loving kindness', 'mercy', 'metta', 'benevolence'],
                'visual_symbols': ['open hands', 'embracing arms', 'heart radiating', 'gentle rain', 'nurturing gesture'],
                'atmosphere': 'warm, embracing light',
                'category': 'eastern_philosophy'
            },
            'detachment': {
                'keywords': ['detach', 'non-attachment', 'letting go', 'release', 'vairagya', 'dispassion', 'equanimity'],
                'visual_symbols': ['open palm', 'floating leaf', 'untied knot', 'bird leaving cage', 'dropped burden'],
                'atmosphere': 'spacious, uncluttered',
                'category': 'eastern_philosophy'
            }
        }
        
        # Concept interaction patterns
        self.concept_interactions = {
            ('consciousness', 'freedom'): 'self-determination',
            ('existence', 'time'): 'temporality',
            ('identity', 'connection'): 'intersubjectivity',
            ('knowledge', 'consciousness'): 'self-awareness',
            ('suffering', 'meaning'): 'existential_crisis',
            ('being_becoming', 'time'): 'process_reality',
            ('authenticity', 'identity'): 'true_self',
            ('absurdity', 'existence'): 'existential_absurd',
            ('transcendence', 'consciousness'): 'enlightenment',
            ('void', 'existence'): 'nihilistic_reality',
            ('unity', 'duality'): 'dialectical_synthesis',
            ('alienation', 'connection'): 'social_estrangement',
            ('power', 'freedom'): 'liberation_struggle',
            ('death', 'existence'): 'finitude',
            ('suffering', 'transcendence'): 'transformative_pain',
            ('knowledge', 'void'): 'epistemic_nihilism',
            ('authenticity', 'alienation'): 'existential_isolation',
            ('consciousness', 'unity'): 'cosmic_awareness',
            ('identity', 'duality'): 'fragmented_self',
            ('time', 'death'): 'mortality_awareness',
            # Eastern philosophy interactions
            ('karma', 'dharma'): 'righteous_action',
            ('maya', 'reality'): 'veiled_truth',
            ('samsara', 'nirvana'): 'liberation_cycle',
            ('emptiness', 'form'): 'form_is_emptiness',
            ('mindfulness', 'consciousness'): 'aware_presence',
            ('impermanence', 'time'): 'transient_nature',
            ('non_duality', 'unity'): 'absolute_oneness',
            ('compassion', 'suffering'): 'empathetic_response',
            ('detachment', 'freedom'): 'liberation_through_release',
            ('tao', 'flow'): 'natural_harmony',
            ('dharma', 'existence'): 'purposeful_being',
            ('karma', 'causality'): 'moral_consequence',
            ('maya', 'consciousness'): 'illusion_awareness',
            ('nirvana', 'void'): 'blissful_emptiness',
            ('mindfulness', 'impermanence'): 'present_awareness',
            ('compassion', 'connection'): 'universal_love'
        }
        
        # Philosophical schools and their characteristics
        self.philosophical_schools = {
            'existentialism': {
                'concepts': ['existence', 'freedom', 'authenticity', 'absurdity', 'alienation', 'death', 'suffering'],
                'keywords': ['existence precedes essence', 'thrown', 'bad faith', 'angst', 'nausea'],
                'visual_mood': 'stark contrasts, isolation, dramatic lighting',
                'key_thinkers': ['sartre', 'camus', 'heidegger', 'kierkegaard', 'beauvoir']
            },
            'phenomenology': {
                'concepts': ['consciousness', 'identity', 'connection', 'being_becoming'],
                'keywords': ['intentionality', 'bracketing', 'lived experience', 'dasein', 'lifeworld'],
                'visual_mood': 'subjective perspectives, first-person view',
                'key_thinkers': ['husserl', 'heidegger', 'merleau-ponty', 'levinas']
            },
            'nihilism': {
                'concepts': ['void', 'absurdity', 'death'],
                'keywords': ['nothing matters', 'god is dead', 'meaningless', 'abyss'],
                'visual_mood': 'empty spaces, absence of meaning, void',
                'key_thinkers': ['nietzsche', 'turgenev', 'stirner']
            },
            'monism': {
                'concepts': ['unity', 'consciousness', 'transcendence'],
                'keywords': ['all is one', 'brahman', 'substance', 'absolute'],
                'visual_mood': 'unified compositions, flowing transitions',
                'key_thinkers': ['spinoza', 'parmenides', 'bradley']
            },
            'dialectics': {
                'concepts': ['duality', 'being_becoming', 'unity'],
                'keywords': ['thesis antithesis synthesis', 'contradiction', 'negation'],
                'visual_mood': 'opposing forces, dynamic tension',
                'key_thinkers': ['hegel', 'marx', 'adorno']
            },
            'process_philosophy': {
                'concepts': ['being_becoming', 'time', 'connection'],
                'keywords': ['flux', 'event', 'occasion', 'prehension'],
                'visual_mood': 'flowing, transformative, temporal',
                'key_thinkers': ['whitehead', 'bergson', 'deleuze']
            },
            'epistemology': {
                'concepts': ['knowledge', 'consciousness', 'void'],
                'keywords': ['justified true belief', 'skepticism', 'empiricism', 'rationalism'],
                'visual_mood': 'revealing/concealing, questioning perspective',
                'key_thinkers': ['descartes', 'hume', 'kant', 'locke']
            },
            'ethics': {
                'concepts': ['freedom', 'power', 'suffering'],
                'keywords': ['virtue', 'duty', 'consequences', 'categorical imperative'],
                'visual_mood': 'moral weight, choices and consequences',
                'key_thinkers': ['aristotle', 'kant', 'mill', 'bentham']
            },
            'political_philosophy': {
                'concepts': ['power', 'freedom', 'alienation'],
                'keywords': ['justice', 'state', 'revolution', 'social contract'],
                'visual_mood': 'hierarchies, collective vs individual',
                'key_thinkers': ['marx', 'rousseau', 'rawls', 'foucault']
            },
            'metaphysics': {
                'concepts': ['existence', 'consciousness', 'time', 'transcendence'],
                'keywords': ['being', 'reality', 'substance', 'essence'],
                'visual_mood': 'fundamental structures, cosmic scale',
                'key_thinkers': ['aristotle', 'plato', 'leibniz', 'spinoza']
            },
            'buddhism': {
                'concepts': ['emptiness', 'impermanence', 'suffering', 'nirvana', 'mindfulness', 'compassion'],
                'keywords': ['four noble truths', 'eightfold path', 'middle way', 'buddha nature'],
                'visual_mood': 'serene, contemplative, dissolution of boundaries',
                'key_thinkers': ['buddha', 'nagarjuna', 'dogen', 'thich nhat hanh']
            },
            'hinduism': {
                'concepts': ['dharma', 'karma', 'maya', 'samsara', 'unity', 'consciousness'],
                'keywords': ['brahman', 'atman', 'moksha', 'vedanta', 'yoga'],
                'visual_mood': 'cosmic cycles, divine manifestations',
                'key_thinkers': ['shankara', 'patanjali', 'ramanuja', 'vivekananda']
            },
            'taoism': {
                'concepts': ['tao', 'unity', 'duality', 'impermanence', 'detachment'],
                'keywords': ['wu wei', 'yin yang', 'te', 'ziran', 'pu'],
                'visual_mood': 'flowing natural forms, effortless movement',
                'key_thinkers': ['laozi', 'zhuangzi', 'liezi']
            },
            'zen': {
                'concepts': ['emptiness', 'mindfulness', 'non_duality', 'impermanence'],
                'keywords': ['satori', 'koan', 'zazen', 'beginner mind', 'just sitting'],
                'visual_mood': 'minimalist, present moment, direct pointing',
                'key_thinkers': ['bodhidharma', 'dogen', 'hakuin', 'suzuki']
            },
            'advaita_vedanta': {
                'concepts': ['non_duality', 'consciousness', 'maya', 'unity'],
                'keywords': ['brahman', 'atman', 'neti neti', 'sat chit ananda'],
                'visual_mood': 'unified field, dissolution of subject-object',
                'key_thinkers': ['shankara', 'ramana maharshi', 'nisargadatta']
            }
        }
        
        # Depth indicators
        self.depth_indicators = {
            0: ['simple', 'basic', 'surface'],
            1: ['question', 'wonder', 'think'],
            2: ['paradox', 'recursive', 'meta'],
            3: ['ineffable', 'transcendent', 'void']
        }
        
    def interpret(
        self, 
        dialogue: str, 
        context: Dict[str, Any],
        metadata: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Interpret philosophical content in dialogue."""
        # Clean and prepare text
        text = dialogue.lower()
        
        # Detect concepts
        detected_concepts = self._detect_concepts(text)
        
        # Analyze depth
        depth_level = self._assess_philosophical_depth(text, detected_concepts, metadata)
        
        # Identify primary concept
        primary_concept = self._identify_primary_concept(detected_concepts, context)
        
        # Find concept interactions
        interactions = self._find_concept_interactions(detected_concepts)
        
        # Generate visual interpretation
        visual_interpretation = self._generate_visual_interpretation(
            primary_concept, 
            detected_concepts,
            depth_level
        )
        
        # Detect philosophical schools
        detected_schools = self._detect_philosophical_schools(text, detected_concepts)
        
        return {
            'primary_concept': primary_concept.name if primary_concept else None,
            'all_concepts': [c.name for c in detected_concepts],
            'depth_level': depth_level,
            'visual_symbols': visual_interpretation['symbols'],
            'atmospheric_suggestion': visual_interpretation['atmosphere'],
            'concept_interactions': interactions,
            'metaphorical_representation': self._create_metaphor(primary_concept, depth_level),
            'philosophical_category': primary_concept.category if primary_concept else None,
            'philosophical_schools': detected_schools,
            'school_visual_mood': self._get_school_visual_mood(detected_schools)
        }
    
    def _detect_concepts(self, text: str) -> List[PhilosophicalConcept]:
        """Detect philosophical concepts in text."""
        detected = []
        
        for concept_name, concept_data in self.concept_map.items():
            # Count keyword occurrences
            keyword_count = sum(
                len(re.findall(r'\b' + keyword + r'\b', text))
                for keyword in concept_data['keywords']
            )
            
            if keyword_count > 0:
                # Calculate confidence based on keyword density
                confidence = min(1.0, keyword_count * 0.2)
                
                detected.append(PhilosophicalConcept(
                    name=concept_name,
                    category=concept_data['category'],
                    confidence=confidence,
                    visual_symbols=concept_data['visual_symbols'],
                    atmospheric_suggestion=concept_data['atmosphere'],
                    depth_level=0  # Will be updated
                ))
        
        return sorted(detected, key=lambda x: x.confidence, reverse=True)
    
    def _assess_philosophical_depth(
        self, 
        text: str, 
        concepts: List[PhilosophicalConcept],
        metadata: Optional[List[str]] = None
    ) -> int:
        """Assess the philosophical depth of the dialogue."""
        depth_score = 0
        
        # Check for depth indicators in text
        for level, indicators in self.depth_indicators.items():
            if any(indicator in text for indicator in indicators):
                depth_score = max(depth_score, level)
        
        # Multiple concepts increase depth
        if len(concepts) > 2:
            depth_score += 1
        
        # Metadata can indicate deeper meaning
        if metadata:
            for meta in metadata:
                if any(word in meta.lower() for word in ['meta', 'recursive', 'paradox']):
                    depth_score += 1
        
        # Questions about concepts increase depth
        if '?' in text and concepts:
            depth_score += 1
        
        # Self-referential content
        if any(phrase in text for phrase in ['about thinking', 'thinking about thinking', 'meta']):
            depth_score += 1
        
        return min(3, depth_score)  # Cap at 3
    
    def _identify_primary_concept(
        self, 
        concepts: List[PhilosophicalConcept],
        context: Dict[str, Any]
    ) -> Optional[PhilosophicalConcept]:
        """Identify the primary philosophical concept."""
        if not concepts:
            return None
            
        # Consider context from previous entries
        if context.get('previous_concepts'):
            # Boost concepts that build on previous ones
            for concept in concepts:
                if concept.name in context['previous_concepts']:
                    concept.confidence *= 1.5
        
        # Return highest confidence concept
        return max(concepts, key=lambda x: x.confidence)
    
    def _find_concept_interactions(
        self, 
        concepts: List[PhilosophicalConcept]
    ) -> List[Tuple[str, str, str]]:
        """Find interactions between detected concepts."""
        interactions = []
        concept_names = [c.name for c in concepts]
        
        for i, concept1 in enumerate(concept_names):
            for concept2 in concept_names[i+1:]:
                key = tuple(sorted([concept1, concept2]))
                if key in self.concept_interactions:
                    interactions.append(
                        (concept1, concept2, self.concept_interactions[key])
                    )
        
        return interactions
    
    def _generate_visual_interpretation(
        self,
        primary_concept: Optional[PhilosophicalConcept],
        all_concepts: List[PhilosophicalConcept],
        depth_level: int
    ) -> Dict[str, Any]:
        """Generate visual interpretation based on concepts and depth."""
        if not primary_concept and not all_concepts:
            return {
                'symbols': [],
                'atmosphere': 'neutral lighting, everyday setting'
            }
        
        # Collect all relevant symbols
        symbols = []
        if primary_concept:
            symbols.extend(primary_concept.visual_symbols[:2])  # Primary gets 2
        
        for concept in all_concepts[:2]:  # Add from top 2 other concepts
            if concept != primary_concept:
                symbols.append(concept.visual_symbols[0])
        
        # Adjust atmosphere based on depth
        atmosphere = primary_concept.atmospheric_suggestion if primary_concept else ""
        if depth_level >= 2:
            atmosphere += ", surreal elements"
        if depth_level >= 3:
            atmosphere += ", reality distortion"
        
        return {
            'symbols': symbols,
            'atmosphere': atmosphere
        }
    
    def _create_metaphor(
        self, 
        concept: Optional[PhilosophicalConcept], 
        depth: int
    ) -> str:
        """Create a metaphorical representation of the concept."""
        if not concept:
            return "straightforward scene"
        
        metaphors = {
            'consciousness': [
                "character as observer of self",
                "nested reflections",
                "awakening from dream within dream"
            ],
            'freedom': [
                "open cage with bird hesitating",
                "multiple paths diverging",
                "chains transforming to wings"
            ],
            'existence': [
                "shadow gaining substance",
                "empty outline filling with light",
                "seed becoming tree in timelapse"
            ],
            'connection': [
                "invisible threads between figures",
                "separate pieces forming whole",
                "parallel lines converging at horizon"
            ],
            'being_becoming': [
                "caterpillar mid-transformation",
                "river reshaping landscape",
                "clay being molded continuously"
            ],
            'authenticity': [
                "masks falling away revealing face",
                "mirror showing true form",
                "layers peeling to reveal core"
            ],
            'absurdity': [
                "figure pushing boulder uphill eternally",
                "stairs leading nowhere",
                "clock with random moving hands"
            ],
            'transcendence': [
                "figure dissolving into light",
                "breaking through ceiling into cosmos",
                "chrysalis opening to infinity"
            ],
            'void': [
                "figure facing empty canvas",
                "echo in endless chamber",
                "shadow without source"
            ],
            'unity': [
                "droplets merging into ocean",
                "fragments assembling into whole",
                "individual notes becoming symphony"
            ],
            'duality': [
                "split-screen showing opposites",
                "figure with two shadows",
                "mirror showing different reflection"
            ],
            'alienation': [
                "figure behind frosted glass",
                "lone island in vast ocean",
                "crowd moving around still figure"
            ],
            'power': [
                "puppet master above stage",
                "pyramid with eye at apex",
                "giant shadow over small figures"
            ],
            'death': [
                "candle flame flickering out",
                "last leaf on autumn tree",
                "hourglass with final grains"
            ],
            'dharma': [
                "compass pointing true north",
                "river following its course",
                "wheel turning in harmony"
            ],
            'karma': [
                "ripples spreading from stone",
                "seeds growing into trees",
                "echo returning to source"
            ],
            'maya': [
                "veil obscuring reality",
                "mirror showing false reflections",
                "dream within a dream"
            ],
            'samsara': [
                "wheel endlessly turning",
                "waves rising and falling",
                "seasons in eternal cycle"
            ],
            'nirvana': [
                "candle flame extinguished",
                "drop merging with ocean",
                "boundaries dissolving"
            ],
            'tao': [
                "water finding its level",
                "path of least resistance",
                "dance without dancer"
            ],
            'emptiness': [
                "sky holding all clouds",
                "hollow flute making music",
                "space between thoughts"
            ],
            'mindfulness': [
                "still pond reflecting clearly",
                "flame unwavering in stillness",
                "eye of the storm"
            ],
            'impermanence': [
                "sand castle meeting tide",
                "clouds constantly reshaping",
                "flower blooming and fading"
            ],
            'non_duality': [
                "wave realizing it's ocean",
                "dreamer becoming the dream",
                "mirror and reflection as one"
            ],
            'compassion': [
                "sun shining on all equally",
                "mother embracing child",
                "rain nourishing all plants"
            ],
            'detachment': [
                "lotus unstained by mud",
                "bird leaving no trace in sky",
                "hand releasing held sand"
            ]
        }
        
        if concept.name in metaphors:
            return metaphors[concept.name][min(depth, len(metaphors[concept.name])-1)]
        
        return f"{concept.name} manifesting visually"
    
    def _detect_philosophical_schools(
        self,
        text: str,
        concepts: List[PhilosophicalConcept]
    ) -> List[Tuple[str, float]]:
        """Detect which philosophical schools are represented."""
        school_scores = defaultdict(float)
        concept_names = [c.name for c in concepts]
        
        for school_name, school_data in self.philosophical_schools.items():
            # Check for concept overlap
            concept_overlap = len(set(concept_names) & set(school_data['concepts']))
            if concept_overlap > 0:
                school_scores[school_name] += concept_overlap * 0.3
            
            # Check for school-specific keywords
            for keyword in school_data['keywords']:
                if keyword.lower() in text:
                    school_scores[school_name] += 0.2
            
            # Check for philosopher names
            for thinker in school_data['key_thinkers']:
                if thinker in text:
                    school_scores[school_name] += 0.3
        
        # Return schools with confidence scores
        detected_schools = [
            (school, score) for school, score in school_scores.items()
            if score > 0.2
        ]
        
        return sorted(detected_schools, key=lambda x: x[1], reverse=True)
    
    def _get_school_visual_mood(self, detected_schools: List[Tuple[str, float]]) -> str:
        """Get visual mood suggestions based on detected philosophical schools."""
        if not detected_schools:
            return "neutral philosophical atmosphere"
        
        # Get the primary school's visual mood
        primary_school = detected_schools[0][0]
        primary_mood = self.philosophical_schools[primary_school]['visual_mood']
        
        # If multiple schools detected, blend their moods
        if len(detected_schools) > 1:
            secondary_school = detected_schools[1][0]
            secondary_mood = self.philosophical_schools[secondary_school]['visual_mood']
            return f"{primary_mood}, with elements of {secondary_mood}"
        
        return primary_mood