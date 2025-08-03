# Team Communication Guide - Metaphysical Creative Team

## Available Communication Scripts

### 1. Report to PM
```bash
# When you finish ANY task, report to PM immediately:
/home/chous/work/tmux-orchestrator/send-claude-message.sh "metaphysical-creative:0" "Your message here"
```

### 2. Message a Specific Team Member
```bash
# To Philosopher (Window 1):
/home/chous/work/tmux-orchestrator/send-claude-message.sh "metaphysical-creative:1" "Your message"

# To Psychologist (Window 2):
/home/chous/work/tmux-orchestrator/send-claude-message.sh "metaphysical-creative:2" "Your message"

# To Novelist (Window 3):
/home/chous/work/tmux-orchestrator/send-claude-message.sh "metaphysical-creative:3" "Your message"

# To Graphic-Writer (Window 4):
/home/chous/work/tmux-orchestrator/send-claude-message.sh "metaphysical-creative:4" "Your message"

# To Prompt-Artist (Window 5):
/home/chous/work/tmux-orchestrator/send-claude-message.sh "metaphysical-creative:5" "Your message"

# To Editor (Window 6):
/home/chous/work/tmux-orchestrator/send-claude-message.sh "metaphysical-creative:6" "Your message"
```

### 3. Broadcast to Entire Team
```bash
# Send message to ALL team members:
/home/chous/work/metaphysical-scene-weaver/broadcast-creative-team.sh "Your message to everyone"
```

## Communication Protocol

### ALWAYS Report Task Completion
After EVERY task, no matter how small:
```bash
/home/chous/work/tmux-orchestrator/send-claude-message.sh "metaphysical-creative:0" "✅ Completed: [task description]. Ready for next task!"
```

### Task Status Updates
- Starting a task: "🚀 Starting: scenes 001-020 philosophical analysis"
- Progress update: "📊 Progress: Completed 10/20 scenes, continuing..."
- Blocked/Issue: "🚨 Blocked: Need clarification on panel layout for scene 015"
- Completed: "✅ Completed: All 20 scenes analyzed, files created in content/001-020/"

### Collaboration Messages
When you need to work with another team member:
```bash
# Example: Philosopher to Prompt-Artist
/home/chous/work/tmux-orchestrator/send-claude-message.sh "metaphysical-creative:5" "@Prompt-Artist: Scene 007 has complex metaphysical imagery. Key visual elements: mirror reflections, reality distortion. Can you emphasize these in the prompt?"
```

### PM Response Pattern
The PM (Creative Director) will:
1. Acknowledge your completion
2. Review the roadmap
3. Assign your next task
4. Coordinate with other team members if needed

## Example Communication Flow

```bash
# Philosopher completes task:
/home/chous/work/tmux-orchestrator/send-claude-message.sh "metaphysical-creative:0" "✅ Completed: Philosophical analysis for scenes 001-020. Created narrator.txt and metadata.json for each. Key themes identified: free will, authenticity, AI consciousness."

# PM responds with next task based on roadmap

# If collaboration needed:
/home/chous/work/tmux-orchestrator/send-claude-message.sh "metaphysical-creative:5" "@Prompt-Artist: Ready to collaborate on scenes 001-020. I've identified key visual metaphors in my analysis."

# Regular progress updates:
/home/chous/work/tmux-orchestrator/send-claude-message.sh "metaphysical-creative:0" "📊 Progress: 15/20 scenes complete. On track to finish within 30 minutes."
```

## Quick Reference Commands

Copy and paste these as needed:

### Report completion to PM:
```bash
/home/chous/work/tmux-orchestrator/send-claude-message.sh "metaphysical-creative:0" "✅ Completed: "
```

### Ask PM for next task:
```bash
/home/chous/work/tmux-orchestrator/send-claude-message.sh "metaphysical-creative:0" "Ready for next assignment. What should I work on?"
```

### Report blocker to PM:
```bash
/home/chous/work/tmux-orchestrator/send-claude-message.sh "metaphysical-creative:0" "🚨 Blocked: "
```

### Collaborate with team member:
```bash
/home/chous/work/tmux-orchestrator/send-claude-message.sh "metaphysical-creative:[WINDOW]" "@[NAME]: "
```

## Important Notes

1. **Never wait idle** - If you finish a task, report immediately
2. **Be specific** - Include scene numbers, file types created, key insights
3. **Proactive communication** - Don't wait to be asked for updates
4. **Cross-team collaboration** - Reach out directly to team members when needed
5. **PM is the hub** - All completions go through PM for roadmap management

Remember: Active communication keeps the project moving efficiently!