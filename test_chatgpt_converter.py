#!/usr/bin/env python3
"""Test the ChatGPT converter with actual scene files."""

import json
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from utils.json_to_chatgpt_converter import SceneToPromptConverter

def test_converter():
    """Test the converter with scene 174."""
    # Load scene 174
    with open('content/0174/dialogue.json', 'r') as f:
        scene = json.load(f)
    
    # Convert to prompt
    converter = SceneToPromptConverter()
    prompt = converter.convert_scene_to_prompt(scene)
    
    print('SCENE 174 CHATGPT PROMPT:')
    print('=' * 70)
    print(prompt)
    print('=' * 70)
    print(f'\nPrompt length: {len(prompt)} characters')
    print(f'Suitable for ChatGPT: {"YES" if len(prompt) < 2000 else "NO (too long)"}')
    
    # Save to file for easy testing
    with open('content/0174/chatgpt_prompt.txt', 'w') as f:
        f.write(prompt)
    print(f'\nPrompt saved to: content/0174/chatgpt_prompt.txt')

if __name__ == "__main__":
    test_converter()