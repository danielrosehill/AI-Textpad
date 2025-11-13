"""Version management for text transformations."""

from typing import List, Optional


class VersionManager:
    """Manages version history for text transformations."""

    def __init__(self, original_text: str = ""):
        """Initialize version manager.

        Args:
            original_text: Initial text content
        """
        self.original_text = original_text
        self.versions: List[str] = [original_text] if original_text else []
        self.current_index = 0

    def add_version(self, text: str):
        """Add a new version of the text.

        If not at the end of history, this will truncate future versions.

        Args:
            text: New version text
        """
        # If we're not at the end, remove all versions after current
        if self.current_index < len(self.versions) - 1:
            self.versions = self.versions[:self.current_index + 1]

        self.versions.append(text)
        self.current_index = len(self.versions) - 1

    def get_current(self) -> str:
        """Get current version text.

        Returns:
            Current version text or empty string
        """
        if 0 <= self.current_index < len(self.versions):
            return self.versions[self.current_index]
        return ""

    def get_original(self) -> str:
        """Get original text.

        Returns:
            Original text
        """
        return self.original_text

    def can_go_back(self) -> bool:
        """Check if can navigate to previous version.

        Returns:
            True if previous version exists
        """
        return self.current_index > 0

    def can_go_forward(self) -> bool:
        """Check if can navigate to next version.

        Returns:
            True if next version exists
        """
        return self.current_index < len(self.versions) - 1

    def go_back(self) -> Optional[str]:
        """Navigate to previous version.

        Returns:
            Previous version text or None if can't go back
        """
        if self.can_go_back():
            self.current_index -= 1
            return self.get_current()
        return None

    def go_forward(self) -> Optional[str]:
        """Navigate to next version.

        Returns:
            Next version text or None if can't go forward
        """
        if self.can_go_forward():
            self.current_index += 1
            return self.get_current()
        return None

    def restore_original(self) -> str:
        """Navigate back to original text.

        Returns:
            Original text
        """
        self.current_index = 0
        return self.get_current()

    def reset(self, new_text: str = ""):
        """Reset version history with new text.

        Args:
            new_text: New starting text
        """
        self.original_text = new_text
        self.versions = [new_text] if new_text else []
        self.current_index = 0

    def get_version_count(self) -> int:
        """Get total number of versions.

        Returns:
            Number of versions
        """
        return len(self.versions)

    def get_current_index(self) -> int:
        """Get current version index (0-based).

        Returns:
            Current index
        """
        return self.current_index
