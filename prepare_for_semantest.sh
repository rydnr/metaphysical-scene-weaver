#!/usr/bin/env bash
# Prepare prompts for Semantest ChatGPT browser addon

echo "🎨 Preparing prompts for Semantest browser addon"
echo "==============================================="
echo ""

# Check Python availability
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found!"
    exit 1
fi

# Run the automation script
python3 semantest_browser_automation.py

echo ""
echo "📋 Next steps:"
echo "1. Open semantest_interface.html in your browser"
echo "2. Copy each prompt and paste into ChatGPT"
echo "3. Ensure Semantest addon is active"
echo "4. Generate images for all 20 scenes"
echo "5. Save images to generated_images/ folder"
echo ""
echo "Happy generating! 🚀"