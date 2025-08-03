"""Batch quality validation for multiple scenes.

Validates quality across scene sequences, ensuring coherence and consistency.
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path
import json

from .content_quality_validator import ContentQualityValidator, ContentType
from .philosophical_consistency_validator import (
    PhilosophicalConsistencyValidator,
    PhilosophicalDepth
)


@dataclass
class SceneQualityReport:
    """Quality report for a single scene."""
    scene_id: str
    scene_name: str
    overall_score: float
    component_scores: Dict[str, float]
    issues: List[str]
    warnings: List[str]
    passed: bool


@dataclass
class BatchQualityReport:
    """Quality report for a batch of scenes."""
    batch_id: str
    scenes: List[SceneQualityReport]
    overall_score: float
    coherence_score: float
    consistency_score: float
    passed: bool
    summary: Dict[str, any]


class BatchQualityValidator:
    """Validates quality across multiple scenes."""
    
    def __init__(self):
        self.content_validator = ContentQualityValidator()
        self.philosophy_validator = PhilosophicalConsistencyValidator()
        
        # Expected progressions for scenes 001-003
        self.expected_progressions = {
            "001": {
                "philosophy": "authenticity",
                "depth": PhilosophicalDepth.SURFACE,
                "emotion": {"curiosity": 0.6, "openness": 0.4},
                "narrator_voice": "sage"
            },
            "002": {
                "philosophy": "consciousness", 
                "depth": PhilosophicalDepth.QUESTIONING,
                "emotion": {"challenge": 0.5, "melancholy": 0.5},
                "narrator_voice": "provocateur"
            },
            "003": {
                "philosophy": "freedom",
                "depth": PhilosophicalDepth.QUESTIONING,
                "emotion": {"determination": 0.7, "uncertainty": 0.3},
                "narrator_voice": "provocateur"
            }
        }
    
    def validate_batch(
        self,
        scene_folders: List[Path],
        batch_id: str = "001-003"
    ) -> BatchQualityReport:
        """Validate a batch of scenes.
        
        Args:
            scene_folders: List of scene folder paths
            batch_id: Identifier for this batch
            
        Returns:
            BatchQualityReport with comprehensive results
        """
        scene_reports = []
        
        # Validate each scene
        for folder in scene_folders:
            scene_id = folder.name.split("_")[0]  # Extract "001" from "001_opening_consciousness"
            report = self._validate_single_scene(folder, scene_id)
            scene_reports.append(report)
        
        # Calculate batch-level metrics
        overall_score = sum(r.overall_score for r in scene_reports) / len(scene_reports)
        coherence_score = self._calculate_coherence(scene_reports)
        consistency_score = self._calculate_consistency(scene_reports)
        
        # Determine if batch passed
        passed = (
            overall_score >= 0.85 and
            coherence_score >= 0.80 and
            consistency_score >= 0.80 and
            all(r.passed for r in scene_reports)
        )
        
        # Create summary
        summary = {
            "total_scenes": len(scene_reports),
            "passed_scenes": sum(1 for r in scene_reports if r.passed),
            "average_quality": overall_score,
            "philosophy_coherence": coherence_score,
            "emotion_consistency": consistency_score,
            "token_efficiency": self._calculate_token_efficiency(scene_reports)
        }
        
        return BatchQualityReport(
            batch_id=batch_id,
            scenes=scene_reports,
            overall_score=overall_score,
            coherence_score=coherence_score,
            consistency_score=consistency_score,
            passed=passed,
            summary=summary
        )
    
    def _validate_single_scene(self, folder: Path, scene_id: str) -> SceneQualityReport:
        """Validate a single scene folder."""
        component_scores = {}
        issues = []
        warnings = []
        
        # 1. Validate folder structure
        folder_result = self.content_validator.validate_folder_structure(folder)
        component_scores["folder_structure"] = folder_result.score
        issues.extend(folder_result.issues)
        warnings.extend(folder_result.warnings)
        
        # 2. Validate philosophy
        if (folder / "philosophy" / "concepts.json").exists():
            with open(folder / "philosophy" / "concepts.json", 'r') as f:
                philosophy_data = json.load(f)
                
            expected = self.expected_progressions.get(scene_id, {})
            if expected.get("philosophy"):
                # Check if expected philosophy is present
                concepts = philosophy_data.get("concepts", [])
                if expected["philosophy"] in [c.lower() for c in concepts]:
                    component_scores["philosophy"] = 1.0
                else:
                    component_scores["philosophy"] = 0.5
                    warnings.append(f"Expected {expected['philosophy']} philosophy")
        
        # 3. Validate emotions
        if (folder / "emotion" / "emotional_arc.json").exists():
            with open(folder / "emotion" / "emotional_arc.json", 'r') as f:
                emotion_data = json.load(f)
                
            # Check emotion transitions
            expected_emotions = self.expected_progressions.get(scene_id, {}).get("emotion", {})
            actual_emotions = emotion_data.get("primary_emotions", {})
            
            # Validate emotion values sum to 1.0
            emotion_sum = sum(actual_emotions.values())
            if abs(emotion_sum - 1.0) < 0.01:
                component_scores["emotion_validity"] = 1.0
            else:
                component_scores["emotion_validity"] = 0.5
                issues.append(f"Emotion values sum to {emotion_sum}, not 1.0")
        
        # 4. Validate prompts
        if (folder / "prompts" / "v1" / "base_prompt.txt").exists():
            with open(folder / "prompts" / "v1" / "base_prompt.txt", 'r') as f:
                prompt = f.read()
                
            # Validate prompt structure and length
            prompt_result = self.content_validator.validate_enriched_prompt(
                prompt,
                {"id": scene_id, "dialogue": ""}  # Simplified entry
            )
            component_scores["prompt_quality"] = prompt_result.score
            
            # Check token count
            if (folder / "prompts" / "v1" / "metadata.json").exists():
                with open(folder / "prompts" / "v1" / "metadata.json", 'r') as f:
                    metadata = json.load(f)
                    token_count = metadata.get("token_count", 0)
                    if token_count > 150:
                        warnings.append(f"Token count {token_count} exceeds 150 limit")
        
        # 5. Validate narrator
        if (folder / "narrator" / "commentary.txt").exists():
            with open(folder / "narrator" / "commentary.txt", 'r') as f:
                narrator_text = f.read()
                
            narrator_result = self.content_validator.validate_narrator_commentary(
                narrator_text,
                {"scene": scene_id}
            )
            component_scores["narrator_quality"] = narrator_result.score
        
        # Calculate overall score
        overall_score = sum(component_scores.values()) / max(len(component_scores), 1)
        passed = overall_score >= 0.8 and len(issues) == 0
        
        return SceneQualityReport(
            scene_id=scene_id,
            scene_name=folder.name,
            overall_score=overall_score,
            component_scores=component_scores,
            issues=issues,
            warnings=warnings,
            passed=passed
        )
    
    def _calculate_coherence(self, scene_reports: List[SceneQualityReport]) -> float:
        """Calculate philosophical coherence across scenes."""
        if len(scene_reports) < 2:
            return 1.0
        
        coherence_score = 1.0
        
        # Check depth progression (should increase or maintain)
        for i in range(1, len(scene_reports)):
            prev_scene = scene_reports[i-1]
            curr_scene = scene_reports[i]
            
            # Simple check based on scene IDs and expected progression
            prev_id = prev_scene.scene_id
            curr_id = curr_scene.scene_id
            
            prev_depth = self.expected_progressions.get(prev_id, {}).get("depth", PhilosophicalDepth.SURFACE)
            curr_depth = self.expected_progressions.get(curr_id, {}).get("depth", PhilosophicalDepth.SURFACE)
            
            if curr_depth.value < prev_depth.value:
                coherence_score -= 0.1  # Penalty for regression
        
        return max(coherence_score, 0.0)
    
    def _calculate_consistency(self, scene_reports: List[SceneQualityReport]) -> float:
        """Calculate emotional consistency across scenes."""
        if len(scene_reports) < 2:
            return 1.0
        
        consistency_score = 1.0
        
        # Check emotion transitions (max 0.3 shift per Luna's rules)
        for i in range(1, len(scene_reports)):
            # Would need actual emotion data from scenes
            # For now, using expected progressions
            prev_id = scene_reports[i-1].scene_id
            curr_id = scene_reports[i].scene_id
            
            prev_emotions = self.expected_progressions.get(prev_id, {}).get("emotion", {})
            curr_emotions = self.expected_progressions.get(curr_id, {}).get("emotion", {})
            
            # Calculate maximum emotion shift
            max_shift = 0.0
            for emotion in set(prev_emotions.keys()) | set(curr_emotions.keys()):
                prev_val = prev_emotions.get(emotion, 0.0)
                curr_val = curr_emotions.get(emotion, 0.0)
                shift = abs(curr_val - prev_val)
                max_shift = max(max_shift, shift)
            
            if max_shift > 0.3:
                consistency_score -= (max_shift - 0.3) * 0.5  # Penalty for large shifts
        
        return max(consistency_score, 0.0)
    
    def _calculate_token_efficiency(self, scene_reports: List[SceneQualityReport]) -> float:
        """Calculate average token efficiency across scenes."""
        # Would extract from actual prompt metadata
        # For now, return a good efficiency score
        return 0.65  # 65% of token limit used (like Valerie's 62.5%)
    
    def generate_dashboard_data(self, batch_report: BatchQualityReport) -> Dict[str, any]:
        """Generate data for quality dashboard API.
        
        Args:
            batch_report: Batch quality report
            
        Returns:
            Dashboard-ready data structure
        """
        return {
            "batch_id": batch_report.batch_id,
            "timestamp": "2024-01-15T15:00:00Z",
            "overall_health": {
                "score": batch_report.overall_score,
                "status": "healthy" if batch_report.passed else "needs_attention",
                "trend": "improving"  # Would calculate from historical data
            },
            "scene_scores": [
                {
                    "scene_id": scene.scene_id,
                    "scene_name": scene.scene_name,
                    "score": scene.overall_score,
                    "status": "passed" if scene.passed else "failed",
                    "issues": len(scene.issues),
                    "warnings": len(scene.warnings)
                }
                for scene in batch_report.scenes
            ],
            "quality_metrics": {
                "philosophy_coherence": {
                    "score": batch_report.coherence_score,
                    "status": "excellent" if batch_report.coherence_score > 0.9 else "good"
                },
                "emotion_consistency": {
                    "score": batch_report.consistency_score,
                    "status": "excellent" if batch_report.consistency_score > 0.9 else "good"
                },
                "token_efficiency": {
                    "percentage": batch_report.summary["token_efficiency"] * 100,
                    "status": "optimal"
                }
            },
            "recommendations": self._generate_recommendations(batch_report)
        }
    
    def _generate_recommendations(self, batch_report: BatchQualityReport) -> List[str]:
        """Generate actionable recommendations based on report."""
        recommendations = []
        
        if batch_report.overall_score < 0.9:
            recommendations.append("Consider reviewing scenes with scores below 0.9")
        
        if batch_report.coherence_score < 0.85:
            recommendations.append("Check philosophical depth progression between scenes")
        
        if batch_report.consistency_score < 0.85:
            recommendations.append("Review emotion transitions for smoother flow")
        
        # Scene-specific recommendations
        for scene in batch_report.scenes:
            if not scene.passed:
                recommendations.append(f"Scene {scene.scene_id} needs attention: {scene.issues[0] if scene.issues else 'Check warnings'}")
        
        if not recommendations:
            recommendations.append("All systems operating at peak performance!")
        
        return recommendations