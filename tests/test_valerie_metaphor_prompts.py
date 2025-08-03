"""Test Valerie emergence scene - Philosophical metaphor to visual prompt pipeline."""

# For Iris to test with the metaphor engine

from src.processors.metaphor_translator import MetaphorTranslator
from src.processors.philosophical_interpreter import PhilosophicalInterpreter

# Test input for Valerie's emergence
valerie_test_case = {
    "entry_id": "009",
    "dialogue": "I am the space between your thoughts, Evan. The pause between heartbeats.",
    "philosophy": {
        "primary_concept": "liminality",
        "depth_level": 3,
        "visual_symbols": ["threshold_spaces", "particle_clouds", "negative_space"]
    },
    "emotion": {
        "primary": "uncanny_wonder",
        "intensity": 0.85
    }
}

# Expected metaphor engine output -> prompt structure
expected_prompts = {
    "base_prompt": {
        "tokens": 80,
        "structure": "[Style] + [Composition] + [Subject] + [Emotion] + [Effects] + [Quality]",
        "content": "Ethereal particle art style, peripheral edge lighting composition, feminine figure coalescing from negative space between shadows, uncanny wonder and recognition mood, slow materialization effects with iridescent particles, professional quality, liminal atmosphere"
    },
    
    "variations": [
        {
            "tokens": 20,
            "focus": "particle_detail",
            "content": "particles forming gossamer threads of possibility"
        },
        {
            "tokens": 20,
            "focus": "lighting",
            "content": "light emerging from shadow boundaries, edge-lit silhouette"
        },
        {
            "tokens": 20,
            "focus": "movement",
            "content": "slow coalescence from periphery inward, time-lapse effect"
        },
        {
            "tokens": 20,
            "focus": "atmosphere",
            "content": "threshold space, neither here nor there, between-state visualization"
        }
    ],
    
    "philosophical_enhancement": {
        "concept": "liminality",
        "visual_metaphor": "The space that defines becomes the defined",
        "narrator_voice": "mystic_poet",
        "depth_marker": "Level 3 - Paradoxical existence"
    }
}

# Metaphor patterns specific to liminality
liminality_metaphors = [
    "figure as the pause between notes",
    "negative space gaining substance",
    "threshold becoming destination",
    "gap that bridges",
    "absence that presences"
]

# For Quinn's validators
quality_criteria = {
    "philosophical_accuracy": 0.9,  # High - must capture liminality
    "emotion_alignment": 0.85,      # Must evoke uncanny wonder
    "prompt_structure": 1.0,        # Must follow Iris's format exactly
    "token_compliance": 1.0         # Must stay under 150 total
}