#!/usr/bin/env bash

# Setup GPG signing for Metaphysical Scene Weaver team members
PROJECT_DIR="/home/chous/work/metaphysical-scene-weaver"

echo "🔐 Setting up GPG signing for Metaphysical Scene Weaver team..."

# Function to configure git for a specific team member
configure_git_for_member() {
    local member_name="$1"
    local member_email="$2"
    
    echo "Configuring for $member_name..."
    
    # Set git config in project directory
    git -C "$PROJECT_DIR" config user.name "$member_name"
    git -C "$PROJECT_DIR" config user.email "$member_email"
    git -C "$PROJECT_DIR" config commit.gpgsign true
    
    # Check if GPG key exists for this email
    if gpg --list-secret-keys "$member_email" &>/dev/null; then
        KEY_ID=$(gpg --list-secret-keys --keyid-format LONG "$member_email" | grep sec | awk '{print $2}' | cut -d'/' -f2)
        git -C "$PROJECT_DIR" config user.signingkey "$KEY_ID"
        echo "✅ GPG key found and configured for $member_name"
    else
        echo "⚠️  No GPG key found for $member_email"
        echo "   To create one: gpg --gen-key"
    fi
}

# Team member configurations
declare -A TEAM_MEMBERS=(
    ["Aria-MSW"]="aria@metaphysical-scene-weaver.ai"
    ["Sophia-MSW"]="sophia@metaphysical-scene-weaver.ai"
    ["Luna-MSW"]="luna@metaphysical-scene-weaver.ai"
    ["Rex-MSW"]="rex@metaphysical-scene-weaver.ai"
    ["Nova-MSW"]="nova@metaphysical-scene-weaver.ai"
    ["Iris-MSW"]="iris@metaphysical-scene-weaver.ai"
    ["Quinn-MSW"]="quinn@metaphysical-scene-weaver.ai"
)

# Check which window we're in
if [ -n "$TMUX" ]; then
    WINDOW_NAME=$(tmux display-message -p '#W')
    
    # Extract member name from window (e.g., "Sophia-Philosophy" -> "Sophia")
    MEMBER_BASE=$(echo "$WINDOW_NAME" | cut -d'-' -f1)
    
    # Look for matching team member
    for member in "${!TEAM_MEMBERS[@]}"; do
        if [[ "$member" == "$MEMBER_BASE"* ]]; then
            configure_git_for_member "$member" "${TEAM_MEMBERS[$member]}"
            exit 0
        fi
    done
fi

# If not in a recognized tmux window, show all members
echo "Team member GPG configuration:"
for member in "${!TEAM_MEMBERS[@]}"; do
    echo "- $member: ${TEAM_MEMBERS[$member]}"
done

echo ""
echo "To configure for a specific member, run this script from their tmux window"
echo "Or manually run: git config user.name 'Member-Name' && git config user.email 'email@domain'""