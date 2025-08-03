#!/usr/bin/env bash
# Simple script to generate images for our consciousness/reality story

echo "🎨 Metaphysical Scene Weaver - Image Generation"
echo "=============================================="
echo ""
echo "This script will:"
echo "1. Read prompts from content/001/ through content/020/"
echo "2. Call Semantest API to generate images"
echo "3. Save images next to prompt files"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found!"
    exit 1
fi

# Check if content folders exist
if [ ! -d "content" ]; then
    echo "❌ Content directory not found!"
    exit 1
fi

# Count available scenes
SCENE_COUNT=$(find content -maxdepth 1 -type d -name "[0-9]*" | wc -l)
echo "✅ Found $SCENE_COUNT scenes ready for generation"
echo ""

# Run the generator
echo "🚀 Starting image generation..."
echo "Note: This requires Semantest API to be running"
echo ""

python3 generate_images.py

echo ""
echo "✅ Generation complete!"
