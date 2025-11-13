"""Loader for transformation prompts from files."""

from pathlib import Path
from typing import List, Dict, Tuple
import re


class TransformLoader:
    """Loads transformation prompts from filesystem."""

    def __init__(self, prompts_dir: Path):
        """Initialize transformation loader.

        Args:
            prompts_dir: Directory containing transformation prompt files
        """
        self.prompts_dir = Path(prompts_dir)

    def load_from_directory(self) -> List[Tuple[str, str, str]]:
        """Load all transformations from prompts directory.

        Returns:
            List of tuples: (name, category, prompt_content)
        """
        transformations = []

        if not self.prompts_dir.exists():
            return transformations

        # Recursively find all markdown files
        for prompt_file in self.prompts_dir.rglob("*.md"):
            name, category, content = self._parse_prompt_file(prompt_file)
            if content:
                transformations.append((name, category, content))

        return transformations

    def _parse_prompt_file(self, file_path: Path) -> Tuple[str, str, str]:
        """Parse a prompt file and extract metadata.

        Args:
            file_path: Path to prompt file

        Returns:
            Tuple of (name, category, content)
        """
        try:
            content = file_path.read_text(encoding="utf-8")

            # Extract category from directory structure
            relative_path = file_path.relative_to(self.prompts_dir)
            if len(relative_path.parts) > 1:
                category = relative_path.parts[0].replace("-", " ").replace("_", " ").title()
            else:
                category = "General"

            # Extract name from filename
            name = file_path.stem.replace("-", " ").replace("_", " ").title()

            # Look for a title in the content (first H1 heading)
            title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if title_match:
                name = title_match.group(1).strip()

            return name, category, content.strip()

        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return "", "", ""

    def categorize_transformations(self, transformations: List[Tuple[str, str, str]]) -> Dict[str, List[Tuple[str, str]]]:
        """Organize transformations by category.

        Args:
            transformations: List of (name, category, prompt) tuples

        Returns:
            Dictionary mapping category -> list of (name, prompt) tuples
        """
        categorized = {}

        for name, category, prompt in transformations:
            if category not in categorized:
                categorized[category] = []
            categorized[category].append((name, prompt))

        # Sort within each category
        for category in categorized:
            categorized[category].sort(key=lambda x: x[0])

        return categorized
