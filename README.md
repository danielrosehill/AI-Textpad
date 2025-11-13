# AI-Textpad

**LLM-powered text transformation utility for Linux desktop**

AI-Textpad is a lightweight, fast text editor designed for applying AI-powered transformations to markdown text. Perfect for quickly cleaning up voice notes, reformatting content, adjusting writing style, and more.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Ubuntu%20%7C%20Linux-lightgrey.svg)

## Features

- **Split-Pane Editor**: View original and transformed text side-by-side
- **100+ Text Transformations**: Pre-built templates for common editing tasks
- **Multi-Transform Support**: Apply up to 5 transformations simultaneously
- **Version Navigation**: Move backward/forward through transformation history
- **Smart Personalization**: Optional user details for personalized outputs (emails, signatures)
- **Quick Workflow**: Paste → Transform → Copy with no file persistence needed
- **Flexible Selection**: Transform entire document or selected text only
- **Search & Organize**: Find transformations quickly with search and categories

## Use Cases

- **Voice Note Cleanup**: Auto-add punctuation and paragraph breaks
- **Format Conversion**: Transform to email, blog post, social media, RFP, bug report, etc.
- **Style Adjustment**: Switch between business/casual, formal/informal tone
- **Word Count Control**: Expand or reduce to target word count
- **Simplification**: Break up paragraphs, simplify language, adjust sentence structure
- **Grammar Transforms**: Change tense (past/present) or perspective (1st/3rd person)
- **Creative Styles**: Shakespearean, hyperbolic, telegram format, and more
- **Localization**: Convert between UK/US English variants

## Quick Start

### Prerequisites

