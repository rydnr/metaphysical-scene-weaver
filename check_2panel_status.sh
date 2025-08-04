#!/bin/bash

echo "=== 2-PANEL SCENE TRANSFORMATION STATUS ==="
echo

completed=0
total=0

for scene in 070 074 076 086 094 106 108 110 114 116 120 122 124 126 130 132 134 138 142 144; do
  total=$((total + 1))
  files=$(ls /home/chous/work/metaphysical-scene-weaver/content/scenes/$scene 2>/dev/null | wc -l)
  if [ $files -gt 1 ]; then
    echo "✅ Scene $scene: TRANSFORMED (has $files files)"
    completed=$((completed + 1))
  else
    echo "❌ Scene $scene: NEEDS WORK (only dialogue)"
  fi
done

echo
echo "=== SUMMARY ==="
echo "Completed: $completed / $total 2-panel scenes"
percentage=$((completed * 100 / total))
echo "Progress: ${percentage}%"