#!/usr/bin/env python3
"""
Semantest ChatGPT Browser Addon Automation Script
Simple script to call the semantest-chatgpt browser addon for image generation
"""

import os
import json
import time
from pathlib import Path
from typing import Dict, List

# Configuration
CONTENT_DIR = Path("content")
OUTPUT_DIR = Path("generated_images")
PROMPT_FILENAME = "prompt.txt"
ENRICHED_PROMPT_FILENAME = "prompt_enriched.txt"

class SemantestAutomation:
    """Simple automation for Semantest ChatGPT browser addon"""
    
    def __init__(self):
        self.prompts_to_process = []
        self.results = []
        
    def collect_prompts(self):
        """Collect all prompts from content folders"""
        print("📂 Collecting prompts from content folders...")
        
        for scene_dir in sorted(CONTENT_DIR.iterdir()):
            if not scene_dir.is_dir():
                continue
                
            scene_id = scene_dir.name
            
            # Check for enriched prompt first, then regular prompt
            enriched_path = scene_dir / ENRICHED_PROMPT_FILENAME
            regular_path = scene_dir / PROMPT_FILENAME
            
            prompt_path = None
            if enriched_path.exists():
                prompt_path = enriched_path
            elif regular_path.exists():
                prompt_path = regular_path
                
            if prompt_path:
                try:
                    prompt_text = prompt_path.read_text(encoding='utf-8')
                    # Extract just the visual description (skip narrator lines)
                    lines = prompt_text.strip().split('\n')
                    visual_prompt = []
                    for line in lines:
                        if not line.startswith('[NARRATOR'):
                            visual_prompt.append(line)
                    
                    clean_prompt = '\n'.join(visual_prompt).strip()
                    
                    self.prompts_to_process.append({
                        'scene_id': scene_id,
                        'prompt': clean_prompt,
                        'source_file': str(prompt_path)
                    })
                    print(f"  ✅ Found prompt for scene {scene_id}")
                except Exception as e:
                    print(f"  ❌ Error reading {prompt_path}: {e}")
        
        print(f"\n📊 Total prompts collected: {len(self.prompts_to_process)}")
        
    def generate_batch_file(self):
        """Generate a batch file for manual processing"""
        batch_file = Path("semantest_batch.json")
        
        print("\n📝 Generating batch file for Semantest...")
        
        batch_data = {
            "project": "Metaphysical Scene Weaver",
            "style": "philosophical graphic novel, surrealist elements",
            "quality": "high",
            "scenes": self.prompts_to_process
        }
        
        with open(batch_file, 'w', encoding='utf-8') as f:
            json.dump(batch_data, f, indent=2, ensure_ascii=False)
            
        print(f"✅ Batch file created: {batch_file}")
        print("\n📋 Instructions for manual processing:")
        print("1. Open ChatGPT in your browser")
        print("2. Ensure Semantest addon is active")
        print("3. Copy prompts from semantest_batch.json")
        print("4. Process each scene through the addon")
        print("5. Save generated images to generated_images/ folder")
        
    def create_individual_files(self):
        """Create individual prompt files for easier manual processing"""
        prompt_dir = Path("prompts_for_semantest")
        prompt_dir.mkdir(exist_ok=True)
        
        print(f"\n📁 Creating individual prompt files in {prompt_dir}/...")
        
        for item in self.prompts_to_process:
            scene_id = item['scene_id']
            prompt = item['prompt']
            
            # Create a clean filename
            filename = f"{scene_id}_prompt.txt"
            filepath = prompt_dir / filename
            
            # Add style suffix to each prompt
            full_prompt = f"{prompt}\n\nStyle: philosophical graphic novel, surrealist elements, high quality digital art"
            
            filepath.write_text(full_prompt, encoding='utf-8')
            print(f"  ✅ Created {filename}")
            
        print(f"\n✅ All prompt files created in {prompt_dir}/")
        
    def create_html_interface(self):
        """Create a simple HTML interface for easier copying"""
        html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Semantest Prompt Interface</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; }
        .scene { background: white; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .scene-id { font-weight: bold; color: #333; margin-bottom: 10px; }
        .prompt { background: #f9f9f9; padding: 15px; border: 1px solid #ddd; border-radius: 4px; margin: 10px 0; }
        .copy-btn { background: #4CAF50; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; }
        .copy-btn:hover { background: #45a049; }
        .status { color: #666; font-size: 14px; margin-top: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎨 Metaphysical Scene Weaver - Semantest Prompts</h1>
        <p>Click "Copy" next to each prompt, then paste into ChatGPT with Semantest addon active.</p>
        <hr>
"""
        
        for item in self.prompts_to_process:
            scene_id = item['scene_id']
            prompt = item['prompt']
            full_prompt = f"{prompt}\n\nStyle: philosophical graphic novel, surrealist elements, high quality digital art"
            
            # Escape quotes for JavaScript
            escaped_prompt = full_prompt.replace('"', '\\"').replace('\n', '\\n')
            
            html_content += f"""
        <div class="scene">
            <div class="scene-id">Scene {scene_id}</div>
            <div class="prompt">{prompt}</div>
            <button class="copy-btn" onclick="copyToClipboard('{scene_id}', &quot;{escaped_prompt}&quot;)">Copy Prompt</button>
            <div class="status" id="status-{scene_id}"></div>
        </div>
"""
        
        html_content += """
    </div>
    <script>
    function copyToClipboard(sceneId, text) {
        navigator.clipboard.writeText(text).then(function() {
            document.getElementById('status-' + sceneId).textContent = '✅ Copied to clipboard!';
            setTimeout(() => {
                document.getElementById('status-' + sceneId).textContent = '';
            }, 2000);
        }, function(err) {
            document.getElementById('status-' + sceneId).textContent = '❌ Copy failed';
        });
    }
    </script>
</body>
</html>
"""
        
        html_file = Path("semantest_interface.html")
        html_file.write_text(html_content, encoding='utf-8')
        print(f"\n🌐 HTML interface created: {html_file}")
        print("   Open this file in your browser for easy prompt copying!")

def main():
    """Main execution"""
    print("🚀 Semantest Browser Automation Script")
    print("=" * 50)
    
    automation = SemantestAutomation()
    
    # Collect all prompts
    automation.collect_prompts()
    
    if not automation.prompts_to_process:
        print("\n❌ No prompts found to process!")
        return
    
    # Generate outputs
    automation.generate_batch_file()
    automation.create_individual_files()
    automation.create_html_interface()
    
    print("\n✨ Setup complete! You can now:")
    print("1. Open semantest_interface.html in your browser")
    print("2. Use ChatGPT with Semantest addon to generate images")
    print("3. Save generated images to the generated_images/ folder")
    
    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)
    print(f"\n📁 Output directory ready: {OUTPUT_DIR}/")

if __name__ == "__main__":
    main()