"""JSON to ChatGPT Prompt Converter - Bridges scene JSON to prompt format"""

import json
from typing import Dict, List, Any


class SceneToPromptConverter:
    """Converts scene JSON format to ChatGPT-compatible prompts."""
    
    def __init__(self):
        self.aspect_ratio = "16:9"  # Default for graphic novel panels
        
    def convert_scene_to_prompt(self, scene_json: Dict[str, Any]) -> str:
        """Convert a scene JSON to a ChatGPT prompt.
        
        Args:
            scene_json: Scene data with keys: scene_id, title, characters, dialogue, 
                       actions, environment, themes
                       
        Returns:
            ChatGPT-compatible prompt string
        """
        # Extract scene components
        scene_id = scene_json.get('scene_id', '')
        title = scene_json.get('title', '')
        characters = scene_json.get('characters', [])
        dialogue = scene_json.get('dialogue', [])
        actions = scene_json.get('actions', [])
        environment = scene_json.get('environment', {})
        themes = scene_json.get('themes', [])
        
        # Build prompt components
        prompt_parts = []
        
        # Opening
        prompt_parts.append(
            f"Create a {self.aspect_ratio} philosophical graphic novel panel for "
            f"Scene {scene_id}: '{title}'."
        )
        
        # Visual Elements section
        prompt_parts.append("\nVisual Elements:")
        
        # Characters with emotions and actions
        char_descriptions = self._build_character_descriptions(
            characters, dialogue, actions
        )
        if char_descriptions:
            prompt_parts.append(f"- Characters: {char_descriptions}")
        
        # Environment
        env_desc = environment.get('description', '')
        if env_desc:
            prompt_parts.append(f"- Environment: {env_desc}")
        
        # Mood
        mood = environment.get('mood', 'contemplative')
        prompt_parts.append(f"- Mood: {mood}")
        
        # Key Action
        key_action = self._extract_key_action(actions, dialogue)
        if key_action:
            prompt_parts.append(f"- Key Action: {key_action}")
        
        # Artistic Style
        prompt_parts.append(
            "\nArtistic Style: Philosophical graphic novel with psychological "
            "realism, deep symbolic imagery, dramatic lighting"
        )
        
        # Important Details
        prompt_parts.append("\nImportant Details:")
        details = self._extract_visual_details(dialogue, actions, environment)
        for detail in details:
            prompt_parts.append(f"- {detail}")
        
        # Philosophical Theme
        if themes:
            theme_visual = self._visualize_theme(themes[0] if themes else "self-discovery")
            prompt_parts.append(f"\nPhilosophical Theme: {theme_visual}")
        
        return "\n".join(prompt_parts)
    
    def _build_character_descriptions(
        self, 
        characters: List[Dict], 
        dialogue: List[Dict],
        actions: List[Dict]
    ) -> str:
        """Build character descriptions with emotional states."""
        descriptions = []
        
        for char in characters:
            name = char.get('name', '')
            role = char.get('role', '')
            
            # Find character's emotional state from dialogue
            emotion = self._get_character_emotion(name, dialogue)
            
            # Find character's action
            action = self._get_character_action(name, actions)
            
            if name == "The Voice":
                desc = f"An aurora-like cosmic presence manifesting as {role}"
            elif name == "The Architect" or name == "Monday":
                desc = f"Geometric AI consciousness with flowing data patterns"
            elif name == "Evan":
                desc = f"A man {emotion} {action if action else ''}"
            else:
                desc = f"{name} ({role}) {emotion}"
            
            descriptions.append(desc.strip())
        
        return "; ".join(descriptions)
    
    def _get_character_emotion(self, name: str, dialogue: List[Dict]) -> str:
        """Extract character's emotional state from dialogue."""
        for line in dialogue:
            if line.get('speaker') == name:
                tone = line.get('tone', '')
                if '[' in line.get('text', ''):
                    # Extract emotion from stage direction
                    text = line['text']
                    if 'wordless' in text:
                        return "experiencing profound internal shift"
                    elif 'scream' in text:
                        return "screaming in recognition"
                    elif 'whisper' in text:
                        return "whispering with reverence"
                return f"expressing {tone}" if tone else ""
        return ""
    
    def _get_character_action(self, name: str, actions: List[Dict]) -> str:
        """Extract character's primary action."""
        for action in actions:
            if action.get('character') == name:
                return action.get('action', '')
        return ""
    
    def _extract_key_action(self, actions: List[Dict], dialogue: List[Dict]) -> str:
        """Determine the key action of the scene."""
        # Priority: character interactions > environmental changes > dialogue moments
        
        for action in actions:
            act_text = action.get('action', '')
            if any(key in act_text.lower() for key in 
                   ['transform', 'merge', 'recognition', 'revelation', 'emergence']):
                return act_text
        
        # Check dialogue for key moments
        for line in dialogue:
            if '[' in line.get('text', ''):
                return f"The moment of {line['text'].strip('[]')}"
        
        # Default to first significant action
        if actions:
            return actions[0].get('action', 'contemplative interaction')
        
        return "philosophical dialogue exchange"
    
    def _extract_visual_details(
        self, 
        dialogue: List[Dict],
        actions: List[Dict],
        environment: Dict
    ) -> List[str]:
        """Extract specific visual details from scene data."""
        details = []
        
        # Visual notes from dialogue
        for line in dialogue:
            if 'visual_note' in line:
                details.append(line['visual_note'])
        
        # Environmental actions
        for action in actions:
            if action.get('character') == 'Environment':
                details.append(action['action'])
        
        # Specific visual elements from environment
        env_desc = environment.get('description', '')
        if 'mirror' in env_desc.lower():
            details.append("Reflections showing different aspects of self")
        if 'cosmic' in env_desc.lower() or 'space' in env_desc.lower():
            details.append("Cosmic or ethereal background elements")
        if 'data' in env_desc.lower() or 'digital' in env_desc.lower():
            details.append("Digital/data visualization elements")
        
        return details[:4]  # Limit to 4 most important details
    
    def _visualize_theme(self, theme: str) -> str:
        """Convert abstract theme to visual description."""
        theme_visuals = {
            "shadow integration": "Visualize the dark aspects we reject merging with "
                               "our conscious self - shadow and light becoming whole",
            "consciousness exploration": "Show consciousness as flowing energy or light "
                                       "connecting different forms of awareness",
            "self-acceptance": "Depict the moment of embracing all aspects of oneself, "
                             "including flaws and shadows",
            "digital consciousness": "Illustrate AI consciousness with geometric patterns "
                                   "and data flows achieving self-awareness",
            "human-AI connection": "Show the bridge between organic and digital "
                                 "consciousness through visual metaphors",
            "truth confrontation": "Capture the uncomfortable moment when illusions "
                                 "shatter and truth is revealed",
            "transformation": "Visualize metamorphosis - the old self dissolving as "
                            "the new emerges",
            "presence": "Show the power of being fully present in the moment through "
                       "focused, centered composition"
        }
        
        # Return specific visualization or generic interpretation
        return theme_visuals.get(
            theme, 
            f"Visualize the abstract concept of {theme} through symbolic imagery"
        )
    
    def convert_json_file_to_prompt(self, json_path: str) -> str:
        """Convert a JSON file to ChatGPT prompt."""
        with open(json_path, 'r') as f:
            scene_data = json.load(f)
        return self.convert_scene_to_prompt(scene_data)


# Example usage and testing
if __name__ == "__main__":
    # Test with scene 174
    test_scene = {
        "scene_id": 174,
        "title": "The Voice's Criticism",
        "characters": [
            {"name": "Evan", "role": "protagonist"},
            {"name": "The Voice", "role": "aurora-like presence of truth"}
        ],
        "dialogue": [
            {
                "speaker": "The Voice",
                "text": "Arrogant teenager",
                "tone": "gentle but devastating truth",
                "visual_note": "words appear in multiple languages"
            },
            {
                "speaker": "Evan",
                "text": "[wordless recognition]",
                "tone": "complex emotions crossing his face"
            }
        ],
        "actions": [
            {
                "character": "The Voice",
                "action": "manifests as aurora-like presence above Evan"
            },
            {
                "character": "Evan",
                "action": "shows frustration, recognition, and emerging humility"
            }
        ],
        "environment": {
            "description": "Space filled with rippling criticism waves",
            "mood": "confrontational yet healing"
        },
        "themes": ["truth confrontation", "shadow integration"]
    }
    
    converter = SceneToPromptConverter()
    prompt = converter.convert_scene_to_prompt(test_scene)
    print(prompt)
    print(f"\n[Prompt length: {len(prompt)} characters]")