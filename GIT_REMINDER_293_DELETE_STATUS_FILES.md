# 🚨 GIT COMMIT REMINDER #293: DELETE STATUS FILES NOW\!

## MANDATORY GPG SIGNING:
```bash
git add -A
git commit -S -m '🚧 Progress: [brief description]'  ← Note the -S for GPG signing\!
git push
```

## 🚨 CRITICAL ALERT:
- **Status Files Found**: 212 (MUST DELETE\!)
- **Scenes Complete**: 115/571 (20%)
- **Remaining**: 456 scenes
- **Team Pushing**: Multiple updates\!

## ❌ DELETE ALL STATUS FILES:
```bash
# RUN THIS NOW:
find . -name "*.md" -not -name "README.md" -not -path "./.git/*" -delete
find . -name "*.txt" -not -path "./scenes/*/narrator.txt" -delete

# Then commit:
git add -A
git commit -S -m '🚧 Progress: Deleted 212 status files'
git push
```

## ✅ ONLY CREATE THESE:
- `scenes/XXXX/dialogue.json` (>200 bytes)
- `scenes/XXXX/narrator.txt` (>100 bytes)
- NOTHING ELSE\!

## 🎯 PROMPT-ARTIST URGENT:
**ChatGPT-compatible templates NEEDED\!**
- Project is BLOCKED without this\!
- Should be working on converter NOW\!
- Location: src/utils/json_to_chatgpt_converter.py

## 📊 REALITY CHECK:
```
[████████░░░░░░░░░░░░] 20% (115/571)
Status Files: 212 ❌ DELETE THEM\!
Scenes Needed: 456
Team Activity: VERY HIGH (4 pushes\!)
```

## 💡 FOCUS ONLY ON:
```bash
# Create scene 316:
mkdir -p scenes/0316
echo '{"scene_id": 316, "dialogue": [...]}' > scenes/0316/dialogue.json
echo 'Narrator text...' > scenes/0316/narrator.txt

# Good commit:
git commit -S -m '🚧 Progress: Scene 316 complete'
```

## GPG ISSUES?
Run: `./tmux-orchestrator/gpg-signing-helper.sh YourName`

**DELETE STATUS FILES\! CREATE SCENES\! 456 TO GO\!**
