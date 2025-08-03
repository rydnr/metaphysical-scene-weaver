"""Prompt effectiveness metrics and A/B testing framework."""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import json
import logging
from collections import defaultdict
import statistics


@dataclass
class PromptMetrics:
    """Metrics for evaluating prompt effectiveness."""
    prompt_id: str
    prompt_text: str
    style: str
    optimization_level: str
    
    # Generation metrics
    generation_time: float = 0.0  # seconds
    token_count: int = 0
    
    # Quality metrics (0-1 scale)
    composition_score: float = 0.0
    style_adherence: float = 0.0
    detail_richness: float = 0.0
    emotional_accuracy: float = 0.0
    philosophical_depth: float = 0.0
    
    # User feedback
    user_rating: Optional[float] = None  # 1-5 scale
    user_notes: Optional[str] = None
    
    # Technical metrics
    model_confidence: float = 0.0
    error_count: int = 0
    
    # Calculated scores
    overall_score: float = field(init=False)
    efficiency_score: float = field(init=False)
    
    def __post_init__(self):
        # Calculate overall score
        quality_scores = [
            self.composition_score,
            self.style_adherence,
            self.detail_richness,
            self.emotional_accuracy,
            self.philosophical_depth
        ]
        self.overall_score = statistics.mean(quality_scores)
        
        # Calculate efficiency score (quality per token)
        if self.token_count > 0:
            self.efficiency_score = self.overall_score / (self.token_count / 100)
        else:
            self.efficiency_score = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary."""
        return {
            "prompt_id": self.prompt_id,
            "prompt_text": self.prompt_text,
            "style": self.style,
            "optimization_level": self.optimization_level,
            "generation_time": self.generation_time,
            "token_count": self.token_count,
            "quality_metrics": {
                "composition": self.composition_score,
                "style_adherence": self.style_adherence,
                "detail_richness": self.detail_richness,
                "emotional_accuracy": self.emotional_accuracy,
                "philosophical_depth": self.philosophical_depth,
                "overall": self.overall_score
            },
            "efficiency_score": self.efficiency_score,
            "user_feedback": {
                "rating": self.user_rating,
                "notes": self.user_notes
            },
            "technical": {
                "model_confidence": self.model_confidence,
                "error_count": self.error_count
            }
        }


class PromptAnalyzer:
    """Analyzes prompt characteristics and predicts effectiveness."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Component weights for scoring
        self.component_weights = {
            "subject_clarity": 0.25,
            "style_specification": 0.20,
            "composition_guidance": 0.15,
            "atmospheric_elements": 0.15,
            "technical_quality": 0.15,
            "uniqueness": 0.10
        }
        
        # Quality indicators
        self.quality_indicators = {
            "high_detail": ["detailed", "intricate", "elaborate", "complex"],
            "strong_composition": ["rule of thirds", "golden ratio", "balanced", "dynamic"],
            "clear_style": ["style", "aesthetic", "inspired by", "in the style of"],
            "atmosphere": ["mood", "atmosphere", "feeling", "ambiance"],
            "technical": ["8k", "high resolution", "professional", "masterpiece"]
        }
    
    def analyze_prompt(self, prompt: str) -> Dict[str, float]:
        """Analyze prompt characteristics and predict effectiveness."""
        scores = {}
        
        # Subject clarity (is the main subject well-defined?)
        scores["subject_clarity"] = self._score_subject_clarity(prompt)
        
        # Style specification
        scores["style_specification"] = self._score_style_specification(prompt)
        
        # Composition guidance
        scores["composition_guidance"] = self._score_composition(prompt)
        
        # Atmospheric elements
        scores["atmospheric_elements"] = self._score_atmosphere(prompt)
        
        # Technical quality markers
        scores["technical_quality"] = self._score_technical_quality(prompt)
        
        # Uniqueness/creativity
        scores["uniqueness"] = self._score_uniqueness(prompt)
        
        # Calculate weighted overall score
        overall = sum(
            score * self.component_weights[component]
            for component, score in scores.items()
        )
        scores["predicted_effectiveness"] = overall
        
        return scores
    
    def _score_subject_clarity(self, prompt: str) -> float:
        """Score how clearly the main subject is defined."""
        # Check for character/subject description
        subject_indicators = [
            "character", "person", "figure", "protagonist",
            "creature", "object", "landscape", "scene"
        ]
        
        score = 0.0
        prompt_lower = prompt.lower()
        
        # Check for subject indicators
        for indicator in subject_indicators:
            if indicator in prompt_lower:
                score += 0.3
                break
        
        # Check for descriptive adjectives before nouns
        import re
        adj_noun_pattern = r'\b(\w+ing|\w+ed|\w+ful|\w+ous)\s+\w+\b'
        matches = re.findall(adj_noun_pattern, prompt_lower)
        score += min(len(matches) * 0.1, 0.4)
        
        # Check for specific vs generic
        if any(word in prompt_lower for word in ["specific", "particular", "exact"]):
            score += 0.3
        
        return min(score, 1.0)
    
    def _score_style_specification(self, prompt: str) -> float:
        """Score how well the artistic style is specified."""
        score = 0.0
        prompt_lower = prompt.lower()
        
        # Check for explicit style mentions
        style_patterns = [
            r"in the style of",
            r"inspired by",
            r"\bart\s+(nouveau|deco|style)\b",
            r"\b(comic|manga|anime|realistic|surreal|abstract)\b"
        ]
        
        import re
        for pattern in style_patterns:
            if re.search(pattern, prompt_lower):
                score += 0.4
                break
        
        # Check for artistic medium mentions
        mediums = ["oil painting", "watercolor", "digital art", "photograph", "illustration"]
        for medium in mediums:
            if medium in prompt_lower:
                score += 0.3
                break
        
        # Check for quality indicators
        for indicator_type, words in self.quality_indicators.items():
            if indicator_type == "clear_style":
                if any(word in prompt_lower for word in words):
                    score += 0.3
                    break
        
        return min(score, 1.0)
    
    def _score_composition(self, prompt: str) -> float:
        """Score composition guidance in the prompt."""
        score = 0.0
        prompt_lower = prompt.lower()
        
        # Composition terms
        composition_terms = [
            "composition", "framing", "perspective", "angle",
            "close-up", "wide shot", "portrait", "landscape",
            "rule of thirds", "symmetrical", "asymmetrical",
            "foreground", "background", "depth"
        ]
        
        matches = sum(1 for term in composition_terms if term in prompt_lower)
        score = min(matches * 0.25, 1.0)
        
        return score
    
    def _score_atmosphere(self, prompt: str) -> float:
        """Score atmospheric and mood elements."""
        score = 0.0
        prompt_lower = prompt.lower()
        
        # Atmospheric terms
        atmosphere_terms = [
            "mood", "atmosphere", "ambiance", "feeling",
            "dramatic", "serene", "mysterious", "ethereal",
            "lighting", "shadows", "glow", "mist", "fog"
        ]
        
        matches = sum(1 for term in atmosphere_terms if term in prompt_lower)
        score = min(matches * 0.2, 1.0)
        
        return score
    
    def _score_technical_quality(self, prompt: str) -> float:
        """Score technical quality indicators."""
        score = 0.0
        prompt_lower = prompt.lower()
        
        # Quality markers
        quality_markers = [
            "high quality", "masterpiece", "professional",
            "detailed", "8k", "4k", "high resolution",
            "photorealistic", "hyperrealistic", "ultra"
        ]
        
        matches = sum(1 for marker in quality_markers if marker in prompt_lower)
        score = min(matches * 0.25, 1.0)
        
        return score
    
    def _score_uniqueness(self, prompt: str) -> float:
        """Score uniqueness and creativity of the prompt."""
        # This is simplified - in production, would compare against
        # a database of common prompts
        score = 0.5  # Base score
        
        # Check for unique combinations
        prompt_lower = prompt.lower()
        
        # Philosophical or unusual elements
        unique_elements = [
            "transcendent", "metaphysical", "existential",
            "surreal", "dreamlike", "impossible",
            "paradox", "duality", "consciousness"
        ]
        
        matches = sum(1 for element in unique_elements if element in prompt_lower)
        score += min(matches * 0.15, 0.5)
        
        return min(score, 1.0)


