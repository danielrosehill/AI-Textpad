"""Dialog for selecting text transformations."""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
    QPushButton, QLabel, QLineEdit, QTabWidget, QWidget, QMessageBox
)
from PyQt6.QtCore import Qt
from typing import List, Tuple

from ..storage.database import ConfigDatabase


class TransformDialog(QDialog):
    """Dialog for selecting transformations to apply."""

    MAX_SELECTIONS = 5

    def __init__(self, db: ConfigDatabase, parent=None):
        """Initialize transform dialog.

        Args:
            db: Database instance
            parent: Parent widget
        """
        super().__init__(parent)
        self.db = db
        self.selected_items = []

        self.setWindowTitle("Select Transformations")
        self.setMinimumSize(700, 500)

        self._setup_ui()
        self._load_transformations()

    def _setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)

        # Instructions
        instructions = QLabel(
            f"Select up to {self.MAX_SELECTIONS} transformations to apply (in order):"
        )
        layout.addWidget(instructions)

        # Search box
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Type to filter transformations...")
        self.search_box.textChanged.connect(self._filter_transformations)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_box)
        layout.addLayout(search_layout)

        # Tabs for categories
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        # Selected transformations display
        selected_label = QLabel("Selected transformations:")
        self.selected_list = QListWidget()
        self.selected_list.setMaximumHeight(100)
        layout.addWidget(selected_label)
        layout.addWidget(self.selected_list)

        # Buttons
        button_layout = QHBoxLayout()

        self.clear_button = QPushButton("Clear Selection")
        self.clear_button.clicked.connect(self._clear_selection)

        self.ok_button = QPushButton("Apply Transformations")
        self.ok_button.clicked.connect(self.accept)
        self.ok_button.setDefault(True)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(self.clear_button)
        button_layout.addStretch()
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(self.ok_button)

        layout.addLayout(button_layout)

    def _load_transformations(self):
        """Load transformations from database."""
        # Get all categories
        categories = self.db.get_categories()

        if not categories:
            # Show message if no transformations loaded
            QMessageBox.information(
                self,
                "No Transformations",
                "No transformations found. Please load transformation prompts first."
            )
            return

        # Create a tab for each category
        for category in categories:
            list_widget = QListWidget()
            list_widget.itemClicked.connect(self._on_item_clicked)

            # Load transformations for this category
            transformations = self.db.get_transformations(category)
            for trans in transformations:
                item = QListWidgetItem(trans['name'])
                item.setData(Qt.ItemDataRole.UserRole, trans)
                list_widget.addItem(item)

            self.tab_widget.addTab(list_widget, category)

        # Add "All" tab
        all_list = QListWidget()
        all_list.itemClicked.connect(self._on_item_clicked)
        all_transformations = self.db.get_transformations()
        for trans in all_transformations:
            item = QListWidgetItem(f"{trans['name']} ({trans['category']})")
            item.setData(Qt.ItemDataRole.UserRole, trans)
            all_list.addItem(item)
        self.tab_widget.insertTab(0, all_list, "All")

    def _on_item_clicked(self, item: QListWidgetItem):
        """Handle transformation item click.

        Args:
            item: Clicked list item
        """
        trans = item.data(Qt.ItemDataRole.UserRole)

        # Check if already selected
        if any(t['id'] == trans['id'] for t in self.selected_items):
            # Deselect
            self.selected_items = [t for t in self.selected_items if t['id'] != trans['id']]
        else:
            # Check max selections
            if len(self.selected_items) >= self.MAX_SELECTIONS:
                QMessageBox.warning(
                    self,
                    "Maximum Reached",
                    f"You can only select up to {self.MAX_SELECTIONS} transformations at once."
                )
                return
            # Add selection
            self.selected_items.append(trans)

        self._update_selected_list()

    def _update_selected_list(self):
        """Update the selected transformations list."""
        self.selected_list.clear()
        for trans in self.selected_items:
            self.selected_list.addItem(f"{len(self.selected_items)}. {trans['name']}")

    def _clear_selection(self):
        """Clear all selected transformations."""
        self.selected_items = []
        self._update_selected_list()

    def _filter_transformations(self, text: str):
        """Filter transformations based on search text.

        Args:
            text: Search query
        """
        text = text.lower()

        # Filter each tab
        for i in range(self.tab_widget.count()):
            list_widget = self.tab_widget.widget(i)
            if isinstance(list_widget, QListWidget):
                for j in range(list_widget.count()):
                    item = list_widget.item(j)
                    trans = item.data(Qt.ItemDataRole.UserRole)
                    # Show if name or category matches
                    matches = (
                        text in trans['name'].lower() or
                        text in trans['category'].lower()
                    )
                    item.setHidden(not matches)

    def get_selected_transformations(self) -> List[Tuple[str, str]]:
        """Get selected transformations as (name, prompt) tuples.

        Returns:
            List of (name, prompt) tuples
        """
        return [(t['name'], t['prompt']) for t in self.selected_items]
