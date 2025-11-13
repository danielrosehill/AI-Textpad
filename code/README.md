# AI-Textpad - Code Directory

This directory contains the complete codebase for AI-Textpad.

## Project Structure

```
code/
├── ai_textpad/              # Main Python package
│   ├── __init__.py
│   ├── main.py             # Application entry point
│   ├── api/                # OpenRouter API integration
│   │   ├── __init__.py
│   │   └── openrouter.py
│   ├── storage/            # Database and configuration
│   │   ├── __init__.py
│   │   └── database.py
│   ├── transforms/         # Transformation management
│   │   ├── __init__.py
│   │   ├── loader.py       # Load prompts from filesystem
│   │   └── version_manager.py
│   └── ui/                 # PyQt6 user interface
│       ├── __init__.py
│       ├── main_window.py  # Main application window
│       ├── transform_dialog.py
│       └── settings_dialog.py
├── build.sh                # Build .deb package
├── update.sh               # Update version and rebuild
├── setup.py                # Python package setup
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Development Setup

### Prerequisites

- Python 3.10 or higher
- PyQt6
- Ubuntu/Debian-based Linux distribution

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Running from Source

```bash
python3 -m ai_textpad.main
```

Or:

```bash
python3 ai_textpad/main.py
```

## Building

### Build .deb Package

```bash
./build.sh
```

This creates `ai-textpad_<version>_all.deb` in the current directory.

### Update Version and Rebuild

```bash
./update.sh
```

This script:
1. Prompts for version increment (patch/minor/major)
2. Updates version in `setup.py` and `__init__.py`
3. Runs the build process
4. Creates new .deb package

### Install Package

```bash
sudo dpkg -i ai-textpad_<version>_all.deb
```

After installation, launch with:
```bash
ai-textpad
```

Or find it in your application menu under "Office" or "Text Editor".

## Configuration

Configuration is stored in `~/.config/ai-textpad/`:
- `config.db` - SQLite database containing settings and transformations

### Required Configuration

1. **OpenRouter API Key**: Required for transformations
   - Get from: https://openrouter.ai/keys
   - Configure via Settings dialog in the application

2. **Model Selection**: Choose from available models (default: `openai/gpt-4o-mini`)

3. **Transformation Prompts**: Place in `../prompts/` directory (relative to repo root)

## Architecture

### Technology Stack

- **GUI Framework**: PyQt6 (native Qt for KDE Plasma)
- **Async I/O**: qasync for async/await support in Qt
- **HTTP Client**: httpx for OpenRouter API calls
- **Database**: SQLite for configuration and prompt storage

### Key Components

1. **ConfigDatabase** ([storage/database.py](ai_textpad/storage/database.py))
   - Manages configuration, user details, and transformations
   - SQLite-based with simple API

2. **OpenRouterClient** ([api/openrouter.py](ai_textpad/api/openrouter.py))
   - Async API client for OpenRouter
   - Handles prompt construction and API calls

3. **VersionManager** ([transforms/version_manager.py](ai_textpad/transforms/version_manager.py))
   - In-memory version history
   - Navigation (back/forward/restore)

4. **TransformLoader** ([transforms/loader.py](ai_textpad/transforms/loader.py))
   - Loads transformation prompts from filesystem
   - Organizes by category

5. **MainWindow** ([ui/main_window.py](ai_textpad/ui/main_window.py))
   - Split-pane text editor
   - Version navigation UI
   - Toolbar and actions

## Features Implemented

- ✅ Split-pane editor (original/transformed)
- ✅ Transformation selection dialog with search
- ✅ Multi-transform support (up to 5 simultaneously)
- ✅ Version navigation (back/forward/restore)
- ✅ Copy to clipboard
- ✅ Download as markdown (timestamped filename)
- ✅ Settings dialog (API key, model, user details)
- ✅ User details injection for personalization
- ✅ .deb package build system
- ✅ Version management scripts

## Future Enhancements (v2)

- Custom transformation creation UI
- CRUD operations for transformation library
- Folder organization for transforms
- Dedicated prompt management screen
- Enhanced error handling and retry logic
- Transformation favorites/pinning
- Keyboard shortcuts
- Dark mode theme

## Testing

To test the application without installing:

```bash
# Install dependencies
pip install -r requirements.txt

# Run from source
python3 -m ai_textpad.main
```

Make sure to:
1. Configure your OpenRouter API key in Settings
2. Have transformation prompts in `../prompts/` directory

## Troubleshooting

### "No transformations found"
- Ensure `../prompts/` directory exists and contains `.md` files
- Check that prompts are organized in subdirectories (used as categories)

### "API Key Required"
- Go to Settings → API Settings
- Enter your OpenRouter API key from https://openrouter.ai/keys

### Dependencies not found
```bash
pip install --upgrade -r requirements.txt
```

### Package build fails
- Ensure you have `dpkg-deb` installed: `sudo apt install dpkg-dev`
- Check that all Python files are valid

## License

See repository root for license information.

## Contributing

See main repository README for contribution guidelines.
