"""Simple test for emotional mapping without full imports."""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import only what we need directly
import json


def test_visual_rules_basic():
    """Test basic visual rules functionality."""
    print("\n=== Testing Visual Rules Basic Functionality ===")
    
    # Import locally to avoid circular dependencies
    from src.utils.visual_rules import VisualRules, EmotionCategory
    
    rules = VisualRules()
    
    # Test basic emotion mapping
    emotions = ['joy', 'sadness', 'melancholy', 'existential_dread', 'transcendent_joy']
    
    for emotion in emotions:
        visuals = rules.get_emotion_visuals(emotion, 0.7)
        print(f"\n{emotion.upper()}:")
        print(f"  Colors: {visuals['color_palette']['primary_colors'][:2]}")
        print(f"  Temperature: {visuals['color_palette']['temperature']:.1f}")
        print(f"  Lighting: {visuals['lighting']['color_temperature']}K")
        print(f"  Body language energy: {visuals['body_language']['energy_level']:.1f}")


def test_emotion_blending():
    """Test emotion blending functionality."""
    print("\n\n=== Testing Emotion Blending ===")
    
    from src.utils.visual_rules import VisualRules
    
    rules = VisualRules()
    
    # Test blending
    blends = [
        ('joy', 'sadness', 0.7),
        ('fear', 'wonder', 0.5),
        ('melancholy', 'serenity', 0.6)
    ]
    
    for primary, secondary, ratio in blends:
        result = rules.blend_emotions(primary, secondary, ratio)
        print(f"\n{primary} + {secondary} ({ratio}):")
        print(f"  Blended temperature: {result['color_palette']['temperature']:.2f}")
        print(f"  Energy transition: {result['body_language']['energy_level']:.2f}")


def test_cultural_variations():
    """Test cultural variations in visual rules."""
    print("\n\n=== Testing Cultural Variations ===")
    
    from src.utils.visual_rules import VisualRules
    
    rules = VisualRules()
    
    cultures = ['western', 'eastern', 'latin']
    
    for culture in cultures:
        visuals = rules.get_emotion_visuals('joy', 0.8, culture)
        cultural_mods = visuals['cultural_modifiers']
        
        print(f"\n{culture.upper()} culture:")
        print(f"  Emotion intensity: {cultural_mods['emotion_intensity']}")
        print(f"  Eye contact: {cultural_mods['eye_contact']}")
        print(f"  Personal space: {cultural_mods['personal_space']}")
        print(f"  Adjusted energy: {visuals['body_language']['energy_level']:.2f}")


def test_emotion_transitions():
    """Test emotion transition calculations."""
    print("\n\n=== Testing Emotion Transitions ===")
    
    from src.utils.visual_rules import VisualRules
    
    rules = VisualRules()
    
    # Test transition
    from_emotion = 'anger'
    to_emotion = 'serenity'
    
    print(f"\nTransition: {from_emotion} → {to_emotion}")
    
    for progress in [0.0, 0.25, 0.5, 0.75, 1.0]:
        transition = rules.get_transition_visuals(from_emotion, to_emotion, progress)
        
        print(f"\nProgress {progress:.0%}:")
        print(f"  Temperature: {transition['color_palette']['temperature']:.2f}")
        print(f"  Fog density: {transition['atmosphere']['fog_density']:.2f}")
        print(f"  Energy: {transition['body_language_shift']['energy_transition']:.2f}")


def test_cinematography_selection():
    """Test cinematography style selection."""
    print("\n\n=== Testing Cinematography Selection ===")
    
    from src.utils.visual_rules import VisualRules
    
    rules = VisualRules()
    
    emotions_intensities = [
        ('joy', 0.3),
        ('joy', 0.8),
        ('sadness', 0.6),
        ('existential_dread', 0.9),
        ('wonder', 0.7),
        ('melancholy', 0.5)
    ]
    
    for emotion, intensity in emotions_intensities:
        visuals = rules.get_emotion_visuals(emotion, intensity)
        cinema = visuals['cinematography']
        
        print(f"\n{emotion} (intensity {intensity}):")
        print(f"  Style: {rules._select_cinematography_style(emotion, intensity)}")
        print(f"  Primary shot: {cinema['shot_types'][0]}")
        print(f"  Camera movement: {cinema['camera_movement'][0]}")


def test_symbolic_elements():
    """Test symbolic element mapping."""
    print("\n\n=== Testing Symbolic Elements ===")
    
    from src.utils.visual_rules import VisualRules
    
    rules = VisualRules()
    
    emotions = ['melancholy', 'transcendent_joy', 'existential_dread', 'wonder']
    
    for emotion in emotions:
        symbols = rules.symbolic_elements[emotion]
        
        print(f"\n{emotion.upper()} symbols:")
        print(f"  Objects: {', '.join(symbols.objects[:3])}")
        print(f"  Natural: {', '.join(symbols.natural_elements[:2])}")
        print(f"  Motifs: {', '.join(symbols.recurring_motifs[:2])}")
        
        # Check cultural symbols
        if 'western' in symbols.cultural_symbols:
            print(f"  Western: {symbols.cultural_symbols['western'][0]}")
        if 'eastern' in symbols.cultural_symbols:
            print(f"  Eastern: {symbols.cultural_symbols['eastern'][0]}")


if __name__ == "__main__":
    print("VISUAL RULES TEST SUITE (SIMPLE)")
    print("=" * 50)
    
    test_visual_rules_basic()
    test_emotion_blending()
    test_cultural_variations()
    test_emotion_transitions()
    test_cinematography_selection()
    test_symbolic_elements()
    
    print("\n\nAll tests completed!")
    print("=" * 50)