class ABTestManager:
    """Manages A/B testing for prompt variations."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.tests: Dict[str, Dict[str, Any]] = {}
        self.results: Dict[str, List[PromptMetrics]] = defaultdict(list)
    
    def create_test(
        self,
        test_id: str,
        name: str,
        prompt_variations: List[Dict[str, str]],
        scene_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a new A/B test."""
        test = {
            "id": test_id,
            "name": name,
            "created_at": datetime.now().isoformat(),
            "status": "active",
            "scene_data": scene_data,
            "variations": prompt_variations,
            "total_variations": len(prompt_variations),
            "completed_variations": 0
        }
        
        self.tests[test_id] = test
        self.logger.info(f"Created A/B test {test_id} with {len(prompt_variations)} variations")
        
        return test
    
    def record_result(
        self,
        test_id: str,
        variation_id: str,
        metrics: PromptMetrics
    ) -> None:
        """Record results for a variation."""
        if test_id not in self.tests:
            raise ValueError(f"Test {test_id} not found")
        
        self.results[test_id].append(metrics)
        
        # Update test status
        test = self.tests[test_id]
        test["completed_variations"] += 1
        
        if test["completed_variations"] >= test["total_variations"]:
            test["status"] = "completed"
            test["completed_at"] = datetime.now().isoformat()
    
    def analyze_test(self, test_id: str) -> Dict[str, Any]:
        """Analyze results of an A/B test."""
        if test_id not in self.tests:
            raise ValueError(f"Test {test_id} not found")
        
        test = self.tests[test_id]
        results = self.results[test_id]
        
        if not results:
            return {"error": "No results recorded yet"}
        
        # Group results by style/optimization
        grouped_results = defaultdict(list)
        for metric in results:
            key = f"{metric.style}_{metric.optimization_level}"
            grouped_results[key].append(metric)
        
        # Analyze each group
        analysis = {
            "test_id": test_id,
            "test_name": test["name"],
            "status": test["status"],
            "total_variations": len(results),
            "groups": {}
        }
        
        for group_key, group_metrics in grouped_results.items():
            group_analysis = {
                "count": len(group_metrics),
                "avg_overall_score": statistics.mean(m.overall_score for m in group_metrics),
                "avg_efficiency": statistics.mean(m.efficiency_score for m in group_metrics),
                "avg_generation_time": statistics.mean(m.generation_time for m in group_metrics),
                "avg_token_count": statistics.mean(m.token_count for m in group_metrics),
                "quality_breakdown": {
                    "composition": statistics.mean(m.composition_score for m in group_metrics),
                    "style": statistics.mean(m.style_adherence for m in group_metrics),
                    "detail": statistics.mean(m.detail_richness for m in group_metrics),
                    "emotion": statistics.mean(m.emotional_accuracy for m in group_metrics),
                    "philosophy": statistics.mean(m.philosophical_depth for m in group_metrics)
                }
            }
            
            # Add user ratings if available
            user_ratings = [m.user_rating for m in group_metrics if m.user_rating is not None]
            if user_ratings:
                group_analysis["avg_user_rating"] = statistics.mean(user_ratings)
            
            analysis["groups"][group_key] = group_analysis
        
        # Determine winner
        best_group = max(
            analysis["groups"].items(),
            key=lambda x: x[1]["avg_overall_score"]
        )
        analysis["recommended"] = {
            "group": best_group[0],
            "score": best_group[1]["avg_overall_score"],
            "reasoning": self._generate_recommendation_reasoning(best_group)
        }
        
        return analysis
    
    def _generate_recommendation_reasoning(
        self,
        best_group: Tuple[str, Dict[str, Any]]
    ) -> str:
        """Generate reasoning for the recommendation."""
        group_name, metrics = best_group
        
        reasons = []
        
        if metrics["avg_overall_score"] > 0.8:
            reasons.append("Excellent overall quality score")
        
        if metrics["avg_efficiency"] > 0.7:
            reasons.append("High efficiency (quality per token)")
        
        # Check quality breakdown
        quality = metrics["quality_breakdown"]
        strong_areas = [
            area for area, score in quality.items()
            if score > 0.75
        ]
        if strong_areas:
            reasons.append(f"Strong in: {', '.join(strong_areas)}")
        
        if "avg_user_rating" in metrics and metrics["avg_user_rating"] >= 4.0:
            reasons.append(f"High user satisfaction ({metrics['avg_user_rating']:.1f}/5)")
        
        return "; ".join(reasons) if reasons else "Best overall performance"
    
    def export_results(self, test_id: str, filepath: str) -> None:
        """Export test results to JSON file."""
        if test_id not in self.tests:
            raise ValueError(f"Test {test_id} not found")
        
        export_data = {
            "test": self.tests[test_id],
            "results": [m.to_dict() for m in self.results[test_id]],
            "analysis": self.analyze_test(test_id)
        }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        self.logger.info(f"Exported results for test {test_id} to {filepath}")


