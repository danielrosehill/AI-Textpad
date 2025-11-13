#!/bin/bash
# Update script for AI-Textpad - rebuilds and increments version

set -e

echo "AI-Textpad Update Script"
echo "========================"
echo ""

# Get current version
CURRENT_VERSION=$(python3 -c "import re; content = open('setup.py').read(); print(re.search(r'VERSION = \"(.+?)\"', content).group(1))")
echo "Current version: $CURRENT_VERSION"
echo ""

# Parse version components
IFS='.' read -ra VERSION_PARTS <<< "$CURRENT_VERSION"
MAJOR="${VERSION_PARTS[0]}"
MINOR="${VERSION_PARTS[1]}"
PATCH="${VERSION_PARTS[2]}"

# Ask user which component to increment
echo "Which version component to increment?"
echo "1) Patch (${MAJOR}.${MINOR}.${PATCH} -> ${MAJOR}.${MINOR}.$((PATCH+1)))"
echo "2) Minor (${MAJOR}.${MINOR}.${PATCH} -> ${MAJOR}.$((MINOR+1)).0)"
echo "3) Major (${MAJOR}.${MINOR}.${PATCH} -> $((MAJOR+1)).0.0)"
echo "4) Custom version"
echo ""
read -p "Enter choice [1-4]: " choice

case $choice in
    1)
        NEW_VERSION="${MAJOR}.${MINOR}.$((PATCH+1))"
        ;;
    2)
        NEW_VERSION="${MAJOR}.$((MINOR+1)).0"
        ;;
    3)
        NEW_VERSION="$((MAJOR+1)).0.0"
        ;;
    4)
        read -p "Enter custom version: " NEW_VERSION
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

echo ""
echo "New version will be: $NEW_VERSION"
read -p "Continue? [y/N]: " confirm

if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

# Update version in setup.py
echo ""
echo "Updating version in setup.py..."
sed -i "s/VERSION = \"$CURRENT_VERSION\"/VERSION = \"$NEW_VERSION\"/" setup.py

# Update version in __init__.py
sed -i "s/__version__ = \"$CURRENT_VERSION\"/__version__ = \"$NEW_VERSION\"/" ai_textpad/__init__.py

echo "Version updated to $NEW_VERSION"
echo ""

# Run build
echo "Running build..."
./build.sh

echo ""
echo "Update complete!"
echo "New package: ai-textpad_${NEW_VERSION}_all.deb"
echo ""
echo "Don't forget to:"
echo "1. Commit the version changes"
echo "2. Create a git tag: git tag v${NEW_VERSION}"
echo "3. Push changes: git push && git push --tags"
