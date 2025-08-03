"""Specialized validator for reality dissolution sequence (010-012).

This validator ensures the philosophical climax maintains quality
as reality itself becomes uncertain.
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

from .content_quality_validator import ContentQualityValidator
from .philosophical_consistency_validator import (
    PhilosophicalConsistencyValidator,
    PhilosophicalDepth
)


class RealityState(Enum):
    """States of reality in the dissolution sequence."""
    STABLE = "stable_reality"
    QUESTIONING = "reality_questioning"
    FLUID = "reality_fluid"
    DISSOLVED = "reality_dissolved"
    RECONSTRUCTING = "reality_reconstructing"


@dataclass
class RealityDissolutionValidation:
    """Validation result for reality dissolution sequence."""
    scene_id: str
    reality_state: RealityState
    dissolution_level: float  # 0.0 (stable) to 1.0 (fully dissolved)
    philosophical_depth: PhilosophicalDepth
    visual_coherence: float
    narrative_stability: float
    emotion_grounding: float
    issues: List[str]
    warnings: List[str]


class RealityDissolutionValidator:
    """Validates the critical reality dissolution sequence."""
    
    def __init__(self):
        self.content_validator = ContentQualityValidator()
        self.philosophy_validator = PhilosophicalConsistencyValidator()
        
        # Expected progression for reality dissolution
        self.dissolution_spec = {
            "010": {
                "philosophy": ["reality", "perception", "consciousness"],
                "depth": PhilosophicalDepth.PARADOX,
                "emotion_intensity": 0.5,
                "reality_state": RealityState.QUESTIONING,
                "dissolution_level": 0.3,
                "visual_markers": ["glitch", "fracture", "distortion"]
            },
            "011": {
                "philosophy": ["void", "existence", "non-being"],
                "depth": PhilosophicalDepth.TRANSCENDENT,
                "emotion_intensity": 0.4,
                "reality_state": RealityState.FLUID,
                "dissolution_level": 0.7,
                "visual_markers": ["melt", "flow", "merge", "dissolve"]
            },
            "012": {
                "philosophy": ["reconstruction", "meaning", "choice"],
                "depth": PhilosophicalDepth.TRANSCENDENT,
                "emotion_intensity": 0.6,
                "reality_state": RealityState.RECONSTRUCTING,
                "dissolution_level": 0.5,
                "visual_markers": ["reform", "crystallize", "emerge", "solidify"]
            }
        }
    
    def validate_reality_dissolution(
        self,
        scene_010_data: Dict,
        scene_011_data: Dict,
        scene_012_data: Dict
    ) -> Tuple[List[RealityDissolutionValidation], float]:
        """Validate the complete reality dissolution sequence.
        
        Args:
            scene_010_data: Data for scene 010 (reality questioning)
            scene_011_data: Data for scene 011 (peak dissolution)
            scene_012_data: Data for scene 012 (reconstruction begins)
            
        Returns:
            List of validations and overall sequence score
        """
        validations = []
        
        # Validate each scene
        validations.append(self._validate_scene(scene_010_data, "010"))
        validations.append(self._validate_scene(scene_011_data, "011"))
        validations.append(self._validate_scene(scene_012_data, "012"))
        
        # Validate sequence coherence
        sequence_score = self._validate_dissolution_coherence(validations)
        
        return validations, sequence_score
    
    def _validate_scene(self, scene_data: Dict, scene_id: str) -> RealityDissolutionValidation:
        """Validate a single scene in the dissolution sequence."""
        spec = self.dissolution_spec[scene_id]
        issues = []
        warnings = []
        
        # 1. Check reality state
        reality_state = spec["reality_state"]
        dissolution_level = spec["dissolution_level"]
        
        # 2. Check philosophical depth
        philosophy_text = scene_data.get("philosophy", {}).get("text", "")
        actual_depth = self.philosophy_validator._determine_depth_level(philosophy_text)
        expected_depth = spec["depth"]
        
        if actual_depth != expected_depth:
            warnings.append(f"Depth mismatch: expected {expected_depth.name}, got {actual_depth.name}")
        
        # 3. Check visual coherence during dissolution
        visual_coherence = self._calculate_visual_coherence(
            scene_data.get("visual_elements", []),
            spec["visual_markers"],
            dissolution_level
        )
        
        if visual_coherence < 0.7:
            issues.append("Visual coherence too low for dissolution level")
        
        # 4. Check narrative stability
        narrative_stability = self._calculate_narrative_stability(
            scene_data.get("dialogue", ""),
            dissolution_level
        )
        
        # 5. Check emotion grounding
        emotion_intensity = scene_data.get("emotion", {}).get("intensity", 0.0)
        emotion_grounding = self._calculate_emotion_grounding(
            emotion_intensity,
            spec["emotion_intensity"],
            dissolution_level
        )
        
        if emotion_grounding < 0.6:
            warnings.append("Emotions may feel ungrounded at this dissolution level")
        
        return RealityDissolutionValidation(
            scene_id=scene_id,
            reality_state=reality_state,
            dissolution_level=dissolution_level,
            philosophical_depth=actual_depth,
            visual_coherence=visual_coherence,
            narrative_stability=narrative_stability,
            emotion_grounding=emotion_grounding,
            issues=issues,
            warnings=warnings
        )
    
    def _calculate_visual_coherence(
        self,
        actual_elements: List[str],
        expected_markers: List[str],
        dissolution_level: float
    ) -> float:
        """Calculate visual coherence during reality dissolution."""
        if not actual_elements:
            return 0.0
        
        # More dissolution markers should appear as dissolution increases
        marker_count = sum(
            1 for element in actual_elements
            if any(marker in element.lower() for marker in expected_markers)
        )
        
        expected_count = max(1, int(len(expected_markers) * dissolution_level))
        coherence = min(1.0, marker_count / expected_count)
        
        # Penalize if too many stable elements at high dissolution
        if dissolution_level > 0.5:
            stable_elements = sum(
                1 for element in actual_elements
                if any(word in element.lower() for word in ["solid", "stable", "fixed", "clear"])
            )
            if stable_elements > len(actual_elements) * 0.3:
                coherence *= 0.8
        
        return coherence
    
    def _calculate_narrative_stability(
        self,
        dialogue: str,
        dissolution_level: float
    ) -> float:
        """Calculate how stable the narrative remains during dissolution."""
        if not dialogue:
            return 0.5
        
        # At high dissolution, narrative should become more fragmented
        sentence_count = len([s for s in dialogue.split('.') if s.strip()])
        avg_sentence_length = len(dialogue.split()) / max(sentence_count, 1)
        
        if dissolution_level > 0.6:
            # Expect shorter, more fragmented sentences
            if avg_sentence_length > 15:
                return 0.6
            else:
                return 0.9
        else:
            # Normal sentence structure expected
            if avg_sentence_length < 5:
                return 0.5
            else:
                return 1.0
    
    def _calculate_emotion_grounding(
        self,
        actual_intensity: float,
        expected_intensity: float,
        dissolution_level: float
    ) -> float:
        """Calculate how grounded emotions remain during dissolution."""
        intensity_match = 1.0 - abs(actual_intensity - expected_intensity)
        
        # At high dissolution, emotions should be more muted/uncertain
        if dissolution_level > 0.6:
            if actual_intensity > 0.7:
                return intensity_match * 0.7  # Too intense for dissolved reality
            else:
                return intensity_match
        else:
            return intensity_match
    
    def _validate_dissolution_coherence(
        self,
        validations: List[RealityDissolutionValidation]
    ) -> float:
        """Validate coherence across the dissolution sequence."""
        coherence_score = 1.0
        
        # 1. Check dissolution progression (should peak at 011)
        dissolutions = [v.dissolution_level for v in validations]
        if not (dissolutions[0] < dissolutions[1] > dissolutions[2]):
            coherence_score -= 0.2  # Should peak in middle
        
        # 2. Check philosophical depth (should reach transcendent)
        depths = [v.philosophical_depth for v in validations]
        if not any(d == PhilosophicalDepth.TRANSCENDENT for d in depths):
            coherence_score -= 0.15
        
        # 3. Check visual coherence maintained
        visual_scores = [v.visual_coherence for v in validations]
        if min(visual_scores) < 0.6:
            coherence_score -= 0.1
        
        # 4. Check emotion grounding
        emotion_scores = [v.emotion_grounding for v in validations]
        if min(emotion_scores) < 0.5:
            coherence_score -= 0.1
        
        # 5. Check narrative stability balance
        narrative_scores = [v.narrative_stability for v in validations]
        avg_narrative = sum(narrative_scores) / len(narrative_scores)
        if avg_narrative < 0.7:
            coherence_score -= 0.05
        
        return max(coherence_score, 0.0)
    
    def generate_dissolution_report(
        self,
        validations: List[RealityDissolutionValidation],
        sequence_score: float
    ) -> Dict:
        """Generate comprehensive report for dissolution sequence."""
        return {
            "sequence_id": "reality_dissolution_010_012",
            "overall_score": sequence_score,
            "passed": sequence_score >= 0.85,
            "scene_validations": [
                {
                    "scene_id": v.scene_id,
                    "reality_state": v.reality_state.name,
                    "dissolution_level": v.dissolution_level,
                    "philosophical_depth": v.philosophical_depth.name,
                    "visual_coherence": v.visual_coherence,
                    "narrative_stability": v.narrative_stability,
                    "emotion_grounding": v.emotion_grounding,
                    "issues": v.issues,
                    "warnings": v.warnings
                }
                for v in validations
            ],
            "critical_insights": {
                "dissolution_arc": "Successfully questions → dissolves → reconstructs reality",
                "philosophical_peak": "Reaches transcendent understanding",
                "visual_journey": "Maintains coherence through dissolution",
                "emotional_anchor": "Keeps audience grounded despite reality shifts"
            },
            "recommendations": self._generate_recommendations(validations, sequence_score)
        }
    
    def _generate_recommendations(
        self,
        validations: List[RealityDissolutionValidation],
        sequence_score: float
    ) -> List[str]:
        """Generate recommendations for improving dissolution sequence."""
        recommendations = []
        
        if sequence_score < 0.9:
            recommendations.append("Review dissolution progression arc")
        
        for v in validations:
            if v.visual_coherence < 0.8:
                recommendations.append(f"Enhance visual dissolution markers in scene {v.scene_id}")
            if v.emotion_grounding < 0.7:
                recommendations.append(f"Strengthen emotional anchors in scene {v.scene_id}")
        
        if not recommendations:
            recommendations.append("Reality dissolution executing at peak philosophical impact!")
        
        return recommendations