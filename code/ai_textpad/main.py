"""Main entry point for AI-Textpad application."""

import sys
import asyncio
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
import qasync

from .storage.database import ConfigDatabase
from .ui.main_window import MainWindow
from .transforms.loader import TransformLoader


def load_default_transformations(db: ConfigDatabase):
    """Load default transformations from prompts directory if not already loaded.

    Args:
        db: Database instance
    """
    # Check if transformations already loaded
    if db.get_categories():
        return

    # Find prompts directory
    repo_root = Path(__file__).parent.parent.parent
    prompts_dir = repo_root / "prompts"

    if not prompts_dir.exists():
        print(f"Warning: Prompts directory not found at {prompts_dir}")
        return

    # Load transformations
    loader = TransformLoader(prompts_dir)
    transformations = loader.load_from_directory()

    # Add to database
    for name, category, prompt in transformations:
        db.add_transformation(
            name=name,
            category=category,
            prompt=prompt,
            user_created=False
        )

    print(f"Loaded {len(transformations)} transformations from {prompts_dir}")


def main():
    """Main application entry point."""
    # Create QApplication
    app = QApplication(sys.argv)
    app.setApplicationName("AI-Textpad")
    app.setOrganizationName("Daniel Rosehill")

    # Set up async event loop
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    # Initialize database
    db = ConfigDatabase()

    # Load default transformations on first run
    load_default_transformations(db)

    # Create and show main window
    window = MainWindow(db)
    window.show()

    # Run event loop
    with loop:
        loop.run_forever()


if __name__ == "__main__":
    main()
