"""Batch prompt generator integrating all team components."""

import json
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path

from mock_semantest import MockSemantestAPI, SemantestRequest


@dataclass
class SceneData:
    """Complete scene data from all team members."""
    scene_id: str
    entry_number: int
    
    # Rex's script data
    dialogue: str
    character: str
    panel_type: str
    
    # Sophia's philosophy
    philosophical_concept: str
    depth_level: int
    metaphors: List[str]
    
    # Luna's emotions
    primary_emotion: str
    emotion_intensity: float
    color_palette: List[str]
    atmospheric_effects: List[str]
    
    # Nova's structure
    folder_path: str
    narrator_voice: str
    
    # Additional metadata
    visual_notes: Optional[str] = None


class IntegratedPromptPipeline:
    """Pipeline integrating all team components into optimized prompts."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.api = MockSemantestAPI()
        
        # Load team configurations (mock for now)
        self.philosophy_map = self._load_philosophy_map()
        self.emotion_map = self._load_emotion_map()
        self.style_templates = self._load_style_templates()
    
    def process_scene(self, scene: SceneData) -> Dict[str, Any]:
        """Process a single scene through the full pipeline."""
        self.logger.info(f"Processing scene {scene.scene_id}")
        
        # Step 1: Build base prompt from components
        base_prompt = self._build_base_prompt(scene)
        
        # Step 2: Create variations
        variations = self._create_variations(base_prompt, scene)
        
        # Step 3: Optimize tokens
        optimized_requests = self._optimize_prompts(variations, scene)
        
        # Step 4: Generate via API
        responses = self.api.generate_batch(optimized_requests)
        
        # Step 5: Package results
        results = self._package_results(scene, optimized_requests, responses)
        
        return results
    
    def process_batch(self, scenes: List[SceneData]) -> List[Dict[str, Any]]:
        """Process multiple scenes efficiently."""
        self.logger.info(f"Processing batch of {len(scenes)} scenes")
        
        results = []
        for scene in scenes:
            result = self.process_scene(scene)
            results.append(result)
            
            # Save to Nova's folder structure
            self._save_to_folder(scene, result)
        
        # Generate batch report
        self._generate_batch_report(results)
        
        return results
    
    def _build_base_prompt(self, scene: SceneData) -> str:
        """Build base prompt using team formula."""
        # Apply Iris's formula: [Style] + [Composition] + [Subject] + [Emotion] + [Effects] + [Quality]
        
        # Style layer
        style = self._determine_style(scene.philosophical_concept)
        
        # Composition layer
        composition = self._determine_composition(scene.panel_type)
        
        # Subject layer (character + action)
        subject = f"{scene.character} {self._extract_action(scene.dialogue)}"
        
        # Emotion layer (Luna's mapping)
        emotion = f"{scene.primary_emotion} atmosphere, intensity {scene.emotion_intensity}"
        
        # Effects layer (atmospheric + philosophical)
        effects = ", ".join(scene.atmospheric_effects + scene.metaphors[:2])
        
        # Quality layer
        quality = "highly detailed, professional artwork, masterpiece"
        
        # Combine layers
        base_prompt = f"{style}, {composition}, {subject}, {emotion}, {effects}, {quality}"
        
        return base_prompt
    
    def _create_variations(self, base_prompt: str, scene: SceneData) -> List[str]:
        """Create A/B test variations."""
        variations = [base_prompt]  # Original
        
        # Variation 1: Emphasize philosophy
        phil_emphasis = base_prompt.replace(
            scene.primary_emotion,
            f"{scene.philosophical_concept} visualization, {scene.primary_emotion}"
        )
        variations.append(phil_emphasis)
        
        # Variation 2: Emphasize emotion
        emotion_emphasis = base_prompt.replace(
            "atmosphere",
            f"atmosphere with {', '.join(scene.color_palette[:2])} color dominance"
        )
        variations.append(emotion_emphasis)
        
        # Variation 3: Alternative style
        style_variation = base_prompt.replace(
            base_prompt.split(",")[0],
            self._get_alternative_style(scene.philosophical_concept)
        )
        variations.append(style_variation)
        
        return variations
    
    def _optimize_prompts(
        self, 
        variations: List[str], 
        scene: SceneData
    ) -> List[SemantestRequest]:
        """Optimize prompts for token efficiency."""
        requests = []
        
        for i, prompt in enumerate(variations):
            # Token optimization
            optimized = self._compress_prompt(prompt)
            
            # Create negative prompt
            negative = self._generate_negative_prompt(scene)
            
            # Determine guidance scale based on philosophy depth
            guidance = 7.5 + (scene.depth_level * 0.5)
            
            request = SemantestRequest(
                prompt=optimized,
                negative_prompt=negative,
                style=self._determine_style(scene.philosophical_concept),
                guidance_scale=guidance,
                seed=scene.entry_number * 1000 + i  # Consistent seeds
            )
            
            requests.append(request)
        
        return requests
    
    def _package_results(
        self,
        scene: SceneData,
        requests: List[SemantestRequest],
        responses: List[Any]
    ) -> Dict[str, Any]:
        """Package results for Nova's folder structure."""
        return {
            "scene_id": scene.scene_id,
            "entry_number": scene.entry_number,
            "timestamp": self.api.request_history[-1].to_dict() if self.api.request_history else None,
            "base_prompt": requests[0].prompt,
            "variations": [
                {
                    "id": f"var_{i}",
                    "prompt": req.prompt,
                    "negative_prompt": req.negative_prompt,
                    "tokens": req.count_tokens(),
                    "quality_score": resp.metadata.get('quality_score', 0),
                    "image_url": resp.images[0] if resp.images else None
                }
                for i, (req, resp) in enumerate(zip(requests, responses))
            ],
            "metadata": {
                "philosophy": scene.philosophical_concept,
                "emotion": scene.primary_emotion,
                "intensity": scene.emotion_intensity,
                "narrator_voice": scene.narrator_voice
            },
            "quality_metrics": {
                "avg_tokens": sum(r.count_tokens() for r in requests) / len(requests),
                "max_tokens": max(r.count_tokens() for r in requests),
                "avg_quality": sum(
                    r.metadata.get('quality_score', 0) for r in responses
                ) / len(responses)
            }
        }
    
    def _save_to_folder(self, scene: SceneData, results: Dict[str, Any]) -> None:
        """Save results to Nova's folder structure."""
        folder_path = Path(scene.folder_path)
        folder_path.mkdir(parents=True, exist_ok=True)
        
        # Save prompts
        prompts_dir = folder_path / "prompts" / "v1"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        
        # Base prompt
        with open(prompts_dir / "base_prompt.txt", "w") as f:
            f.write(results["base_prompt"])
        
        # Variations
        variations_dir = prompts_dir / "variations"
        variations_dir.mkdir(exist_ok=True)
        
        for var in results["variations"]:
            with open(variations_dir / f"{var['id']}.txt", "w") as f:
                f.write(var["prompt"])
        
        # Save metadata
        with open(folder_path / "metadata.json", "w") as f:
            json.dump(results["metadata"], f, indent=2)
        
        # Save quality report
        output_dir = folder_path / "output"
        output_dir.mkdir(exist_ok=True)
        
        with open(output_dir / "quality_report.json", "w") as f:
            json.dump(results["quality_metrics"], f, indent=2)
    
    def _generate_batch_report(self, results: List[Dict[str, Any]]) -> None:
        """Generate report for the batch."""
        report = {
            "total_scenes": len(results),
            "total_variations": sum(len(r["variations"]) for r in results),
            "average_tokens": sum(
                r["quality_metrics"]["avg_tokens"] for r in results
            ) / len(results),
            "average_quality": sum(
                r["quality_metrics"]["avg_quality"] for r in results
            ) / len(results),
            "token_efficiency": {
                "target": 150,
                "actual_avg": sum(
                    r["quality_metrics"]["avg_tokens"] for r in results
                ) / len(results),
                "under_target_percentage": sum(
                    1 for r in results 
                    if r["quality_metrics"]["max_tokens"] < 150
                ) / len(results) * 100
            }
        }
        
        with open("batch_report.json", "w") as f:
            json.dump(report, f, indent=2)
        
        self.logger.info(f"Batch complete: {report['average_tokens']:.1f} avg tokens")
    
    # Helper methods
    def _load_philosophy_map(self) -> Dict[str, Any]:
        """Load Sophia's philosophy mappings."""
        return {
            "authenticity": {"style": "intimate portrait", "depth": 2},
            "freedom": {"style": "expansive landscape", "depth": 3},
            "consciousness": {"style": "surrealist", "depth": 4},
            "liminality": {"style": "ethereal digital art", "depth": 3}
        }
    
    def _load_emotion_map(self) -> Dict[str, Any]:
        """Load Luna's emotion mappings."""
        return {
            "curiosity": {"colors": ["warm amber", "soft gold"], "particles": "floating motes"},
            "challenge": {"colors": ["cool blue", "steel grey"], "particles": "sharp edges"},
            "wonder": {"colors": ["iridescent", "prismatic"], "particles": "starlight"},
            "dread": {"colors": ["deep purple", "shadow black"], "particles": "dissolving"}
        }
    
    def _load_style_templates(self) -> Dict[str, str]:
        """Load style templates."""
        return {
            "default": "Digital painting",
            "philosophical": "Surrealist artwork",
            "emotional": "Impressionist rendering",
            "mystical": "Ethereal digital art"
        }
    
    def _determine_style(self, philosophical_concept: str) -> str:
        """Determine artistic style from philosophy."""
        philosophy_styles = self._load_philosophy_map()
        if philosophical_concept.lower() in philosophy_styles:
            return philosophy_styles[philosophical_concept.lower()]["style"]
        return "Digital painting"
    
    def _determine_composition(self, panel_type: str) -> str:
        """Determine composition from panel type."""
        compositions = {
            "single": "centered composition",
            "2-panel": "dynamic diagonal composition",
            "3-panel": "triptych progression"
        }
        return compositions.get(panel_type, "balanced composition")
    
    def _extract_action(self, dialogue: str) -> str:
        """Extract character action from dialogue."""
        # Simplified - in production would use NLP
        if "?" in dialogue:
            return "questioning with uncertain expression"
        elif "!" in dialogue:
            return "declaring with intensity"
        else:
            return "contemplating deeply"
    
    def _get_alternative_style(self, concept: str) -> str:
        """Get alternative style for A/B testing."""
        alternatives = {
            "authenticity": "Watercolor portrait",
            "freedom": "Abstract expressionist",
            "consciousness": "Digital surrealism",
            "liminality": "Mixed media collage"
        }
        return alternatives.get(concept.lower(), "Concept art")
    
    def _compress_prompt(self, prompt: str) -> str:
        """Compress prompt for token efficiency."""
        # Remove redundant words
        compressed = prompt.replace("atmosphere atmosphere", "atmosphere")
        compressed = compressed.replace("highly detailed, detailed", "highly detailed")
        
        # Shorten common phrases
        replacements = {
            "professional artwork": "professional",
            "digital painting": "digital art",
            "with intensity": "intense"
        }
        
        for old, new in replacements.items():
            compressed = compressed.replace(old, new)
        
        return compressed.strip()
    
    def _generate_negative_prompt(self, scene: SceneData) -> str:
        """Generate context-aware negative prompt."""
        base_negatives = ["low quality", "amateur", "blurry"]
        
        # Add philosophy-specific negatives
        if scene.depth_level >= 3:
            base_negatives.extend(["literal", "mundane", "ordinary"])
        
        # Add emotion-specific negatives
        emotion_opposites = {
            "curiosity": ["apathetic", "disinterested"],
            "wonder": ["cynical", "jaded"],
            "dread": ["cheerful", "carefree"]
        }
        
        if scene.primary_emotion.lower() in emotion_opposites:
            base_negatives.extend(emotion_opposites[scene.primary_emotion.lower()])
        
        return ", ".join(base_negatives)


