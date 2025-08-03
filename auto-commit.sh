#!/usr/bin/env bash

# Auto-commit script for Metaphysical Scene Weaver team
# Runs every 10 minutes to commit work in progress

PROJECT_DIR="/home/chous/work/metaphysical-scene-weaver"
LOG_FILE="$PROJECT_DIR/.auto-commit.log"

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# Function to get appropriate emoji based on changes
get_emoji() {
    local changes="$1"
    
    # Philosophy changes
    if echo "$changes" | grep -q "philosophical_interpreter"; then
        echo "🧠"
    # Emotion changes
    elif echo "$changes" | grep -q "emotional_mapper"; then
        echo "❤️"
    # Script parsing changes
    elif echo "$changes" | grep -q "script_parser"; then
        echo "📝"
    # Integration changes
    elif echo "$changes" | grep -q "integrations\|api"; then
        echo "🔌"
    # Prompt changes
    elif echo "$changes" | grep -q "prompt_generator"; then
        echo "🎨"
    # Test changes
    elif echo "$changes" | grep -q "test"; then
        echo "🧪"
    # Documentation changes
    elif echo "$changes" | grep -q "\.md"; then
        echo "📚"
    # Default work in progress
    else
        echo "🚧"
    fi
}

# Check if git directory exists
if [ ! -d "$PROJECT_DIR/.git" ]; then
    log "ERROR: Not a git repository"
    exit 1
fi

cd "$PROJECT_DIR"

# Check for changes
if git diff --quiet && git diff --cached --quiet; then
    log "No changes to commit"
    exit 0
fi

# Get list of changed files
CHANGES=$(git status --porcelain)
EMOJI=$(get_emoji "$CHANGES")

# Stage all changes
git add -A

# Create commit message
COMMIT_MSG="$EMOJI WIP: Auto-commit $(date '+%H:%M')"

# Add summary of changes
if [ $(echo "$CHANGES" | wc -l) -gt 0 ]; then
    COMMIT_MSG="$COMMIT_MSG

Changed files:"
    echo "$CHANGES" | while read line; do
        COMMIT_MSG="$COMMIT_MSG
- ${line:3}"
    done
fi

# Commit with GPG signing
git commit -S -m "$COMMIT_MSG" > /dev/null 2>&1

if [ $? -eq 0 ]; then
    log "Successfully committed changes"
else
    log "ERROR: Failed to commit changes"
    exit 1
fi