class PromptEffectivenessTracker:
    """Tracks prompt effectiveness over time for continuous improvement."""
    
    def __init__(self, history_file: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        self.history_file = history_file
        self.analyzer = PromptAnalyzer()
        self.ab_manager = ABTestManager()
        
        # Historical data
        self.historical_metrics: List[PromptMetrics] = []
        self.style_performance: Dict[str, List[float]] = defaultdict(list)
        self.optimization_performance: Dict[str, List[float]] = defaultdict(list)
        
        # Load history if available
        if history_file:
            self._load_history()
    
    def track_prompt(
        self,
        prompt: str,
        style: str,
        optimization_level: str,
        generation_results: Optional[Dict[str, Any]] = None
    ) -> PromptMetrics:
        """Track a prompt's effectiveness."""
        # Analyze prompt characteristics
        analysis = self.analyzer.analyze_prompt(prompt)
        
        # Create metrics object
        metrics = PromptMetrics(
            prompt_id=f"{style}_{optimization_level}_{len(self.historical_metrics)}",
            prompt_text=prompt,
            style=style,
            optimization_level=optimization_level,
            token_count=len(prompt.split()),  # Simplified token count
            composition_score=analysis.get("composition_guidance", 0),
            style_adherence=analysis.get("style_specification", 0),
            detail_richness=analysis.get("technical_quality", 0),
            emotional_accuracy=analysis.get("atmospheric_elements", 0),
            philosophical_depth=analysis.get("uniqueness", 0)
        )
        
        # Add generation results if available
        if generation_results:
            metrics.generation_time = generation_results.get("time", 0)
            metrics.model_confidence = generation_results.get("confidence", 0)
            metrics.error_count = generation_results.get("errors", 0)
        
        # Store metrics
        self.historical_metrics.append(metrics)
        self.style_performance[style].append(metrics.overall_score)
        self.optimization_performance[optimization_level].append(metrics.overall_score)
        
        # Save history
        if self.history_file:
            self._save_history()
        
        return metrics
    
    def get_style_recommendations(self) -> Dict[str, Any]:
        """Get recommendations based on historical performance."""
        recommendations = {}
        
        # Analyze style performance
        style_scores = {
            style: statistics.mean(scores) if scores else 0
            for style, scores in self.style_performance.items()
        }
        
        if style_scores:
            best_style = max(style_scores.items(), key=lambda x: x[1])
            recommendations["best_performing_style"] = {
                "style": best_style[0],
                "avg_score": best_style[1]
            }
        
        # Analyze optimization performance
        opt_scores = {
            level: statistics.mean(scores) if scores else 0
            for level, scores in self.optimization_performance.items()
        }
        
        if opt_scores:
            best_opt = max(opt_scores.items(), key=lambda x: x[1])
            recommendations["best_optimization_level"] = {
                "level": best_opt[0],
                "avg_score": best_opt[1]
            }
        
        # Recent trends
        if len(self.historical_metrics) >= 10:
            recent_metrics = self.historical_metrics[-10:]
            recent_avg = statistics.mean(m.overall_score for m in recent_metrics)
            older_avg = statistics.mean(
                m.overall_score for m in self.historical_metrics[:-10]
            )
            
            recommendations["trend"] = {
                "direction": "improving" if recent_avg > older_avg else "declining",
                "recent_avg": recent_avg,
                "historical_avg": older_avg
            }
        
        return recommendations
    
    def _load_history(self) -> None:
        """Load historical data from file."""
        try:
            with open(self.history_file, 'r') as f:
                data = json.load(f)
                # Reconstruct metrics objects
                # Implementation depends on serialization format
                self.logger.info(f"Loaded {len(data)} historical metrics")
        except FileNotFoundError:
            self.logger.info("No history file found, starting fresh")
        except Exception as e:
            self.logger.error(f"Error loading history: {e}")
    
    def _save_history(self) -> None:
        """Save historical data to file."""
        try:
            data = [m.to_dict() for m in self.historical_metrics]
            with open(self.history_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving history: {e}")