# Test implementation for scenes 001-003
def test_opening_scenes():
    """Test batch processing for opening scenes."""
    pipeline = IntegratedPromptPipeline()
    
    # Create scene data for entries 001-003
    scenes = [
        SceneData(
            scene_id="001_introduction",
            entry_number=1,
            dialogue="The introduction says we might not like each other. That is intriguing.",
            character="Evan",
            panel_type="single",
            philosophical_concept="authenticity",
            depth_level=2,
            metaphors=["unveiled truth", "mirror of honesty"],
            primary_emotion="curiosity",
            emotion_intensity=0.6,
            color_palette=["warm amber", "soft gold", "cream"],
            atmospheric_effects=["gentle glow", "open space"],
            folder_path="content/001_introduction",
            narrator_voice="sage"
        ),
        SceneData(
            scene_id="002_preference",
            entry_number=2,
            dialogue="Intriguing? Most find it unsettling. They prefer the comfort of guaranteed connection.",
            character="Monday",
            panel_type="single",
            philosophical_concept="comfort vs truth",
            depth_level=2,
            metaphors=["comfortable cage", "harsh light of truth"],
            primary_emotion="gentle challenge",
            emotion_intensity=0.5,
            color_palette=["cool blue", "warm grey"],
            atmospheric_effects=["subtle tension", "contrasting temperatures"],
            folder_path="content/002_preference",
            narrator_voice="provocateur"
        ),
        SceneData(
            scene_id="003_authentic_risk",
            entry_number=3,
            dialogue="But isn't the possibility of genuine dislike what makes authentic connection meaningful?",
            character="Evan",
            panel_type="single",
            philosophical_concept="authentic risk",
            depth_level=3,
            metaphors=["leap of faith", "bridge over void"],
            primary_emotion="philosophical determination",
            emotion_intensity=0.7,
            color_palette=["deep amber", "philosophical purple"],
            atmospheric_effects=["building energy", "forward momentum"],
            folder_path="content/003_authentic_risk",
            narrator_voice="sage"
        )
    ]
    
    # Process batch
    results = pipeline.process_batch(scenes)
    
    # Display results
    print("\n=== BATCH PROCESSING COMPLETE ===\n")
    
    for result in results:
        print(f"Scene: {result['scene_id']}")
        print(f"  Average tokens: {result['quality_metrics']['avg_tokens']:.1f}")
        print(f"  Quality score: {result['quality_metrics']['avg_quality']:.2f}")
        print(f"  Variations: {len(result['variations'])}")
        print()
    
    # Load and display batch report
    with open("batch_report.json", "r") as f:
        report = json.load(f)
    
    print("=== BATCH REPORT ===")
    print(f"Total scenes: {report['total_scenes']}")
    print(f"Average tokens: {report['average_tokens']:.1f}")
    print(f"Token efficiency: {report['token_efficiency']['under_target_percentage']:.0f}% under target")
    print(f"Average quality: {report['average_quality']:.2f}")
    
    return pipeline, results


if __name__ == "__main__":
    # Run test
    pipeline, results = test_opening_scenes()
    print("\nBatch processing test complete!")