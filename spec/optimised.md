# AI-Textpad Development Specification

## Project Overview

AI-Textpad is a lightweight text editing utility for Linux desktop that leverages LLM APIs to apply templated text transformations. It enables quick, reliable edits to markdown text using predefined transformation prompts sent to OpenRouter API.

## Core Concept

- **Input**: Markdown text (often voice notes or draft content)
- **Process**: Apply one or more transformation templates via LLM
- **Output**: Transformed markdown text
- **API**: OpenRouter with configurable models (default: `openai/gpt-5-mini`)
- **Temperature**: Minimum (for consistency)

## Architecture

### Directory Structure
```
AI-Textpad/
├── code/           # Application codebase
├── spec/           # Specifications and documentation
│   ├── optimised.md
│   └── models.md
└── prompts/        # Text transformation templates
```

### Technology Stack
- **Target OS**: Ubuntu (KDE Plasma)
- **Package Format**: `.deb`
- **Backend Storage**: SQLite or JSON (choose based on best fit for local GUI)
- **UI Framework**: TBD (consider forking existing plain text editor)

## User Interface Design

### Layout: Split-Pane Editor

```
┌──────────────────────────────────────────────────┐
│  [New] [Copy] [Download]    [Transform Menu ▼]  │
├─────────────────────┬────────────────────────────┤
│                     │                            │
│   Original Text     │   Transformed Text         │
│   (Left Pane)       │   (Right Pane)            │
│                     │                            │
│   Updates as you    │   Latest version          │
│   navigate versions │   Editable                │
│                     │                            │
└─────────────────────┴────────────────────────────┘
       ◄  [Restore Original]  ►
```

### UI Components

1. **Top Bar**
   - New button: Start fresh editing session
   - Copy to Clipboard button
   - Download button: Save as markdown (filename: timestamp)
   - Transform selection menu with search

2. **Split Panes**
   - **Left**: Original text (updates when navigating versions)
   - **Right**: Transformed text (always latest, user-editable)

3. **Version Navigation**
   - Previous/Next version arrows
   - Restore original button
   - In-memory versioning (no file persistence needed)

4. **Transform Menu**
   - Category-organized transforms
   - Freeform search
   - Support for selecting up to 5 simultaneous transformations

### Selection Modes

- **Select All + Transform**: Applies to entire document
- **Select Text + Right-Click**: Context menu to transform only selected portion

## Text Transformations

### Categories & Examples

#### Voice Note Processing
- Voice note cleanup (punctuation, paragraphs)

#### Format Transformations
- Format as: Email, Blog Post, Social Media Post, Blog Outline, RFP, Bug Report, Feature Request, Reddit Post

#### Style Transformations
- Business ↔ Casual
- Formal ↔ Informal

#### Word Count Adjustments
- Expand to X words
- Reduce to X words

#### Simplification
- Add/Remove metaphors
- Simplify language
- Use simpler sentence structure
- Break up long paragraphs

#### Text Formatting
- Add subheadings
- Add bold subheadings
- Move links to end

#### Grammatical Transformations
- First ↔ Third person
- Past ↔ Present tense

#### Style Guide Conformity
- CMS style guide
- UK/US English variants

#### Creative/Experimental
- Make hyperbolic
- Cheesy sales ad style
- Shakespearean
- Archaic vocabulary
- Add random foreign words
- Maximize complexity
- Telegraph format
- Stuff with platitudes
- Painfully inspirational
- Humblebrag format

#### Specialized
- Obfuscation (for whistleblowing - removes names/places)

### Transform Loading

Transformations are loaded from `/prompts` directory as system prompts. The body text serves as the user prompt.

## Transformation Logic

### Multi-Transform Execution

When multiple transformations are selected (up to 5):

```
API Request = System Prompt + Preface + Concatenated Instructions + Text

Preface: "Please apply the following list of edits to the text:"
Instructions: Each transform separated by horizontal rules
Text: Latest version (original on first run, edited text on subsequent runs)
```

### Version Management

- **First transform**: Left pane = original, Right pane = transformed
- **Subsequent transforms**:
  - Right pane content (which can be manually edited) becomes the source text
  - New result appears in right pane
  - Left pane updates to show previous version
- **Navigation**: Move backward/forward through transformation history
- **Storage**: In-memory only (no file persistence for versions)

## Backend Data Storage

### Persistent Configuration
- API key (OpenRouter)
- Model preference
- Transformation prompt library
- User details (optional, see below)

### Storage Implementation
Choose between:
- SQLite database
- File-based JSON storage

Both are viable; select based on best fit for local GUI application.

## User Details Feature

### Problem
Without context, LLM cannot personalize outputs (e.g., email signatures).

### Solution
Optional user detail store containing:
- Name
- Email
- Other relevant info

### Implementation
Inject user details into prompt construction:
```
System Prompt +
Transform Prompt +
User Details (if applicable) +
Text
```

Apply either:
- Universally: "Customize using these details if necessary"
- Selectively: Only for relevant transforms (e.g., email formatting)

## Build & Deployment

### Scripts Required
- `build.sh` - Build .deb package
- `update.sh` - Rebuild from source with version increment
- `.gitignore` - Exclude build artifacts

### Versioning
- Proper semantic versioning between releases
- Version number auto-increment in update script

### Distribution
- Primary: `.deb` package for Ubuntu
- Open source project on GitHub

## Future Features (v2)

### Custom Transformation Management
- User-created transform prompts
- CRUD operations on transform library
- Folder organization
- Dedicated prompt management screen (separate from main UI)

## Design Principles

1. **Quick & Versatile**: Fast workflow for paste-transform-copy operations
2. **Simple UI**: Avoid feature creep and crowding
3. **Reliable**: Minimal temperature for consistent results
4. **No Persistence Needed**: Designed for ephemeral text editing
5. **Extensible**: Easy to add new transformations

## Development Priorities

### Phase 1 (MVP)
- Basic text editor with split panes
- Core transformation engine
- 20-30 essential transforms
- Version navigation
- API configuration
- .deb build process

### Phase 2
- Custom transformation management
- User details store
- Enhanced transform organization
- Additional transforms

## Technical Considerations

### Error Handling
- LLMs sometimes produce unexpected results
- Version navigation allows fallback to previous versions
- Original text always preserved

### Performance
- Lightweight operation (in-memory versioning)
- Minimal backend requirements
- Fast API calls with low temperature

### Extensibility
- Transform library easily expandable
- Category system supports growth
- Search functionality scales with transform count
