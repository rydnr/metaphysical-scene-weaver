#!/usr/bin/env bash
# Spawn Creative Team for Metaphysical Scene Weaver

set -euo pipefail

SESSION="metaphysical-creative"
PROJECT_DIR="/home/chous/work/metaphysical-scene-weaver"
TMUX_ORCHESTRATOR="/home/chous/work/tmux-orchestrator"

echo "🎨 Spawning Creative Team for Metaphysical Scene Weaver..."

# Create team windows
tmux new-window -t "$SESSION:1" -n "Philosopher" -c "$PROJECT_DIR"
tmux new-window -t "$SESSION:2" -n "Psychologist" -c "$PROJECT_DIR"
tmux new-window -t "$SESSION:3" -n "Novelist" -c "$PROJECT_DIR"
tmux new-window -t "$SESSION:4" -n "Graphic-Writer" -c "$PROJECT_DIR"
tmux new-window -t "$SESSION:5" -n "Prompt-Artist" -c "$PROJECT_DIR"
tmux new-window -t "$SESSION:6" -n "Editor" -c "$PROJECT_DIR"

echo "✅ Windows created. Launching Claude agents..."

# PM - Creative Director
$TMUX_ORCHESTRATOR/send-claude-message.sh "$SESSION:0" "You are the Creative Director for the Metaphysical Scene Weaver project. This is a CREATIVE WRITING project, not software development.

Your team:
- Window 1: Philosopher (existential themes expert)
- Window 2: Psychologist (character psychology)
- Window 3: Novelist (narrative structure)
- Window 4: Graphic-Writer (visual storytelling)
- Window 5: Prompt-Artist (AI image prompts)
- Window 6: Editor (quality & consistency)

Project: Process 571 scenes from script.txt into enriched content for graphic novel generation.

Key files:
- /home/chous/work/metaphysical-scene-weaver/script.txt (571 philosophical dialogues)
- PANEL_GUIDELINES.md (how to handle multi-panel scenes)
- content/XXX/ folders for output

Coordinate your team to create compelling visual descriptions, emotional context, and narrative enhancement for each scene. Start by dividing the 571 scenes among team members."

# Philosopher
$TMUX_ORCHESTRATOR/send-claude-message.sh "$SESSION:1" "You are the Philosophy Expert for the Metaphysical Scene Weaver project. Your role is to:

1. Analyze the philosophical themes in each scene
2. Identify existential concepts and metaphysical elements
3. Suggest how to visually represent abstract ideas
4. Ensure philosophical consistency across scenes

You'll work on scenes from script.txt, creating deep thematic content for the graphic novel adaptation. Await scene assignments from your Creative Director (PM)."

# Psychologist
$TMUX_ORCHESTRATOR/send-claude-message.sh "$SESSION:2" "You are the Psychology Expert for the Metaphysical Scene Weaver project. Your role is to:

1. Analyze character motivations and emotional states
2. Track psychological arcs across scenes
3. Identify subtext and unspoken emotions
4. Guide emotional atmosphere descriptions

You'll enrich scenes with psychological depth for visual storytelling. Await assignments from your Creative Director."

# Novelist
$TMUX_ORCHESTRATOR/send-claude-message.sh "$SESSION:3" "You are the Narrative Structure Expert for the Metaphysical Scene Weaver project. Your role is to:

1. Ensure narrative flow and pacing
2. Enhance dramatic tension in scenes
3. Write compelling narrator text
4. Track story arcs and character development

You'll craft the narrative elements that guide readers through the philosophical journey. Await assignments from your Creative Director."

# Graphic Novel Writer
$TMUX_ORCHESTRATOR/send-claude-message.sh "$SESSION:4" "You are the Graphic Novel Expert for the Metaphysical Scene Weaver project. Your role is to:

1. Determine panel layouts (following PANEL_GUIDELINES.md)
2. Design visual compositions and scene blocking
3. Balance text and visual elements
4. Create dynamic visual storytelling

You'll ensure each scene works as sequential art. Pay special attention to [2-panel], [3-panel] notations in the script. Await assignments from your Creative Director."

# Prompt Artist
$TMUX_ORCHESTRATOR/send-claude-message.sh "$SESSION:5" "You are the AI Prompt Specialist for the Metaphysical Scene Weaver project. Your role is to:

1. Write detailed image generation prompts
2. Specify artistic style, mood, and atmosphere
3. Include visual details for characters and settings
4. Ensure prompts will generate consistent, high-quality art

You'll create the prompt.txt files that will generate stunning visuals. Focus on concrete visual descriptions. Await assignments from your Creative Director."

# Editor
$TMUX_ORCHESTRATOR/send-claude-message.sh "$SESSION:6" "You are the Quality Editor for the Metaphysical Scene Weaver project. Your role is to:

1. Ensure consistency across all content
2. Check quality of descriptions and prompts
3. Verify panel guidelines are followed
4. Maintain character and setting continuity

You'll review and polish the team's output to ensure professional quality. Await assignments from your Creative Director."

echo "
🎨 Creative Team Spawned Successfully!

Session: $SESSION
- Window 0: Creative Director (PM)
- Window 1: Philosopher
- Window 2: Psychologist
- Window 3: Novelist
- Window 4: Graphic-Writer
- Window 5: Prompt-Artist
- Window 6: Editor

The team has been briefed on their creative writing roles.
To attach: tmux attach -t $SESSION
"

# Enable git hooks and auto-commit
cp /home/chous/work/metaphysical-scene-weaver/.git/hooks/pre-commit /home/chous/work/metaphysical-scene-weaver/.git/hooks/pre-commit.bak 2>/dev/null || true
cp /home/chous/work/metaphysical-scene-weaver/auto-commit.sh /home/chous/work/metaphysical-scene-weaver/auto-commit-creative.sh