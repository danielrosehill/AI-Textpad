"""Main window for AI-Textpad application."""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTextEdit, QSplitter, QToolBar, QLabel, QMessageBox
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon
from datetime import datetime
from pathlib import Path
import asyncio
from typing import List, Optional

from ..storage.database import ConfigDatabase
from ..api.openrouter import OpenRouterClient
from ..transforms.version_manager import VersionManager
from .transform_dialog import TransformDialog
from .settings_dialog import SettingsDialog


class MainWindow(QMainWindow):
    """Main application window with split-pane editor."""

    def __init__(self, db: ConfigDatabase):
        """Initialize main window.

        Args:
            db: Database instance
        """
        super().__init__()
        self.db = db
        self.version_manager = VersionManager()
        self.selected_transformations: List[tuple] = []  # List of (name, prompt) tuples

        self.setWindowTitle("AI-Textpad")
        self.setMinimumSize(QSize(1200, 700))

        self._setup_ui()
        self._setup_toolbar()
        self._connect_signals()

    def _setup_ui(self):
        """Set up the user interface."""
        # Central widget with main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Splitter for two panes
        self.splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left pane: Original text
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(5, 5, 5, 5)

        left_label = QLabel("Original Text")
        left_label.setStyleSheet("font-weight: bold; font-size: 12pt;")
        self.original_text_edit = QTextEdit()
        self.original_text_edit.setPlaceholderText("Paste your text here to begin...")

        left_layout.addWidget(left_label)
        left_layout.addWidget(self.original_text_edit)

        # Right pane: Transformed text
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(5, 5, 5, 5)

        right_label = QLabel("Transformed Text")
        right_label.setStyleSheet("font-weight: bold; font-size: 12pt;")
        self.transformed_text_edit = QTextEdit()
        self.transformed_text_edit.setPlaceholderText("Transformed text will appear here...")

        right_layout.addWidget(right_label)
        right_layout.addWidget(self.transformed_text_edit)

        # Add panes to splitter
        self.splitter.addWidget(left_widget)
        self.splitter.addWidget(right_widget)
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 1)

        main_layout.addWidget(self.splitter)

        # Version navigation bar
        nav_widget = QWidget()
        nav_layout = QHBoxLayout(nav_widget)
        nav_layout.setContentsMargins(10, 5, 10, 5)

        self.back_button = QPushButton("◄ Previous")
        self.back_button.setEnabled(False)

        self.version_label = QLabel("Version: 1/1")
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.forward_button = QPushButton("Next ►")
        self.forward_button.setEnabled(False)

        self.restore_button = QPushButton("↺ Restore Original")
        self.restore_button.setEnabled(False)

        nav_layout.addWidget(self.back_button)
        nav_layout.addWidget(self.version_label)
        nav_layout.addWidget(self.forward_button)
        nav_layout.addStretch()
        nav_layout.addWidget(self.restore_button)

        main_layout.addWidget(nav_widget)

    def _setup_toolbar(self):
        """Set up the toolbar."""
        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(toolbar)

        # New button
        new_action = QAction("New", self)
        new_action.triggered.connect(self.new_document)
        toolbar.addAction(new_action)

        toolbar.addSeparator()

        # Transform button
        self.transform_action = QAction("Transform", self)
        self.transform_action.triggered.connect(self.show_transform_dialog)
        toolbar.addAction(self.transform_action)

        toolbar.addSeparator()

        # Copy button
        copy_action = QAction("Copy to Clipboard", self)
        copy_action.triggered.connect(self.copy_to_clipboard)
        toolbar.addAction(copy_action)

        # Download button
        download_action = QAction("Download", self)
        download_action.triggered.connect(self.download_text)
        toolbar.addAction(download_action)

        toolbar.addSeparator()

        # Settings button
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.show_settings)
        toolbar.addAction(settings_action)

        # Add stretch to push next items to the right
        spacer = QWidget()
        spacer.setSizePolicy(
            QWidget().sizePolicy().horizontalPolicy(),
            QWidget().sizePolicy().verticalPolicy()
        )
        toolbar.addWidget(spacer)

        # Status label
        self.status_label = QLabel("Ready")
        toolbar.addWidget(self.status_label)

    def _connect_signals(self):
        """Connect signals and slots."""
        self.back_button.clicked.connect(self.go_back)
        self.forward_button.clicked.connect(self.go_forward)
        self.restore_button.clicked.connect(self.restore_original)

        # Update version manager when original text changes
        self.original_text_edit.textChanged.connect(self.on_original_text_changed)

    def on_original_text_changed(self):
        """Handle changes to original text."""
        text = self.original_text_edit.toPlainText()
        if not self.version_manager.versions:
            self.version_manager.reset(text)
            self._update_navigation_buttons()

    def new_document(self):
        """Start a new document."""
        if self.original_text_edit.toPlainText() or self.transformed_text_edit.toPlainText():
            reply = QMessageBox.question(
                self,
                "New Document",
                "This will clear all text. Continue?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return

        self.original_text_edit.clear()
        self.transformed_text_edit.clear()
        self.version_manager.reset()
        self.selected_transformations = []
        self._update_navigation_buttons()
        self.status_label.setText("Ready")

    def show_transform_dialog(self):
        """Show transformation selection dialog."""
        # Check if API key is configured
        api_key = self.db.get_config("openrouter_api_key")
        if not api_key:
            QMessageBox.warning(
                self,
                "API Key Required",
                "Please configure your OpenRouter API key in Settings."
            )
            self.show_settings()
            return

        # Check if there's text to transform
        text = self.transformed_text_edit.toPlainText() or self.original_text_edit.toPlainText()
        if not text.strip():
            QMessageBox.warning(
                self,
                "No Text",
                "Please enter some text to transform."
            )
            return

        dialog = TransformDialog(self.db, self)
        if dialog.exec():
            self.selected_transformations = dialog.get_selected_transformations()
            if self.selected_transformations:
                asyncio.create_task(self.apply_transformations())

    def show_settings(self):
        """Show settings dialog."""
        dialog = SettingsDialog(self.db, self)
        dialog.exec()

    async def apply_transformations(self):
        """Apply selected transformations to text."""
        self.status_label.setText("Transforming...")
        self.transform_action.setEnabled(False)

        try:
            # Get source text (transformed pane if it has content, otherwise original)
            source_text = self.transformed_text_edit.toPlainText() or self.original_text_edit.toPlainText()

            # Get API configuration
            api_key = self.db.get_config("openrouter_api_key")
            model = self.db.get_config("model", "openai/gpt-4o-mini")

            # Get user details
            user_details = self.db.get_all_user_details()

            # Extract just the prompts
            prompts = [prompt for _, prompt in self.selected_transformations]

            # Call API
            async with OpenRouterClient(api_key, model) as client:
                transformed = await client.transform_text(
                    source_text,
                    prompts,
                    user_details if user_details else None
                )

            # Update UI
            self.version_manager.add_version(transformed)
            self.transformed_text_edit.setPlainText(transformed)

            # Update original pane to show previous version
            if self.version_manager.current_index > 0:
                prev_version = self.version_manager.versions[self.version_manager.current_index - 1]
                self.original_text_edit.setPlainText(prev_version)

            self._update_navigation_buttons()
            self.status_label.setText("Transform complete")

        except Exception as e:
            QMessageBox.critical(
                self,
                "Transform Error",
                f"Error applying transformations: {str(e)}"
            )
            self.status_label.setText("Transform failed")

        finally:
            self.transform_action.setEnabled(True)

    def go_back(self):
        """Navigate to previous version."""
        prev_text = self.version_manager.go_back()
        if prev_text is not None:
            self.transformed_text_edit.setPlainText(prev_text)
            # Update original pane
            if self.version_manager.current_index > 0:
                self.original_text_edit.setPlainText(
                    self.version_manager.versions[self.version_manager.current_index - 1]
                )
            else:
                self.original_text_edit.setPlainText(self.version_manager.original_text)
            self._update_navigation_buttons()

    def go_forward(self):
        """Navigate to next version."""
        next_text = self.version_manager.go_forward()
        if next_text is not None:
            self.transformed_text_edit.setPlainText(next_text)
            # Update original pane
            self.original_text_edit.setPlainText(
                self.version_manager.versions[self.version_manager.current_index - 1]
            )
            self._update_navigation_buttons()

    def restore_original(self):
        """Restore original text."""
        original = self.version_manager.restore_original()
        self.original_text_edit.setPlainText(original)
        self.transformed_text_edit.setPlainText(original)
        self._update_navigation_buttons()

    def _update_navigation_buttons(self):
        """Update state of navigation buttons."""
        self.back_button.setEnabled(self.version_manager.can_go_back())
        self.forward_button.setEnabled(self.version_manager.can_go_forward())
        self.restore_button.setEnabled(self.version_manager.current_index > 0)

        # Update version label
        count = self.version_manager.get_version_count()
        current = self.version_manager.get_current_index() + 1
        self.version_label.setText(f"Version: {current}/{count}")

    def copy_to_clipboard(self):
        """Copy transformed text to clipboard."""
        text = self.transformed_text_edit.toPlainText()
        if text:
            from PyQt6.QtWidgets import QApplication
            QApplication.clipboard().setText(text)
            self.status_label.setText("Copied to clipboard")
        else:
            QMessageBox.information(
                self,
                "No Text",
                "There is no transformed text to copy."
            )

    def download_text(self):
        """Download transformed text as markdown file."""
        text = self.transformed_text_edit.toPlainText()
        if not text:
            QMessageBox.information(
                self,
                "No Text",
                "There is no transformed text to download."
            )
            return

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"transformed_{timestamp}.md"

        # Save to Desktop
        desktop = Path.home() / "Desktop"
        filepath = desktop / filename

        try:
            filepath.write_text(text, encoding="utf-8")
            self.status_label.setText(f"Saved to {filename}")
        except Exception as e:
            QMessageBox.critical(
                self,
                "Save Error",
                f"Error saving file: {str(e)}"
            )
