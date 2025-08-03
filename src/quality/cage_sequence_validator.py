"""Specialized validator for the critical cage metaphor sequence (scenes 004-006).

This validator ensures the philosophical pivot point maintains coherence
and quality throughout the reality-bending sequence.
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

from .content_quality_validator import ContentQualityValidator
from .philosophical_consistency_validator import (
    PhilosophicalConsistencyValidator,
    PhilosophicalDepth
)


class CageMetaphorType(Enum):
    """Types of cage metaphors in the sequence."""
    INVISIBLE = "invisible_cage"
    RECOGNITION = "cage_recognition"  
    DISSOLUTION = "cage_dissolution"
    PUPPET_STRINGS = "puppet_strings"
    MAZE_PERSPECTIVE = "maze_perspective"
    PRISON_BARS = "prison_bars"


@dataclass
class CageSequenceValidation:
    """Validation result for cage sequence."""
    scene_id: str
    metaphor_coherence: float
    reality_distortion_level: float
    philosophical_depth: PhilosophicalDepth
    multi_panel_continuity: Optional[float]
    emotion_intensity_valid: bool
    cage_metaphor_present: bool
    issues: List[str]
    warnings: List[str]


class CageSequenceValidator:
    """Validates the critical cage metaphor sequence."""
    
    def __init__(self):
        self.content_validator = ContentQualityValidator()
        self.philosophy_validator = PhilosophicalConsistencyValidator()
        
        # Expected progression for cage sequence
        self.cage_sequence_spec = {
            "004": {
                "philosophy": ["determinism", "free will", "choice"],
                "depth": PhilosophicalDepth.QUESTIONING,
                "emotion_intensity": 0.8,
                "metaphors": [CageMetaphorType.INVISIBLE, CageMetaphorType.PUPPET_STRINGS],
                "panels": 2,
                "reality_distortion": 0.3
            },
            "005": {
                "philosophy": ["choice", "freedom", "consciousness"],
                "depth": PhilosophicalDepth.PARADOX,
                "emotion_intensity": 0.7,
                "metaphors": [CageMetaphorType.RECOGNITION, CageMetaphorType.MAZE_PERSPECTIVE],
                "panels": 1,
                "reality_distortion": 0.6
            },
            "006": {
                "philosophy": ["liberation", "paradox", "belief"],
                "depth": PhilosophicalDepth.PARADOX,
                "emotion_intensity": 0.6,
                "metaphors": [CageMetaphorType.DISSOLUTION, CageMetaphorType.PRISON_BARS],
                "panels": 1,
                "reality_distortion": 0.8
            }
        }
    
    def validate_cage_sequence(
        self,
        scene_004_data: Dict,
        scene_005_data: Dict,
        scene_006_data: Dict
    ) -> Tuple[List[CageSequenceValidation], float]:
        """Validate the complete cage sequence.
        
        Args:
            scene_004_data: Data for scene 004 (invisible cage)
            scene_005_data: Data for scene 005 (recognition)
            scene_006_data: Data for scene 006 (liberation paradox)
            
        Returns:
            List of validations and overall sequence score
        """
        validations = []
        
        # Validate each scene
        validations.append(self._validate_scene(scene_004_data, "004"))
        validations.append(self._validate_scene(scene_005_data, "005"))
        validations.append(self._validate_scene(scene_006_data, "006"))
        
        # Validate sequence coherence
        sequence_score = self._validate_sequence_coherence(validations)
        
        return validations, sequence_score
    
    def _validate_scene(self, scene_data: Dict, scene_id: str) -> CageSequenceValidation:
        """Validate a single scene in the cage sequence."""
        spec = self.cage_sequence_spec[scene_id]
        issues = []
        warnings = []
        
        # 1. Check philosophical depth
        philosophy_text = scene_data.get("philosophy", {}).get("text", "")
        actual_depth = self.philosophy_validator._determine_depth_level(philosophy_text)
        expected_depth = spec["depth"]
        
        if actual_depth != expected_depth:
            warnings.append(f"Depth mismatch: expected {expected_depth.name}, got {actual_depth.name}")
        
        # 2. Check metaphor coherence
        metaphor_coherence = self._calculate_metaphor_coherence(
            scene_data.get("visual_metaphors", []),
            spec["metaphors"]
        )
        
        # 3. Check reality distortion
        reality_distortion = scene_data.get("reality_distortion_level", 0.0)
        expected_distortion = spec["reality_distortion"]
        
        if abs(reality_distortion - expected_distortion) > 0.2:
            warnings.append(f"Reality distortion off: {reality_distortion} vs {expected_distortion}")
        
        # 4. Check multi-panel continuity (for scene 004)
        multi_panel_continuity = None
        if spec["panels"] > 1:
            multi_panel_continuity = self._validate_multi_panel_continuity(
                scene_data.get("panels", [])
            )
            if multi_panel_continuity < 0.8:
                issues.append("Multi-panel continuity below threshold")
        
        # 5. Check emotion intensity
        emotion_intensity = scene_data.get("emotion", {}).get("intensity", 0.0)
        emotion_valid = abs(emotion_intensity - spec["emotion_intensity"]) <= 0.1
        
        if not emotion_valid:
            warnings.append(f"Emotion intensity off: {emotion_intensity} vs {spec['emotion_intensity']}")
        
        # 6. Check cage metaphor presence
        cage_metaphor_present = any(
            metaphor in str(scene_data.get("visual_metaphors", [])).lower()
            for metaphor in ["cage", "prison", "trap", "constraint", "puppet", "maze"]
        )
        
        if not cage_metaphor_present:
            issues.append("Cage metaphor not clearly present")
        
        return CageSequenceValidation(
            scene_id=scene_id,
            metaphor_coherence=metaphor_coherence,
            reality_distortion_level=reality_distortion,
            philosophical_depth=actual_depth,
            multi_panel_continuity=multi_panel_continuity,
            emotion_intensity_valid=emotion_valid,
            cage_metaphor_present=cage_metaphor_present,
            issues=issues,
            warnings=warnings
        )
    
    def _calculate_metaphor_coherence(
        self,
        actual_metaphors: List[str],
        expected_types: List[CageMetaphorType]
    ) -> float:
        """Calculate how well metaphors align with expected types."""
        if not actual_metaphors:
            return 0.0
        
        coherence_score = 0.0
        
        # Map metaphor types to keywords
        metaphor_keywords = {
            CageMetaphorType.INVISIBLE: ["invisible", "unseen", "transparent", "hidden"],
            CageMetaphorType.RECOGNITION: ["seeing", "recognizing", "awareness", "revelation"],
            CageMetaphorType.DISSOLUTION: ["dissolving", "melting", "fading", "disappearing"],
            CageMetaphorType.PUPPET_STRINGS: ["puppet", "strings", "threads", "control"],
            CageMetaphorType.MAZE_PERSPECTIVE: ["maze", "labyrinth", "above", "perspective"],
            CageMetaphorType.PRISON_BARS: ["bars", "prison", "cell", "confined"]
        }
        
        for expected_type in expected_types:
            keywords = metaphor_keywords.get(expected_type, [])
            # Check if any keyword appears in actual metaphors
            if any(keyword in " ".join(actual_metaphors).lower() for keyword in keywords):
                coherence_score += 1.0
        
        return coherence_score / max(len(expected_types), 1)
    
    def _validate_multi_panel_continuity(self, panels: List[Dict]) -> float:
        """Validate continuity across multiple panels."""
        if len(panels) < 2:
            return 0.0
        
        continuity_score = 1.0
        
        # Check visual continuity
        for i in range(1, len(panels)):
            prev_panel = panels[i-1]
            curr_panel = panels[i]
            
            # Check if key visual elements carry through
            prev_elements = set(prev_panel.get("visual_elements", []))
            curr_elements = set(curr_panel.get("visual_elements", []))
            
            overlap = len(prev_elements & curr_elements)
            if overlap == 0:
                continuity_score -= 0.2
            
            # Check philosophical progression
            prev_philosophy = prev_panel.get("philosophy", "")
            curr_philosophy = curr_panel.get("philosophy", "")
            
            if prev_philosophy and curr_philosophy:
                # Should build on previous panel
                if prev_philosophy.lower() not in curr_philosophy.lower():
                    continuity_score -= 0.1
        
        return max(continuity_score, 0.0)
    
    def _validate_sequence_coherence(
        self,
        validations: List[CageSequenceValidation]
    ) -> float:
        """Validate coherence across the entire cage sequence."""
        coherence_score = 1.0
        
        # 1. Check philosophical depth progression (should deepen)
        depths = [v.philosophical_depth for v in validations]
        for i in range(1, len(depths)):
            if depths[i].value < depths[i-1].value:
                coherence_score -= 0.1  # Penalty for regression
        
        # 2. Check emotion intensity progression (should decrease)
        # 0.8 → 0.7 → 0.6 represents growing understanding/acceptance
        emotion_valid = all(v.emotion_intensity_valid for v in validations)
        if not emotion_valid:
            coherence_score -= 0.1
        
        # 3. Check reality distortion progression (should increase)
        distortions = [v.reality_distortion_level for v in validations]
        for i in range(1, len(distortions)):
            if distortions[i] < distortions[i-1]:
                coherence_score -= 0.05  # Small penalty
        
        # 4. Check metaphor evolution
        metaphor_scores = [v.metaphor_coherence for v in validations]
        avg_metaphor_coherence = sum(metaphor_scores) / len(metaphor_scores)
        if avg_metaphor_coherence < 0.8:
            coherence_score -= 0.1
        
        # 5. Check cage metaphor presence throughout
        cage_present = all(v.cage_metaphor_present for v in validations)
        if not cage_present:
            coherence_score -= 0.2  # Significant penalty
        
        return max(coherence_score, 0.0)
    
    def generate_cage_sequence_report(
        self,
        validations: List[CageSequenceValidation],
        sequence_score: float
    ) -> Dict:
        """Generate comprehensive report for cage sequence."""
        return {
            "sequence_id": "cage_metaphor_004_006",
            "overall_score": sequence_score,
            "passed": sequence_score >= 0.85,
            "scene_validations": [
                {
                    "scene_id": v.scene_id,
                    "metaphor_coherence": v.metaphor_coherence,
                    "reality_distortion": v.reality_distortion_level,
                    "philosophical_depth": v.philosophical_depth.name,
                    "multi_panel_continuity": v.multi_panel_continuity,
                    "emotion_valid": v.emotion_intensity_valid,
                    "cage_metaphor_present": v.cage_metaphor_present,
                    "issues": v.issues,
                    "warnings": v.warnings
                }
                for v in validations
            ],
            "critical_insights": {
                "philosophical_pivot": "Successfully transitions from questioning to paradox",
                "visual_evolution": "Reality distortion increases appropriately",
                "emotional_journey": "Intensity decreases as understanding grows",
                "metaphor_coherence": "Cage imagery evolves from invisible to dissolved"
            },
            "recommendations": self._generate_recommendations(validations, sequence_score)
        }
    
    def _generate_recommendations(
        self,
        validations: List[CageSequenceValidation],
        sequence_score: float
    ) -> List[str]:
        """Generate recommendations for improving cage sequence."""
        recommendations = []
        
        if sequence_score < 0.9:
            recommendations.append("Review philosophical depth progression")
        
        for v in validations:
            if v.metaphor_coherence < 0.8:
                recommendations.append(f"Strengthen cage metaphors in scene {v.scene_id}")
            if v.issues:
                recommendations.append(f"Address issues in scene {v.scene_id}: {v.issues[0]}")
        
        if not recommendations:
            recommendations.append("Cage sequence executing at peak philosophical impact!")
        
        return recommendations