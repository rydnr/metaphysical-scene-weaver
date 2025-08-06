#!/bin/bash

for i in {1..170}; do
  scene=$(printf "%04d" $i)
  if [ -f "content/$scene/metadata.json" ]; then
    field_count=$(cat "content/$scene/metadata.json" | jq 'keys | length')
    if [ "$field_count" -eq "5" ]; then
      echo "Scene $scene: $field_count fields (needs enhancement)"
    fi
  fi
done