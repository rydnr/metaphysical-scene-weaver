#\!/usr/bin/env bash
# Broadcast to all creative team members

SESSION="metaphysical-creative"
MESSAGE="$1"

for window in 0 1 2 3 4 5 6; do
    /home/chous/work/tmux-orchestrator/send-claude-message.sh "$SESSION:$window" "$MESSAGE"
    sleep 0.5
done

echo "Message broadcast to all creative team members"
