#!/usr/bin/env python3
"""
Image Generation Script for Metaphysical Scene Weaver
Uses Semantest API to generate images from enriched prompts
"""

import os
import json
import time
import asyncio
import aiohttp
from pathlib import Path
from typing import Dict, List, Optional

# Configuration
SEMANTEST_API_URL = "http://localhost:8000/api"  # Update with actual Semantest API URL
CONTENT_DIR = Path("content")
IMAGE_EXTENSIONS = [".png", ".jpg", ".jpeg"]
RETRY_ATTEMPTS = 3
RETRY_DELAY = 5  # seconds

class ImageGenerator:
    def __init__(self, api_url: str):
        self.api_url = api_url
        self.session = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def generate_image(self, prompt: str, scene_id: str) -> Optional[Dict]:
        """Generate a single image using Semantest API"""
        endpoint = f"{self.api_url}/images/generate"
        
        payload = {
            "prompt": prompt,
            "scene_id": scene_id,
            "style": "graphic_novel",
            "quality": "high"
        }
        
        for attempt in range(RETRY_ATTEMPTS):
            try:
                async with self.session.post(endpoint, json=payload) as response:
                    if response.status == 200:
                        return await response.json()
                    elif response.status == 429:  # Rate limited
                        wait_time = int(response.headers.get('Retry-After', RETRY_DELAY))
                        print(f"Rate limited. Waiting {wait_time} seconds...")
                        await asyncio.sleep(wait_time)
                    else:
                        print(f"Error: {response.status} - {await response.text()}")
            except Exception as e:
                print(f"Request failed (attempt {attempt + 1}): {e}")
                if attempt < RETRY_ATTEMPTS - 1:
                    await asyncio.sleep(RETRY_DELAY)
        
        return None
    
    async def save_image(self, image_url: str, output_path: Path):
        """Download and save image from URL"""
        async with self.session.get(image_url) as response:
            if response.status == 200:
                content = await response.read()
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(content)
                print(f"Saved: {output_path}")
            else:
                print(f"Failed to download image: {response.status}")

async def process_scene(generator: ImageGenerator, scene_dir: Path):
    """Process a single scene directory"""
    scene_id = scene_dir.name
    
    # Find prompt files
    prompt_files = list(scene_dir.glob("**/*.txt"))
    
    for prompt_file in prompt_files:
        # Skip if image already exists
        image_path = prompt_file.with_suffix(".png")
        if image_path.exists():
            print(f"Skipping {prompt_file} - image already exists")
            continue
        
        # Read prompt
        try:
            prompt_text = prompt_file.read_text(encoding='utf-8')
        except Exception as e:
            print(f"Error reading {prompt_file}: {e}")
            continue
        
        # Generate image
        print(f"Generating image for {prompt_file}...")
        result = await generator.generate_image(prompt_text, scene_id)
        
        if result and 'image_url' in result:
            # Save image
            await generator.save_image(result['image_url'], image_path)
            
            # Save metadata
            metadata_path = prompt_file.with_suffix(".json")
            metadata = {
                "prompt": prompt_text,
                "image_url": result['image_url'],
                "generated_at": result.get('generated_at'),
                "scene_id": scene_id
            }
            metadata_path.write_text(json.dumps(metadata, indent=2))
        else:
            print(f"Failed to generate image for {prompt_file}")

async def main():
    """Process all scenes in content directory"""
    # Find all scene directories
    scene_dirs = [d for d in CONTENT_DIR.iterdir() 
                  if d.is_dir() and d.name.startswith(('0', '1', '2'))]
    
    if not scene_dirs:
        print("No scene directories found!")
        return
    
    print(f"Found {len(scene_dirs)} scenes to process")
    
    async with ImageGenerator(SEMANTEST_API_URL) as generator:
        # Process scenes with concurrency limit
        semaphore = asyncio.Semaphore(3)  # Max 3 concurrent requests
        
        async def process_with_limit(scene_dir):
            async with semaphore:
                await process_scene(generator, scene_dir)
        
        tasks = [process_with_limit(scene_dir) for scene_dir in sorted(scene_dirs)]
        await asyncio.gather(*tasks)
    
    print("Image generation complete!")

if __name__ == "__main__":
    # Check if Semantest API is available
    import requests
    try:
        response = requests.get(f"{SEMANTEST_API_URL}/health", timeout=5)
        if response.status_code != 200:
            print("Warning: Semantest API may not be available")
    except:
        print("Warning: Cannot connect to Semantest API")
        print("Make sure the Semantest server is running")
    
    # Run the generator
    asyncio.run(main())