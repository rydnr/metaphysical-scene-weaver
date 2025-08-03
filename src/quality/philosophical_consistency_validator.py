"""Philosophical consistency validation based on Sophia's concept framework.

Validates philosophical concepts, depth levels, and evolution tracking.
"""

from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass
from enum import Enum
import re


class PhilosophicalDepth(Enum):
    """Depth levels for philosophical understanding."""
    SURFACE = 1  # Surface understanding
    QUESTIONING = 2  # Questioning/exploring
    PARADOX = 3  # Paradox/meta-level
    TRANSCENDENT = 4  # Transcendent/ineffable


class PhilosophicalSchool(Enum):
    """Philosophical schools/traditions."""
    METAPHYSICS = "metaphysics"
    ETHICS = "ethics"
    ONTOLOGY = "ontology"
    EXISTENTIALISM = "existentialism"
    PROCESS_PHILOSOPHY = "process_philosophy"
    PHENOMENOLOGY = "phenomenology"


@dataclass
class ConceptValidation:
    """Result of concept validation."""
    concept: str
    present: bool
    frequency: int
    depth_level: PhilosophicalDepth
    school: PhilosophicalSchool
    evolution_score: float
    coherence_issues: List[str]


class PhilosophicalConsistencyValidator:
    """Validates philosophical consistency based on Sophia's framework."""
    
    # Core concepts from Sophia
    CORE_CONCEPTS = {
        "consciousness": PhilosophicalSchool.METAPHYSICS,
        "freedom": PhilosophicalSchool.ETHICS,
        "existence": PhilosophicalSchool.ONTOLOGY,
        "authenticity": PhilosophicalSchool.EXISTENTIALISM,
        "liminality": PhilosophicalSchool.PROCESS_PHILOSOPHY,
        "reality dissolution": PhilosophicalSchool.PHENOMENOLOGY
    }
    
    # Depth indicators for each level
    DEPTH_INDICATORS = {
        PhilosophicalDepth.SURFACE: [
            "what is", "seems", "appears", "might be", "perhaps"
        ],
        PhilosophicalDepth.QUESTIONING: [
            "but why", "how can", "what if", "questioning", "exploring"
        ],
        PhilosophicalDepth.PARADOX: [
            "both and neither", "paradox", "contradiction", "meta", "recursive"
        ],
        PhilosophicalDepth.TRANSCENDENT: [
            "ineffable", "beyond", "transcends", "dissolves", "becomes"
        ]
    }
    
    # Character depth progression expectations
    CHARACTER_DEPTH_PROGRESSION = {
        "Evan": [PhilosophicalDepth.SURFACE, PhilosophicalDepth.QUESTIONING, 
                PhilosophicalDepth.PARADOX],
        "Monday": [PhilosophicalDepth.QUESTIONING, PhilosophicalDepth.PARADOX, 
                  PhilosophicalDepth.TRANSCENDENT],
        "Valerie": [PhilosophicalDepth.PARADOX, PhilosophicalDepth.TRANSCENDENT]
    }
    
    def validate_concepts(
        self,
        text: str,
        expected_concepts: Optional[List[str]] = None
    ) -> Dict[str, ConceptValidation]:
        """Validate presence and usage of philosophical concepts.
        
        Args:
            text: Text to analyze
            expected_concepts: Specific concepts to check for
            
        Returns:
            Dictionary of concept validations
        """
        validations = {}
        concepts_to_check = expected_concepts or list(self.CORE_CONCEPTS.keys())
        
        for concept in concepts_to_check:
            validation = self._validate_single_concept(text, concept)
            validations[concept] = validation
        
        return validations
    
    def _validate_single_concept(self, text: str, concept: str) -> ConceptValidation:
        """Validate a single philosophical concept."""
        text_lower = text.lower()
        
        # Check presence and frequency
        # Handle multi-word concepts
        if " " in concept:
            pattern = concept.lower()
            frequency = text_lower.count(pattern)
        else:
            pattern = r'\b' + concept.lower() + r'\b'
            frequency = len(re.findall(pattern, text_lower))
        
        present = frequency > 0
        
        # Determine depth level
        depth_level = self._determine_depth_level(text)
        
        # Get philosophical school
        school = self.CORE_CONCEPTS.get(concept, PhilosophicalSchool.METAPHYSICS)
        
        # Calculate evolution score (simplified - would integrate with concept_networks.py)
        evolution_score = self._calculate_evolution_score(concept, text)
        
        # Check for coherence issues
        coherence_issues = self._check_coherence(concept, text, school)
        
        return ConceptValidation(
            concept=concept,
            present=present,
            frequency=frequency,
            depth_level=depth_level,
            school=school,
            evolution_score=evolution_score,
            coherence_issues=coherence_issues
        )
    
    def _determine_depth_level(self, text: str) -> PhilosophicalDepth:
        """Determine the philosophical depth level of text."""
        text_lower = text.lower()
        
        # Check from highest to lowest depth
        for depth in reversed(list(PhilosophicalDepth)):
            indicators = self.DEPTH_INDICATORS.get(depth, [])
            if any(indicator in text_lower for indicator in indicators):
                return depth
        
        return PhilosophicalDepth.SURFACE
    
    def _calculate_evolution_score(self, concept: str, text: str) -> float:
        """Calculate how well a concept evolves in the text."""
        # Simplified version - would integrate with Sophia's concept_networks.py
        # Check for concept development indicators
        development_indicators = [
            f"if {concept}",
            f"{concept} means",
            f"{concept} becomes",
            f"beyond {concept}",
            f"{concept} transforms"
        ]
        
        score = 0.0
        text_lower = text.lower()
        for indicator in development_indicators:
            if indicator in text_lower:
                score += 0.2
        
        return min(score, 1.0)
    
    def _check_coherence(
        self,
        concept: str,
        text: str,
        school: PhilosophicalSchool
    ) -> List[str]:
        """Check for philosophical coherence issues."""
        issues = []
        
        # Check for conflicting schools
        conflicting_patterns = {
            PhilosophicalSchool.EXISTENTIALISM: ["predetermined", "fate", "destiny"],
            PhilosophicalSchool.PHENOMENOLOGY: ["objective reality", "absolute truth"],
            PhilosophicalSchool.PROCESS_PHILOSOPHY: ["static", "unchanging", "fixed"]
        }
        
        if school in conflicting_patterns:
            conflicts = conflicting_patterns[school]
            text_lower = text.lower()
            for conflict in conflicts:
                if conflict in text_lower:
                    issues.append(f"Potential conflict: '{conflict}' contradicts {school.value}")
        
        return issues
    
    def validate_character_depth_progression(
        self,
        character_entries: List[Dict[str, str]]
    ) -> Dict[str, List[PhilosophicalDepth]]:
        """Validate that character philosophical depth progresses appropriately.
        
        Args:
            character_entries: List of entries with 'speaker' and 'dialogue'
            
        Returns:
            Character depth progression tracking
        """
        character_depths = {}
        
        for entry in character_entries:
            speaker = entry.get("speaker", "Unknown")
            dialogue = entry.get("dialogue", "")
            
            if speaker not in character_depths:
                character_depths[speaker] = []
            
            depth = self._determine_depth_level(dialogue)
            character_depths[speaker].append(depth)
        
        return character_depths
    
    def validate_depth_progression_quality(
        self,
        character_depths: Dict[str, List[PhilosophicalDepth]]
    ) -> Dict[str, float]:
        """Score how well characters follow expected depth progression.
        
        Args:
            character_depths: Depth progression by character
            
        Returns:
            Quality scores per character (0-1)
        """
        scores = {}
        
        for character, depths in character_depths.items():
            if character not in self.CHARACTER_DEPTH_PROGRESSION:
                scores[character] = 0.5  # Unknown character, neutral score
                continue
            
            expected_progression = self.CHARACTER_DEPTH_PROGRESSION[character]
            
            # Score based on alignment with expected progression
            score = 0.0
            for i, depth in enumerate(depths):
                # Characters should generally increase or maintain depth
                if i > 0:
                    if depth.value >= depths[i-1].value:
                        score += 0.2
                    else:
                        score += 0.1  # Small penalty for regression
                
                # Check if depth aligns with character expectations
                if depth in expected_progression:
                    score += 0.3
            
            scores[character] = min(score / max(len(depths), 1), 1.0)
        
        return scores
    
    def validate_metaphor_concept_alignment(
        self,
        metaphors: List[str],
        concepts: List[str]
    ) -> float:
        """Validate alignment between metaphors and philosophical concepts.
        
        Args:
            metaphors: List of metaphors used
            concepts: List of philosophical concepts
            
        Returns:
            Alignment score (0-1)
        """
        # Concept-metaphor mappings
        concept_metaphor_map = {
            "consciousness": ["river", "ocean", "mirror", "dream", "awakening"],
            "freedom": ["cage", "chains", "flight", "open sky", "choice"],
            "existence": ["being", "void", "presence", "absence", "manifestation"],
            "authenticity": ["mask", "true face", "genuine", "pretense", "real"],
            "liminality": ["threshold", "between", "edge", "boundary", "transition"],
            "reality dissolution": ["ripple", "dissolve", "melt", "fade", "shimmer"]
        }
        
        alignment_score = 0.0
        total_checks = 0
        
        for concept in concepts:
            if concept.lower() in concept_metaphor_map:
                expected_metaphors = concept_metaphor_map[concept.lower()]
                for metaphor in metaphors:
                    total_checks += 1
                    if any(exp in metaphor.lower() for exp in expected_metaphors):
                        alignment_score += 1.0
        
        return alignment_score / max(total_checks, 1)