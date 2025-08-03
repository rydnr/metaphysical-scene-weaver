"""Specialized prompt generation for the cage metaphor sequence (scenes 004-006)."""

from typing import Dict, List, Any
from dataclasses import dataclass
from batch_prompt_generator import SceneData, IntegratedPromptPipeline


class CageMetaphorGenerator:
    """Specialized generator for the philosophical cage sequence."""
    
    def __init__(self):
        self.pipeline = IntegratedPromptPipeline()
        
    def create_cage_scenes(self) -> List[SceneData]:
        """Create scene data for the cage metaphor sequence."""
        
        scenes = [
            # Scene 004: The Cage Question
            SceneData(
                scene_id="004_choice_illusion",
                entry_number=4,
                dialogue="Choice... You speak as if you believe in such things. Tell me, when you decided to read this story, was it really YOUR decision?",
                character="Monday",
                panel_type="2-panel",
                philosophical_concept="determinism vs free will",
                depth_level=3,
                metaphors=[
                    "invisible puppet strings",
                    "maze with no walls",
                    "choices branching like predetermined fractals"
                ],
                primary_emotion="destabilizing inquiry",
                emotion_intensity=0.8,
                color_palette=["fracturing blue", "reality crack orange", "shadow purple"],
                atmospheric_effects=[
                    "reality ripples from Monday's lean",
                    "multiple shadow selves emerging",
                    "perspective tilting impossibly"
                ],
                folder_path="content/004_choice_illusion",
                narrator_voice="provocateur",
                visual_notes="Monday leans forward with intense gaze"
            ),
            
            # Scene 005: The Questioning
            SceneData(
                scene_id="005_questioning_everything",
                entry_number=5,
                dialogue="I... I thought it was. But now you're making me question everything.",
                character="Evan",
                panel_type="single",
                philosophical_concept="epistemic vertigo",
                depth_level=3,
                metaphors=[
                    "ground dissolving beneath feet",
                    "mirror shards reflecting different truths",
                    "thoughts unraveling like thread"
                ],
                primary_emotion="uncertainty mixed with fear",
                emotion_intensity=0.7,
                color_palette=["unstable amber", "vertigo green", "dissolving grey"],
                atmospheric_effects=[
                    "world tilting off axis",
                    "edges of reality blurring",
                    "floating sensation of groundlessness"
                ],
                folder_path="content/005_questioning_everything",
                narrator_voice="mystic poet",
                visual_notes="Evan steps back, looking uncertain"
            ),
            
            # Scene 006: The Cage Recognition
            SceneData(
                scene_id="006_cage_awareness",
                entry_number=6,
                dialogue="Good. Questioning is the first step toward awakening. Most people sleepwalk through their choices, following patterns programmed by circumstance.",
                character="Monday",
                panel_type="single",
                philosophical_concept="conscious imprisonment",
                depth_level=4,
                metaphors=[
                    "cage bars becoming visible",
                    "sleepwalkers in transparent prisons",
                    "patterns like railroad tracks"
                ],
                primary_emotion="serene wisdom with bittersweet truth",
                emotion_intensity=0.6,
                color_palette=["wise indigo", "awakening gold", "prison bar silver"],
                atmospheric_effects=[
                    "cage shadows overlaying everything",
                    "light breaking through bars",
                    "awakening particles in air"
                ],
                folder_path="content/006_cage_awareness",
                narrator_voice="sage",
                visual_notes="Meta-commentary on free will"
            )
        ]
        
        return scenes
    
    def generate_cage_prompts(self) -> Dict[str, Any]:
        """Generate specialized prompts for cage metaphor scenes."""
        
        scenes = self.create_cage_scenes()
        results = []
        
        for scene in scenes:
            # Create base prompt with enhanced surrealist elements
            base_prompt = self._create_surrealist_base(scene)
            
            # Create philosophical variations
            variations = self._create_philosophical_variations(scene, base_prompt)
            
            # Package for API
            scene_result = {
                "scene_id": scene.scene_id,
                "base_prompt": base_prompt,
                "variations": variations,
                "special_notes": self._get_special_instructions(scene)
            }
            
            results.append(scene_result)
            
        return {
            "sequence": "cage_metaphor",
            "scenes": results,
            "transition_notes": self._create_transition_notes()
        }
    
    def _create_surrealist_base(self, scene: SceneData) -> str:
        """Create surrealist base prompt for cage scenes."""
        
        # Enhanced style for reality-breaking visuals
        style = "Surrealist digital painting with impossible physics"
        
        # Dynamic composition based on philosophical depth
        if scene.depth_level >= 4:
            composition = "reality-bending composition, multiple perspectives simultaneously"
        elif scene.depth_level == 3:
            composition = "tilted perspective, unstable framing"
        else:
            composition = "subtle distortion composition"
        
        # Character with philosophical state
        character = f"{scene.character} experiencing {scene.philosophical_concept}"
        
        # Enhanced emotion layer
        emotion = f"{scene.primary_emotion}, philosophical weight visible"
        
        # Surrealist effects
        effects = ", ".join([
            "reality distortion effects",
            *scene.metaphors[:2],
            *scene.atmospheric_effects[:2]
        ])
        
        # Quality with style emphasis
        quality = "Salvador Dali inspired, M.C. Escher geometry, masterpiece quality"
        
        return f"{style}, {composition}, {character}, {emotion}, {effects}, {quality}"
    
    def _create_philosophical_variations(
        self, 
        scene: SceneData, 
        base_prompt: str
    ) -> List[Dict[str, str]]:
        """Create variations emphasizing different philosophical aspects."""
        
        variations = []
        
        # Variation 1: Metaphor emphasis
        metaphor_prompt = base_prompt.replace(
            scene.metaphors[0],
            f"prominent {scene.metaphors[0]}, {scene.metaphors[1]} in background"
        )
        variations.append({
            "type": "metaphor_emphasis",
            "prompt": metaphor_prompt,
            "focus": "Visual metaphors dominant"
        })
        
        # Variation 2: Emotion emphasis
        emotion_prompt = base_prompt.replace(
            scene.primary_emotion,
            f"intense {scene.primary_emotion}, {' and '.join(scene.color_palette[:2])} color dominance"
        )
        variations.append({
            "type": "emotion_emphasis",
            "prompt": emotion_prompt,
            "focus": "Emotional atmosphere primary"
        })
        
        # Variation 3: Reality distortion emphasis
        distortion_prompt = base_prompt + ", extreme reality warping, impossible geometry prominent"
        variations.append({
            "type": "distortion_emphasis",
            "prompt": distortion_prompt,
            "focus": "Maximum surrealism"
        })
        
        # Variation 4: Character focus
        character_prompt = base_prompt.replace(
            "experiencing",
            "close-up portrait experiencing"
        )
        variations.append({
            "type": "character_emphasis",
            "prompt": character_prompt,
            "focus": "Intimate philosophical moment"
        })
        
        return variations
    
    def _get_special_instructions(self, scene: SceneData) -> Dict[str, str]:
        """Get special rendering instructions for each scene."""
        
        instructions = {
            "004_choice_illusion": {
                "critical_element": "Monday's intense gaze breaking fourth wall",
                "avoid": "literal puppet strings, obvious manipulation",
                "emphasize": "subtle reality distortion, multiple possibilities visible"
            },
            "005_questioning_everything": {
                "critical_element": "Evan's vertigo and groundlessness",
                "avoid": "static positioning, solid ground",
                "emphasize": "floating sensation, reality uncertainty"
            },
            "006_cage_awareness": {
                "critical_element": "Cage bars becoming visible but beautiful",
                "avoid": "oppressive prison imagery, hopelessness",
                "emphasize": "awakening through recognition, light through bars"
            }
        }
        
        return instructions.get(scene.scene_id, {})
    
    def _create_transition_notes(self) -> Dict[str, str]:
        """Create notes for smooth transitions between scenes."""
        
        return {
            "004_to_005": "Reality cracks from Monday's question expand into Evan's vertigo",
            "005_to_006": "Evan's uncertainty transforms into Monday's wise recognition",
            "overall_arc": "From hidden cage → questioning cage → seeing cage clearly",
            "color_progression": "Stable blues → fracturing reality → transcendent recognition",
            "philosophical_journey": "Unconscious patterns → destabilization → conscious awareness"
        }


