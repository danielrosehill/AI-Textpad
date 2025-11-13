"""Settings dialog for configuring AI-Textpad."""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit,
    QPushButton, QLabel, QComboBox, QTabWidget, QWidget, QTextEdit,
    QMessageBox
)
from PyQt6.QtCore import Qt

from ..storage.database import ConfigDatabase


class SettingsDialog(QDialog):
    """Dialog for application settings."""

    DEFAULT_MODELS = [
        "openai/gpt-4o-mini",
        "openai/gpt-4o-nano",
        "x-ai/grok-4-fast",
        "google/gemini-2.5-flash-lite",
        "switchpoint/router",
        "z-ai/glm-4.5-air:free",
        "cognitivecomputations/dolphin-mistral-24b-venice-edition:free",
    ]

    def __init__(self, db: ConfigDatabase, parent=None):
        """Initialize settings dialog.

        Args:
            db: Database instance
            parent: Parent widget
        """
        super().__init__(parent)
        self.db = db

        self.setWindowTitle("Settings")
        self.setMinimumSize(600, 400)

        self._setup_ui()
        self._load_settings()

    def _setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)

        # Tab widget for different settings categories
        self.tab_widget = QTabWidget()

        # API Settings tab
        api_tab = QWidget()
        api_layout = QFormLayout(api_tab)

        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_input.setPlaceholderText("Enter your OpenRouter API key")
        api_layout.addRow("OpenRouter API Key:", self.api_key_input)

        show_key_btn = QPushButton("Show/Hide")
        show_key_btn.clicked.connect(self._toggle_api_key_visibility)
        api_layout.addRow("", show_key_btn)

        self.model_combo = QComboBox()
        self.model_combo.addItems(self.DEFAULT_MODELS)
        self.model_combo.setEditable(True)
        api_layout.addRow("Model:", self.model_combo)

        api_info = QLabel(
            "Get your API key from: https://openrouter.ai/keys\n"
            "Default model: openai/gpt-4o-mini"
        )
        api_info.setWordWrap(True)
        api_info.setStyleSheet("color: gray; font-size: 10pt;")
        api_layout.addRow("", api_info)

        self.tab_widget.addTab(api_tab, "API Settings")

        # User Details tab
        user_tab = QWidget()
        user_layout = QFormLayout(user_tab)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Your full name")
        user_layout.addRow("Name:", self.name_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("your.email@example.com")
        user_layout.addRow("Email:", self.email_input)

        self.additional_info = QTextEdit()
        self.additional_info.setPlaceholderText(
            "Any additional information to help personalize transformations\n"
            "(e.g., job title, company, preferences)"
        )
        self.additional_info.setMaximumHeight(100)
        user_layout.addRow("Additional Info:", self.additional_info)

        user_info = QLabel(
            "These details will be included in transformations when relevant\n"
            "(e.g., for email signatures, personalized content)"
        )
        user_info.setWordWrap(True)
        user_info.setStyleSheet("color: gray; font-size: 10pt;")
        user_layout.addRow("", user_info)

        self.tab_widget.addTab(user_tab, "User Details")

        layout.addWidget(self.tab_widget)

        # Buttons
        button_layout = QHBoxLayout()

        save_button = QPushButton("Save")
        save_button.clicked.connect(self._save_settings)
        save_button.setDefault(True)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)

        button_layout.addStretch()
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(save_button)

        layout.addLayout(button_layout)

    def _toggle_api_key_visibility(self):
        """Toggle API key visibility."""
        if self.api_key_input.echoMode() == QLineEdit.EchoMode.Password:
            self.api_key_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)

    def _load_settings(self):
        """Load current settings from database."""
        # API settings
        api_key = self.db.get_config("openrouter_api_key", "")
        self.api_key_input.setText(api_key)

        model = self.db.get_config("model", "openai/gpt-4o-mini")
        index = self.model_combo.findText(model)
        if index >= 0:
            self.model_combo.setCurrentIndex(index)
        else:
            self.model_combo.setCurrentText(model)

        # User details
        self.name_input.setText(self.db.get_user_detail("name", ""))
        self.email_input.setText(self.db.get_user_detail("email", ""))
        self.additional_info.setPlainText(self.db.get_user_detail("additional_info", ""))

    def _save_settings(self):
        """Save settings to database."""
        # Validate API key
        api_key = self.api_key_input.text().strip()
        if not api_key:
            reply = QMessageBox.question(
                self,
                "No API Key",
                "You haven't entered an API key. You won't be able to use transformations. Continue?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return

        # Save API settings
        if api_key:
            self.db.set_config("openrouter_api_key", api_key)

        model = self.model_combo.currentText().strip()
        if model:
            self.db.set_config("model", model)

        # Save user details
        name = self.name_input.text().strip()
        if name:
            self.db.set_user_detail("name", name)

        email = self.email_input.text().strip()
        if email:
            self.db.set_user_detail("email", email)

        additional = self.additional_info.toPlainText().strip()
        if additional:
            self.db.set_user_detail("additional_info", additional)

        QMessageBox.information(
            self,
            "Settings Saved",
            "Your settings have been saved successfully."
        )

        self.accept()
