#!/usr/bin/env bash

# Hook management script for Metaphysical Scene Weaver
PROJECT_DIR="/home/chous/work/metaphysical-scene-weaver"

case "$1" in
    "enable")
        echo "✅ Enabling auto-commit hooks..."
        # For systemd systems
        if command -v systemctl &> /dev/null; then
            echo "Using systemd timers..."
            # Copy service files to user directory
            mkdir -p ~/.config/systemd/user/
            cp "$PROJECT_DIR/metaphysical-auto-commit.service" ~/.config/systemd/user/
            cp "$PROJECT_DIR/metaphysical-auto-commit.timer" ~/.config/systemd/user/
            systemctl --user daemon-reload
            systemctl --user enable metaphysical-auto-commit.timer
            systemctl --user start metaphysical-auto-commit.timer
            echo "✅ Systemd timer enabled"
        else
            echo "⚠️  Systemd not available, using simple background loop"
            # Fallback: Simple background script
            nohup bash -c 'while true; do /home/chous/work/metaphysical-scene-weaver/auto-commit.sh; sleep 600; done' > /dev/null 2>&1 &
            echo $! > "$PROJECT_DIR/.auto-commit.pid"
            echo "✅ Background auto-commit process started (PID: $(cat $PROJECT_DIR/.auto-commit.pid))"
        fi
        ;;
        
    "disable")
        echo "🛑 Disabling auto-commit hooks..."
        if command -v systemctl &> /dev/null; then
            systemctl --user stop metaphysical-auto-commit.timer
            systemctl --user disable metaphysical-auto-commit.timer
            echo "✅ Systemd timer disabled"
        else
            if [ -f "$PROJECT_DIR/.auto-commit.pid" ]; then
                kill $(cat "$PROJECT_DIR/.auto-commit.pid") 2>/dev/null
                rm "$PROJECT_DIR/.auto-commit.pid"
                echo "✅ Background process stopped"
            fi
        fi
        ;;
        
    "status")
        echo "📊 Auto-commit hook status:"
        if command -v systemctl &> /dev/null; then
            systemctl --user status metaphysical-auto-commit.timer
        else
            if [ -f "$PROJECT_DIR/.auto-commit.pid" ]; then
                PID=$(cat "$PROJECT_DIR/.auto-commit.pid")
                if ps -p $PID > /dev/null; then
                    echo "✅ Background process running (PID: $PID)"
                else
                    echo "❌ Background process not running"
                fi
            else
                echo "❌ No auto-commit process found"
            fi
        fi
        
        echo ""
        echo "📝 Recent commits:"
        if [ -f "$PROJECT_DIR/.auto-commit.log" ]; then
            tail -n 10 "$PROJECT_DIR/.auto-commit.log"
        else
            echo "No auto-commit log found"
        fi
        ;;
        
    *)
        echo "Usage: $0 {enable|disable|status}"
        echo ""
        echo "Commands:"
        echo "  enable  - Enable auto-commit hooks (every 10 minutes)"
        echo "  disable - Disable auto-commit hooks"
        echo "  status  - Show hook status and recent activity"
        exit 1
        ;;
esac