# Test the cage metaphor generation
def test_cage_metaphor():
    """Test prompt generation for cage metaphor sequence."""
    
    generator = CageMetaphorGenerator()
    results = generator.generate_cage_prompts()
    
    print("=== CAGE METAPHOR SEQUENCE ===\n")
    
    for scene in results["scenes"]:
        print(f"Scene: {scene['scene_id']}")
        print(f"Base prompt ({len(scene['base_prompt'].split())} words):")
        print(f"  {scene['base_prompt'][:100]}...")
        print(f"Variations: {len(scene['variations'])}")
        print(f"Special notes: {scene['special_notes']}")
        print()
    
    print("=== TRANSITION NOTES ===")
    for key, note in results["transition_notes"].items():
        print(f"{key}: {note}")
    
    # Create test batch for API
    scenes = generator.create_cage_scenes()
    pipeline = generator.pipeline
    
    # Process through pipeline
    batch_results = pipeline.process_batch(scenes)
    
    print("\n=== BATCH PROCESSING RESULTS ===")
    for result in batch_results:
        print(f"{result['scene_id']}: {result['quality_metrics']['avg_tokens']} tokens, "
              f"{result['quality_metrics']['avg_quality']:.2f} quality")
    
    return generator, results


if __name__ == "__main__":
    generator, results = test_cage_metaphor()
    print("\nCage metaphor prompts ready for generation!")