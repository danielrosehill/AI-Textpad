"""Database management for AI-Textpad configuration."""

import sqlite3
from pathlib import Path
from typing import Optional, Dict, Any
import json


class ConfigDatabase:
    """Manages SQLite database for application configuration."""

    def __init__(self, db_path: Optional[Path] = None):
        """Initialize database connection.

        Args:
            db_path: Path to SQLite database file. Defaults to ~/.config/ai-textpad/config.db
        """
        if db_path is None:
            config_dir = Path.home() / ".config" / "ai-textpad"
            config_dir.mkdir(parents=True, exist_ok=True)
            db_path = config_dir / "config.db"

        self.db_path = db_path
        self.conn = sqlite3.connect(str(db_path))
        self.conn.row_factory = sqlite3.Row
        self._init_tables()

    def _init_tables(self):
        """Create database tables if they don't exist."""
        cursor = self.conn.cursor()

        # Configuration table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS config (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # User details table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_details (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Transformations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transformations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                prompt TEXT NOT NULL,
                user_created INTEGER DEFAULT 0,
                sort_order INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        self.conn.commit()

    def get_config(self, key: str, default: Any = None) -> Any:
        """Get configuration value.

        Args:
            key: Configuration key
            default: Default value if key doesn't exist

        Returns:
            Configuration value or default
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT value FROM config WHERE key = ?", (key,))
        row = cursor.fetchone()

        if row is None:
            return default

        # Try to parse as JSON, fallback to string
        try:
            return json.loads(row[0])
        except (json.JSONDecodeError, TypeError):
            return row[0]

    def set_config(self, key: str, value: Any):
        """Set configuration value.

        Args:
            key: Configuration key
            value: Configuration value (will be JSON-encoded if not string)
        """
        if not isinstance(value, str):
            value = json.dumps(value)

        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO config (key, value)
            VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET
                value = excluded.value,
                updated_at = CURRENT_TIMESTAMP
        """, (key, value))
        self.conn.commit()

    def get_user_detail(self, key: str, default: str = "") -> str:
        """Get user detail value.

        Args:
            key: Detail key (e.g., 'name', 'email')
            default: Default value if key doesn't exist

        Returns:
            User detail value or default
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT value FROM user_details WHERE key = ?", (key,))
        row = cursor.fetchone()
        return row[0] if row else default

    def set_user_detail(self, key: str, value: str):
        """Set user detail value.

        Args:
            key: Detail key
            value: Detail value
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO user_details (key, value)
            VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET
                value = excluded.value,
                updated_at = CURRENT_TIMESTAMP
        """, (key, value))
        self.conn.commit()

    def get_all_user_details(self) -> Dict[str, str]:
        """Get all user details as dictionary.

        Returns:
            Dictionary of user details
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT key, value FROM user_details")
        return {row[0]: row[1] for row in cursor.fetchall()}

    def add_transformation(self, name: str, category: str, prompt: str,
                          user_created: bool = True, sort_order: int = 0) -> int:
        """Add a new transformation.

        Args:
            name: Transformation name
            category: Category name
            prompt: System prompt for the transformation
            user_created: Whether this is a user-created transformation
            sort_order: Sort order within category

        Returns:
            ID of created transformation
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO transformations (name, category, prompt, user_created, sort_order)
            VALUES (?, ?, ?, ?, ?)
        """, (name, category, prompt, int(user_created), sort_order))
        self.conn.commit()
        return cursor.lastrowid

    def get_transformations(self, category: Optional[str] = None) -> list:
        """Get transformations, optionally filtered by category.

        Args:
            category: Category to filter by (None for all)

        Returns:
            List of transformation dictionaries
        """
        cursor = self.conn.cursor()
        if category:
            cursor.execute("""
                SELECT id, name, category, prompt, user_created, sort_order
                FROM transformations
                WHERE category = ?
                ORDER BY sort_order, name
            """, (category,))
        else:
            cursor.execute("""
                SELECT id, name, category, prompt, user_created, sort_order
                FROM transformations
                ORDER BY category, sort_order, name
            """)

        return [dict(row) for row in cursor.fetchall()]

    def get_categories(self) -> list:
        """Get all transformation categories.

        Returns:
            List of category names
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM transformations ORDER BY category")
        return [row[0] for row in cursor.fetchall()]

    def update_transformation(self, transformation_id: int, **kwargs):
        """Update transformation fields.

        Args:
            transformation_id: ID of transformation to update
            **kwargs: Fields to update (name, category, prompt, sort_order)
        """
        allowed_fields = {'name', 'category', 'prompt', 'sort_order'}
        updates = {k: v for k, v in kwargs.items() if k in allowed_fields}

        if not updates:
            return

        set_clause = ", ".join(f"{k} = ?" for k in updates.keys())
        set_clause += ", updated_at = CURRENT_TIMESTAMP"
        values = list(updates.values()) + [transformation_id]

        cursor = self.conn.cursor()
        cursor.execute(f"""
            UPDATE transformations
            SET {set_clause}
            WHERE id = ?
        """, values)
        self.conn.commit()

    def delete_transformation(self, transformation_id: int):
        """Delete a transformation.

        Args:
            transformation_id: ID of transformation to delete
        """
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM transformations WHERE id = ?", (transformation_id,))
        self.conn.commit()

    def close(self):
        """Close database connection."""
        self.conn.close()
