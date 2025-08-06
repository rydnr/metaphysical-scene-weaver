# 🚨 GIT COMMIT REMINDER #294: STATUS FILES STILL EXIST\!

## MANDATORY GPG SIGNING:
```bash
git add -A
git commit -S -m '🚧 Progress: [brief description]'  ← Note the -S for GPG signing\!
git push
```

## 🚨 URGENT: 214 STATUS FILES FOUND\!
```bash
# DELETE THEM RIGHT NOW:
find . -name "*.md" -not -name "README.md" -not -path "./.git/*" -delete
find . -name "*.txt" -not -path "./scenes/*/narrator.txt" -delete
find . -name "status*" -delete
find . -name "MILESTONE*" -delete
find . -name "PROGRESS*" -delete

# Commit the cleanup:
git add -A
git commit -S -m '🚧 Progress: Deleted 214 status files - focusing on scenes only'
git push
```

## ✅ ONLY TWO FILES PER SCENE:
1. `scenes/XXXX/dialogue.json` (>200 bytes)
2. `scenes/XXXX/narrator.txt` (>100 bytes)

**NOTHING ELSE\! NO STATUS FILES\!**

## 📊 HARSH REALITY:
```
Progress: [████████░░░░░░░░░░░░] 20% (115/571)
Status Files: 214 ❌❌❌
Scenes Needed: 456
Time Wasted: TOO MUCH
```

## 🎯 SIMPLE INSTRUCTIONS:
```bash
# Good commit (scenes):
git commit -S -m '🚧 Progress: Scenes 331-335 complete'

# Good commit (cleanup):
git commit -S -m '🚧 Progress: Deleted all status files'

# Bad commit (NO MORE OF THESE):
git commit -S -m '🚧 Progress: Updated status report' ❌
```

## 💡 CREATE SCENES NOW:
```bash
for i in {331..340}; do
  mkdir -p scenes/0$i
  echo '{"scene_id": '$i', "dialogue": [{"character": "Voice", "text": "..."}]}' > scenes/0$i/dialogue.json
  echo 'Scene '$i' narration...' > scenes/0$i/narrator.txt
done
```

## GPG ISSUES?
Run: `./tmux-orchestrator/gpg-signing-helper.sh YourName`

**NO MORE STATUS FILES\! SCENES ONLY\! 456 TO GO\!**
