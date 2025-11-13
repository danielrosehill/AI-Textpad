#!/bin/bash
# Build script for AI-Textpad

set -e

echo "Building AI-Textpad..."

# Get version from setup.py
VERSION=$(python3 -c "import re; content = open('setup.py').read(); print(re.search(r'VERSION = \"(.+?)\"', content).group(1))")
echo "Version: $VERSION"

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info debian/

# Build Python wheel
echo "Building Python package..."
python3 setup.py sdist bdist_wheel

# Create Debian package structure
echo "Creating Debian package structure..."
mkdir -p debian/DEBIAN
mkdir -p debian/usr/local/bin
mkdir -p debian/usr/share/applications
mkdir -p debian/opt/ai-textpad

# Create control file
cat > debian/DEBIAN/control <<EOF
Package: ai-textpad
Version: $VERSION
Section: text
Priority: optional
Architecture: all
Depends: python3 (>= 3.10), python3-pip
Maintainer: Daniel Rosehill <public@danielrosehill.com>
Description: LLM-powered text transformation utility
 AI-Textpad is a lightweight text editing utility for Linux desktop
 that applies LLM-powered text transformations to markdown content.
 .
 Features split-pane editing, version navigation, and support for
 multiple simultaneous transformations.
Homepage: https://github.com/danielrosehill/AI-Textpad
EOF

# Copy package files
echo "Copying package files..."
cp -r ai_textpad debian/opt/ai-textpad/
cp requirements.txt debian/opt/ai-textpad/
cp setup.py debian/opt/ai-textpad/

# Create launcher script
cat > debian/usr/local/bin/ai-textpad <<'EOF'
#!/bin/bash
# Launcher for AI-Textpad

cd /opt/ai-textpad
exec python3 -m ai_textpad.main "$@"
EOF

chmod +x debian/usr/local/bin/ai-textpad

# Create desktop entry
cat > debian/usr/share/applications/ai-textpad.desktop <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=AI-Textpad
Comment=LLM-powered text transformation utility
Exec=/usr/local/bin/ai-textpad
Icon=text-editor
Terminal=false
Categories=Office;TextEditor;Utility;
Keywords=text;editor;AI;LLM;transform;
EOF

# Create postinst script for pip dependencies
cat > debian/DEBIAN/postinst <<'EOF'
#!/bin/bash
set -e

echo "Installing Python dependencies..."
pip3 install --no-cache-dir -r /opt/ai-textpad/requirements.txt

exit 0
EOF

chmod +x debian/DEBIAN/postinst

# Build .deb package
echo "Building .deb package..."
PACKAGE_NAME="ai-textpad_${VERSION}_all.deb"
dpkg-deb --build debian "$PACKAGE_NAME"

echo ""
echo "Build complete!"
echo "Package: $PACKAGE_NAME"
echo ""
echo "To install: sudo dpkg -i $PACKAGE_NAME"
echo "To uninstall: sudo apt remove ai-textpad"
