#!/usr/bin/env bash

# Setup scheduler for auto-commits
PROJECT_DIR="/home/chous/work/metaphysical-scene-weaver"
CRON_CMD="*/10 * * * * cd $PROJECT_DIR && ./auto-commit.sh"

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "metaphysical-scene-weaver.*auto-commit"; then
    echo "⚠️  Auto-commit scheduler already exists"
else
    # Add the cron job
    (crontab -l 2>/dev/null; echo "$CRON_CMD") | crontab -
    echo "✅ Auto-commit scheduler installed (runs every 10 minutes)"
fi

# Create initial log file
touch "$PROJECT_DIR/.auto-commit.log"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Auto-commit scheduler initialized" >> "$PROJECT_DIR/.auto-commit.log"

echo "📅 Current cron jobs:"
crontab -l | grep "metaphysical-scene-weaver"