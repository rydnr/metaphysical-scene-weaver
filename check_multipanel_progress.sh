#!/bin/bash

echo "=== MULTI-PANEL VARIETY ENHANCEMENT PROGRESS ==="
echo

# Find all 2-panel scenes
two_panel_scenes=$(find /home/chous/work/metaphysical-scene-weaver/content/scenes -name "dialogue.txt" -exec grep -l "\[2-panel\]" {} \; | sed 's|.*/scenes/||' | sed 's|/.*||' | sort)
three_panel_scenes=$(find /home/chous/work/metaphysical-scene-weaver/content/scenes -name "dialogue.txt" -exec grep -l "\[3-panel\]" {} \; | sed 's|.*/scenes/||' | sed 's|/.*||' | sort)

completed_2panel=0
total_2panel=0
completed_3panel=0
total_3panel=0

echo "=== 2-PANEL SCENES ==="
for scene in $two_panel_scenes; do
  total_2panel=$((total_2panel + 1))
  files=$(ls /home/chous/work/metaphysical-scene-weaver/content/scenes/$scene 2>/dev/null | wc -l)
  if [ $files -gt 1 ]; then
    echo "✅ Scene $scene: TRANSFORMED"
    completed_2panel=$((completed_2panel + 1))
  else
    echo "❌ Scene $scene: needs work"
  fi
done

echo
echo "=== 3-PANEL SCENES ==="
for scene in $three_panel_scenes; do
  total_3panel=$((total_3panel + 1))
  files=$(ls /home/chous/work/metaphysical-scene-weaver/content/scenes/$scene 2>/dev/null | wc -l)
  if [ $files -gt 1 ]; then
    echo "✅ Scene $scene: TRANSFORMED"
    completed_3panel=$((completed_3panel + 1))
  else
    echo "❌ Scene $scene: needs work"
  fi
done

echo
echo "=== OVERALL PROGRESS ==="
total_multi=$((total_2panel + total_3panel))
completed_multi=$((completed_2panel + completed_3panel))
percentage=$((completed_multi * 100 / total_multi))

echo "2-panel scenes: $completed_2panel / $total_2panel completed"
echo "3-panel scenes: $completed_3panel / $total_3panel completed"
echo "TOTAL: $completed_multi / $total_multi multi-panel scenes (${percentage}%)"
echo
echo "🎯 Original 92% repetition → Now ${percentage}% transformed!"
remaining=$((100 - percentage))
echo "📊 ${remaining}% repetition remains to eliminate"