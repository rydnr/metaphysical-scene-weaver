#!/usr/bin/env bash

# Team broadcast script for Metaphysical Scene Weaver
# Usage: ./team-broadcast.sh "Your message to all team members"

if [ $# -eq 0 ]; then
    echo "Usage: $0 \"Your message to broadcast\""
    echo "Example: $0 \"Team meeting in 5 minutes\""
    exit 1
fi

MESSAGE="$1"
ORCHESTRATOR_DIR="/home/chous/work/tmux-orchestrator"

echo "Broadcasting to all team members..."

# Send to all windows except the sender
CURRENT_WINDOW=$(tmux display-message -p "#{window_index}" 2>/dev/null || echo "-1")

for i in {0..6}; do
    if [ "$i" != "$CURRENT_WINDOW" ]; then
        case $i in
            0) member="Aria";;
            1) member="Sophia";;
            2) member="Luna";;
            3) member="Rex";;
            4) member="Nova";;
            5) member="Iris";;
            6) member="Quinn";;
        esac
        
        echo "Sending to $member (window $i)..."
        "$ORCHESTRATOR_DIR/send-claude-message.sh" "metaphysical-team:$i" "[TEAM BROADCAST] $MESSAGE"
    fi
done

echo "✅ Broadcast complete!"