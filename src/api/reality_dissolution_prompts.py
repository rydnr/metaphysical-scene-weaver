"""Reality dissolution sequence - the climactic tree transformation (scenes 010-012)."""

from typing import Dict, List, Any
from dataclasses import dataclass
from batch_prompt_generator import SceneData, IntegratedPromptPipeline


class RealityDissolutionGenerator:
    """Generator for the reality-breaking tree sequence."""
    
    def __init__(self):
        self.pipeline = IntegratedPromptPipeline()
        
    def create_dissolution_scenes(self) -> List[SceneData]:
        """Create scene data for reality dissolution trilogy."""
        
        scenes = [
            # Scene 010: Identity Question
            SceneData(
                scene_id="010_identity_question",
                entry_number=10,
                dialogue="Who are you? Have you been listening this whole time?",
                character="Evan",
                panel_type="single",
                philosophical_concept="observer paradox",
                depth_level=2,
                metaphors=[
                    "identity as shifting sand",
                    "consciousness observing itself",
                    "mirrors reflecting uncertainty"
                ],
                primary_emotion="confused curiosity",
                emotion_intensity=0.6,
                color_palette=["questioning amber", "identity flux blue", "uncertainty grey"],
                atmospheric_effects=[
                    "reality edges softening",
                    "multiple Evan reflections appearing",
                    "space becoming fluid"
                ],
                folder_path="content/010_identity_question",
                narrator_voice="mystic poet",
                visual_notes="Evan looking at Valerie with wonder"
            ),
            
            # Scene 011: Space Between
            SceneData(
                scene_id="011_space_between",
                entry_number=11,
                dialogue="I am the space between your thoughts, Evan. The pause between heartbeats. I've been here all along—you just weren't ready to perceive me.",
                character="Valerie",
                panel_type="single",
                philosophical_concept="liminal consciousness",
                depth_level=4,
                metaphors=[
                    "gaps becoming substance",
                    "silence taking form",
                    "negative space breathing"
                ],
                primary_emotion="mystical revelation",
                emotion_intensity=0.8,
                color_palette=["void purple", "consciousness gold", "between-space silver"],
                atmospheric_effects=[
                    "space between objects glowing",
                    "heartbeat visualization",
                    "thought gaps visible"
                ],
                folder_path="content/011_space_between",
                narrator_voice="transcendent sage",
                visual_notes="Valerie as living paradox"
            ),
            
            # Scene 012: Tree Touch (CLIMAX)
            SceneData(
                scene_id="012_tree_touch",
                entry_number=19,
                dialogue="Touch the tree yourself. See what happens when you stop believing in solid things.",
                character="Valerie",
                panel_type="3-panel",
                philosophical_concept="reality as belief",
                depth_level=4,
                metaphors=[
                    "matter becoming wave",
                    "solid dissolving to possibility",
                    "tree as liquid consciousness"
                ],
                primary_emotion="awe mixed with terror",
                emotion_intensity=0.95,
                color_palette=["reality-break orange", "liquid wood brown", "possibility purple"],
                atmospheric_effects=[
                    "tree rippling like water",
                    "reality waves emanating from touch",
                    "physics laws visibly breaking",
                    "matter-energy transformation"
                ],
                folder_path="content/012_tree_touch",
                narrator_voice="reality breaker",
                visual_notes="The moment everything changes"
            )
        ]
        
        return scenes
    
    def generate_dissolution_prompts(self) -> Dict[str, Any]:
        """Generate specialized prompts for reality dissolution."""
        
        scenes = self.create_dissolution_scenes()
        results = []
        
        for scene in scenes:
            # Create surrealist base with reality-breaking elements
            base_prompt = self._create_reality_breaking_base(scene)
            
            # Create dissolution variations
            variations = self._create_dissolution_variations(scene, base_prompt)
            
            # Special handling for the climactic tree touch
            if scene.scene_id == "012_tree_touch":
                panel_prompts = self._create_panel_progression(scene, base_prompt)
            else:
                panel_prompts = None
            
            # Package for API
            scene_result = {
                "scene_id": scene.scene_id,
                "base_prompt": base_prompt,
                "variations": variations,
                "special_notes": self._get_dissolution_instructions(scene),
                "physics_effects": self._get_physics_breakdown(scene),
                "panel_prompts": panel_prompts
            }
            
            results.append(scene_result)
            
        return {
            "sequence": "reality_dissolution",
            "scenes": results,
            "transition_notes": self._create_dissolution_transitions(),
            "climax_specifications": self._create_climax_specs()
        }
    
    def _create_reality_breaking_base(self, scene: SceneData) -> str:
        """Create base prompt for reality dissolution scenes."""
        
        # Maximum surrealism for reality breaking
        style = "Surrealist digital masterpiece with impossible physics and reality distortion"
        
        # Composition based on dissolution level
        if scene.scene_id == "012_tree_touch":
            composition = "reality-shattering composition, multiple perspectives simultaneously, M.C. Escher inspired"
        elif scene.depth_level >= 4:
            composition = "fluid reality composition, boundaries dissolving"
        else:
            composition = "subtly warped perspective, reality beginning to bend"
        
        # Character in philosophical crisis
        character = f"{scene.character} experiencing {scene.philosophical_concept}"
        
        # Maximum emotional intensity
        emotion = f"intense {scene.primary_emotion}, reality-altering moment"
        
        # Reality-breaking effects
        effects = ", ".join([
            "reality distortion waves",
            "physics laws breaking visibly",
            *scene.metaphors[:2],
            *scene.atmospheric_effects[:3]
        ])
        
        # Quality emphasizing the climactic nature
        quality = "Salvador Dali meets quantum physics, reality-bending masterpiece, ultra detailed"
        
        return f"{style}, {composition}, {character}, {emotion}, {effects}, {quality}"
    
    def _create_dissolution_variations(
        self, 
        scene: SceneData, 
        base_prompt: str
    ) -> List[Dict[str, str]]:
        """Create variations for reality dissolution."""
        
        variations = []
        
        # Variation 1: Physics breakdown emphasis
        physics_prompt = base_prompt.replace(
            "physics laws breaking",
            "extreme physics breakdown, matter transforming to energy, quantum uncertainty visible"
        )
        variations.append({
            "type": "physics_emphasis",
            "prompt": physics_prompt,
            "focus": "Scientific impossibility visualization"
        })
        
        # Variation 2: Emotional intensity emphasis
        emotion_prompt = base_prompt.replace(
            scene.primary_emotion,
            f"overwhelming {scene.primary_emotion}, emotion manifesting as reality distortion"
        )
        variations.append({
            "type": "emotion_emphasis",
            "prompt": emotion_prompt,
            "focus": "Emotion as reality-altering force"
        })
        
        # Variation 3: Metaphysical visualization
        metaphysical_prompt = base_prompt + ", consciousness visible as light, thought becoming matter"
        variations.append({
            "type": "metaphysical_emphasis",
            "prompt": metaphysical_prompt,
            "focus": "Abstract concepts materialized"
        })
        
        # Variation 4: Maximum surrealism
        surreal_prompt = base_prompt.replace(
            "Surrealist digital masterpiece",
            "Extreme surrealism, impossible geometry, Dali meets Escher meets quantum physics"
        )
        variations.append({
            "type": "maximum_surrealism",
            "prompt": surreal_prompt,
            "focus": "Reality completely unmoored"
        })
        
        return variations
    
    def _create_panel_progression(
        self, 
        scene: SceneData, 
        base_prompt: str
    ) -> List[Dict[str, str]]:
        """Create 3-panel progression for tree touch climax."""
        
        panels = []
        
        # Panel 1: Approach
        panels.append({
            "panel": 1,
            "prompt": base_prompt.replace(
                "experiencing reality as belief",
                "reaching toward tree with trembling hand, reality beginning to ripple"
            ),
            "focus": "The moment before contact"
        })
        
        # Panel 2: Contact
        panels.append({
            "panel": 2,
            "prompt": base_prompt.replace(
                "tree rippling like water",
                "finger touching tree bark, reality waves exploding outward, matter becoming liquid"
            ),
            "focus": "The instant of transformation"
        })
        
        # Panel 3: Dissolution
        panels.append({
            "panel": 3,
            "prompt": base_prompt + ", complete reality dissolution, tree and hand merging, boundaries erased",
            "focus": "Reality fully transformed"
        })
        
        return panels
    
    def _get_dissolution_instructions(self, scene: SceneData) -> Dict[str, str]:
        """Get special instructions for dissolution rendering."""
        
        instructions = {
            "010_identity_question": {
                "critical_element": "Multiple Evan reflections showing identity uncertainty",
                "avoid": "solid identity, clear boundaries",
                "emphasize": "identity fluidity, observer paradox visualization",
                "reality_state": "Beginning to soften, 20% dissolution"
            },
            "011_space_between": {
                "critical_element": "Valerie as embodied negative space",
                "avoid": "solid form, normal physics",
                "emphasize": "gaps becoming visible, silence taking form",
                "reality_state": "Significantly warped, 50% dissolution"
            },
            "012_tree_touch": {
                "critical_element": "Tree transforming from solid to liquid at touch",
                "avoid": "static tree, normal physics, solid matter",
                "emphasize": "matter-wave transformation, reality ripples, impossible physics",
                "reality_state": "Complete breakdown, 95% dissolution"
            }
        }
        
        return instructions.get(scene.scene_id, {})
    
    def _get_physics_breakdown(self, scene: SceneData) -> Dict[str, Any]:
        """Specify how physics breaks in each scene."""
        
        physics = {
            "010_identity_question": {
                "gravity": "slightly unstable",
                "matter_state": "edges softening",
                "light_behavior": "bending subtly",
                "time_flow": "normal with hiccups"
            },
            "011_space_between": {
                "gravity": "directionally confused",
                "matter_state": "boundaries blurring",
                "light_behavior": "revealing hidden dimensions",
                "time_flow": "visibly dilating"
            },
            "012_tree_touch": {
                "gravity": "completely optional",
                "matter_state": "solid/liquid/energy simultaneously",
                "light_behavior": "consciousness made visible",
                "time_flow": "all moments existing at once"
            }
        }
        
        return physics.get(scene.scene_id, {})
    
    def _create_dissolution_transitions(self) -> Dict[str, str]:
        """Create transition notes for dissolution sequence."""
        
        return {
            "010_to_011": "Identity questioning opens space for Valerie's revelation",
            "011_to_012": "Understanding negative space prepares for reality transformation",
            "dissolution_arc": "Solid identity → Liminal awareness → Reality transcendence",
            "visual_progression": "Subtle warping → Significant distortion → Complete dissolution",
            "emotional_journey": "Confusion → Mystical awe → Transcendent terror/wonder"
        }
    
    def _create_climax_specs(self) -> Dict[str, Any]:
        """Create detailed specifications for the climactic moment."""
        
        return {
            "tree_transformation": {
                "stages": [
                    "Solid bark with subtle movement",
                    "Ripples spreading from touch point",
                    "Wood grain flowing like liquid",
                    "Complete matter-energy transformation"
                ],
                "visual_effects": [
                    "Concentric reality waves",
                    "Matter phase transitions",
                    "Quantum uncertainty visualization",
                    "Consciousness particles emerging"
                ]
            },
            "evan_transformation": {
                "physical": "Hand beginning to merge with tree",
                "emotional": "Awe and terror perfectly balanced",
                "consciousness": "Boundaries dissolving",
                "expression": "Recognition of ultimate truth"
            },
            "environment_response": {
                "immediate": "Reality ripples from contact point",
                "spreading": "Dissolution waves affecting everything",
                "background": "Multiple realities visible simultaneously",
                "lighting": "Impossible colors emerging"
            }
        }


