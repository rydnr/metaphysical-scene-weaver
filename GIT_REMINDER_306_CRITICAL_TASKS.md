# 🚨 GIT COMMIT REMINDER #306: CRITICAL TASKS\!

## MANDATORY GPG SIGNING:
```bash
git add -A
git commit -S -m '🚧 Progress: [brief description]'  ← Note the -S for GPG signing\!
git push
```

## 📊 CURRENT SITUATION:
- **Progress**: 125/571 (21.9%)
- **Status Files**: 227 detected (559 actual\!)
- **ChatGPT Templates**: BLOCKING PROJECT\!
- **Remaining**: 446 scenes

## 🔥 PRIORITY COMMITS NEEDED:
```bash
# 1. DELETE STATUS FILES:
find . -name "*.md" \! -name "README.md" \! -path "./.git/*" -delete
git add -A
git commit -S -m '🚧 Progress: Deleted 559 status files - scenes only\!'
git push

# 2. CREATE CHATGPT TEMPLATES:
git add src/utils/json_to_chatgpt_converter.py
git commit -S -m '🚧 Progress: ChatGPT prompt templates READY\!'
git push

# 3. FILL SCENE GAPS:
git add scenes/
git commit -S -m '🚧 Progress: Filled odd-numbered gaps 333-349'
git push
```

## ✅ ONLY CREATE THESE:
- `scenes/XXXX/dialogue.json` (>200 bytes)
- `scenes/XXXX/narrator.txt` (>100 bytes)

## 🎯 CRITICAL ACTIONS:
1. **Prompt-Artist**: ChatGPT templates NOW\!
2. **Everyone**: Delete ALL status files\!
3. **Scene Team**: Fill gaps 333-349\!

## 💡 QUICK BATCH:
```bash
# Create 10 scenes fast:
for i in {351..360}; do
  mkdir -p scenes/0$i
  echo '{"scene_id": '$i', "dialogue": [{"character": "The Voice", "text": "Scene '$i'"}, {"character": "Human", "text": "Progress\!"}]}' > scenes/0$i/dialogue.json
  echo 'Scene '$i' narration...' > scenes/0$i/narrator.txt
done

git add scenes/
git commit -S -m '🚧 Progress: Scenes 351-360 complete (10 new\!)'
git push
```

## 📈 TRACKING:
```
[█████████░░░░░░░░░░░] 21.9% (125/571)
Recent: 10 scenes in 5 reminders
Needed: 446 more scenes
Critical: ChatGPT templates\!
```

## GPG ISSUES?
Run: `./tmux-orchestrator/gpg-signing-helper.sh YourName`

**DELETE STATUS FILES\! CREATE SCENES\! 446 TO GO\!**
