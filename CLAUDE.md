# AI-Textpad

## Project Overview

AI-Textpad is a lightweight text editing utility for Linux desktop (Ubuntu/KDE Plasma) that applies LLM-powered text transformations to markdown content.

## Key Features

- **Split-pane editor**: Original text (left) and transformed text (right)
- **Text transformations**: Pre-defined templates for common editing tasks (formatting, style changes, grammar adjustments, etc.)
- **Multi-transform support**: Apply up to 5 transformations simultaneously
- **Version navigation**: Move backward/forward through transformation history
- **Quick workflow**: Paste → Transform → Copy operations with no file persistence
- **Selection modes**: Transform entire document or selected text only

## Technical Details

- **API**: OpenRouter (default model: `openai/gpt-5-mini`)
- **Backend**: SQLite or JSON for configuration storage
- **Package**: `.deb` for Ubuntu distribution
- **Transform Library**: Located in `/prompts` directory

## Repository Structure

- `spec/` - Full project specifications and model configurations
  - [optimised.md](spec/optimised.md) - Complete development specification
  - [models.md](spec/models.md) - Available LLM models and configurations
  - `raw.md` - Original draft specification
- `code/` - Application codebase
- `prompts/` - Text transformation templates

## Development

Refer to [spec/optimised.md](spec/optimised.md) for complete development specification including:
- UI/UX design
- Transformation logic
- Backend architecture
- Build & deployment process
- Future feature roadmap