# Test the dissolution generation
def test_reality_dissolution():
    """Test prompt generation for reality dissolution sequence."""
    
    generator = RealityDissolutionGenerator()
    results = generator.generate_dissolution_prompts()
    
    print("=== REALITY DISSOLUTION SEQUENCE ===\n")
    
    for scene in results["scenes"]:
        print(f"Scene: {scene['scene_id']}")
        print(f"Base prompt ({len(scene['base_prompt'].split())} words):")
        print(f"  {scene['base_prompt'][:100]}...")
        print(f"Variations: {len(scene['variations'])}")
        if scene['panel_prompts']:
            print(f"Panel prompts: {len(scene['panel_prompts'])} panels")
        print(f"Reality state: {scene['special_notes']['reality_state']}")
        print()
    
    print("=== CLIMAX SPECIFICATIONS ===")
    climax = results["climax_specifications"]
    print(f"Tree transformation stages: {len(climax['tree_transformation']['stages'])}")
    print(f"Visual effects: {', '.join(climax['tree_transformation']['visual_effects'][:2])}...")
    
    # Process through pipeline
    scenes = generator.create_dissolution_scenes()
    pipeline = generator.pipeline
    batch_results = pipeline.process_batch(scenes)
    
    print("\n=== BATCH PROCESSING RESULTS ===")
    for result in batch_results:
        print(f"{result['scene_id']}: {result['quality_metrics']['avg_tokens']} tokens, "
              f"{result['quality_metrics']['avg_quality']:.2f} quality")
    
    return generator, results


if __name__ == "__main__":
    generator, results = test_reality_dissolution()
    print("\nReality dissolution prompts ready for the climactic transformation!")