- Ubuntu 20.04+ (or compatible Debian-based Linux)
- Python 3.10 or higher
- OpenRouter API key ([get one free](https://openrouter.ai/keys))

### Installation

#### Option 1: Install .deb Package (Recommended)

```bash
# Download latest release
wget https://github.com/danielrosehill/AI-Textpad/releases/latest/download/ai-textpad_0.1.0_all.deb

# Install
sudo dpkg -i ai-textpad_0.1.0_all.deb

# Launch
ai-textpad
```

#### Option 2: Run from Source

```bash
# Clone repository
git clone https://github.com/danielrosehill/AI-Textpad.git
cd AI-Textpad/code

# Install dependencies
pip install -r requirements.txt

# Run
python3 -m ai_textpad.main
```

### Initial Setup

1. **Launch AI-Textpad**
2. **Open Settings** (toolbar)
3. **Configure API Settings**:
   - Enter your OpenRouter API key
   - Select model (default: `openai/gpt-4o-mini`)
4. **(Optional) Add User Details**:
   - Name and email for personalized outputs
5. **Start transforming text!**

## How to Use

### Basic Workflow

1. **Paste or type** text in the left pane
2. **Click Transform** button in toolbar
3. **Select transformations** (up to 5) from the dialog
4. **Apply** - transformed text appears in right pane
5. **Edit freely** in right pane if needed
6. **Apply more transforms** - uses edited text as input
7. **Navigate versions** with ◄ ► buttons
8. **Copy to clipboard** or **Download as markdown**

### Transform Categories

- **Voice Processing**: Voice note cleanup
- **Format Transformations**: Email, blog, social media, RFP, bug report, etc.
- **Style Transformations**: Business ↔ Casual, Formal ↔ Informal
- **Word Count**: Expand/reduce to target
- **Simplification**: Add/remove metaphors, simplify language, break paragraphs
- **Text Formatting**: Add subheadings, move links to end
- **Grammar**: Change tense, perspective
- **Style Guides**: CMS, UK/US English
- **Creative**: Shakespearean, hyperbolic, telegram format, humblebrag
- **Specialized**: Obfuscation (for anonymization)

### Tips

- **Multi-transforms**: Select multiple complementary transforms (e.g., "Voice cleanup" + "Format as email")
- **Iterative editing**: Edit manually in right pane, then apply more transforms
- **Version history**: Made a mistake? Use ◄ to go back to previous version
- **Search**: Can't find a transform? Use the search box in the dialog
- **Restore original**: Hit "↺ Restore Original" to start over

## Repository Structure

```
AI-Textpad/
├── code/                   # Application codebase
│   ├── ai_textpad/        # Python package
│   ├── build.sh           # Build .deb package
│   ├── update.sh          # Version update script
│   └── README.md          # Developer documentation
├── prompts/               # Transformation prompt templates
├── spec/                  # Project specifications
│   ├── optimised.md       # Complete development spec
│   ├── models.md          # Available LLM models
│   └── raw.md            # Original draft spec
├── CLAUDE.md             # AI agent instructions
├── README.md             # This file
└── LICENSE               # MIT License
```

## Development

See [code/README.md](code/README.md) for:
- Development setup
- Architecture overview
- Building from source
- Contributing guidelines

### Building

```bash
cd code/
./build.sh
```

Creates `ai-textpad_<version>_all.deb`

### Version Management

```bash
cd code/
./update.sh
```

Prompts for version increment and rebuilds package.

## Customization

### Adding Your Own Transformations

Create transformation prompt files in `prompts/` directory:

```markdown
# prompts/my-category/my-transform.md

Transform the following text by [describe transformation].
Maintain markdown formatting.
```

The app will automatically load them on next launch.

### User Details for Personalization

Configure in Settings → User Details:
- Name
- Email
- Additional context

These details are injected into relevant transformations (e.g., email signatures).

## Technical Details

- **Framework**: PyQt6 (native Qt for KDE Plasma)
- **API**: OpenRouter for LLM access
- **Backend**: SQLite for configuration storage
- **Async**: qasync for non-blocking API calls
- **Package**: Native .deb for Ubuntu

### Supported Models

Default models (configurable in Settings):
- `openai/gpt-4o-mini` (default - fast and economical)
- `openai/gpt-4o-nano` (most economical)
- `x-ai/grok-4-fast` (fast inference)
- `google/gemini-2.5-flash-lite`
- `switchpoint/router` (auto-routing)
- Free models for testing

See [spec/models.md](spec/models.md) for complete list.

## Roadmap

### v0.1.0 (Current)
- ✅ Core transformation engine
- ✅ Split-pane UI
- ✅ Version navigation
- ✅ Settings dialog
- ✅ .deb packaging

### v0.2.0 (Planned)
- [ ] Custom transformation creator UI
- [ ] CRUD operations for transform library
- [ ] Folder organization for custom prompts
- [ ] Keyboard shortcuts
- [ ] Transformation favorites/pinning

### v0.3.0 (Future)
- [ ] Dark mode theme
- [ ] Export/import transformation sets
- [ ] Batch processing multiple files
- [ ] Plugin system for custom integrations

## FAQ

**Q: Why OpenRouter instead of direct API access?**
A: OpenRouter provides unified access to multiple LLM providers with a single API key and handles rate limiting, fallbacks, and cost optimization.

**Q: Does this work offline?**
A: Transformations require API access. However, local models (Ollama) may be supported in future versions.

**Q: Is my data stored or shared?**
A: No. Text is sent only to OpenRouter API for transformation. No persistent storage of your text content. Configuration is stored locally in `~/.config/ai-textpad/`.

**Q: Can I use my own prompts?**
A: Yes! Currently by placing `.md` files in `prompts/` directory. v0.2.0 will add a UI for custom prompt management.

**Q: What about Windows/macOS?**
A: Currently Linux-only. Cross-platform support may come in future versions.

## Support

- **Issues**: [GitHub Issues](https://github.com/danielrosehill/AI-Textpad/issues)
- **Discussions**: [GitHub Discussions](https://github.com/danielrosehill/AI-Textpad/discussions)
- **Email**: public@danielrosehill.com

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Author

**Daniel Rosehill**
- Website: [danielrosehill.com](https://danielrosehill.com)
- GitHub: [@danielrosehill](https://github.com/danielrosehill)
- Email: public@danielrosehill.com

## Acknowledgments

- Built with [PyQt6](https://www.riverbankcomputing.com/software/pyqt/)
- LLM access via [OpenRouter](https://openrouter.ai)
- Inspired by the need for quick, reliable text transformations

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

See [code/README.md](code/README.md) for development setup.

---

**Made with ❤️ for writers, developers, and anyone who works with text**
